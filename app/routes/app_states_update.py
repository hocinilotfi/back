from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.tools.transformer import grade_into_score
import pandas as pd

router = APIRouter()
from app.tools.instances_manager import df
from app.tools.instances_manager import statesSerializer


# Pydantic model for the input JSON data
class ThresholdsInput(BaseModel):
    thresholds: List[float]
    scale: Optional[int] = None


@router.post("/app_states_update")
async def app_states_update(thresholds_input: ThresholdsInput):

    statesSerializer.thresholds = thresholds_input.thresholds
    statesSerializer.scale = thresholds_input.scale
    statesSerializer.sava_states()

    df2 = df.copy()
    df2["score"] = df["FinalGrade"].apply(
        lambda x: grade_into_score(
            x, thresholds=thresholds_input.thresholds, scale=thresholds_input.scale
        )
    )
    data_json = df2.to_dict(orient="records")
    return data_json
