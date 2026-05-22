from fastapi import FastAPI, HTTPException

from app.database import load_from_db

app = FastAPI(title="CA Data Vision API")

@app.get("/")
def home():
    return {"message": "CA Data Vision API running"}

@app.get("/clients")
def get_clients():

    try:
        clients, _, _ = load_from_db()
        return clients.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transactions")
def get_transactions():

    try:
        _, _, transactions = load_from_db()
        return transactions.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))