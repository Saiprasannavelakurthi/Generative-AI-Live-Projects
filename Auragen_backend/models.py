from typing import Any

from pydantic import BaseModel, Field, ConfigDict


# ==========================================================
# Generate UI Request
# ==========================================================

class GenerateUIRequest(BaseModel):
    """
    Request model for adaptive React UI generation.
    """

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    # ------------------------------------------------------
    # User Prompt
    # ------------------------------------------------------

    prompt: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Natural language request describing the UI to generate.",
        examples=["Generate a responsive login form"],
    )

    # ------------------------------------------------------
    # DOM Context
    # ------------------------------------------------------

    dom_state: str = Field(
        default="",
        description="Current DOM structure.",
    )

    form_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Current form values that must be preserved.",
    )

    # ------------------------------------------------------
    # Context Awareness
    # ------------------------------------------------------

    session_id: str = Field(
        default="",
        max_length=100,
        description="Unique session identifier.",
    )

    page_name: str = Field(
        default="",
        max_length=100,
        description="Current page name.",
    )

    current_component: str = Field(
        default="",
        max_length=100,
        description="Current React component.",
    )

    active_field: str = Field(
        default="",
        max_length=100,
        description="Currently focused input field.",
    )

    cognitive_score: float = Field(
        default=0.0,
        ge=0,
        le=10,
        description="Current cognitive load score (0-10).",
    )

    user_action: str = Field(
        default="",
        max_length=100,
        description="Latest user interaction.",
    )


# ==========================================================
# Generate UI Response
# ==========================================================

class GenerateUIResponse(BaseModel):
    """
    Response returned after successful UI generation.
    """

    model_config = ConfigDict(
        extra="ignore",
    )

    filename: str = Field(
        ...,
        description="Generated component filename.",
    )

    generated_code: str = Field(
        ...,
        description="Generated React component source code.",
    )

    preserved_data: bool = Field(
        default=True,
        description="Whether previous user-entered data was preserved.",
    )

    page_name: str = Field(
        default="",
        description="Target page.",
    )

    context_version: int = Field(
        default=3,
        ge=1,
        description="Adaptive context engine version.",
    )