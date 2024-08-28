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
from cv_research_1go import CV_1go_agents, CV_1go_tasks

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
#pdf_path = os.path.join(current_dir, "CVs", "Cvitanic_Jaksa_2021.pdf")
pdf_path = os.path.join(current_dir, "CVs", "khai_cv.pdf")
# --- Tools ---
pdf_search_tool = PDFSearchTool(
        pdf=pdf_path,
        config=dict(
            llm=dict(
                provider="openai",
                    #provider="anthropic", 
                    config=dict(
                #model = "claude-3-haiku-20240307",
                model="gpt-4o-mini", 
            )),
            embedder=dict(provider="openai", config=dict(
                model="text-embedding-3-small",  
            )),
        ),
    )



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
print(result)