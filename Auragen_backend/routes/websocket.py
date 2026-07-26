import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from generator import generator
from utils.context_utils import prepare_dom_context
from utils.validator import validate_component
from utils.security_validator import validate_security
from utils.save_code import save_component
from utils.logger import logger


router = APIRouter()


@router.websocket("/ws/generate")
async def generate_ui_websocket(websocket: WebSocket):

    await websocket.accept()

    try:
        data = await websocket.receive_json()

        prompt = data.get("prompt", "").strip()
        dom_state = prepare_dom_context(
            data.get("dom_state")
        )
        form_data = data.get("form_data", {})

        if not prompt:
            await websocket.send_json({
                "type": "error",
                "message": "Prompt cannot be empty."
            })
            return

        full_code = ""

        for token in generator.stream_component(
            user_prompt=prompt,
            dom_state=dom_state,
            form_data=form_data
        ):
            full_code += token

            await websocket.send_json({
                "type": "token",
                "content": token
            })

        # Full generation completed.
        # Now run Week 2 validation.
        valid, validation_message = validate_component(
            full_code
        )

        if not valid:
            logger.warning(
                f"WebSocket validation failed: "
                f"{validation_message}"
            )

            await websocket.send_json({
                "type": "error",
                "message": validation_message
            })
            return

        safe, security_message = validate_security(
            full_code
        )

        if not safe:
            logger.warning(
                f"WebSocket security failed: "
                f"{security_message}"
            )

            await websocket.send_json({
                "type": "error",
                "message": security_message
            })
            return

        # Save only after validation succeeds
        filename = "GeneratedComponent"

        saved_filename = save_component(
            filename,
            full_code
        )

        await websocket.send_json({
            "type": "complete",
            "filename": saved_filename,
            "generated_code": full_code
        })

        logger.info(
            f"WebSocket generation completed: "
            f"{saved_filename}"
        )

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")

    except Exception:
        logger.exception(
            "WebSocket generation failed"
        )

        try:
            await websocket.send_json({
                "type": "error",
                "message": "UI generation failed."
            })
        except Exception:
            pass