from bs4 import BeautifulSoup
import requests

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def getLegislatorEmails(name, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mailtos = soup.select("a[href]")
    emailList = []
    for i in mailtos:
        if "mailto:" in i["href"]:
            emailList.append(i["href"])
    emails = [email.lstrip("mailto:") for email in emailList]
    return (name, emails)


def gmail_send_message(creds):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content("This is automated draft mail")

        message["To"] = "gduser1@workspacesamples.dev"
        message["From"] = "gduser2@workspacesamples.dev"
        message["Subject"] = "Automated draft"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message
