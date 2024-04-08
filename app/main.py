from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import app_states_update, get_scores, predictions, get_states


app = FastAPI()

# CORS settings
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(get_states.router)
app.include_router(get_scores.router)
app.include_router(app_states_update.router)
app.include_router(predictions.router)
