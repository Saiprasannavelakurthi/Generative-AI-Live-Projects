# 🚀 AuraGen AI

> **AI-Powered Adaptive User Interface Generator**

AuraGen AI is an intelligent full-stack application that dynamically generates React UI components based on real-time user interactions. It combines behavioral telemetry, cognitive load analysis, prompt engineering, and Large Language Models (Groq LLM) to create adaptive interfaces that respond to user behavior.

---

# 📌 Overview

AuraGen AI continuously monitors user interactions such as:

- Mouse movement
- Mouse velocity
- Hesitation
- Click patterns
- DOM state
- Current page
- Active component
- Form data

These signals are sent to a FastAPI backend through WebSockets. The backend analyzes the user's cognitive state, builds an AI prompt, generates a React component using Groq LLM, validates the generated code, and streams it back to the frontend where it is rendered instantly.

---

# ✨ Features

## Frontend

- React + Vite
- Tailwind CSS
- WebSocket Client
- Live Telemetry Collection
- Dynamic JSX Rendering
- Babel Runtime Compilation
- Error Boundary
- Transition Animations
- Live Code Editor
- Automatic Component Reloading

---

## Backend

- FastAPI
- WebSocket Server
- REST APIs
- LangChain Prompt Templates
- Groq LLM Integration
- AI Prompt Builder
- Cognitive Load Engine
- Decision Engine
- Component Cache
- JSX Validator
- Babel AST Validation
- Security Validation
- Component Storage
- Streaming Component Generation

---

# 🧠 AI Workflow

```text
User

↓

Mouse Movement
Click Pattern
Hesitation

↓

Telemetry Collection

↓

WebSocket

↓

FastAPI Backend

↓

Cognitive Engine

↓

Decision Engine

↓

Prompt Builder

↓

Groq LLM

↓

React JSX

↓

Validation

├── JSX Validator
├── Babel Parser
├── Security Validator

↓

Save Component

↓

WebSocket Stream

↓

React Dynamic Renderer
```

---

# 🏗 Project Structure

```text
Generative-AI-Live-Projects/

│
├── Auragen_backend/
│
│   ├── app.py
│   ├── generator.py
│   ├── prompt.py
│   ├── websocket_manager.py
│   │
│   ├── routes/
│   │      generate.py
│   │
│   ├── services/
│   │      babel_service.py
│   │      cache_service.py
│   │      cognitive_engine.py
│   │      decision_engine.py
│   │      generation_controller.py
│   │      groq_service.py
│   │      prompt_builder.py
│   │
│   ├── utils/
│   │      context_utils.py
│   │      design_rules.py
│   │      logger.py
│   │      save_code.py
│   │      security_validator.py
│   │      validator.py
│   │
│   ├── generated/
│   ├── tests/
│   └── requirements.txt
│
└── auragen-app/
    │
    ├── src/
    │
    ├── components/
    │
    ├── hooks/
    │      useTelemetrySocket.js
    │      useMouseTelemetry.js
    │      useMouseVelocityAndHesitation.js
    │      useClickPatterns.js
    │
    ├── utils/
    ├── App.jsx
    └── main.jsx
```

---

# 🧠 Backend Pipeline

### 1. Receive Telemetry

The frontend sends user interaction events through a WebSocket connection.

Examples:

- Mouse movement
- Clicks
- Hesitation
- Current DOM
- Active page
- Form state

---

### 2. Cognitive Engine

Calculates a cognitive score using:

- Mouse velocity
- Acceleration
- Click activity
- Hesitation

Returns:

```json
{
    "score": 6.8,
    "high_load": true
}
```

---

### 3. Decision Engine

Chooses the interface style.

- Low Load → Rich UI
- Medium Load → Balanced UI
- High Load → Simplified UI

---

### 4. Prompt Builder

Builds an adaptive prompt using

- User request
- Current page
- DOM state
- Current component
- Active field
- Cognitive score

---

### 5. Groq LLM

Generates a production-ready React Functional Component.

---

### 6. Validation

Generated code is checked using:

- React Validator
- Babel Parser
- Security Validator

---

### 7. Component Storage

Validated JSX is saved locally.

---

### 8. Streaming

Generated JSX is streamed back to the frontend.

---

# 💻 Frontend Pipeline

The frontend continuously performs:

- Mouse tracking
- Velocity calculation
- Hesitation detection
- Click analysis
- Telemetry buffering
- WebSocket communication
- Dynamic JSX rendering
- Runtime compilation using Babel

---

# 🔒 Security

AuraGen blocks unsafe JavaScript.

Examples:

- eval()
- new Function()
- document.write()
- dangerouslySetInnerHTML
- window.location
- Malicious script execution

---

# 📡 WebSocket Events

### Frontend → Backend

```
telemetry_batch
```

---

### Backend → Frontend

```
cognitive_score
```

```
token
```

```
complete
```

```
error
```

---

# 📦 REST APIs

## Root

```
GET /
```

Returns server status.

---

## Health Check

```
GET /health
```

Returns application health.

---

## Generate UI

```
POST /generate-ui
```

Generates a React component from a prompt.

---

## Stream Generate

```
POST /generate-ui/stream
```

Streams generated React code.

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/Saiprasannavelakurthi/Generative-AI-Live-Projects.git
```

---

## Backend Setup

```bash
cd Auragen_backend

pip install -r requirements.txt

uvicorn app:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd auragen-app

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# 🧪 Testing

Run all backend tests.

```bash
pytest
```

The project includes tests for:

- Cognitive Engine
- Decision Engine
- Generator
- Cache
- Validator
- Security
- Streaming
- Context Utilities

---

# 🛠 Technologies Used

### Frontend

- React
- Vite
- Tailwind CSS
- Babel Standalone
- WebSocket API

### Backend

- Python
- FastAPI
- LangChain
- Groq API
- Pydantic
- Pytest

### AI

- Prompt Engineering
- Adaptive UI Generation
- Cognitive Load Analysis
- Context-Aware UI Generation

---

# 📈 Future Improvements

- User Authentication
- Session Memory
- Theme Personalization
- Multi-page UI Generation
- Voice Interaction
- Keyboard Telemetry
- Eye Tracking Integration
- Cloud Deployment
- Dashboard Analytics
- Multi-User Collaboration

---

⭐ If you found this project useful, consider giving it a star on GitHub.
