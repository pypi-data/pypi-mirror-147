# pyAPI

É um pacote desenvolvido em Python que busca tornar simples o consumo de APIs, possibilitando consultá-las ou mesmo salvar os dados em diferentes formatos e bancos de dados.

## Instalação e atualização
Use o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar o pyAPI. Rode este comando para instalar atualizações do pacote também.
```bash
pip install 
```

## Glossário
- Consumer Key: 
- Consumer Secret:
- Access Token:
- Access Token Secret: 
- Request Token:
- Request Token Secret:
- Request Token URL:
- Authorize URL:
- Request Access Token URL:
- Base URL:
- Endpoint/Resource:
- Redirect URI:
- Authentication:
- Authorization:
- HTTP Header:

## Uso
```python
import json
import os
from dotenv import load_dotenv
from pyAPI import app
from pyAPI import auth
from pyAPI import utils
import requests
from config.paths import ROOT_DIR

# Configurações
load_dotenv(os.path.join(ROOT_DIR, 'config', 'conf', 'dev', '.env'))
request_access_token_url = os.environ.get('OA2_REQUEST_ACCESS_TOKEN_URL')
client_key = os.environ.get('OA2_CLIENT_KEY')
client_secret = os.environ.get('OA2_CLIENT_SECRET')
username = os.environ.get('OA2_USERNAME')
password = os.environ.get('OA2_PASSWORD')

# Obtendo o HTTP Header com Token de Acesso e URL da instância
base_url, auth_header = auth.auth_oauth2_salesforce(
    request_access_token_url=request_access_token_url,
    client_key=client_key,
    client_secret=client_secret,
    username=username,
    password=password
)

# Instanciando a API
salesforce = app.SetupAPI(base_url)

# Passando a parte de Authorization para o HTTP Header do objeto
salesforce.config_header(auth_header)

# Construindo a URL com endpoint para consumo
url = salesforce.build_url('services/data')

# Passando o Payload necessário para o POST e acrescentando o HTTP
#   Header de Content-Type: application/json
salesforce.config_header(Content_Type='application/json')
data = {
    "NewReg": False
}

# Consumindo a API
request = requests.post(url, headers=salesforce.headers, data=json.dumps(data))

# Printando informações sobre o objeto configurado até aqui
salesforce.info()

# Criando pandas.DataFrame e contando os registros
df = utils.json_to_df(request.json())
print(df.count())
```


## Contribuições
Pull requests são bem-vindos. Para grandes alterações, por favor, abra um Issue primeiro para discussão sobre o que você gostaria de mudar no projeto.

## Referências
- [Requests](https://docs.python-requests.org/en/latest/)
- [Rauth](https://rauth.readthedocs.io/en/latest/)
- [Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content](https://www.rfc-editor.org/rfc/rfc7231)
- [HTTP|MDN](https://developer.mozilla.org/pt-BR/docs/Web/HTTP)

## Lincença
[MIT](https://choosealicense.com/licenses/mit/)