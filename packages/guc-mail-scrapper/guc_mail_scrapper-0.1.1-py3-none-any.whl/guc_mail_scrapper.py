from contextlib import contextmanager
from typing import Generator
import urllib.parse
from bs4 import BeautifulSoup
import requests
import re
import os
import urllib

GUC_MAIL_BASE_URL = os.getenv("GUC_MAIL_BASE_URL", "https://mail.guc.edu.eg/owa/")


class InvalidCredentialsError(Exception):
    pass


class ForwardEmailError(Exception):
    pass

@contextmanager
def get_authenticated_session(username: str, password: str) -> Generator[requests.Session, None, None]:
    session = requests.Session()

    session.post(
        GUC_MAIL_BASE_URL + "auth.owa",
        data={
            "destination": GUC_MAIL_BASE_URL,
            "flags": "4",
            "forcedownlevel": "0",
            "username": username,
            "password": password,
        },
    )

    if not is_authenticated(session):
        raise InvalidCredentialsError()

    print("Authenticated")
    
    yield session
    
    logout(session)
    

def logout(session: requests.Session):
    soup = BeautifulSoup(session.get(GUC_MAIL_BASE_URL).text, "html.parser")
    on_click = soup.select_one("#lo")["onclick"] # return onClkLgf('NOk0GdYSsEKNQ_bepP5X-wv0bgnI8twIXZfSIzjtxmf8PP0YayZDL4_2TlEaagsK7zLPH9gsVOo.');        
    canary = re.search(r"^return onClkLgf\('(.*)'\);$", on_click).group(1)
    session.get(f"{GUC_MAIL_BASE_URL}/logoff.owa?canary={urllib.parse.quote(canary)}")
            
    if is_authenticated(session):
        raise Exception("Failed to logout")
    
    print("Logged out")
    

def is_authenticated(session: requests.Session) -> bool:
    req = session.get(GUC_MAIL_BASE_URL, allow_redirects=False)
    return req.text.find("Inbox") != -1

class GucMailScrapper:
    def __init__(self, authenticated_session: requests.Session):
        self.authenticated_session = authenticated_session

    def count_mail_pages(self) -> int:
        res = self.authenticated_session.get(GUC_MAIL_BASE_URL)
        soup = BeautifulSoup(res.text, "html.parser")
        pages = soup.select(".pTxt")
        return len(pages)

    def get_mail_ids(self, page: int) -> list[str]:
        res = self.session.get(f"{GUC_MAIL_BASE_URL}?pg={page}")
        soup = BeautifulSoup(res.text, "html.parser")

        mails = [checkbox["value"] for checkbox in soup.select('input[name="chkmsg"]')]

        return mails

    def forward_mail(self, mail_id: str, forward_to: str):
        url_encoded_mail_id = requests.utils.quote(mail_id)
        read_url = f"{GUC_MAIL_BASE_URL}?ae=PreFormAction&t=IPM.Note&a=Forward&id={url_encoded_mail_id}"
        response = self.authenticated_session.get(read_url)

        soup = BeautifulSoup(response.text, "html.parser")

        inputs = {
            input["name"]: input["value"]
            for input in soup.select("input")
            if input.has_attr("name") and input.has_attr("value")
        }

        inputs["txtbdy"] = soup.select_one("#txtbdyldr").text
        inputs["txtsbj"] = soup.select_one("#txtsbjldr")["value"]
        inputs["txtto"] = forward_to
        inputs["hidcmdpst"] = "snd"

        forward_url = f"{GUC_MAIL_BASE_URL}?ae=PreFormAction&t=IPM.Note&a=Send"
        response = self.authenticated_session.post(forward_url, data=inputs)

        if response.status_code != 200:
            raise ForwardEmailError()
