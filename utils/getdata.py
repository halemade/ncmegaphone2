from bs4 import BeautifulSoup
import requests


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
