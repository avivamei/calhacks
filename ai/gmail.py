# from email_monitor import EmailMonitor

# monitor = EmailMonitor(credentials_file="oauth/client_secret_163202554535-p6pfh8qs471c2b10tusiqr4p8gnn48qi.apps.googleusercontent.com.json")
# email = monitor.search_mail(
#     query={ "from": "notifications-noreply@linkedin.com" },
#     wait_for_match=True,
#     unread=False,
#     labels=["INBOX"],
#     delay=10
# )
# print(email)

from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials

# setup Gmail toolkit
credentials = get_gmail_credentials(
    scopes=["https://mail.google.com/"],
    client_secrets_file="oauth/client_secret_163202554535-p6pfh8qs471c2b10tusiqr4p8gnn48qi.apps.googleusercontent.com.json",
)
api_resource = build_resource_service(credentials=credentials)
gmail_toolkit = GmailToolkit(api_resource=api_resource)
gmail_tools = gmail_toolkit.get_tools()
