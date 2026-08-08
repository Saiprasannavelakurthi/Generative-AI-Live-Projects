# 🧠 AuraGen AI

> **AI-Powered Adaptive User Interface Generator**

AuraGen AI is an intelligent full-stack application that **dynamically generates React UI components in real-time** based on user behavioral signals. It combines WebSocket-based telemetry, cognitive load analysis, multi-model Groq LLM streaming, and in-browser Babel JSX compilation to create a fully adaptive UI playground.

---

## 🎯 What Makes AuraGen Unique?

Unlike traditional UIs that are static, AuraGen **watches how you interact** with the application:

- Moving **slowly** or **hesitating**? It generates a simplified, distraction-free UI.
- **Clicking rapidly** or showing high engagement? It generates a rich, information-dense UI.
- Groq API **rate limit hit**? It instantly streams a smart contextual fallback component matching your selected page — with **zero downtime**.

---

## ✨ Key Features

### 🖥️ Frontend
| Feature | Description |
|---|---|
| **Real-time Telemetry** | Captures mouse velocity, hesitation, click patterns, keyboard activity |
| **Cognitive Load Meter** | Live gauge showing user cognitive engagement level (Calm / Focused / High) |
| **Dynamic JSX Rendering** | In-browser Babel standalone runtime compilation of LLM-generated JSX |
| **WebSocket Streaming** | Token-by-token streaming from Groq LLM for instant visual feedback |
| **Error Boundary** | Graceful rendering fallback for malformed generated components |
| **Live Code Editor** | View and edit the generated JSX directly in the browser |
| **Session Recovery** | Reconnects and replays last generated component on WebSocket reconnect |
| **Analytics Modal** | Live system metrics dashboard (generations, latency, cache hits, model usage) |
| **Keyboard Telemetry** | Tracks typing speed, correction rate, and field activity |
| **Force Generate** | Manual trigger to force immediate component generation |

### ⚙️ Backend
| Feature | Description |
|---|---|
| **FastAPI + WebSocket** | Full-duplex bidirectional real-time communication |
| **Non-Blocking Generation** | `asyncio.create_task` ensures telemetry loop never blocks LLM generation |
| **Cognitive Engine** | Composite score from velocity variance, hesitation, click frequency, field focus |
| **Decision Engine** | Maps page + cognitive load → specific prompt strategy (rich / simple / wizard / minimal) |
| **Multi-Model Fallback** | Cascades across 4 Groq models (`llama-3.1-8b-instant`, `llama-3.3-70b-versatile`, `llama3-8b-8192`, `llama3-70b-8192`) |
| **Smart Fallback Components** | Contextual JSX templates per page type when all LLMs are rate-limited |
| **LangChain Prompt Templates** | Structured system + user prompt engineering per UI type |
| **Babel AST Validation** | Node.js subprocess validates generated JSX before delivery |
| **Security Validation** | Blocks `eval`, `dangerouslySetInnerHTML`, `window.location`, external scripts |
| **Component Cache** | Caches generations to prevent redundant API calls for identical prompts |
| **Component Storage** | Persists all generated components as `.jsx` files in `generated_UI/` |
| **System Metrics API** | `GET /api/v1/metrics` — live backend performance metrics for the analytics modal |

---

## 🧠 AI Workflow

```
User Interaction
  │
  ├── Mouse Movement / Velocity / Hesitation
  ├── Click Patterns
  ├── Keyboard Activity
  └── DOM Form State
          │
          ▼
   Telemetry Batch (WebSocket every 1s)
          │
          ▼
   FastAPI Backend
          │
          ├── Cognitive Engine   → Composite Score (0–10+)
          │
          ├── Decision Engine    → UI Strategy
          │     ├── Score 0–3   → rich_login / rich_dashboard / rich_loan_form
          │     ├── Score 3–5   → simple_login / loan_form / profile_page
          │     ├── Score 5–7   → wizard_login / wizard_loan_form
          │     └── Score 7+    → minimal_login / minimal_ui
          │
          ├── Prompt Builder     → LangChain System + User Prompt
          │
          ├── Groq LLM           → Token Streaming (llama-3.1-8b-instant → fallbacks)
          │     └── Rate Limited? → Smart Fallback Component (per page type)
          │
          ├── Validation
          │     ├── JSX Validator (brace balance, component check)
          │     ├── Babel AST Parser (Node subprocess)
          │     └── Security Validator (eval, XSS, injection checks)
          │
          └── WebSocket Stream   → Frontend Token-by-Token Rendering
                    │
                    ▼
           React Dynamic Renderer
           (Babel Standalone → Live Component)
```

---

## 🏗️ Project Structure

```
Generative-AI-Live-Projects/
│
├── .gitignore                         # Root monorepo gitignore
├── README.md
│
├── Auragen_backend/                   # FastAPI Backend
│   ├── .gitignore
│   ├── .env.example
│   ├── app.py                         # Main FastAPI app, WebSocket handler, metrics API
│   ├── generator.py                   # Core LLM generation orchestrator
│   ├── generator.py                   # Core LLM generation orchestrator
│   ├── models.py                      # Pydantic request/response models
│   ├── prompt.py                      # System prompt assembly
│   ├── websocket_manager.py           # Active WebSocket connection manager
│   ├── config.py                      # Configuration (models, API keys, settings)
│   ├── requirements.txt
│   │
│   ├── routes/
│   │   └── generate.py                # REST endpoint: POST /api/v1/generate-ui
│   │
│   ├── services/
│   │   ├── babel_service.py           # Node.js Babel subprocess validator
│   │   ├── cache_service.py           # LRU component cache
│   │   ├── cognitive_engine.py        # Behavioral signal → cognitive score
│   │   ├── decision_engine.py         # Score + page → UI strategy
│   │   ├── generation_controller.py   # Debounce / threshold generation control
│   │   ├── groq_service.py            # Multi-model streaming + smart fallback
│   │   └── prompt_builder.py          # Maps UI type → LangChain prompt template
│   │
│   ├── utils/
│   │   ├── context_utils.py           # DOM context + form data processor
│   │   ├── design_rules.py            # Global CSS/Tailwind design constraints
│   │   ├── logger.py                  # Structured logger with file + console output
│   │   ├── metrics.py                 # Thread-safe system metrics tracker
│   │   ├── prompt_templates.py        # 20+ LangChain prompt templates per page/tier
│   │   ├── save_code.py               # Persist generated components to disk
│   │   ├── security_validator.py      # Block dangerous JS patterns
│   │   └── validator.py               # JSX structure + brace balance validation
│   │
│   └── tests/
│       ├── test_cache.py
│       ├── test_cognitive_engine.py
│       ├── test_context.py
│       ├── test_decision.py
│       ├── test_generator.py
│       ├── test_groq_fallback.py
│       ├── test_metrics.py
│       ├── test_security.py
│       ├── test_stream.py
│       └── test_validator.py
│
└── auragen-app/                       # React + Vite Frontend
    ├── .gitignore
    ├── index.html
    ├── vite.config.js
    ├── package.json
    │
    └── src/
        ├── App.jsx                    # Main app layout + page selector + controls
        ├── main.jsx
        │
        ├── components/
        │   ├── AnalyticsModal.jsx     # Live metrics modal (polls /api/v1/metrics)
        │   ├── CodeEditorPanel.jsx    # Generated JSX live code viewer/editor
        │   ├── CognitiveLoadMeter.jsx # Animated cognitive load gauge
        │   ├── DynamicCodeRenderer.jsx# Babel runtime → live React component
        │   ├── ErrorPanel.jsx         # Generation error display
        │   ├── RenderBoundary.jsx     # React error boundary
        │   ├── StaticFallbackForm.jsx # Static fallback when component fails
        │   ├── StatusBadge.jsx        # WS connection + fallback status indicator
        │   └── TelemetryReadout.jsx   # Live telemetry stats readout
        │
        ├── hooks/
        │   ├── useClickPatterns.js    # Click frequency + pattern analyzer
        │   ├── useKeyboardTelemetry.js# Typing speed + error rate tracker
        │   ├── useMouseTelemetry.js   # Mouse position + velocity tracker
        │   ├── useMouseVelocityAndHesitation.js  # Velocity + pause detection
        │   └── useTelemetrySocket.js  # WS client + batching + session recovery
        │
        └── utils/
            └── babelLoader.js         # Babel standalone + JSX sanitization
```

---

## 🔌 API Reference

### WebSocket

| Event | Direction | Payload | Description |
|---|---|---|---|
| `telemetry_batch` | Frontend → Backend | Mouse, clicks, form, DOM, cognitive score | Batch telemetry every 1s |
| `session_restore` | Frontend → Backend | `session_id` | Replay last generated component on reconnect |
| `cognitive_score` | Backend → Frontend | `score`, `label` | Live cognitive load update |
| `token` | Backend → Frontend | `content`, `chunk_index` | Streamed JSX token |
| `complete` | Backend → Frontend | `generated_code`, `filename`, `is_fallback` | Generation completed |
| `error` | Backend → Frontend | `message` | Generation or validation failure |

### REST Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to React frontend (`http://localhost:5173`) |
| `GET` | `/api/v1/metrics` | Live system metrics (generations, latency, cache, models) |
| `POST` | `/api/v1/generate-ui` | Synchronous component generation |
| `POST` | `/api/v1/generate-ui/stream` | SSE streaming component generation |

---

## 🔒 Security Features

AuraGen automatically blocks dangerous JavaScript patterns in all generated code:

- `eval()` / `new Function()`
- `document.write()` / `document.cookie`
- `dangerouslySetInnerHTML`
- `window.location` redirects
- `<script>` tag injections
- External URL fetches to unknown origins
- Prototype pollution patterns

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Groq API Key → [https://console.groq.com](https://console.groq.com)

### 1. Clone the Repository

```bash
git clone https://github.com/Saiprasannavelakurthi/Generative-AI-Live-Projects.git
cd Generative-AI-Live-Projects
```

### 2. Backend Setup

```bash
cd Auragen_backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start the backend server
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Backend runs at: `http://127.0.0.1:8000`
API Docs: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup

```bash
cd auragen-app

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🧪 Testing

```bash
cd Auragen_backend
python -m pytest
```

**56 tests** covering:

| Test File | Coverage |
|---|---|
| `test_cache.py` | LRU component cache behavior |
| `test_cognitive_engine.py` | Score calculation from behavioral signals |
| `test_context.py` | DOM + form data context extraction |
| `test_decision.py` | Page + score → UI strategy mapping |
| `test_generator.py` | Full generation pipeline integration |
| `test_groq_fallback.py` | Multi-model fallback + smart template selection |
| `test_metrics.py` | Thread-safe metrics tracker |
| `test_security.py` | Dangerous pattern detection |
| `test_stream.py` | SSE streaming endpoint |
| `test_validator.py` | JSX structure validation |

---

## 🛠️ Technology Stack

### Frontend
- **React 18** + **Vite 8**
- **Tailwind CSS**
- **Babel Standalone** (in-browser JSX compilation)
- **WebSocket API**

### Backend
- **Python 3.13** + **FastAPI**
- **LangChain** + **langchain-groq**
- **Groq API** (`llama-3.1-8b-instant`, `llama-3.3-70b-versatile`)
- **Pydantic v2**
- **Pytest**

### AI & Engineering
- **Behavioral Telemetry** — real-time mouse, click, keyboard signal collection
- **Cognitive Load Analysis** — composite score from multi-signal fusion
- **Adaptive Prompt Engineering** — 20+ specialized LangChain prompt templates
- **Multi-Model Resilience** — automatic cascading fallback across Groq models
- **Smart Fallback System** — contextual JSX templates per page when all LLMs fail

---

## 📈 Roadmap

- [ ] User authentication + session persistence
- [ ] Multi-page adaptive UI generation
- [ ] Theme personalization (dark/light/branded)
- [ ] Voice interaction telemetry
- [ ] Eye tracking integration
- [ ] Cloud deployment (Render / Railway)
- [ ] Multi-user collaboration workspace
- [ ] Export generated components as downloadable ZIP

---

## 📄 License

This project is for educational and portfolio purposes.

---

⭐ If you found this project useful, consider giving it a star on GitHub!

> Built with ❤️ using Groq, LangChain, FastAPI, and React.
