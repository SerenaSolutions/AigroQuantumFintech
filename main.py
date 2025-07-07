
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Financial Advisor Service")

class FinancialQuery(BaseModel):
    query: str
    user_context: dict = {}

@app.post("/advise")
async def get_financial_advice(query: FinancialQuery):
    # Lógica de IA para aconselhamento financeiro (placeholder)
    response_text = f"Entendido: {query.query}. No momento, não posso fornecer aconselhamento financeiro detalhado, mas estou aprendendo!"
    return {"advice": response_text}

@app.get("/")
def read_root():
    return {"message": "AI Financial Advisor Service is running"}
