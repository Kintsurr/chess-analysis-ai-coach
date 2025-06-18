from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Replace with your key
load_dotenv()
openai.api_key = "OPEN_AI_API_KEY"

app = FastAPI()

class MoveData(BaseModel):
    move: str
    evaluation: str
    best_move: str

@app.post("/analyze")
async def analyze_move(data: MoveData):
    try:
        prompt = (
            f"After the move {data.move}, the evaluation is {data.evaluation}. "
            f"The best move suggested by Stockfish is {data.best_move}. "
            "Explain this to a club-level chess player."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful chess coach."},
                {"role": "user", "content": prompt}
            ]
        )
        explanation = response.choices[0].message.content
    except Exception as e:
        explanation = f"API error: {e}"
    return {"explanation": explanation}