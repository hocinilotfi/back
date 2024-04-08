from fastapi import APIRouter

from app.tools.instances_manager import statesSerializer

router = APIRouter()


@router.get("/get_states")
async def get_states():

    return {
        "thresholds": statesSerializer.thresholds,
        "scale": statesSerializer.scale,
    }
