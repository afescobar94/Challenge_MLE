import fastapi
import pandas as pd

from pathlib import Path
from challenge.model import DelayModel


app = fastapi.FastAPI()
model = DelayModel()

_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "data.csv"
_VALID_TIPOVUELO = {"I", "N"}
_VALID_MES = set(range(1, 13))
_VALID_OPERAS = set(pd.read_csv(_DATA_PATH, usecols=["OPERA"])["OPERA"].unique())

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: fastapi.Request) -> dict:
    payload = await request.json()
    flights = payload.get("flights") if isinstance(payload, dict) else None

    if not isinstance(flights, list) or len(flights) == 0:
        raise fastapi.HTTPException(status_code=400, detail="Invalid flights payload")

    for flight in flights:
        if not isinstance(flight, dict):
            raise fastapi.HTTPException(status_code=400, detail="Invalid flight payload")

        opera = flight.get("OPERA")
        tipovuelo = flight.get("TIPOVUELO")
        mes = flight.get("MES")

        if opera not in _VALID_OPERAS:
            raise fastapi.HTTPException(status_code=400, detail="Invalid OPERA value")
        if tipovuelo not in _VALID_TIPOVUELO:
            raise fastapi.HTTPException(status_code=400, detail="Invalid TIPOVUELO value")
        if not isinstance(mes, int) or mes not in _VALID_MES:
            raise fastapi.HTTPException(status_code=400, detail="Invalid MES value")

    flights_df = pd.DataFrame(flights)
    features = model.preprocess(data=flights_df)
    predictions = model.predict(features=features)
    return {"predict": predictions}
