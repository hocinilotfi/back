from fastapi import APIRouter, File, UploadFile, Depends
from app.tools.processor import DataProcessor
from app.tools.transformer import grade_into_score
from joblib import load
import pandas as pd
import io

from app.tools.instances_manager import statesSerializer

router = APIRouter()

# Load model and data processor
model = load("./app/models/best_model.pkl")
data_processor = DataProcessor()
pd.set_option("future.no_silent_downcasting", True)


@router.post("/predict_csv/")
async def predict_csv(csv_data: UploadFile = File(...)):
    try:

        content = await csv_data.read()
        df_received = pd.read_csv(io.StringIO(content.decode("utf-8")))

        df_processed = data_processor.prepare_data_frame(df_received)
        predicted_grades = model.predict(df_processed)
        df_received["FinalGrade"] = predicted_grades
        df_received["score"] = df_received["FinalGrade"].apply(
            lambda x: grade_into_score(
                x, thresholds=statesSerializer.thresholds, scale=statesSerializer.scale
            )
        )
        processed_data = df_received.to_dict(orient="records")
        return processed_data

    except Exception as e:
        return {"error": str(e)}
