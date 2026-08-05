import json
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from models import (
    GenerateUIRequest,
    GenerateUIResponse
)

from generator import generator

from utils.validator import validate_component
from utils.security_validator import validate_security
from utils.save_code import save_component
from utils.context_utils import prepare_dom_context
from utils.logger import logger

def sse_event(event: str, data: dict) -> str:
    """
    Convert Python data into an SSE event.
    """

    return (
        f"event: {event}\n"
        f"data: {json.dumps(data)}\n\n"
    )

router = APIRouter(
    prefix="/generate-ui",
    tags=["React Code Generator"]
)


# ============================================================
# NORMAL UI GENERATION
# ============================================================

@router.post(
    "",
    response_model=GenerateUIResponse
)
def generate_ui(request: GenerateUIRequest):
    request_id = str(uuid.uuid4())

    try:
        logger.info(
            f"Request={request_id} | Generation started"
        )

        # ----------------------------------------------------
        # 1. Validate prompt
        # ----------------------------------------------------

        if not request.prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt cannot be empty"
            )

        # ----------------------------------------------------
        # 2. Prepare DOM context
        # ----------------------------------------------------

        dom_state = prepare_dom_context(
            request.dom_state
        )

        form_data = request.form_data or {}

        # ----------------------------------------------------
        # 3. Generate React component
        # ----------------------------------------------------

        result = generator.generate_component(
            user_prompt=request.prompt,
            dom_state=dom_state,
            form_data=form_data
        )

        generated_code = result["generated_code"]
        filename = result["filename"]

        # ----------------------------------------------------
        # 4. React + Babel validation
        # ----------------------------------------------------

        status, message = validate_component(
            generated_code
        )

        if not status:
            logger.warning(
                f"Request={request_id} | "
                f"Component validation failed: {message}"
            )

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Component Validation Failed",
                    "reason": message
                }
            )

        # ----------------------------------------------------
        # 5. Security validation
        # ----------------------------------------------------

        safe, security_message = validate_security(
            generated_code
        )

        if not safe:
            logger.warning(
                f"Request={request_id} | "
                f"Security validation failed: {security_message}"
            )

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Security Validation Failed",
                    "reason": security_message
                }
            )

        # ----------------------------------------------------
        # 6. Save validated component
        # ----------------------------------------------------

        saved_filename = save_component(
            filename,
            generated_code
        )

        logger.info(
            f"Request={request_id} | "
            f"Component saved | Filename={saved_filename}"
        )

        # ----------------------------------------------------
        # 7. Return response
        # ----------------------------------------------------

        logger.info(
            f"Request={request_id} | Generation completed"
        )

        return GenerateUIResponse(
            filename=saved_filename,
            generated_code=generated_code,
            preserved_data=result.get("preserved_data", True),
            page_name=result.get("page_name", ""),
            context_version=result.get("context_version", 3),
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Request={request_id} | Generate UI request failed"
        )
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# STREAMING UI GENERATION
# ============================================================

@router.post("/stream")
def generate_ui_stream(request: GenerateUIRequest):

    request_id = str(uuid.uuid4())

    # Validate before starting stream
    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )

    dom_state = prepare_dom_context(
        request.dom_state
    )

    form_data = request.form_data or {}

    def token_stream():

        full_code = ""

        try:

            logger.info(
                f"Request={request_id} | Streaming started"
            )

            # Tell frontend generation started
            yield sse_event(
                "start",
                {
                    "request_id": request_id
                }
            )

            # Stream LLM output
            for token in generator.stream_component(
                user_prompt=request.prompt,
                dom_state=dom_state,
                form_data=form_data
            ):

                full_code += token

                yield sse_event(
                    "token",
                    {
                        "request_id": request_id,
                        "content": token
                    }
                )

            logger.info(
                f"Request={request_id} | "
                "LLM streaming completed"
            )

            # React + Babel validation
            status, message = validate_component(
                full_code
            )

            if not status:

                logger.warning(
                    f"Request={request_id} | "
                    f"Validation failed: {message}"
                )

                yield sse_event(
                    "validation_error",
                    {
                        "request_id": request_id,
                        "message": message
                    }
                )

                return

            # Security validation
            safe, security_message = validate_security(
                full_code
            )

            if not safe:

                logger.warning(
                    f"Request={request_id} | "
                    f"Security validation failed: "
                    f"{security_message}"
                )

                yield sse_event(
                    "security_error",
                    {
                        "request_id": request_id,
                        "message": security_message
                    }
                )

                return

            # Save validated streamed component

            saved_filename = save_component(
                "StreamedComponent",
                full_code
            )

            logger.info(
                f"Request={request_id} | "
                f"Streamed component saved | "
                f"Filename={saved_filename}"
            )

            # Code passed validation
            yield sse_event(
                "validated",
                {
                    "request_id": request_id,
                    "valid": True
                }
            )

            logger.info(
                f"Request={request_id} | "
                "Streaming component validated"
            )

            # Final event
            yield sse_event(
                "complete",
                {
                    "request_id": request_id,
                    "filename": saved_filename,
                    "generated_code": full_code,
                    "preserved_data": True,
                    "page_name": "",
                    "context_version": 3
                }
            )

            logger.info(
                f"Request={request_id} | "
                "Streaming completed"
            )

        except Exception:

            logger.exception(
                f"Request={request_id} | "
                "Streaming generation failed"
            )

            yield sse_event(
                "error",
                {
                    "request_id": request_id,
                    "message": "Unable to complete UI generation"
                }
            )

    return StreamingResponse(
        token_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )