from fastapi import APIRouter, HTTPException

from models import (
    GenerateUIRequest,
    GenerateUIResponse
)

from generator import generator

from utils.validator import validate_component
from utils.security_validator import validate_security
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

        # Check empty prompt
        if not request.prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt cannot be empty"
            )

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

        safe, message = validate_security(generated_code)

        if not safe:
            raise HTTPException(
                status_code=400,
                detail=message
            )
        # Save generated component
        saved_filename = save_component(
            filename,
            generated_code
        )

        # Return API response
        return GenerateUIResponse(
            filename=saved_filename,
            generated_code=generated_code
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
