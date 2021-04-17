import requests
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def readCredentials():
    credenciais = []
    with open (r"/mnt/c/Users/thiag/OneDrive/Área de Trabalho/credenciais.txt", 'r') as f:
        return f.read().splitlines()

def login(credenciais: list, driver):
    email_field = driver.find_element_by_id("user_email")
    password_field = driver.find_element_by_id("user_password")
    email_field.send_keys(credenciais[0])
    email_field.send_keys(Keys.RETURN)
    password_field.send_keys(credenciais[1])
    password_field.send_keys(Keys.RETURN)

def driverSetUp():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome("./chromedriver.exe", options=option)

    return driver


def allEvents(soup):
    if soup: data = []
    for heading in soup.find_all("div", attrs={"class": "col-sm-8"}):
        firstParentClass = heading.find_parent('div')['class'][0]
        if firstParentClass == 'row':
            data.append(heading)
    return data




def main():
    ##Criando o driver
    url = "https://portal.brasiljunior.org.br/agenda/eventos?page=1"
    driver = driverSetUp()
    driver.get(url)
    
    time.sleep(3)

    ##Leitura das credenciais
    credenciais = readCredentials()
    login(credenciais, driver)


    driver.get(url)
    time.sleep(2)
    htmlSource = driver.page_source
    
    soup = BeautifulSoup(htmlSource, 'html.parser')
    dados = allEvents(soup)
    print(dados[0])
    



if __name__ == '__main__':
    main()