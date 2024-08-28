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
from crew import O1visa_agents, O1visa_tasks

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
print(result)
