from email_monitor import EmailMonitor

monitor = EmailMonitor(credentials_file="google-cloud/client_secret_275014340897-k0gsju7fh1giri9ilim7cpt001hdrn4d.apps.googleusercontent.com.json")
email = monitor.search_mail(
    query={ "from": "careerbrew@substack.com" },
    wait_for_match=True,
    unread=True,
    labels=["INBOX", "UPDATES"],
    delay=10
)
print(email)