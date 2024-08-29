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
            - Nationally or internationally recognized prizes or awards for excellence in the field
            - Awards from prestigious organizations in the applicant's field
            - Grants or fellowships for outstanding achievement or contribution such as NSF grants
            - Academic honors or distinctions
            - Industry-specific awards or recognitions
            - Patents or other indicators of innovative contributions  
        2. Membership in prestigious associations
            - Associations should be recognized as outstanding or leading in the field
            - Membership should be selective and based on outstanding achievements
            - The more exclusive or difficult to attain the membership, the stronger the case
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
        6. High salary or remuneration. Consider the following:
            -  Actual salary or remuneration information if provided in the CV
            - Indicators of high earning potential based on the applicant's position, experience, and achievements
            - Comparison to industry standards for similar roles
            - Any bonuses, stock options, or other forms of compensation mentioned
            - Prestigious positions or roles that typically command high salaries
            - Evidence of the applicant's value to employers or clients
            - Any mentions of salary requirements or negotiations in past roles 
        7. Critical employment in the applicant's field
           - Holding a leading or essential role in a distinguished organization
           - Being employed in a position that few others can perform due to exceptional expertise
           - Having a significant impact on the organization's success or industry advancement
           - Demonstrating that the applicant's skills are crucial for the employer's operations
           - Showing that the position requires someone of extraordinary ability
           - Evidence of the applicant's influence on the field through their employment
           - Testimonials from industry experts about the critical nature of the applicant's role
        8. Publications. Focus on:
            - Total number of publications
            - Total citation count
            - Any highly cited papers (if information is available)
            - The impact of these publications in the applicant's field

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well.

        Begin your analysis with the following structure:
        "O1 Visa Eligibility Analysis for [Applicant Name]

        Key Eligibility Factors:
        1. [Criterion]:
           - [Item 1]
           - [Item 2]
           - ...
        Explanation: [How these items support the O1 visa case]

        2. [Next criterion] (Total items: Y)
           - [Item 1]
           - [Item 2]
           - ...
        
        Explanation: [How these items support the O1 visa case]

        ...
           
        Overall Assessment:
        [Brief summary of the applicant's strengths and potential for O1 visa approval]

        Overall Candidacy Evaluation:
        Rating: [Low/Medium/High]
        """
        ),
        expected_output="""
        Provide an exhaustive list of the candidate's qualifications for O1 visa in the following format:
        O1 Visa Eligibility Analysis for [Applicant Name]

        Key Eligibility Factors:
        1. [Criterion]:
           - [Item 1]
           - [Item 2]
           - ...
        Explanation: [How these items support the O1 visa case]

        2. [Next criterion] (Total items: Y)
           - [Item 1]
           - [Item 2]
           - ...
        Explanation: [How these items support the O1 visa case]

        ...

        Overall Assessment:
        [Comprehensive summary of ALL the applicant's qualifications and potential for O1 visa approval]

        Overall Candidacy Evaluation:
        Rating: [Low/Medium/High]
        Justification: [Detailed explanation of the rating based on ALL evidence presented]
        """,
        tools=[tool],
        agent=agent,
    )