"""
Este módulo implementa funções utilitárias para o pacote.
"""
import json
import os
import pandas as pd


def prettify_json(raw_json):
    """
    Função utilitária que traz o JSON formatado para facilitar leitura.

    Parameters
    ----------
    raw_json : str
        Texto em JSON cru sem formatação.

    Returns
    -------
    pretty_json : str
        JSON formatado conforme os parâmetros passados para o
        json.dumps()
    """
    pretty_json = json.dumps(raw_json, sort_keys=True, indent=4)
    return pretty_json


def json_to_df(input_json):
    """
    Função utilitária que converte o JSON de entrada em um
    pandas.DataFrame, desde que tenha somente um nível (não seja semi-
    estruturado).

    Parameters
    ----------
    input_json : str
        Texto em JSON.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame do pandas com os dados do JSON convertido.
    """
    if isinstance(input_json, list):
        df = pd.DataFrame.from_dict(input_json)
    elif isinstance(input_json, str):
        try:
            df = pd.read_json(input_json)
        except ValueError as ex:
            print(ex)
    else:
        raise ValueError('Parâmetro passado na função é inválido.')
    return df


def save_into_file(input_json,
                    output_path,
                    fileformat='json',
                    filename='output'):
    """
    Função utilitária que converte e salva o JSON de entrada em
    diferentes formatos, desde que tenha somente um nível (não seja
    semi-estruturado).

    Parameters
    ----------
    input_json : str
        Texto em JSON.

    output_path : str
        Caminho para salvar o arquivo de saída.

    fileformat : str
        Opção de salvamento. Pode ser: json ou csv.

    filename : str
        Nome do arquivo final sem o formato.

    Returns
    -------
    None
    """
    fileformat = fileformat.lower()
    accepted_formats = ['csv', 'json']

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if fileformat not in accepted_formats:
        raise ValueError(f'Especificar formato de salvamento: {accepted_formats}')

    if fileformat == 'json':
        try:
            with open(output_path + '/' + f'{filename}.json', 'w') as p:
                json.dump(input_json, p)
        except Exception as ex:
            print(ex)

    elif fileformat == 'csv':
        try:
            df = json_to_df(input_json)
            df.to_csv(output_path + f'{filename}.csv')
        except Exception as ex:
            print(ex)

# TODO: Implementar o utilitário para integração com Redshift
# TODO: Implementar o utilitário para integração com MS SQL Server
