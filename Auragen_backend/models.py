from pydantic import BaseModel, Field


class GenerateUIRequest(BaseModel):
    """
    Request model for generating a React component.
    """

    prompt: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Describe the React component to generate."
    )


class GenerateUIResponse(BaseModel):
    """
    Response model returned after code generation.
    """

    filename: str
    generated_code: str