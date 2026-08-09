import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from generator import generator
from models import (
    GenerateUIRequest,
    GenerateUIResponse,
)

from utils.context_utils import prepare_dom_context
from utils.logger import logger
from utils.save_code import save_component
from utils.security_validator import validate_security
from utils.validator import validate_component, clean_code


router = APIRouter(
    prefix="/generate-ui",
    tags=["React Code Generator"],
)


# ==========================================================
# Helper
# ==========================================================

def sse_event(event: str, data: dict) -> str:
    return (
        f"event: {event}\n"
        f"data: {json.dumps(data)}\n\n"
    )


# ==========================================================
# Generate UI
# ==========================================================

@router.post(
    "",
    response_model=GenerateUIResponse,
)
def generate_ui(request: GenerateUIRequest):

    request_id = str(uuid.uuid4())

    logger.info(
        f"[{request_id}] Generate UI request received."
    )

    try:

        if not request.prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt cannot be empty.",
            )

        dom_state = prepare_dom_context(
            request.dom_state
        )

        form_data = request.form_data or {}

        result = generator.generate_component(
            user_prompt=request.prompt,
            dom_state=dom_state,
            form_data=form_data,
            session_id=request.session_id,
            page_name=request.page_name,
            current_component=request.current_component,
            active_field=request.active_field,
            cognitive_score=request.cognitive_score,
            user_action=request.user_action,
        )

        generated_code = result["generated_code"]
        print("\n========== GENERATED CODE ==========")
        print(generated_code)
        print("===================================\n")
        status, message = validate_component(
            generated_code
        )

        if not status:

            logger.warning(
                f"[{request_id}] Validation failed: {message}"
            )

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "reason": message,
                },
            )

        safe, security_message = validate_security(
            generated_code
        )

        if not safe:

            logger.warning(
                f"[{request_id}] Security failed: {security_message}"
            )

            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "reason": security_message,
                },
            )

        saved_filename = save_component(
            result["filename"],
            generated_code,
        )

        logger.info(
            f"[{request_id}] Saved {saved_filename}"
        )

        return GenerateUIResponse(
            filename=saved_filename,
            generated_code=generated_code,
            preserved_data=result["preserved_data"],
            page_name=result["page_name"],
            context_version=result["context_version"],
        )

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(
            f"[{request_id}] Generate failed."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ==========================================================
# Streaming API
# ==========================================================

@router.post("/stream")
def generate_ui_stream(request: GenerateUIRequest):

    request_id = str(uuid.uuid4())

    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty.",
        )

    dom_state = prepare_dom_context(
        request.dom_state
    )

    form_data = request.form_data or {}

    def token_stream():

        full_code = ""

        try:

            logger.info(
                f"[{request_id}] Stream started."
            )

            yield sse_event(
                "start",
                {
                    "request_id": request_id,
                },
            )

            for token in generator.stream_component(
                user_prompt=request.prompt,
                dom_state=dom_state,
                form_data=form_data,
                session_id=request.session_id,
                page_name=request.page_name,
                current_component=request.current_component,
                active_field=request.active_field,
                cognitive_score=request.cognitive_score,
                user_action=request.user_action,
            ):

                full_code += token

                yield sse_event(
                    "token",
                    {
                        "request_id": request_id,
                        "content": token,
                    },
                )
            full_code = clean_code(full_code)
            status, message = validate_component(
                full_code
            )

            if not status:

                yield sse_event(
                    "validation_error",
                    {
                        "message": message,
                    },
                )

                return

            safe, security_message = validate_security(
                full_code
            )

            if not safe:

                yield sse_event(
                    "security_error",
                    {
                        "message": security_message,
                    },
                )

                return

            saved_filename = save_component(
                "StreamedComponent",
                full_code,
            )

            yield sse_event(
                "complete",
                {
                    "filename": saved_filename,
                    "generated_code": full_code,
                    "page_name": request.page_name,
                    "preserved_data": True,
                    "context_version": 3,
                },
            )

            logger.info(
                f"[{request_id}] Stream completed."
            )

        except Exception:

            logger.exception(
                f"[{request_id}] Streaming failed."
            )

            yield sse_event(
                "error",
                {
                    "message": "Streaming failed.",
                },
            )

    return StreamingResponse(
        token_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )