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
    mode: Literal['Remote, In-Person, Hybrid']

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

def get_email_data():
    # establish gmail connection
    gmail_tools, search_tool = init_gmail_conn()

    # initialize llms
    gmail_llm = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview", temperature=0).bind_tools([gmail_tools[2]])
    parser_llm = ChatGroq(model='llama3-groq-70b-8192-tool-use-preview', temperature=0).with_structured_output(JobInfo, include_raw=True)
    metadata_llm = ChatGroq(model='llama3-groq-70b-8192-tool-use-preview', temperature=0).with_structured_output(JobMetadata, include_raw=True)

    # get emails
    emails = get_emails(gmail_llm, gmail_tools)

    # parse emails
    search_results, email_infos = parse_emails(emails, parser_llm, search_tool)

    # get job metadata
    job_metadata = get_job_metadata(search_tool, metadata_llm, search_results, email_infos)
    return email_infos, job_metadata