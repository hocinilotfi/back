from app.tools.states import StatesSerializer
import pandas as pd

statesSerializer = StatesSerializer("./app/data/app_states.json")
df = pd.read_csv("./app/data/exercice_data.csv", encoding="latin-1")
