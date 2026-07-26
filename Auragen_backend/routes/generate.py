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

from services.cache_service import (
    create_cache_key,
    get_cached,
    set_cached
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

    try:

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
        # 3. Create cache key
        # ----------------------------------------------------

        cache_key = create_cache_key(
            request.prompt,
            dom_state,
            form_data
        )

        # ----------------------------------------------------
        # 4. Check cache
        # ----------------------------------------------------

        cached = get_cached(cache_key)

        if cached:

            logger.info(
                f"Cache HIT | Prompt: {request.prompt}"
            )

            return GenerateUIResponse(
                filename=cached["filename"],
                generated_code=cached["generated_code"]
            )

        logger.info(
            f"Cache MISS | Prompt: {request.prompt}"
        )

        # ----------------------------------------------------
        # 5. Generate React component
        # ----------------------------------------------------

        result = generator.generate_component(
            user_prompt=request.prompt,
            dom_state=dom_state,
            form_data=form_data
        )

        generated_code = result["generated_code"]
        filename = result["filename"]

        # ----------------------------------------------------
        # 6. React + Babel validation
        # ----------------------------------------------------

        status, message = validate_component(
            generated_code
        )

        if not status:

            logger.warning(
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
        # 7. Security validation
        # ----------------------------------------------------

        safe, security_message = validate_security(
            generated_code
        )

        if not safe:

            logger.warning(
                f"Security validation failed: "
                f"{security_message}"
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
        # 8. Save validated component
        # ----------------------------------------------------

        saved_filename = save_component(
            filename,
            generated_code
        )

        # ----------------------------------------------------
        # 9. Prepare cache value
        # ----------------------------------------------------

        response_data = {
            "filename": saved_filename,
            "generated_code": generated_code
        }

        # ----------------------------------------------------
        # 10. Save result to cache
        # ----------------------------------------------------

        set_cached(
            cache_key,
            response_data
        )

        logger.info(
            f"Cache SAVED | Filename: {saved_filename}"
        )

        # ----------------------------------------------------
        # 11. Return response
        # ----------------------------------------------------

        return GenerateUIResponse(
            filename=saved_filename,
            generated_code=generated_code
        )

    except HTTPException:
        raise

    except Exception:

        logger.exception(
            "Generate UI request failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate UI"
        )


# ============================================================
# STREAMING UI GENERATION
# ============================================================

@router.post("/stream")
def generate_ui_stream(request: GenerateUIRequest):

    # --------------------------------------------------------
    # 1. Validate prompt before starting StreamingResponse
    # --------------------------------------------------------

    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )

    # --------------------------------------------------------
    # 2. Prepare Week 3 context
    # --------------------------------------------------------

    dom_state = prepare_dom_context(
        request.dom_state
    )

    form_data = request.form_data or {}

    # --------------------------------------------------------
    # 3. Streaming generator
    # --------------------------------------------------------

    def token_stream():

        full_code = ""

        try:

            logger.info(
                f"Streaming started | Prompt: {request.prompt}"
            )

            # ------------------------------------------------
            # 4. Receive LLM tokens
            # ------------------------------------------------

            for token in generator.stream_component(
                user_prompt=request.prompt,
                dom_state=dom_state,
                form_data=form_data
            ):

                full_code += token

                # IMPORTANT:
                # These tokens are preview text only.
                # Frontend must NOT execute partial JSX.
                yield token

            logger.info(
                "LLM streaming completed"
            )

            # ------------------------------------------------
            # 5. Validate complete React component
            # Includes Babel validation
            # ------------------------------------------------

            status, message = validate_component(
                full_code
            )

            if not status:
                logger.warning(
                    f"Streaming component validation failed: "
                    f"{message}"
                )

                yield f"\n[VALIDATION_ERROR] {message}"
                return

            # ------------------------------------------------
            # 6. Security validation
            # ------------------------------------------------

            safe, security_message = validate_security(
                full_code
            )

            if not safe:
                logger.warning(
                    f"Streaming security validation failed: "
                    f"{security_message}"
                )

                yield f"\n[SECURITY_ERROR] {security_message}"
                return

            # ------------------------------------------------
            # 7. Successful validation
            # ------------------------------------------------

            logger.info(
                "Streaming component validated successfully"
            )


        except Exception:
            logger.exception(
                "Streaming generation failed"
            )
            yield "\n[STREAM_ERROR] Unable to complete UI generation."
            return

    # --------------------------------------------------------
    # 8. Return HTTP stream
    # --------------------------------------------------------

    return StreamingResponse(
        token_stream(),
        media_type="text/plain"
    )