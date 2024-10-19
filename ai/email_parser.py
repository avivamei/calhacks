import os
import json
import getpass

from pprint import pprint
from typing import Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from langchain_google_community import GmailToolkit
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_community.gmail.utils import clean_email_body
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials

from search_promtps import BASE_SEARCH, NEW_APPLICATIONS

load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

# setup Gmail toolkit
credentials = get_gmail_credentials(
    scopes=["https://mail.google.com/"],
    client_secrets_file="oauth/client_secret_163202554535-p6pfh8qs471c2b10tusiqr4p8gnn48qi.apps.googleusercontent.com.json",
)
api_resource = build_resource_service(credentials=credentials)
gmail_toolkit = GmailToolkit(api_resource=api_resource)
gmail_tools = gmail_toolkit.get_tools()
gmail_llm = ChatGroq(model="llama3-groq-8b-8192-tool-use-preview", temperature=0, max_retries=2).bind_tools(gmail_tools)

serper_search = GoogleSerperAPIWrapper()
search_tool = Tool(name='serper_search', func=serper_search.run, description='Useful for when you need to search for information on the internet.')

response = gmail_llm.invoke([
    ('system', BASE_SEARCH.format(status='new applications only', num_results='15')),
    ('user', NEW_APPLICATIONS)
])
print(response.tool_calls)
emails = []
for tc in response.tool_calls:
    tool = list(filter(lambda x: x.name == tc['name'], gmail_tools))[0]
    tool_out = tool.invoke(tc)
    print(tool_out)
    tool_outputs = json.loads(tool_out.content)
    emails.extend(tool_outputs)

for e in emails:
    e['body'] = e['body'].replace('\n', '').replace('\r', '')
    pprint(e)
print(f'Found {len(emails)} emails!')