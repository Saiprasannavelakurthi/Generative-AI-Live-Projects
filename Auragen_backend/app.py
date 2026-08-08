import asyncio
import queue
import re
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from generator import generator
from websocket_manager import manager

from routes.generate import router as generate_router

from services.cognitive_engine import cognitive_engine
from services.groq_service import groq_service
from services.decision_engine import decision_engine
from services.generation_controller import generation_controller

from utils.validator import validate_component, clean_code
from utils.security_validator import validate_security
from utils.save_code import save_component
from utils.logger import logger
from utils.metrics import metrics_tracker

# Track last generated state per connection
last_page_per_session = {}
last_decision_per_session = {}
last_tier_per_session = {}

# Store last successfully generated code per session for reconnect replay
last_generated_per_session: dict[str, dict] = {}

# Active generation lock per session — prevents duplicate concurrent LLM calls
generating_sessions: set[str] = set()


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="AuraGen AI Backend",
    version="1.0.0",
    description="Adaptive React UI Generator using Groq + LangChain",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Routes
# ==========================================================

app.include_router(generate_router, prefix="/api/v1")


# ==========================================================
# Metrics HTTP endpoint — used by AnalyticsModal.jsx
# ==========================================================

@app.get("/api/v1/metrics")
def get_metrics():
    """Return live system metrics for the analytics dashboard."""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                **metrics_tracker.get_summary(),
                "is_fallback_active": getattr(groq_service, "is_fallback_active", False),
            },
        }
    )


# ==========================================================
# Generation Task — runs as a background asyncio.Task
# so the WebSocket receive loop is never blocked.
# ==========================================================

async def generate_component_task(
    websocket: WebSocket,
    session_id: str,
    current_page: str,
    gen_kwargs: dict,
):
    """
    Streams Groq tokens to the client in real time and sends a
    complete payload when done.  Runs as an asyncio background task
    so the WebSocket receive loop stays unblocked.
    """
    full_code = ""
    start_time = time.perf_counter()

    try:
        # Notify frontend: generation starting
        await manager.send_json(
            websocket,
            {
                "type": "generation_start",
                "page_name": current_page,
            },
        )

        token_q: queue.Queue = queue.Queue()

        def stream_worker():
            try:
                for token in generator.stream_component(**gen_kwargs):
                    token_q.put(token)
            except Exception as exc:
                logger.error(f"Stream worker error: {exc}")
            finally:
                token_q.put(None)   # sentinel

        loop = asyncio.get_running_loop()
        fut = loop.run_in_executor(None, stream_worker)

        connection_alive = True
        while True:
            try:
                token = token_q.get_nowait()
            except queue.Empty:
                # Yield to event loop so keep-alive pings / other coroutines run
                await asyncio.sleep(0.02)
                if fut.done() and token_q.empty():
                    break
                continue

            if token is None:
                break

            full_code += token
            sent = await manager.send_json(
                websocket,
                {"type": "token", "content": token},
            )
            if not sent:
                connection_alive = False

        await fut   # propagate any executor exception

        if not connection_alive:
            logger.info(
                f"Client disconnected mid-stream for session {session_id}. Caching result."
            )

        logger.info(f"All tokens sent. Total code length: {len(full_code)}")

        # ── Clean & validate ──────────────────────────────────────────────

        full_code = clean_code(full_code)

        # Wrap bare JSX that has no Component function
        if not (
            re.search(r"const\s+Component\s*=", full_code)
            or re.search(r"function\s+Component\s*\(", full_code)
        ):
            full_code = (
                "const Component = () => {\n"
                "    return (\n"
                f"{full_code}\n"
                "    );\n"
                "};"
            )

        status, message = validate_component(full_code)

        if not status:
            logger.warning(f"Validation failed: {message} — attempting repair")
            repaired = re.sub(r'd="[^"\n]*$', r'd="M12 4v16m8-8H4"', full_code, flags=re.MULTILINE)
            repaired = clean_code(repaired)
            rep_status, rep_msg = validate_component(repaired)
            if rep_status:
                full_code = repaired
                logger.info("JSX auto-repair succeeded.")
            else:
                logger.warning(f"JSX repair failed: {rep_msg} — skipping generation")
                await manager.send_json(websocket, {"type": "error", "message": message})
                return

        safe, security_message = validate_security(full_code)
        if not safe:
            logger.warning(f"Security check failed: {security_message}")
            await manager.send_json(websocket, {"type": "error", "message": security_message})
            return

        # ── Save & dispatch ───────────────────────────────────────────────

        filename = (
            current_page
            .replace(" ", "")
            .replace("/", "")
            .replace("\\", "")
        )
        saved_filename = save_component(filename, full_code)

        elapsed = round(time.perf_counter() - start_time, 2)
        metrics_tracker.record_generation(
            latency_sec=elapsed,
            cached=False,
            model_name="groq",
        )
        logger.info(f"Generated {saved_filename} in {elapsed}s")

        complete_payload = {
            "type": "complete",
            "filename": saved_filename,
            "generated_code": full_code,
            "generation_time": elapsed,
            "page_name": current_page,
            "session_id": session_id,
            "is_fallback": getattr(groq_service, "is_fallback_active", False),
            "preserved_data": True,
            "context_version": 3,
        }
        last_generated_per_session[session_id] = complete_payload
        await manager.send_json(websocket, complete_payload)

    except Exception as e:
        logger.exception("Component generation task failed.")
        await manager.send_json(websocket, {"type": "error", "message": str(e)})

    finally:
        generating_sessions.discard(session_id)


# ==========================================================
# WebSocket
# ==========================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)
    metrics_tracker.update_connections(len(manager.active_connections))

    logger.info("Frontend connected.")
    logger.info(f"Active Connections: {len(manager.active_connections)}")

    try:

        while True:

            data = await websocket.receive_json()

            # ── Session restore: replay last generated component ──────────
            if data.get("type") == "session_restore":
                restore_session_id = data.get("session_id", "")
                if restore_session_id and restore_session_id in last_generated_per_session:
                    cached = last_generated_per_session[restore_session_id]
                    logger.info(f"Replaying cached generation for session {restore_session_id}")
                    await manager.send_json(websocket, cached)
                continue

            # ── Ignore non-telemetry payloads ─────────────────────────────
            if data.get("type") != "telemetry_batch":
                await manager.send_json(websocket, {"status": "received"})
                continue

            session_id = data.get("session_id", "default")
            current_page = data.get("page_name", "login")

            # ── Cognitive score ───────────────────────────────────────────
            result = cognitive_engine.calculate_score(
                data.get("events", []),
                session_id=session_id,
            )

            await manager.send_json(
                websocket,
                {
                    "type": "cognitive_score",
                    "score": result["score"],
                    "high_load": result["high_load"],
                },
            )

            # ── Decision engine ───────────────────────────────────────────
            current_decision = decision_engine.decide_ui(
                score=result["score"],
                page_name=current_page,
                current_component=data.get("current_component", ""),
                active_field=data.get("active_field", ""),
                user_action=data.get("user_action", ""),
            )

            current_tier = (
                "calm" if result["score"] < 3.0
                else "hesitation" if result["score"] >= 6.0
                else "normal"
            )

            last_page = last_page_per_session.get(session_id)
            last_decision = last_decision_per_session.get(session_id)
            last_tier = last_tier_per_session.get(session_id)

            logger.info(
                f"Decision='{current_decision}' | Page='{current_page}' "
                f"| Score={result['score']:.2f} | Action='{data.get('user_action', '')}'"
            )

            # ── Generation guard ──────────────────────────────────────────
            if session_id in generating_sessions:
                # Already generating — skip but do NOT drop the connection
                continue

            page_changed = (last_page is None or current_page != last_page)
            decision_changed = (last_decision is None or current_decision != last_decision)
            tier_changed = (last_tier is None or current_tier != last_tier)
            force_gen = bool(data.get("force_generate", False))
            high_friction = result["high_load"]
            is_hesitation = data.get("user_action") == "hesitation"

            should_generate = (
                page_changed
                or force_gen
                or decision_changed
                or tier_changed
                or high_friction
                or is_hesitation
            )

            if not should_generate:
                continue

            if page_changed or force_gen:
                generation_controller.reset(session_id)

            if not generation_controller.can_generate(session_id):
                continue

            # ── Lock session and update state ─────────────────────────────
            generating_sessions.add(session_id)
            last_page_per_session[session_id] = current_page
            last_decision_per_session[session_id] = current_decision
            last_tier_per_session[session_id] = current_tier

            logger.info(f"========== START GENERATION ({current_page}) ==========")
            logger.info(
                f"Decision='{current_decision}' | Page='{current_page}' "
                f"| Score={result['score']:.2f} | Action='{data.get('user_action', '')}'"
            )

            prompt = (
                f"Generate an adaptive React UI for "
                f"{current_page} page "
                f"based on the current context, "
                f"user interaction and cognitive score."
            )

            gen_kwargs = dict(
                user_prompt=prompt,
                dom_state=data.get("dom_state", ""),
                form_data=data.get("form_data", {}),
                session_id=session_id,
                page_name=current_page,
                current_component=data.get("current_component", ""),
                active_field=data.get("active_field", ""),
                cognitive_score=result["score"],
                user_action=data.get("user_action", ""),
            )

            # ── Fire-and-forget background task ───────────────────────────
            # The task runs concurrently; the receive loop stays unblocked.
            asyncio.create_task(
                generate_component_task(
                    websocket=websocket,
                    session_id=session_id,
                    current_page=current_page,
                    gen_kwargs=gen_kwargs,
                )
            )

    except (WebSocketDisconnect, RuntimeError):
        manager.disconnect(websocket)
        logger.info("Frontend disconnected.")

    except Exception:
        logger.exception("Unexpected WebSocket error.")
        manager.disconnect(websocket)