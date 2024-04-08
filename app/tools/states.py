# Function to load thresholds and scale from file
import json
from fastapi import HTTPException, status


class StatesSerializer:
    def __init__(self, json_file_path) -> None:
        try:
            with open(json_file_path, "r") as file:
                data = json.load(file)
                self.json_file_path = json_file_path
                self.thresholds = data.get("thresholds", [])
                self.scale = data.get("scale")
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thresholds file not found",
            )

    def sava_states(self):
        data = {"thresholds": self.thresholds, "scale": self.scale}
        with open(self.json_file_path, "w") as file:
            json.dump(data, file)
