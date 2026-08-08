import time
from typing import List, Any, Generator
from langchain_groq import ChatGroq

from config import GROQ_API_KEY, MODEL_NAME, FALLBACK_MODELS, TEMPERATURE, MAX_TOKENS
from utils.logger import logger


def _get_fallback_component(messages: List[Any]) -> str:
    """
    Generate a smart contextual template component when all external LLMs fail or are rate-limited.
    Ensures 100% application resilience.
    """
    user_prompt = ""
    if messages:
        last_m = messages[-1]
        user_prompt = (last_m.content if hasattr(last_m, "content") else str(last_m)).lower()

    full_prompt = " ".join(
        [str(m.content) if hasattr(m, "content") else str(m) for m in messages]
    ).lower()

    search_target = user_prompt if user_prompt else full_prompt

    if "loan" in search_target:
        return """const Component = () => {
    const [amount, setAmount] = React.useState(10000);
    const [salary, setSalary] = React.useState(5000);

    return (
        <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-xl w-full mx-auto text-slate-800">
            <h2 className="text-2xl font-bold text-indigo-600 mb-1">Instant Loan Application</h2>
            <p className="text-slate-500 text-xs mb-6">Calculated EMI estimate based on your income</p>
            <div className="space-y-4">
                <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Monthly Salary ($)</label>
                    <input
                        type="number"
                        value={salary}
                        onChange={(e) => setSalary(Number(e.target.value))}
                        className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                    />
                </div>
                <div>
                    <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                        <span>Requested Loan Amount</span>
                        <span className="text-indigo-600">${amount.toLocaleString()}</span>
                    </div>
                    <input
                        type="range"
                        min="1000"
                        max="50000"
                        step="1000"
                        value={amount}
                        onChange={(e) => setAmount(Number(e.target.value))}
                        className="w-full accent-indigo-600"
                    />
                </div>
                <div className="p-4 bg-indigo-50 rounded-xl border border-indigo-100 flex items-center justify-between">
                    <span className="text-xs font-medium text-indigo-900">Estimated Monthly EMI</span>
                    <span className="text-lg font-bold text-indigo-600">${Math.round(amount / 24)}/mo</span>
                </div>
                <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">
                    Submit Application Now →
                </button>
            </div>
        </div>
    );
};"""

    if "dashboard" in search_target:
        return """const Component = () => {
    return (
        <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl w-full max-w-4xl mx-auto text-slate-800">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-xl font-bold text-slate-900">AuraGen Dashboard Summary</h2>
                    <p className="text-xs text-slate-500">Real-time Telemetry & System Status</p>
                </div>
                <span className="px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-xs font-semibold">
                    Live System Active
                </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                    <p className="text-xs text-slate-500 font-medium">Total Balance</p>
                    <h3 className="text-2xl font-bold text-indigo-600 mt-1">$24,500</h3>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                    <p className="text-xs text-slate-500 font-medium">Active Loans</p>
                    <h3 className="text-2xl font-bold text-indigo-600 mt-1">2</h3>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                    <p className="text-xs text-slate-500 font-medium">Next EMI Due</p>
                    <h3 className="text-2xl font-bold text-slate-900 mt-1">$350</h3>
                </div>
            </div>
        </div>
    );
};"""

    if "register" in search_target:
        return """const Component = () => {
    return (
        <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md w-full mx-auto text-slate-800">
            <h2 className="text-2xl font-bold text-slate-900 mb-1">Create Account</h2>
            <p className="text-slate-500 text-xs mb-6">Sign up to get started with AuraGen</p>
            <div className="space-y-4">
                <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                    <input type="text" placeholder="John Doe" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm" />
                </div>
                <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
                    <input type="email" placeholder="name@example.com" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm" />
                </div>
                <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
                    <input type="password" placeholder="••••••••" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm" />
                </div>
                <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">
                    Register Account
                </button>
            </div>
        </div>
    );
};"""

    if "profile" in search_target:
        return """const Component = () => {
    return (
        <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-lg w-full mx-auto text-slate-800">
            <div className="flex items-center space-x-4 mb-6">
                <div className="w-14 h-14 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xl font-bold">
                    JD
                </div>
                <div>
                    <h2 className="text-xl font-bold text-slate-900">User Profile</h2>
                    <p className="text-xs text-slate-500">Account settings and preferences</p>
                </div>
            </div>
            <div className="space-y-4">
                <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                    <input type="text" defaultValue="John Doe" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm" />
                </div>
                <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
                    <input type="email" defaultValue="john@example.com" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm" />
                </div>
                <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">
                    Save Profile Changes
                </button>
            </div>
        </div>
    );
};"""

    if "contact" in search_target:
        return """const Component = () => {
    return (
        <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md w-full mx-auto text-slate-800">
            <h2 className="text-2xl font-bold text-slate-900 mb-1">Contact Support</h2>
            <p className="text-slate-500 text-xs mb-6">Send us a message and we'll reply shortly</p>
            <div className="space-y-4">
                <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Your Message</label>
                    <textarea rows="4" placeholder="How can we help you?" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm"></textarea>
                </div>
                <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">
                    Send Message
                </button>
            </div>
        </div>
    );
};"""

    if "login" in search_target:
        return """const Component = () => {
    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [remember, setRemember] = React.useState(false);

    return (
        <div className="flex flex-col items-center justify-center p-6 bg-slate-900/90 rounded-2xl border border-slate-700/60 shadow-2xl backdrop-blur-md max-w-md w-full mx-auto text-slate-200">
            <div className="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center mb-4 text-blue-400 font-bold text-xl">
                A
            </div>
            <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 mb-1">
                Welcome Back
            </h2>
            <p className="text-slate-400 text-xs mb-6 text-center">
                Adaptive login view optimized for minimal hesitation
            </p>
            <form className="w-full space-y-4" onSubmit={(e) => e.preventDefault()}>
                <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Username / Email</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="enter your username"
                        className="w-full px-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-sm"
                    />
                </div>
                <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••"
                        className="w-full px-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-sm"
                    />
                </div>
                <div className="flex items-center justify-between text-xs text-slate-400">
                    <label className="flex items-center space-x-2 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={remember}
                            onChange={(e) => setRemember(e.target.checked)}
                            className="rounded bg-slate-800 border-slate-700 text-blue-500 focus:ring-0"
                        />
                        <span>Remember me</span>
                    </label>
                    <a href="#forgot" className="text-blue-400 hover:text-blue-300 transition-colors">
                        Forgot Password?
                    </a>
                </div>
                <button
                    type="submit"
                    className="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-blue-500/20 transition-all duration-200 transform active:scale-95"
                >
                    Sign In
                </button>
            </form>
        </div>
    );
};"""

    return """const Component = () => {
    return (
        <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-lg w-full mx-auto text-slate-800">
            <h2 className="text-lg font-bold text-indigo-600 mb-2">Adaptive Component Ready</h2>
            <p className="text-slate-500 text-sm">
                Interface dynamically synchronized with user interaction telemetry.
            </p>
        </div>
    );
};"""


class GroqService:
    """
    Handles communication with Groq LLM with multi-model fallback resilience.
    """

    def __init__(self):
        self.models = [MODEL_NAME] + [m for m in FALLBACK_MODELS if m != MODEL_NAME]
        self.active_model_name = self.models[0]
        self.llm = self._create_llm(self.active_model_name)
        self.is_fallback_active = False

    def _create_llm(self, model_name: str) -> ChatGroq:
        return ChatGroq(
            model=model_name,
            api_key=GROQ_API_KEY,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

    def generate(self, messages: List[Any]) -> str:
        """
        Generate a complete React component with multi-model retry fallback.
        """
        if not messages:
            raise ValueError("Messages cannot be empty.")

        start_time = time.perf_counter()

        for model in self.models:
            try:
                if self.active_model_name != model:
                    self.active_model_name = model
                    self.llm = self._create_llm(model)

                logger.info(f"Invoking Groq model: {model}")
                response = self.llm.invoke(messages)

                if response is None or not hasattr(response, "content"):
                    raise RuntimeError("Empty response received from Groq.")

                content = response.content.strip()
                elapsed = round(time.perf_counter() - start_time, 2)
                logger.info(f"Groq generation ({model}) completed in {elapsed}s.")
                return content

            except Exception as e:
                logger.warning(
                    f"Groq generation with model {model} failed: {e}. Trying next fallback model..."
                )

        logger.error("All Groq models failed/rate-limited. Switching to Smart Fallback Component.")
        return _get_fallback_component(messages)

    def stream_generate(self, messages: List[Any]) -> Generator[str, None, None]:
        """
        Stream React component tokens from Groq with multi-model retry fallback.
        """
        if not messages:
            raise ValueError("Messages cannot be empty.")

        start_time = time.perf_counter()

        for model in self.models:
            try:
                if self.active_model_name != model:
                    self.active_model_name = model
                    self.llm = self._create_llm(model)

                logger.info(f"Streaming from Groq model: {model}")
                full_response = ""
                received_chunks = False

                for chunk in self.llm.stream(messages):
                    if not chunk:
                        continue
                    token = getattr(chunk, "content", "")
                    if not token:
                        continue
                    received_chunks = True
                    full_response += token
                    yield token

                if received_chunks:
                    elapsed = round(time.perf_counter() - start_time, 2)
                    logger.info(f"Groq streaming ({model}) completed in {elapsed}s.")
                    self.is_fallback_active = False
                    return

            except Exception as e:
                logger.warning(
                    f"Groq streaming with model {model} failed: {e}. Trying next fallback model..."
                )

        logger.error("All Groq models failed/rate-limited. Streaming Smart Fallback Component.")
        self.is_fallback_active = True
        fallback_code = _get_fallback_component(messages)
        # Yield fallback code in small chunks to simulate streaming
        chunk_size = 30
        for i in range(0, len(fallback_code), chunk_size):
            yield fallback_code[i : i + chunk_size]


groq_service = GroqService()