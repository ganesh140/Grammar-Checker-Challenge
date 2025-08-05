import uuid 
from fastapi import FastAPI, HTTPException, BackgroundTasks  # The framework
from pydantic import BaseModel  # For defining the structure of the data
import google.generativeai as genai
import json

# To keep it simple, the API key is hardcoded here.
# Chose Gemini
GEMINI_API_KEY = "Enter-Gemini-API-Key"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# API setup
app = FastAPI(
    title="Grammar Checker API",
    description="A simple API to check grammar using Google Gemini.",
    version="1.0.0",
)

# Input and output classes

class GrammarRequest(BaseModel):
    # Input text
    text: str

class Error(BaseModel):
    # Single grammar error
    wrong_sentence: str
    corrected_sentence: str
    error_type: str

class GrammarResponse(BaseModel):
    # List of errors
    errors: list[Error]

class TaskResponse(BaseModel):
    # Unique ID for the task
    task_id: str

# simple dictionary to keep track of tasks and their results like a temporary mini-database in memory.
results = {}

def query_llm(prompt):
    # This function sends the request to Gemini API
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

def check_grammar_background(text: str, task_id: str):
    # Prompt for the AI to follow
    prompt = (
        "Correct the grammar, spelling, and capitalization of the following sentence. "
        "Return the corrected sentence and list the types of errors found (e.g., Grammar, Spelling, Capitalization):\n\n"
        f"Sentence: {text}\n"
        "Respond in JSON format: {\"wrong_sentence\": \"...\", \"corrected_sentence\": \"...\", \"error_type\": \"...\"}"
    )
    try:
        generated_text = query_llm(prompt)
        
        # AI's response might have some extra formatting, so I added this to clean it up.
        cleaned_text = generated_text.strip().replace("```json", "").replace("```", "").strip()
        
        # Cleaned up text into a proper JSON object
        error_obj = json.loads(cleaned_text)
        
        # If there is an error, create a list with it. Otherwise create an empty list.
        errors = [error_obj] if error_obj["wrong_sentence"] != error_obj["corrected_sentence"] else []
        
        # Storing the final result in an in-memory storage.
        results[task_id] = {"status": "SUCCESS", "result": {"errors": errors}}
    except Exception as e:
        # Storing error message
        results[task_id] = {"status": "FAILED", "error": str(e)}

# API Endpoints

@app.post("/check-grammar", response_model=TaskResponse, status_code=202)
def check_grammar(request: GrammarRequest, background_tasks: BackgroundTasks):
    # This is the endpoint that the user calls to start a grammar check.
    
    task_id = str(uuid.uuid4())
    
    results[task_id] = {"status": "PENDING"}

    # FastAPI runs main job in the background so the user doesn't have to wait.
    background_tasks.add_task(check_grammar_background, request.text, task_id)
    
    # Returning the task ID to the user so they can check the result later.
    return {"task_id": task_id}

@app.get("/results/{task_id}")
def get_results(task_id: str):
    # This endpoint lets the user check the status and result of a task.
    result = results.get(task_id)
    
    # Task ID not found error.
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return result
