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

        # ==============================
        # Week 3 Context Data
        # ==============================

        prompt = data.get("prompt", "").strip()

        dom_state = prepare_dom_context(
            data.get("dom_state")
        )

        form_data = data.get("form_data", {})

        session_id = data.get(
            "session_id",
            ""
        )

        page_name = data.get(
            "page_name",
            ""
        )

        current_component = data.get(
            "current_component",
            ""
        )

        active_field = data.get(
            "active_field",
            ""
        )

        cognitive_score = data.get(
            "cognitive_score",
            0.0
        )

        user_action = data.get(
            "user_action",
            ""
        )

        if not prompt:
            await websocket.send_json({
                "type": "error",
                "message": "Prompt cannot be empty."
            })
            return

        logger.info(
            f"Session={session_id} | "
            f"Page={page_name} | "
            f"Component={current_component} | "
            f"Field={active_field} | "
            f"Score={cognitive_score}"
        )

        full_code = ""

        # ==================================
        # Week 3 Generator Call
        # ==================================

        for token in generator.stream_component(
            user_prompt=prompt,
            dom_state=dom_state,
            form_data=form_data,
            session_id=session_id,
            page_name=page_name,
            current_component=current_component,
            active_field=active_field,
            cognitive_score=cognitive_score,
            user_action=user_action
        ):

            full_code += token

            await websocket.send_json({
                "type": "token",
                "content": token
            })

        # ==================================
        # Validation
        # ==================================

        valid, validation_message = validate_component(
            full_code
        )

        if not valid:

            logger.warning(
                f"Validation Failed: {validation_message}"
            )

            await websocket.send_json({
                "type": "error",
                "message": validation_message
            })
            return

        # ==================================
        # Security Validation
        # ==================================

        safe, security_message = validate_security(
            full_code
        )

        if not safe:

            logger.warning(
                f"Security Failed: {security_message}"
            )

            await websocket.send_json({
                "type": "error",
                "message": security_message
            })
            return

        # ==================================
        # Save Component
        # ==================================

        filename = "GeneratedComponent"

        saved_filename = save_component(
            filename,
            full_code
        )

        # ==================================
        # Week 3 Response
        # ==================================

        await websocket.send_json({

            "type": "complete",

            "filename": saved_filename,

            "generated_code": full_code,

            "page_name": page_name,

            "session_id": session_id,

            "preserved_data": True,

            "context_version": 3
        })

        logger.info(
            f"Generation Completed : {saved_filename}"
        )

    except WebSocketDisconnect:

        logger.info(
            "WebSocket client disconnected"
        )

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