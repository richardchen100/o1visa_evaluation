import os
from crewai_tools import PDFSearchTool
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from test_citation import get_citation_count_from_search
load_dotenv()

class CV_1go_agents:
    def CV_research_agent(self, tool):
        return Agent(
            role="O1 Visa Elibility Research Agent",
            goal="Exhaustively search through the CV to find eligibility criteria for O1 visa",
            allow_delegation=False,
            verbose=True,
            backstory=(
                """
                The research agent is an experienced immigration lawyer specializing in O1 visa applications. 
                The agent is very experienced and exhaustive in analyzing the  CV or resume and 
                identify key information that supports the applicant's eligibility for an O1 visa. 
                 """
            ),
            tools=[tool],
        )

class CV_1go_tasks:
    def CV_research_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa. 

        The O1 visa is for individuals with extraordinary ability in sciences, arts, education, business, or athletics. Focus on the following criteria:

        1. Awards and achievements in the field
        2. Membership in prestigious associations
        3. Published material about the applicant
        4. Judging the work of others in the field, This can include:
           - Serving on panels or committees that evaluate research proposals
           - Reviewing academic papers or articles for journals
           - Judging competitions or contests in the applicant's field
           - Evaluating grant applications
           - Serving as an external examiner for students' theses or dissertations
           - Providing expert opinions or peer reviews in the applicant's area of expertise 
        5. Original contributions of major significance
           - Developing a new theory or methodology in their field
           - Creating a groundbreaking invention or technology such as patents
           - Publishing influential research papers with high citation counts
           - Designing innovative algorithms or software that have wide industry adoption
           - Discovering a new species or natural phenomenon
           - Creating a novel artistic style or technique that influences other artists
           - Founding a successful company that disrupts an industry
        6. High salary or remuneration
        7. Critical employment in the applicant's field
           - Holding a leading or essential role in a distinguished organization
           - Being employed in a position that few others can perform due to exceptional expertise
           - Having a significant impact on the organization's success or industry advancement
           - Demonstrating that the applicant's skills are crucial for the employer's operations
           - Showing that the position requires someone of extraordinary ability
           - Evidence of the applicant's influence on the field through their employment
           - Testimonials from industry experts about the critical nature of the applicant's role


        For each relevant piece of information you find, provide:
        1. The specific criterion it supports, itemized if possible
        2. A brief explanation of how it demonstrates extraordinary ability
        3. Any additional context that strengthens the case
        4. Count the number of items for each criterion (e.g., number of awards, publications, etc.)


        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well.

        Begin your analysis with the following structure:
        "O1 Visa Eligibility Analysis for [Applicant Name]

        Key Eligibility Factors:
        1. [Criterion]: [Brief description of evidence]
        Explanation: [How this supports the O1 visa case]

        2. [Next criterion] (Count: Y)
        ...

        Overall Assessment:
        [Brief summary of the applicant's strengths and potential for O1 visa approval]
        """
        ),
        expected_output="""
        Exhaustively list the candidate's qualifications for O1 visa in the following format:
        O1 Visa Eligibility Analysis for [Applicant Name]

        Key Eligibility Factors:
        1. [Criterion]: [Brief description of evidence]
        Explanation: [How this supports the O1 visa case]

        2. [Next criterion] (Count: Y)
        ...

        Overall Assessment:
        [Brief summary of the applicant's strengths and potential for O1 visa approval]
        """,
        tools=[tool],
        agent=agent,
    )