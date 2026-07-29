from typing import Any
from pydantic import BaseModel, Field


class GenerateUIRequest(BaseModel):
    """
    Request model for generating a React component.
    """

    # Existing prompt
    prompt: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Describe the React component to generate."
    )

    # Current DOM structure
    dom_state: str | None = Field(
        default=None,
        description="Current DOM structure of the UI."
    )

    # Existing form values
    form_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Existing form values that must be preserved."
    )

    # ==========================
    # Week 3 - Context Awareness
    # ==========================

    session_id: str = Field(
        default="",
        description="Unique user session ID."
    )

    page_name: str = Field(
        default="",
        description="Current page where the user is interacting."
    )

    current_component: str = Field(
        default="",
        description="Current React component displayed on the page."
    )

    active_field: str = Field(
        default="",
        description="Current input field the user is interacting with."
    )

    cognitive_score: float = Field(
        default=0.0,
        description="Current cognitive load score."
    )

    user_action: str = Field(
        default="",
        description="Latest user action (typing, clicking, scrolling, etc.)."
    )


class GenerateUIResponse(BaseModel):
    """
    Response model returned after code generation.
    """

    filename: str
    generated_code: str

    # ==========================
    # Week 3 Response
    # ==========================

    preserved_data: bool = Field(
        default=True,
        description="Indicates whether user data was preserved."
    )

    page_name: str = Field(
        default="",
        description="Page for which the UI was generated."
    )

    context_version: int = Field(
        default=3,
        description="Current context-aware generation version."
    )