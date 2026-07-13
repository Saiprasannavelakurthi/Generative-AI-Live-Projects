from fastapi import APIRouter, HTTPException

from models import (
    GenerateUIRequest,
    GenerateUIResponse
)

from generator import generator

from utils.validator import validate_component
from utils.save_code import save_component

router = APIRouter(
    prefix="/generate-ui",
    tags=["React Code Generator"]
)


@router.post(
    "",
    response_model=GenerateUIResponse
)
def generate_ui(request: GenerateUIRequest):

    try:

        # Generate React component
        result = generator.generate_component(
            request.prompt
        )

        generated_code = result["generated_code"]
        filename = result["filename"]

        # Validate generated React code
        status, message = validate_component(generated_code)

        if not status:
            raise HTTPException(
                status_code=400,
                detail=message
            )

        # Save generated component
        save_component(filename, generated_code)

        # Return API response
        return GenerateUIResponse(
            filename=filename,
            generated_code=generated_code
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )