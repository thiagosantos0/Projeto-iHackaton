# Projeto-iHackaton
Este projeto foi criado com o objetivo de ser submetido para o evento "iHackaton" da iJunior, onde o tema foi **automação**.

## Sobre o script:
 Primeiramente, utilizamos o **Selenium** (um WebDriver amplamente utilizado em testes automatizados) para abrir a página em segundo plano, onde obtemos os dados de lançamento dos jogos. A partir daí, utilizamos a biblioteca BeautifulSoup para poder fazer um “parse” dos dados que coletamos em formato html. Segue abaixo a função responsável por criar uma lista com os dados dos jogos obtidos em formato HTML:
```
def getGames(html: BeautifulSoup):
    '''
        Input: BeautifulSoup Object.
        Output: list with the tags that contains the data about the games.
    '''
    return html.find_all("span", attrs={"class":"calendar_entry"})
```

Seguindo, temos uma etapa de instanciação de uma classe onde criamos objetos “Game” para cada elemento da lista. Fazendo desta forma, podemos manipular de forma mais simplificada os dados que foram fornecidos e facilitar a criação de métodos mais complexos num futuro. Com os dados em mãos, a execução em segundo plano do WebDriver é então encerrada e tem-se o início da etapa de configuração da API do Google Calendar.
 
O seguinte método é responsável pela leitura do “token” de acesso ao Google Calendar do usuário, na primeira execução o “token” não estará no arquivo (ou estará desatualizado/inválido) e nesse caso **será necessário a confirmação de permissão do usuário**, para execuções seguintes, o “token” é guardado a fim de automatizar o processo de permissão de acesso.

```
def get_authenticated_service():
    credential_path = r"/mnt/c/Users/thiag/OneDrive/Área de Trabalho/private/token.pkl"
    store = Storage(credential_path)
    credentials = store.get()
    scopes = ["https://www.googleapis.com/auth/calendar"]
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, scopes)
        credentials = tools.run_flow(flow, store)
    return build('calendar', 'v3', credentials=credentials)
```
Depois deste passo a configuração está completa.

## Funcionamento:
Três arquivos externos são necessários:
		**Primeiro:** Arquivo contendo o nome do jogo a ser pesquisado.
		**Segundo:** Arquivo .json contendo as credenciais da API do Google Agenda.
		**Terceiro:** Gerado automaticamente. Contém o hash de permissão de acesso ao Google Calendar do usuário. (Isto foi feito para evitar a atividade repetitiva de permitir o acesso a cada execução.)
		O jogo presente no arquivo de entrada é então procurado na base de dados que foi coletada e, se encontrado, pergunta ao usuário se ele deseja fazer um evento automaticamente no Google Calendar no dia do lançamento do jogo em questão. Caso o jogo não for encontrado, a mensagem “Jogo não encontrado” será exibida no terminal.


## Guia para reproduzir localmente:
*PDF com o guia para rodar o script localmente: [PDF](https://docs.google.com/document/d/1ZOlzRWwjN_eufH4mNfXJrsYaXgW2XWKz75QBpW9vHRk/edit?usp=sharing)*


*Criado por: [Thiago Santos](https://github.com/thiagosantos0) e [João Viola](https://github.com/jadviola)* <br/>
*Fonte dos dados: [gameinformer](https://www.gameinformer.com/2021)*
