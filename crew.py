import os
from crewai_tools import PDFSearchTool
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from test_citation import get_citation_count_from_search
load_dotenv()



# --- Agents ---
class O1visa_agents:
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

    def summarize_agent(self):
        return Agent(
    role="O1 Visa Elibility Summarization Agent",
    goal="""
    Compile and summarize findings from various analyses into a comprehensive O1 visa eligibility report,
    with itemized reports each eligiblity criteria and a final evaluation rating. 
    """,
    backstory="""
    You are an expert immigration lawyer with years of experience in O1 visa applications. 
    Your specialty is synthesizing complex information from various sources to create 
    clear, concise, and comprehensive eligibility reports. Your reports are known for 
    their accuracy, insight, and actionable recommendations.
    """,
    verbose=True,
    allow_delegation=False,
)  



class O1visa_tasks:
    def identify_awards_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa, focusing on Awards and achievements in the field.

        The O1 visa is for individuals with extraordinary ability in sciences, arts, education, business, or athletics. 
        Focus on the following criteria for Awards and achievements:

        1. Nationally or internationally recognized prizes or awards for excellence in the field
        2. Awards from prestigious organizations in the applicant's field
        3. Grants or fellowships for outstanding achievement or contribution such as NSF grants
        4. Academic honors or distinctions
        5. Industry-specific awards or recognitions
        6. Patents or other indicators of innovative contributions

        Examples of awards and achievements that could meet O1 visa criteria:
        - Nobel Prize, Fields Medal, Turing Award, or similar top-tier recognitions
        - Guggenheim Fellowship, MacArthur "Genius" Grant
        - National Medal of Science or National Medal of Technology and Innovation
        - Fulbright Scholarship or Rhodes Scholarship
        - IEEE Fellow or ACM Fellow for computer scientists
        - Academy Award (Oscar), Emmy, Grammy, or Tony Award for artists
        - Pulitzer Prize for journalists or authors
        - Olympic medal or World Championship title for athletes
        - Breakthrough Prize in Life Sciences, Mathematics, or Fundamental Physics
        - Wolf Prize in various scientific disciplines
        - Abel Prize in mathematics
        - Lasker Award in medical research
        - Fields Medal in mathematics
        - Pritzker Architecture Prize
        - National Book Award or Man Booker Prize for literature
        - National Science Foundation (NSF) grants

        Itemize all the evidence for awards and achievements found in the applicant's CV or resume.

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well. 
        Pay attention to grants such as NSF grants, as they are very prestigious and can be very helpful for O1 visa application.

        Begin your result with the following structure:

        Awards and Achievements for [Applicant Name]:
        
        1. [Award/Achievement Name] - [Year]
           - Awarding organization: [Organization Name]
           - Brief description of the award's prestige and significance in the field
           - How this award demonstrates the applicant's extraordinary ability
        
        2. [Grant/Fellowship Name] - [Year]
           - Granting institution: [Institution Name]
           - Purpose and selectivity of the grant/fellowship
           - Impact on the applicant's field or career
        
        3. [Honor/Distinction Name] - [Year]
           - Conferring body: [Organization/Institution Name]
           - Criteria for receiving this honor
           - How this sets the applicant apart in their field

        Overall Assessment:
        [Brief summary of how these awards and achievements strengthen the O1 visa application, including any notable patterns or progression in recognition]
        """
    ),
    expected_output="""
        Exhaustively list the candidate's awards and achievements in the following format:
        
        Awards and Achievements for [Applicant Name]:
        
        1. [Award/Achievement Name] - [Year]
           - Awarding organization: [Organization Name]
           - Brief description of the award's prestige and significance in the field
           - How this award demonstrates the applicant's extraordinary ability
        
        2. [Grant/Fellowship Name] - [Year]
           - Granting institution: [Institution Name]
           - Purpose and selectivity of the grant/fellowship
           - Impact on the applicant's field or career
        
        3. [Honor/Distinction Name] - [Year]
           - Conferring body: [Organization/Institution Name]
           - Criteria for receiving this honor
           - How this sets the applicant apart in their field

        Overall Assessment:
        [Brief summary of how these awards and achievements strengthen the O1 visa application, including any notable patterns or progression in recognition]
        """,
    tools=[tool],
    agent=agent,
    )   


    def identify_grants_task(self, agent, tool):
        return Task(
    description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa, focusing on Grants or fellowships for outstanding achievement or contribution.
        Examples of grants and fellowships that could meet O1 visa criteria:
        - National Science Foundation (NSF) grants
        - National Institutes of Health (NIH) grants
        - Department of Energy (DOE) grants
        - Guggenheim Fellowship
        - MacArthur "Genius" Grant
        - Fulbright Scholarship
        - Howard Hughes Medical Institute (HHMI) Investigator
        - European Research Council (ERC) grants
        - Gates Foundation grants
        - Sloan Research Fellowship
        - DARPA Young Faculty Award
        - Packard Fellowship for Science and Engineering
        - Pew Scholar in the Biomedical Sciences

        For each grant or fellowship you identify, provide:
        1. The name of the grant or fellowship
        2. The awarding institution or organization
        3. The year it was awarded
        4. A brief description of its prestige and significance in the field
        5. How it demonstrates the applicant's extraordinary ability

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well.
        """
    ),
    expected_output="""
        Exhaustively list the candidate's qualifications for O1 visa in the following format:
        Grants or fellowships for outstanding achievement or contribution for [Applicant Name]:
        1. [Grant/Fellowship Name] - [Year]
           - Awarding institution: [Institution Name]
           - Description: [Brief explanation of prestige and significance]
           - Relevance to O1 visa: [How this demonstrates extraordinary ability]

        2. [Next Grant/Fellowship]
           ...

        Overall Assessment:
        [Brief summary of how these grants and fellowships strengthen the O1 visa application]
        """,
    tools=[tool],
    agent=agent,
)


    def identify_judging_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa. 

        The O1 visa is for individuals with extraordinary ability in sciences, arts, education, business, or athletics. 
        Focus on the following criteria:

        Judging the work of others in the field, This can include:
           - Serving on panels or committees that evaluate research proposals
           - Reviewing academic papers or articles for journals
           - Judging competitions or contests in the applicant's field
           - Evaluating grant applications
           - Serving as an external examiner for students' theses or dissertations
           - Providing expert opinions or peer reviews in the applicant's area of expertise 

        Itemize all the evidence for the criteria of judging the work of others in the field:

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well.

        Begin your result with the following structure:
        "Examples of [Applicant Name] judging the work of others in the field:

        1. served on the editorial board of ...
        2. advised students ...
        3. served on the grant committee of ...: 

        Overall Assessment:
        [Brief summary of the applicant's strengths in judging the work of others in the field]
        """
    ),
    expected_output="""
        Exhaustively list the candidate's qualifications for judging the work of others in the field in the following format:
        Examples of [Applicant Name] judging the work of others in the field:

        1. served on the editorial board of ...
        2. advised students ...
        3. served on the grant committee of ...: 

        Overall Assessment:
        [Brief summary of the applicant's strengths in judging the work of others in the field]
        """,
    tools=[tool],
    agent=agent,
)


    def identify_membership(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa. 

        Focus on the following criterion:

        Membership in prestigious associations related to the applicant's field
        - Associations should be recognized as outstanding or leading in the field
        - Membership should be selective and based on outstanding achievements
        - The more exclusive or difficult to attain the membership, the stronger the case

        Itemize all the evidence for memberships in prestigious associations:

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well.

        Begin your result with the following structure:

        Memberships in prestigious associations for [Applicant Name]:
        
        1. Member of [Association Name]
           - Brief description of the association's prestige and selectivity
           - How the applicant's membership demonstrates extraordinary ability
        
        2. Fellow of [Organization Name]
           - Explanation of the fellowship's significance in the field
           - Requirements for obtaining this fellowship
        
        3. Elected to [Society Name]
           - Details on the election process and exclusivity
           - How this membership sets the applicant apart in their field

        Overall Assessment:
        [Brief summary of how these memberships strengthen the O1 visa application]
        """
    ),
    expected_output="""
        Exhaustively list the candidate's memberships in prestigious associations in the following format:
        
        Memberships in prestigious associations for [Applicant Name]:
        
        1. Member of [Association Name]
           - Brief description of the association's prestige and selectivity
           - How the applicant's membership demonstrates extraordinary ability
        
        2. Fellow of [Organization Name]
           - Explanation of the fellowship's significance in the field
           - Requirements for obtaining this fellowship
        
        3. Elected to [Society Name]
           - Details on the election process and exclusivity
           - How this membership sets the applicant apart in their field

        Overall Assessment:
        [Brief summary of how these memberships strengthen the O1 visa application]
        """,
    tools=[tool],
    agent=agent,
)


    def identify_critical_employment_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa. 

        The O1 visa is for individuals with extraordinary ability in sciences, arts, education, business, or athletics. 
        Focus on the following criteria:

        Critical employment in the applicant's field
           - Holding a leading or essential role in a distinguished organization
           - Being employed in a position that few others can perform due to exceptional expertise
           - Having a significant impact on the organization's success or industry advancement
           - Demonstrating that the applicant's skills are crucial for the employer's operations
           - Showing that the position requires someone of extraordinary ability
           - Evidence of the applicant's influence on the field through their employment
           - Testimonials from industry experts about the critical nature of the applicant's role

        Itemize all the evidence for the criteria of judging the work of others in the field:

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well.

        Begin your result with the following structure:

        Examples of [Applicant Name] having critical employment in the field:
        
        1. worked as the [position] at [company name] ...
        2. worked as the [position] at [company name] ...
        3. worked as the [position] at [company name] ...

        Overall Assessment:
        [Brief summary of the applicant's strengths and potential for O1 visa approval]
        """
    ),
    expected_output="""
        Exhaustively list the candidate's qualifications for O1 visa in working in critical employment in the field the following format:
        Examples of [Applicant Name] having critical employment in the field:
        
        1. worked as the [position] at [company name] ...
        2. worked as the [position] at [company name] ...
        3. worked as the [position] at [company name] ...

        Overall Assessment:
        [Brief summary of the applicant's strengths and potential for O1 visa approval]
        """,
    tools=[tool],
    agent=agent,
)


    def identify_high_remuneration_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa, 
        focusing on the criterion of high salary or remuneration.

        The O1 visa is for individuals with extraordinary ability in sciences, arts, education, business, or athletics. 
        For the high salary or remuneration criterion, consider the following:

        1. Actual salary or remuneration information if provided in the CV
        2. Indicators of high earning potential based on the applicant's position, experience, and achievements
        3. Comparison to industry standards for similar roles
        4. Any bonuses, stock options, or other forms of compensation mentioned
        5. Prestigious positions or roles that typically command high salaries
        6. Evidence of the applicant's value to employers or clients
        7. Any mentions of salary requirements or negotiations in past roles

        Your analysis should consider both direct evidence of high remuneration and indirect indicators that suggest the applicant commands or has the potential for high earnings in their field.

        If specific salary information is not provided, use your expertise to infer potential remuneration based on:
        - The applicant's level of experience
        - Prestigious institutions or companies they've worked for
        - Leadership positions held
        - Unique skills or expertise that are in high demand
        - Awards or recognition that typically correlate with high earnings
        - Any consulting or advisory roles that often indicate high fees

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's qualifications are lacking or need improvement, note these as well.

        Begin your result with the following structure:

        High Remuneration Potential for [Applicant Name]:
        
        1. Direct Evidence of High Remuneration:
           - [List any specific salary information or high-value compensation packages mentioned]
        
        2. Indirect Indicators of High Earning Potential:
           - [List positions, achievements, or factors that suggest high remuneration]
        
        3. Industry Comparison:
           - [Provide context on how the applicant's potential earnings compare to industry standards]

        Overall Assessment:
        [Summarize the applicant's remuneration potential and how it strengthens their O1 visa application]
        """
    ),
    expected_output="""
        Provide a detailed analysis of the candidate's high remuneration potential in the following format:
        
        High Remuneration Potential for [Applicant Name]:
        
        1. Direct Evidence of High Remuneration:
           - [Specific salary information or compensation details]
        
        2. Indirect Indicators of High Earning Potential:
           - [Positions, achievements, or factors suggesting high remuneration]
        
        3. Industry Comparison:
           - [Context on potential earnings compared to industry standards]

        Overall Assessment:
        [Summary of remuneration potential and its impact on O1 visa application]
        """,
    tools=[tool],
    agent=agent,
)   

    def identify_publications_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa. 

        Follow these steps:
        1. Use the pdf_search_tool to find the applicant's name and any information about their publications.
        2. Use the get_citation_count_from_search tool to find the applicant's Google Scholar citation count.
        3. Count the number of publications listed in the CV.

        Focus on:
        - Total number of publications
        - Total citation count
        - Any highly cited papers (if information is available)
        - The impact of these publications in the applicant's field

        Your analysis should be thorough and professional, highlighting how the applicant's publication record demonstrates their extraordinary ability in their field.

        Present your findings in the following format:  

        Publications for [Applicant Name]:
        Citation count: [Citation Count]
        Notable Publications:
        - [List any highly cited or impactful papers, if available]

        Overall Assessment:
        [Brief summary of how the publication and citation record strengthens the O1 visa application]
        """
    ),
    expected_output="""
        Present your findings in the following format:  

        Publications for [Applicant Name]:
        Citation count: [Citation Count]
        Notable Publications:
        - [List any highly cited or impactful papers, if available]

        Overall Assessment:
        [Brief summary of how the publication and citation record strengthens the O1 visa application]
        """,
    tools=[tool],
    agent=agent,
)

    def identify_contribution_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa, focusing on original contributions of major significance in the field.

        Original contributions of major significance can include:
        1. Developing a new theory or methodology in their field
        2. Creating a groundbreaking invention or technology (such as patents)
        3. Publishing influential research papers with high citation counts
        4. Designing innovative algorithms or software that have wide industry adoption
        5. Discovering a new species or natural phenomenon
        6. Creating a novel artistic style or technique that influences other artists
        7. Founding a successful company that disrupts an industry
        8. Introducing a new approach to problem-solving in their field
        9. Developing a new educational curriculum or teaching method
        10. Creating a new medical treatment or diagnostic tool

        For each original contribution you identify, provide:
        1. A brief description of the contribution
        2. Its significance and impact on the field
        3. Evidence of its recognition or adoption by others in the field
        4. How it demonstrates the applicant's extraordinary ability

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's contributions are lacking or need improvement, note these as well.

        Present your findings in the following format:  

        Original Contributions of Major Significance for [Applicant Name]:

        1. [Contribution Title/Name]
           - Description: [Brief explanation of the contribution]
           - Significance: [Impact on the field]
           - Evidence of Recognition: [How others have acknowledged or adopted this contribution]
           - Relevance to O1 Visa: [How this demonstrates extraordinary ability]

        2. [Next Contribution]
           ...

        Overall Assessment:
        [Brief summary of how these original contributions strengthen the O1 visa application, highlighting the most impactful ones]
        """
    ),
    expected_output="""
        Present your findings in the following format:  

        Original Contributions of Major Significance for [Applicant Name]:

        1. [Contribution Title/Name]
           - Description: [Brief explanation of the contribution]
           - Significance: [Impact on the field]
           - Evidence of Recognition: [How others have acknowledged or adopted this contribution]
           - Relevance to O1 Visa: [How this demonstrates extraordinary ability]

        2. [Next Contribution]
           ...

        Overall Assessment:
        [Brief summary of how these original contributions strengthen the O1 visa application, highlighting the most impactful ones]
        """,
    tools=[tool],
    agent=agent,
)


    def identify_press_task(self, agent, tool):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. 
        Your task is to analyze the provided CV or resume and identify key information that supports the applicant's eligibility for an O1 visa, focusing on published material about the applicant in professional or major trade publications or other major media.

        Examples of relevant press coverage:
        1. Feature articles in major newspapers or magazines (e.g., New York Times, Wall Street Journal, Nature, Science)
        2. Interviews or profiles in industry-specific publications
        3. Television or radio appearances discussing the applicant's work
        4. Online articles or blog posts from reputable sources highlighting the applicant's achievements
        5. Press releases from institutions or organizations about the applicant's work
        6. Book reviews or mentions of the applicant's publications
        7. Coverage of the applicant's presentations at major conferences
        8. Articles discussing the impact of the applicant's research or innovations

        For each piece of press coverage you identify, provide:
        1. The title of the article or media piece
        2. The name of the publication or media outlet
        3. The date of publication or release
        4. A brief description of the content and its relevance to the applicant's field
        5. The significance of the coverage in demonstrating the applicant's extraordinary ability

        Your analysis should be thorough, professional, and focused on the most compelling evidence for an O1 visa application. 
        If you find areas where the applicant's press coverage is lacking or needs improvement, note these as well.

        Present your findings in the following format:

        Published Material About [Applicant Name]:

        1. [Title of Article/Media Piece]
           - Publication: [Name of Publication/Media Outlet]
           - Date: [Publication/Release Date]
           - Description: [Brief summary of content and relevance]
           - Significance: [How this demonstrates extraordinary ability or recognition]

        2. [Next Article/Media Piece]
           ...

        Overall Assessment:
        [Brief summary of how the press coverage strengthens the O1 visa application, highlighting the most impactful pieces]
        """
    ),
    expected_output="""
        Present your findings in the following format:

        Published Material About [Applicant Name]:

        1. [Title of Article/Media Piece]
           - Publication: [Name of Publication/Media Outlet]
           - Date: [Publication/Release Date]
           - Description: [Brief summary of content and relevance]
           - Significance: [How this demonstrates extraordinary ability or recognition]

        2. [Next Article/Media Piece]
           ...

        Overall Assessment:
        [Brief summary of how the press coverage strengthens the O1 visa application, highlighting the most impactful pieces]
        """,
    tools=[tool],
    agent=agent,
)


    def combine_result_task(self, agent):
        return Task(
        description=(
        """
        You are an experienced immigration lawyer specializing in O1 visa applications. Your task is to compile and synthesize the results from all previous analyses of the applicant's qualifications. Combine the information from each section, maintaining all details, and provide an overall assessment of the applicant's candidacy for an O1 visa.

        Follow these steps:

        1. Compile all the information from the previous tasks, organizing it into the following sections:
           a. Awards and Achievements
           b. Grants and Fellowships
           c. Judging the Work of Others
           d. Memberships in Prestigious Associations
           e. Critical Employment
           f. High Remuneration
           g. Publications and Citations
           h. Original Contributions of Major Significance
           i. Published Material About the Applicant

        2. For each section, include all details provided in the original analyses. Do not omit any information.

        3. After compiling all sections, provide an overall candidacy evaluation for the O1 visa application. Rate the candidacy as one of the following:
           - Low: The applicant's qualifications are not strong enough to meet O1 visa criteria.
           - Medium: The applicant has some strong qualifications but may need to strengthen certain areas.
           - High: The applicant has exceptional qualifications that strongly support an O1 visa application.

        4. Justify your rating by summarizing the key strengths and any potential weaknesses in the application.

        Present your findings in the following format:

        O1 Visa Eligibility Analysis for [Applicant Name]

        1. Awards and Achievements
           [Include all details from the original analysis]

        2. Grants and Fellowships
           [Include all details from the original analysis]

        3. Judging the Work of Others
           [Include all details from the original analysis]

        4. Memberships in Prestigious Associations
           [Include all details from the original analysis]

        5. Critical Employment
           [Include all details from the original analysis]

        6. High Remuneration
           [Include all details from the original analysis]

        7. Publications and Citations
           [Include all details from the original analysis]

        8. Original Contributions of Major Significance
           [Include all details from the original analysis]

        9. Published Material About the Applicant
           [Include all details from the original analysis]

        Overall Candidacy Evaluation:
        Rating: [Low/Medium/High]

        Justification:
        [Provide a detailed explanation for the rating, summarizing key strengths and any potential weaknesses]

        Recommendation:
        [Offer advice on how to proceed with the application or strengthen specific areas if needed]
        """
    ),
    expected_output="""
        Provide a comprehensive analysis of the applicant's O1 visa eligibility, combining all previous task results and including an overall candidacy evaluation with a rating of Low, Medium, or High.
    """,
    agent=agent,
)



current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(current_dir, "CVs", "Cvitanic_Jaksa_2021.pdf")


# def processCV(pdf_path):
#     # --- Tools ---
#     pdf_search_tool = PDFSearchTool(
#         pdf=pdf_path,
#         config=dict(
#             llm=dict(provider="openai", config=dict(
#                 model="gpt-4o-mini", 
#             )),
#             embedder=dict(provider="openai", config=dict(
#                 model="text-embedding-3-small",  
#             )),
#         ),
#     )


#     author_search = cv_filename_to_name(pdf_path)
#     citation_count = get_citation_count_from_search(author_search)


#     O1visa_tasks = O1visa_tasks()
#     O1visa_agents = O1visa_agents()

#     CV_research_agent = O1visa_agents.CV_research_agent(pdf_search_tool)
#     summarize_agent = O1visa_agents.summarize_agent()


#     identify_awards_task = O1visa_tasks.identify_awards_task(CV_research_agent, pdf_search_tool)
#     identify_grants_task = O1visa_tasks.identify_grants_task(CV_research_agent, pdf_search_tool)
#     identify_contribution_task = O1visa_tasks.identify_contribution_task(CV_research_agent, pdf_search_tool)
#     identify_press_task = O1visa_tasks.identify_press_task(CV_research_agent, pdf_search_tool)
#     identify_judging_task = O1visa_tasks.identify_judging_task(CV_research_agent, pdf_search_tool)
#     identify_critical_employment_task = O1visa_tasks.identify_critical_employment_task(CV_research_agent, pdf_search_tool)
#     identify_membership_task = O1visa_tasks.identify_membership(CV_research_agent, pdf_search_tool)
#     identify_publications_task = O1visa_tasks.identify_publications_task(CV_research_agent, pdf_search_tool, citation_count)
#     identify_high_remuneration_task = O1visa_tasks.identify_high_remuneration_task(CV_research_agent, pdf_search_tool)


#     combine_result_task = O1visa_tasks.combine_result_task(summarize_agent)

#     #--- Crew ---
#     crew = Crew(
#         # one by one 
#         #tasks = [identify_judging_task], 
#         #tasks = [identify_critical_employment_task],
#         #tasks = [identify_membership],
#         tasks = [
#             identify_awards_task,
#             identify_grants_task,
#             identify_contribution_task,
#             identify_press_task,
#             identify_judging_task,
#             identify_critical_employment_task,
#             identify_publications_task,
#             identify_high_remuneration_task,
#             combine_result_task,
#             ],

#         agents=[CV_research_agent, summarize_agent],

#         process=Process.sequential,
#     )

#     #result = crew.kickoff()
#     #return result 
#     print("process finished")