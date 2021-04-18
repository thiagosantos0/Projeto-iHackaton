import requests
import os
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def driverSetUp():
    option = webdriver.ChromeOptions()
    #option.add_argument('headless')
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
    driver = webdriver.Chrome("./chromedriver.exe", desired_capabilities=desired_capabilities, options=option)

    return driver

def getGames(html):
    return html.find_all("span", attrs={"class":"calendar_entry"})

def instantiation(data: list):
    instantiated_data = []

    for item in data:
        try:
            name = item.find("a").text
            platforms = item.find("em").text
            date = item.find("time").text

        
            temp = Game(name, platforms, date)
            instantiated_data.append(temp)
        except:
            break
        
    return instantiated_data

def readInput():
    input_str = sys.argv[1]
    return input_str

def clearConsole():
    os.system('clear')

def searchGame(input_game: str, dados_instanciados: list):
    return input_game in [x.getName() for x in dados_instanciados]    

class Game:
    ##Converter o date para Datetime object (lembrete)
    def __init__(self, name: str, platforms: str, date: str):
        self.name = name
        self.platforms = platforms
        self.date = date

    def getName(self):
        return self.name

    def __repr__(self):
        return f"Jogo: {self.name} || Plataformas: {self.platforms} || Data: {self.date}\n"

def main():
    ##Criando o driver
    url = "https://www.gameinformer.com/2021"
    driver = driverSetUp()
    driver.get(url)

    htmlSource = driver.page_source

    soup = BeautifulSoup(htmlSource, 'html.parser')
    dados = getGames(soup)
    dados_instanciados = instantiation(dados)
    
    input_game = readInput()
    #time.sleep(3)
    clearConsole()
    print(dados_instanciados[0])
    if searchGame(input_game, dados_instanciados):
        print(f"Jogo encontrado!! {input_game}")
        option = str(input("Deseja criar um lembrete no Google Calendar? [ S ] - Sim || [ N ] - Não: "))
        driver.close()
        if option.lower() == 's':
            print("Lembrete adicionado com sucesso!!")
        else:
            pass
        

    else:
        print("Jogo não encontrado!!")

if __name__ == '__main__':
    main()