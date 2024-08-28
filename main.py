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
    
    from crew import O1visa_agents, O1visa_tasks
    O1visa_tasks = O1visa_tasks()
    O1visa_agents = O1visa_agents()

    CV_research_agent = O1visa_agents.CV_research_agent(pdf_search_tool)
    summarize_agent = O1visa_agents.summarize_agent()


    identify_awards_task = O1visa_tasks.identify_awards_task(CV_research_agent, pdf_search_tool)
    identify_grants_task = O1visa_tasks.identify_grants_task(CV_research_agent, pdf_search_tool)
    identify_contribution_task = O1visa_tasks.identify_contribution_task(CV_research_agent, pdf_search_tool)
    identify_press_task = O1visa_tasks.identify_press_task(CV_research_agent, pdf_search_tool)
    identify_judging_task = O1visa_tasks.identify_judging_task(CV_research_agent, pdf_search_tool)
    identify_critical_employment_task = O1visa_tasks.identify_critical_employment_task(CV_research_agent, pdf_search_tool)
    identify_membership_task = O1visa_tasks.identify_membership(CV_research_agent, pdf_search_tool)
    identify_publications_task = O1visa_tasks.identify_publications_task(CV_research_agent, pdf_search_tool)
    identify_high_remuneration_task = O1visa_tasks.identify_high_remuneration_task(CV_research_agent, pdf_search_tool)


    combine_result_task = O1visa_tasks.combine_result_task(summarize_agent)

    crew = Crew(
        tasks = [
            identify_awards_task,
            identify_grants_task,
            identify_contribution_task,
            identify_press_task,
            identify_judging_task,
            identify_critical_employment_task,
            identify_publications_task,
            identify_high_remuneration_task,
            combine_result_task,
            ],

        agents=[CV_research_agent, summarize_agent],

        process=Process.sequential,
    )

    result = crew.kickoff()
    # Return the file path
    return FilePathResponse(file_path=str(file_location), 
                            result = str(result))

