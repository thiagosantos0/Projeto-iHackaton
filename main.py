import methods as mtds
from bs4 import BeautifulSoup


CLIENT_SECRETS_FILE = r"/mnt/c/Users/thiag/OneDrive/Área de Trabalho/private/client_secret.json"


def main():
    ##Criando o driver
    url = "https://www.gameinformer.com/2021"
    driver = mtds.driverSetUp()
    driver.get(url)

    htmlSource = driver.page_source

    soup = mtds.createSoup(htmlSource)
    dados = mtds.getGames(soup)
    dados_instanciados = mtds.instantiation(dados)
    input_game = mtds.readInput()

    ##Configurando GoogleApplication
    service = mtds.get_authenticated_service()
    
    #time.sleep(3)
    #clearConsole()
    query = mtds.searchGame(input_game, dados_instanciados)
    start_time = query.date
    start_time, end_time, timezone = mtds.eventConfiguration(start_time)
    #print(f"Data: {query.date}")
    #print(getCalendarID(service))
    if query:
        print(f"Jogo encontrado!! {input_game}")
        option = str(input("Deseja criar um lembrete no Google Calendar? [ S ] - Sim || [ N ] - Não: "))
        driver.close()
        
        if option.lower() == 's':
            event = mtds.createEvent(start_time, end_time, timezone, query)
            mtds.insertEvent(service, event)
            print("Lembrete adicionado com sucesso!!")
        else:
            pass

    else:
        print("Jogo não encontrado!!")

if __name__ == '__main__':
    main()