from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from crewai_tools import PDFSearchTool
from pydantic import BaseModel
from dotenv import load_dotenv
from test_citation import get_citation_count_from_search, cv_filename_to_name
import sys
import os
import re
from pathlib import Path
import shutil
from crewai import Crew, Process

load_dotenv()

app = FastAPI()


# Define the directory where uploaded files will be stored
UPLOAD_DIR = "uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FilePathResponse(BaseModel):
    file_path: str
    result: str


@app.get("/")
def read_root():
    return {"message": "Input your CV for O1 visa evaluation"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(content={"error": "Only PDF files are allowed"}, status_code=400)
    
    # Save the file to the local directory
    file_location = Path(UPLOAD_DIR) / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    pdf_path = str(file_location)
    # --- Tools ---
    pdf_search_tool = PDFSearchTool(
        pdf=pdf_path,
        config=dict(
            llm=dict(provider="anthropic", config=dict(
                model = "claude-3-haiku-20240307",
                #model="gpt-4o", 
            )),
            embedder=dict(provider="openai", config=dict(
                model="text-embedding-3-small",  
            )),
        ),
    )

    # author_search = cv_filename_to_name(pdf_path)
    # citation_count = get_citation_count_from_search(author_search)
    
    from cv_research_1go import CV_1go_agents, CV_1go_tasks
    CV_1go_task = CV_1go_tasks()
    CV_1go_agent = CV_1go_agents()

    CV_research_agent = CV_1go_agent.CV_research_agent(pdf_search_tool)
    CV_research_task = CV_1go_task.CV_research_task(CV_research_agent, pdf_search_tool)

    crew = Crew(
            tasks = [
                CV_research_task
                ],

            agents=[CV_research_agent],
            process=Process.sequential,
        )

    result = crew.kickoff()
    # Return the file path
    return FilePathResponse(file_path=str(file_location), 
                            result = str(result))

