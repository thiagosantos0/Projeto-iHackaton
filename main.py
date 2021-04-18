import methods as mtds



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
    
    query = mtds.searchGame(input_game, dados_instanciados)
    
    
    if query:
        start_time = query.date
        start_time, end_time, timezone = mtds.eventConfiguration(start_time)
        print(f"Jogo encontrado!! {input_game}")
        option = str(input("Deseja criar um lembrete no Google Calendar? [ S ] - Sim || [ N ] - Não: "))
        driver.quit()
        
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