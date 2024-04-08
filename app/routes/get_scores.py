from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional

from app.tools.transformer import grade_into_score
import pandas as pd
from app.tools.instances_manager import df
from app.tools.instances_manager import statesSerializer

router = APIRouter()


@router.get("/get_scores")
async def get_scores():

    df2 = df.copy()
    df2["score"] = df["FinalGrade"].apply(
        lambda x: grade_into_score(
            x, thresholds=statesSerializer.thresholds, scale=statesSerializer.scale
        )
    )
    data_json = df2.to_dict(orient="records")
    return data_json
