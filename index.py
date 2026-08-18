import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from fastapi.responses import HTMLResponse

app = FastAPI(title="Pulse AI Quiz")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remember to paste your AQ. key here!
GEMINI_API_KEY = GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

live_quiz = {
    "topic": "Waiting for topic...",
    "current_index": 0,
    "questions": []
}

class TopicPayload(BaseModel):
    topic: str

class VotePayload(BaseModel):
    option: str

class NavPayload(BaseModel):
    direction: str

@app.post("/api/generate")
def generate_quiz(payload: TopicPayload):
    global live_quiz
    if not client:
        raise HTTPException(status_code=500, detail="API Key not configured")
    
    try:
        # We upgraded the prompt to demand exactly 10 questions
        prompt = (
            f"Create a 10-question multiple choice quiz about '{payload.topic}'. "
            "Return ONLY a valid JSON array of exactly 10 objects. Do not wrap in markdown block backticks. "
            "Each object must follow this exact structure:\n"
            "{\n"
            '  "question": "The question string",\n'
            '  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],\n'
            '  "correct_answer": "Option 1",\n'
            '  "explanation": "Concise 1-sentence reason why this is correct."\n'
            "}"
        )
        
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        data_list = json.loads(raw_text)
        
        if not isinstance(data_list, list) or len(data_list) != 10:
            # Fallback in case AI hallucinates the count
            data_list = data_list[:10] 

        new_questions = []
        for item in data_list:
            new_questions.append({
                "question": item["question"],
                "options": {opt: 0 for opt in item["options"]},
                "correct_answer": item["correct_answer"],
                "explanation": item["explanation"]
            })
            
        live_quiz["topic"] = payload.topic
        live_quiz["questions"] = new_questions
        live_quiz["current_index"] = 0
        
        return {"message": "Quiz generated successfully", "data": live_quiz}
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="AI failed to generate quiz. Try again.")

@app.get("/api/poll")
def get_quiz():
    return live_quiz

@app.post("/api/vote")
def submit_vote(payload: VotePayload):
    global live_quiz
    if not live_quiz["questions"]:
        return {"message": "No active quiz", "data": live_quiz}
        
    current_q = live_quiz["questions"][live_quiz["current_index"]]
    if payload.option in current_q["options"]:
        current_q["options"][payload.option] += 1
    return {"message": "Vote recorded", "data": live_quiz}

@app.post("/api/nav")
def navigate_quiz(payload: NavPayload):
    global live_quiz
    if not live_quiz["questions"]:
        return {"message": "No active quiz", "data": live_quiz}
        
    max_idx = len(live_quiz["questions"]) - 1
    
    if payload.direction == "next" and live_quiz["current_index"] < max_idx:
        live_quiz["current_index"] += 1
    elif payload.direction == "prev" and live_quiz["current_index"] > 0:
        live_quiz["current_index"] -= 1
        
    return {"message": "Navigated", "data": live_quiz}

@app.get("/")
def read_root():
    # This reads your frontend HTML file and serves it at the main URL
    html_path = os.path.join(os.path.dirname(__file__), "../public/index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return {"message": "API Running (index.html not found)"}