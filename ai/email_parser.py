import os
import json
import getpass
import requests
from bs4 import BeautifulSoup

from pprint import pprint
from typing import Literal, TypedDict, Union
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from langchain_google_community import GmailToolkit
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials

load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

class JobInfo(TypedDict):
    '''Metadata relating to the job application.'''
    status: Literal['Applied, Offer, OA, Rejected, Interview']
    company: str
    position: str
    mode: Literal['Remote, In Person, Hybrid']

class JobMetadata(BaseModel):
    location: Union[str, Literal['N/A']] = Field(description='The location of the job if available, else, N/A.', default='N/A')
    payments: float = Field(description='The median salary of the position if provied, else, N/A.', default=-1.0)
    description: Union[str, Literal['N/A']] = Field(description='The detailed job description if enough information is provided, else, N/A.', default='N/A')

def init_gmail_conn():
    # setup Gmail toolkit
    credentials = get_gmail_credentials(
        scopes=["https://mail.google.com/"],
        client_secrets_file="ai/oauth/client_secret_163202554535-p6pfh8qs471c2b10tusiqr4p8gnn48qi.apps.googleusercontent.com.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    gmail_toolkit = GmailToolkit(api_resource=api_resource)
    gmail_tools = gmail_toolkit.get_tools()

    serper_search = GoogleSerperAPIWrapper()
    search_tool = Tool(name='serper_search', func=serper_search.results, description='Useful for when you need to search for information on the internet.')
    return gmail_tools, search_tool

def get_emails(gmail_llm, gmail_tools):
    response = gmail_llm.invoke('Search for emails using the following search filters:\n(\"thank you for applying\" OR \"you\'ve applied\" OR \"received your application\") newer_than:1y. Set the resource parameter ')
    tc = response.tool_calls[0]
    tool = gmail_tools[2]
    tool_out = tool.invoke(tc)
    tool_out = json.loads(tool_out.content)
    emails = tool_out
    for email in emails:
        if email.get('body', None): 
            email['body'] = email['body'].replace('\n', '').replace('\r', '')
    return emails

def get_test_case_emails():
    credentials = get_gmail_credentials(
        scopes=["https://mail.google.com/"],
        client_secrets_file="oauth/client_secret_163202554535-p6pfh8qs471c2b10tusiqr4p8gnn48qi.apps.googleusercontent.com.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    gmail_toolkit = GmailToolkit(api_resource=api_resource)
    gmail_tools = gmail_toolkit.get_tools()

    adobe_applied = gmail_tools[2].invoke('subject:\"Thanks for applying to Adobe\" newer_than:7d', max_results=1)
    codazen_applied = gmail_tools[2].invoke('subject:\"Thank you for applying to Codazen\" newer_than:12d', max_results=1)
    nuro_applied = gmail_tools[2].invoke('subject:\"Thank you for applying to Nuro\" newer_than:12d', max_results=1)
    tesla_applied = gmail_tools[2].invoke('subject:\"Jennifer Thank you for your interest in Tesla\" newer_than:12d', max_results=1)
    google_applied = gmail_tools[2].invoke('subject:\"Thanks for applying to Google\" newer_than:7d', max_results=1)
    intuit_applied = gmail_tools[2].invoke('subject:\"Thank you for applying at Intuit\" newer_than:25d', max_results=1)
    tiktok_applied = gmail_tools[2].invoke('subject:\"Thank you for applying to TikTok!\" newer_than:25d', max_results=1)
    sumo_rejected = gmail_tools[2].invoke('subject:\"Regarding your application to Sumo Logic\" newer_than:7d', max_results=1)
    affirm_rejected = gmail_tools[2].invoke('subject:\"Your Application to Affirm\" newer_than:7d', max_results=1)
    snap_rejected = gmail_tools[2].invoke('subject:\"Regarding your application with Snap Inc.\" newer_than:7d', max_results=1)
    shopify_rejected = gmail_tools[2].invoke('subject:\"Shopify\'s 2025 Engineering Internships - Assessments Update\" newer_than:7d', max_results=1)
    flexport_rejected = gmail_tools[2].invoke('subject:\"Thank you from Flexport!\" newer_than:15d', max_results=1)
    uber_oa = gmail_tools[2].invoke('subject:\"Uber Coding Assessment\" newer_than:7d', max_results=1)
    roblox_oa = gmail_tools[2].invoke('subject:\"[Action Required] Your Roblox Assessments Invitation\" newer_than:10d', max_results=1)
    datadog_oa = gmail_tools[2].invoke('subject:\"Next steps with Datadog!\" newer_than:12d', max_results=1)
    stripe_oa = gmail_tools[2].invoke('subject:\"2024-2025 Stripe University Recruiting HackerRank Challenge Invitation\" newer_than:15d', max_results=1)
    # shopify_oa = gmail_tools[2].invoke('subject:\"Coding Challenge with Shopify\" newer_than:15d', max_results=1)
    # netflix_oa = gmail_tools[2].invoke('subject:\"Complete Your Netflix New Grad Application | Next Steps\" newer_than:45d', max_results=1)
    veeva_interview = gmail_tools[2].invoke('subject:\"Veeva Video Interview Request\" newer_than:70d', max_results=1)
    # pprint([
    #     adobe_applied,
    #     codazen_applied,
    #     nuro_applied,
    #     tesla_applied,
    #     google_applied,
    #     intuit_applied,
    #     tiktok_applied,
    #     sumo_rejected,
    #     affirm_rejected,
    #     snap_rejected,
    #     shopify_rejected,
    #     flexport_rejected,
    #     uber_oa,
    #     roblox_oa,
    #     datadog_oa,
    #     stripe_oa,
    #     netflix_oa,
    #     veeva_interview
    # ])
    emails = [
        adobe_applied[0],
        codazen_applied[0],
        nuro_applied[0],
        tesla_applied[0],
        google_applied[0],
        intuit_applied[0],
        tiktok_applied[0],
        sumo_rejected[0],
        affirm_rejected[0],
        snap_rejected[0],
        shopify_rejected[0],
        flexport_rejected[0],
        uber_oa[0],
        roblox_oa[0],
        datadog_oa[0],
        stripe_oa[0],
        veeva_interview[0]
    ]
    return emails

def parse_tests():
    email_infos = [
        {'status': 'Applied', 'company': 'Adobe', 'position': 'Software Development Engineer', 'mode': 'Remote'},
        {'status': 'Applied', 'company': 'Codazen', 'position': 'Software Engineer', 'mode': 'In Person'},
        {'status': 'Applied', 'company': 'Nuro', 'position': 'SWE I', 'mode': 'Remote'},
        {'status': 'Applied', 'company': 'Tesla', 'position': 'Internship, Fullstack Software Engineer, Maps & Self-Driving Navigation', 'mode': 'In Person'},
        {'status': 'Applied', 'company': 'Google', 'position': 'Software Engineer Intern', 'mode': 'Hybrid'},
        {'status': 'Applied', 'company': 'Intuit', 'position': 'Software Development Intern', 'mode': 'In Person'},
        {'status': 'Applied', 'company': 'TikTok', 'position': 'Software Development Engineer', 'mode': 'In Person'},
        {'status': 'Rejected', 'company': 'Sumo', 'position': 'Software Engineer I - MLE', 'mode': 'Remote'},
        {'status': 'Rejected', 'company': 'Affirm', 'position': 'Software Engineer I (Data Platform)', 'mode': 'Remote'},
        {'status': 'Rejected', 'company': 'Snap', 'position': 'Software Engineer, Full Stack, New Grad Engineer', 'mode': 'Hybrid'},
        {'status': 'Rejected', 'company': 'Shopify', 'position': 'Engineering Internship', 'mode': 'Hybrid'},
        {'status': 'Rejected', 'company': 'Flexport', 'position': 'Software Engineer I, Forwarding Applications', 'mode': 'Remote'},
        {'status': 'OA', 'company': 'Uber', 'position': 'Software Engineer', 'mode': 'Remote'},
        {'status': 'OA', 'company': 'Roblox', 'position': 'Early Career Talent', 'mode': 'In Person'},
        {'status': 'OA', 'company': 'Datadog', 'position': 'Software Engineer - Early Career', 'mode': 'Hybrid'},
        {'status': 'OA', 'company': 'Stripe', 'position': 'Software Engineer I', 'mode': 'Remote'},
        {'status': 'Interview', 'company': 'Veeva', 'position': 'Associate Software Engineer', 'mode': 'Remote'},
    ]
    return email_infos

def test_metadata():
    return [
        {'location': 'Seattle, WA', 'payments': '135000', 'description': 'As an Entry-Level Software Engineer at Adobe, you will be part of a dynamic team responsible for designing, developing, and maintaining innovative software solutions that empower creative professionals and enterprises worldwide. You will collaborate with cross-functional teams, including product managers and designers, to deliver high-quality, scalable, and efficient code. Your work will involve participating in the full software development lifecycle, from brainstorming and coding to testing and deployment. You will also be encouraged to explore new technologies, troubleshoot complex problems, and contribute to Adobe\'s culture of continuous improvement. This role offers an opportunity to work with cutting-edge technologies and grow in a supportive, creative environment.'},
        {'location': 'New York, NY', 'payments': '102000', 'description': 'As an Entry-Level Software Engineer at Codazen, you will be involved in building cutting-edge web and software applications that drive exceptional digital experiences for clients. You will work closely with experienced engineers, designers, and project managers to design, develop, and implement innovative solutions using modern web technologies and frameworks. This role involves writing clean, maintainable, and scalable code, participating in code reviews, and contributing to all phases of the software development lifecycle. You\'ll have the opportunity to solve challenging technical problems, gain hands-on experience with new tools, and collaborate in an agile, fast-paced environment focused on delivering high-quality solutions. Codazen fosters a collaborative, growth-oriented culture where your contributions will directly impact the success of client projects.'},
        {'location': 'San Francisco, CA', 'payments': '98000', 'description': 'As a Software Engineer at Nuro, you will play a key role in building and optimizing the software systems that power autonomous delivery vehicles. You will collaborate with cross-functional teams including robotics engineers, product managers, and data scientists to design, develop, and implement software solutions that enhance vehicle performance, safety, and efficiency. Your responsibilities will include writing high-quality, scalable code, troubleshooting complex technical challenges, and participating in the full software development lifecycle—from concept and architecture to deployment and maintenance. At Nuro, you will work on cutting-edge technology in autonomous systems, making a direct impact on the future of robotics and last-mile delivery. You\'ll thrive in an innovative, fast-paced environment that values creativity, problem-solving, and continuous learning.'},
        {'location': 'Mountain View, CA', 'payments': '87500', 'description': 'As a Software Engineering Intern at Tesla, you will have the opportunity to work on innovative software solutions that drive the future of sustainable energy and transportation. You\'ll collaborate with experienced engineers on projects that could range from enhancing Tesla\'s vehicle software, improving automation systems, to developing scalable backend infrastructure. Your role will involve writing clean, efficient, and maintainable code, debugging complex issues, and participating in code reviews. This internship offers hands-on experience with cutting-edge technologies and real-world problem-solving in a fast-paced, mission-driven environment. You will be encouraged to contribute creative ideas and take ownership of impactful projects, all while learning from Tesla\'s world-class engineering team.'},
        {'location': 'New York, NY', 'payments': '105000', 'description': 'As a Software Engineering Intern at Google, you will contribute to the development of large-scale, high-impact projects that enhance Google\'s products and services used by billions of people globally. You\'ll work alongside experienced engineers in a collaborative environment, tackling complex technical challenges related to areas such as machine learning, cloud computing, infrastructure, or web development. Your responsibilities will include designing, coding, and testing software solutions while participating in code reviews and improving system performance. This internship offers the opportunity to gain hands-on experience with advanced technologies, learn from industry experts, and make a real impact on Google\'s innovative projects. You\'ll be part of a dynamic, fast-paced team that values creativity, problem-solving, and continuous learning.'},
        {'location': 'San Francisco, CA', 'payments': '100000', 'description': 'As a Software Engineering Intern at Intuit, you will contribute to the design, development, and optimization of innovative software solutions that power products like TurboTax, QuickBooks, and Mint. Working closely with seasoned engineers, product managers, and designers, you will participate in the entire software development lifecycle, from coding and debugging to testing and deployment. Your role will involve writing clean, scalable code, improving system performance, and solving complex technical problems. This internship offers hands-on experience with modern tools and frameworks in an agile environment, providing opportunities to learn and grow while contributing to real-world projects that help millions of customers manage their finances. Intuit values creativity, collaboration, and continuous learning, giving you the chance to make a meaningful impact from day one.'},
        {'location': 'New York, NY', 'payments': '90000', 'description': 'As a Software Engineer at TikTok, you will be responsible for developing and optimizing innovative, high-performance systems that support TikTok\'s global platform, used by millions of users daily. You\'ll work on a wide range of projects, from enhancing backend infrastructure and building scalable APIs to developing new features that improve user engagement and experience. Collaborating with cross-functional teams, including product managers, data scientists, and UX designers, you will participate in the full software development lifecycle—design, coding, testing, and deployment. In this role, you\'ll tackle complex technical challenges, write efficient, maintainable code, and contribute to TikTok\'s mission of inspiring creativity and bringing joy to users worldwide. The fast-paced environment at TikTok encourages innovation, creativity, and continuous learning.'},
        {'location': 'Raleigh, NC', 'payments': '125000', 'description': 'As a Software Engineer at Sumo, you will be responsible for designing, developing, and maintaining software solutions that support scalable, high-performance systems for real-time data analytics. You will work closely with cross-functional teams to build features and improve the infrastructure behind Sumo Logic\'s platform, which helps organizations manage, monitor, and secure their applications. Your role will involve writing clean, efficient, and maintainable code, solving complex technical problems, and contributing to both backend services and frontend user experiences. You\'ll participate in all phases of the software development lifecycle, from architecture and design to deployment and optimization. At Sumo, you will have the opportunity to work with cutting-edge technologies in a collaborative, fast-paced environment that values innovation, continuous improvement, and a customer-centric approach.'},
        {'location': 'Portland, OR', 'payments': '160000', 'description': 'As a Software Engineer at Affirm, you will be responsible for designing and developing reliable, scalable systems that power the company\'s mission to provide honest financial products and services. You will collaborate with cross-functional teams, including product managers, data scientists, and designers, to build backend services, APIs, and customer-facing features that enhance the user experience and drive growth. Your role will involve writing clean, maintainable code, participating in code reviews, and solving complex technical challenges in areas like payments processing, machine learning, or fraud detection. At Affirm, you\'ll work in a fast-paced, collaborative environment where innovation, transparency, and continuous improvement are valued, allowing you to make a meaningful impact on the future of finance.'},
        {'location': 'Seattle, WA', 'payments': '142000', 'description': 'As a Software Engineer at Snap, you will contribute to building and optimizing cutting-edge products that enhance the experiences of millions of users on platforms like Snapchat. You will collaborate with cross-functional teams, including product managers, designers, and data scientists, to develop scalable and innovative software solutions. Your responsibilities will include designing and implementing new features, improving system performance, and solving complex technical challenges in areas like augmented reality, messaging, and multimedia. You\'ll work across the full software development lifecycle, from architecture and coding to testing and deployment, in a fast-paced, dynamic environment. Snap fosters a culture of creativity, collaboration, and continuous learning, giving you the opportunity to work with cutting-edge technologies and shape the future of digital communication.'},
        {'location': 'San Francisco, CA', 'payments': '137000', 'description': 'As a Software Engineering Intern at Shopify, you will have the opportunity to contribute to the development of innovative e-commerce solutions that empower businesses around the world. You will work alongside experienced engineers on projects that enhance the Shopify platform, focusing on building scalable features and improving user experiences. Your role will involve writing clean, efficient code, participating in code reviews, and collaborating with cross-functional teams to identify and solve technical challenges. This internship provides hands-on experience with modern technologies and methodologies in an agile environment, allowing you to learn from industry leaders while making meaningful contributions to real-world projects. At Shopify, we value creativity, collaboration, and a passion for problem-solving, providing you with an enriching experience in a fast-paced, dynamic setting.'},
        {'location': 'San Francisco, CA', 'payments': '115000', 'description': 'As a Software Engineer at Flexport, you will play a pivotal role in developing and optimizing software solutions that streamline global trade and logistics operations. You will collaborate with cross-functional teams, including product managers, data scientists, and operations experts, to design, implement, and maintain scalable systems that enhance the efficiency of freight forwarding and supply chain management. Your responsibilities will include writing high-quality, maintainable code, troubleshooting complex issues, and integrating with various APIs and third-party services. In this dynamic, fast-paced environment, you will have the opportunity to tackle challenging technical problems and contribute to the continuous improvement of Flexport\'s platform. At Flexport, we value innovation, teamwork, and a commitment to making global trade more accessible and efficient, empowering you to make a meaningful impact on the industry.'},
        {'location': 'Chicago, IL', 'payments': '100000', 'description': 'As a Software Engineer at Uber, you will be at the forefront of developing innovative software solutions that enhance the user experience for millions of riders and drivers worldwide. You will collaborate with cross-functional teams, including product managers, data scientists, and UX designers, to build scalable systems and features that improve the efficiency of Uber\'s platform. Your responsibilities will include writing clean, efficient code, conducting code reviews, and troubleshooting complex technical challenges. You will participate in the entire software development lifecycle, from design and implementation to testing and deployment. At Uber, you\'ll work in a fast-paced, dynamic environment that fosters creativity and innovation, allowing you to contribute to transformative projects that shape the future of transportation and mobility.'},
        {'location': 'New York, NY', 'payments': '95000', 'description': 'As a Software Engineer at Roblox, you will be instrumental in creating and enhancing the platform that empowers millions of developers and players to engage in immersive gaming experiences. You will collaborate with talented teams across product management, design, and data analytics to design, implement, and optimize scalable software solutions that support Roblox\'s growing ecosystem. Your responsibilities will include writing high-quality, maintainable code, debugging complex issues, and contributing to the development of new features that enhance user engagement and platform performance. In this fast-paced environment, you\'ll have the opportunity to tackle challenging technical problems and experiment with cutting-edge technologies. At Roblox, we value creativity, collaboration, and a passion for gaming, allowing you to make a meaningful impact on the future of interactive entertainment.'},
        {'location': 'Mountain View, CA', 'payments': '70000', 'description': 'As a Software Engineer at Datadog, you will be a key contributor to building and scaling the observability platform that helps organizations monitor their applications and infrastructure in real-time. You will work collaboratively with cross-functional teams, including product managers, designers, and data scientists, to design and implement robust features that enhance the user experience and improve system performance. Your responsibilities will include writing high-quality, maintainable code, conducting thorough testing, and troubleshooting complex technical challenges in a fast-paced environment. At Datadog, you\'ll have the opportunity to work with cutting-edge technologies and innovative solutions that empower companies to gain insights into their systems. We value creativity, collaboration, and a strong commitment to quality, allowing you to make a significant impact on the future of cloud monitoring and analytics.'},
        {'location': 'Seattle, WA', 'payments': '110000', 'description': 'As a Software Engineer at Stripe, you will play a vital role in building and enhancing the technology that powers online payments for millions of businesses globally. You will collaborate with cross-functional teams, including product managers, designers, and data scientists, to develop scalable and secure software solutions that improve the user experience for both merchants and consumers. Your responsibilities will include designing, coding, and testing new features, as well as troubleshooting and optimizing existing systems to ensure high performance and reliability. In this fast-paced environment, you\'ll have the opportunity to tackle complex technical challenges and contribute to innovative projects that redefine the financial landscape. At Stripe, we value collaboration, creativity, and a commitment to excellence, providing you with the opportunity to make a meaningful impact on the future of commerce.'},
        {'location': 'Sunnyvale, CA', 'payments': '140500', 'description': 'As a Software Engineer at Veeva, you will contribute to the development of cutting-edge cloud-based solutions that empower life sciences companies to bring innovative therapies to market more efficiently. Working within a collaborative and agile environment, you will partner with cross-functional teams, including product managers, quality assurance, and design, to design, build, and enhance applications that streamline processes and improve user experiences. Your responsibilities will include writing clean, maintainable code, implementing new features, and resolving complex technical challenges while ensuring high standards of quality and performance. At Veeva, you will have the opportunity to work with the latest technologies and methodologies, allowing you to grow your skills and make a meaningful impact on the healthcare industry while helping clients achieve their goals in regulatory compliance and operational excellence.'},
    ]

def parse_emails(emails, parser_llm, search_tool):
    email_infos = []
    for email in emails:
        if email.get('body', None):
            response = parser_llm.invoke(f'Given the following information relating to a job, extract given information (company, position, and status):\n\nEmail Body:\n{email["body"]}\n\nEmail Subject:\n{email["subject"]}\n\nEmail Sender:\n{email["sender"]}\n\nIf you are unsure of what to input for the `mode` or `status` field, simply choose from one of the options.')
            email_infos.append(json.loads(response['raw'].additional_kwargs['tool_calls'][0]['function']['arguments']))

    search_results = []
    for einfo in email_infos:
        sr = search_tool.invoke('Find me a job description that matches the following job specs: ' + json.dumps([einfo["position"], [einfo["company"]]]))
        search_results.append(sr)
    return search_results, email_infos

def get_job_metadata(search_tool, metadata_llm, search_results, email_infos):
    job_metadata = []
    for sr, ei in zip(search_results, email_infos):
        sr = search_tool.invoke('Find me a job posting that matches the following specs: ' + json.dumps([ei['company'], ei['position']]))
        page_contents = ''
        if not sr['organic']:
            response = metadata_llm.invoke(f'Given the following internet search results for a given job, do your best to fill the information (location, pay, and description). The job description should be that of a standard job descrition that can be found on a company\'s website, not simply pulled from the search results. If you cannot then simply use the default values. Here are the results: {ei["company"]}\n{ei["position"]}')
            job_metadata.append(json.loads(response['raw'].additional_kwargs['tool_calls'][0]['function']['arguments']))
            continue
        soup = BeautifulSoup(requests.get(sr['organic'][0]['link'], headers = {'User-agent': 'your bot 0.1'}).text, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        page_contents += text
        response = metadata_llm.invoke(f'Given the following internet search results for a given job, do your best to fill the information (location, pay, and description). The job description should be that of a standard job descrition that can be found on a company\'s website, not simply pulled from the search results. If you cannot then simply use the default values. Here are the results:\n{page_contents[50:1000]}')
        job_metadata.append(json.loads(response['raw'].additional_kwargs['tool_calls'][0]['function']['arguments']))
    return job_metadata

def get_email_data(test: bool = False):
    if not test:
        # establish gmail connection
        gmail_tools, search_tool = init_gmail_conn()
        print('initialized gmail connection...')

        # initialize llms
        gmail_llm = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview", temperature=0).bind_tools([gmail_tools[2]])
        parser_llm = ChatGroq(model='llama3-groq-70b-8192-tool-use-preview', temperature=0).with_structured_output(JobInfo, include_raw=True)
        metadata_llm = ChatGroq(model='llama3-groq-70b-8192-tool-use-preview', temperature=0).with_structured_output(JobMetadata, include_raw=True)
        print('initialized llms...')

        # get emails
        emails = get_emails(gmail_llm, gmail_tools)
        print('collected emails...')

        # parse emails
        search_results, email_infos = parse_emails(emails, parser_llm, search_tool)
        print('parsed emails...')

        # get job metadata
        job_metadata = get_job_metadata(search_tool, metadata_llm, search_results, email_infos)
        print('retrieved job metadata...')
        return email_infos, job_metadata
    else:
        metadata = test_metadata()
        email_infos = parse_tests()
        return metadata, email_infos