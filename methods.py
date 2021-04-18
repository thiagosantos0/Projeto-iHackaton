import requests
import os
import sys
import time
from bs4 import BeautifulSoup
import pickle
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client 
from oauth2client import tools 
from oauth2client.file import Storage
from datetime import datetime, timedelta

def driverSetUp():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--log-level=3')
    option.add_argument('--ignore-ssl-errors=yes')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-certificate-errors-spki-list')
    option.add_argument('--disable-web-security')
    option.add_argument('--disable-features=VizDisplayCompositor')
    option.add_argument('--disable-breakpad')
    option.add_argument('--allow-insecure-localhost')
    desired_capabilities = option.to_capabilities()
    desired_capabilities['acceptInsecureCerts'] = True
    driver = webdriver.Chrome("./chromedriver.exe", desired_capabilities=desired_capabilities,service_args=["--verbose", "--log-path=chromerun.log"], options=option)

    return driver

def createSoup(htmlSource):
    '''
        Input: Data in HTML format
        Output: BeautifulSoup Object with parsed HTML.
    '''
    return BeautifulSoup(htmlSource, 'html.parser')

def getGames(html: BeautifulSoup):
    '''
        Input: BeautifulSoup Object.
        Output: list with the tags that contains the data about the games.
    '''
    return html.find_all("span", attrs={"class":"calendar_entry"})

def instantiation(data: list):
    '''
        Input: list with data about the games. (each element is in HTML format).
        Output: list with "Game" objects.
    '''
    instantiated_data = []

    for item in data:
        try:
            name = item.find("a").text
            platforms = item.find("em").text
            date = parser.parse(item.find("time").text)

        
            temp = Game(name, platforms, date)
            instantiated_data.append(temp)
        except:
            break
        
    return instantiated_data

def readInput():
    with open(r"/mnt/c/Users/thiag/OneDrive/Área de Trabalho/private/game_input.txt", 'r') as f:
        temp = f.read()
    return temp

def clearConsole():
    os.system('clear')

def searchGame(input_game: str, dados_instanciados: list):
    '''
        Input: Interest game and "Game" object list.
        Output: If found, "game" object, if not, False indicating that the game was not found.
    '''
    for x in dados_instanciados:
        if x.getName() == input_game:
            return x

    return False

def get_authenticated_service():
    credential_path = r"/mnt/c/Users/thiag/OneDrive/Área de Trabalho/private/token.pkl"
    store = Storage(credential_path)
    credentials = store.get()
    scopes = ["https://www.googleapis.com/auth/calendar"]
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, scopes)
        credentials = tools.run_flow(flow, store)
    return build('calendar', 'v3', credentials=credentials)


def getCalendarID(service):
    result = service.calendarList().list().execute()
    return result['items'][0]['id']

def createEvent(start_time, end_time, timezone, game):
    event = {
        'summary': 'Lançamento - ' + game.name,
        'location': '',
        'description': game.platforms,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return event


def insertEvent(service, event):
    service.events().insert(calendarId=getCalendarID(service), body=event).execute()

def setStartTime(date):
    return parser.parse(date)

def eventConfiguration(start_time):
    
    end_time = start_time + timedelta(hours=1)
    timezone = "Brazil/East"
    return start_time, end_time, timezone

class Game:
    def __init__(self, name: str, platforms: str, date: str):
        self.name = name
        self.platforms = platforms
        self.date = date

    def getName(self):
        return self.name

    def __repr__(self):
        return f"Jogo: {self.name} || Plataformas: {self.platforms} || Data: {self.date}\n"

