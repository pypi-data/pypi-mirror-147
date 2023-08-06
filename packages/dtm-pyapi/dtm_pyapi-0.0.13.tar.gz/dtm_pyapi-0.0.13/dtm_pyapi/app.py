"""
Este módulo implementa a aplicação.
"""

from . import utils


class SetupAPI():
    """
    Configura os parâmetros para a API que será utilizada.

    Attributes
    -----------
    base_url : str
        URL da API sem nenhum endpoint ou argumento.
    headers : dict
        Cabeçalho com parâmetros para as requisições HTTP.
    endpoints : list
        Lista de endpoints configurados.

    Methods
    -------
    config_header(self, **kwargs):
        Configura o Header HTTP para as requisições pela API.
    build_url(self, *args):
        Monta a URL que será usada para a requisição à API.
    """

    def config_header(self, header=None,**kwargs):
        """
        Configura o Header HTTP para as requisições pela API.
        Ao invés de informar valores com '-', informe com '_'.
        Será feito o parse e substituição pelo '-' no método.

        Parameters
        ----------
        header : dict
            Dicionário com HTTP Header já definido e que precisa ser
            adicionado ao atributo headers do objeto da API.

        **kwargs
            Parâmetros de chave-valor arbitrários. A chave deve
            ser passada sem aspas e o valor com aspas se for string.

        Returns
        -------
        None
        """
        if kwargs:
            headers = {
                (key.replace('_', '-') if '_' in key else key) : value
                for key, value in kwargs.items()
            }
        if header:
            headers = header
        self.headers.update(headers)

    def set_endpoint(self, *args):
        """
        Configura os endpoints possíveis para consumo da API.

        Parameters
        ----------
        *args : list
            Podem ser passados:
                - recursos: usuario; area/departamento; etc.
                - versões: v1; v2.5; v54.0; etc.
            Podem ser passados juntos como "v1/area/departamento" ou
            separados como "v1", "area", "departamento".

        Returns
        -------
        None
        """
        url = '/'.join(args)
        self.endpoints.append(url)

    def get_endpoints_list(self):
        """
        Retorna uma lista com todos os endpoints já configurados.

        Parameters
        ----------
        None

        Returns
        -------
        endpoints : list
            Lista contendo todos os endpoints já configurados para a API.
        """
        endpoints = self.endpoints
        return endpoints

    def build_url(self, endpoint):
        """
        Monta a URL que será usada para a requisição à API.

        Parameters
        ----------
        enpoint : str
            Recurso que será acessado.

        Returns
        -------
        url : str
            URL final que será usada na requisição.
        """
        if endpoint not in self.endpoints:
            self.set_endpoint(endpoint)
        url = self.base_url + endpoint
        return url

    def __repr__(self) -> str:
        return utils.prettify_json(vars(self))

    def __init__(self, base_url,
                    accept='*/*',
                    accept_encoding='gzip, deflate, br',
                    connection='keep-alive'):
        """
        Construtor da classe

        Parameters
        ----------
        base_url : str
            URL da API sem nenhum endpoint ou argumento.
        accept : str
            Indica qual tipo de conteúdo o cliente consegue entender. É
            enviado pelo cliente para o servidor.
        accept_encoding : str
            Indica qual codificação de conteúdo o cliente está apto a
            entender.
        connection : str
            Controla se a conexão se mantém aberta ou não após o fim da
            transação atual.
        headers : dict
            Dicionário contendo pares chave-valor com os itens que
            serão enviados pelo cabeçalho HTTP nas requisições.
        """
        if not base_url.endswith('/'):
            self.base_url = base_url + '/'
        else:
            self.base_url = base_url

        self.endpoints = []

        self.headers = {}
        self.config_header(Accept=accept,
                            Accept_Encoding=accept_encoding,
                            Connection=connection)
