import json
import jsons
import operator
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import logging
import requests
import pandas as pd
import os
import yaml

ops = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt
}

root_dir = os.path.abspath(os.path.dirname(__file__))
# retrieving base url
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    url_list = yaml.load(file, Loader=yaml.FullLoader)


def ask_dataframe(dataframe: pd.DataFrame, query: str):
    human2sql_request = {
        "dataframe": dataframe.to_dict(),
        "query": query
    }

    human2sql_url = url_list['BASE_URL_HUMAN2SQL_DEV']

    human2sql_response = requests.post(human2sql_url, json=human2sql_request)
    response_df = []
    if human2sql_response.ok:
        res = human2sql_response.json()
        if 'result' in res:
            all_dfs = res['result']
            for df in all_dfs:
                response_df.append(pd.DataFrame(df))
        if 'messages' in res and res['messages']:
            for mex in res['messages']:
                print(mex)
    else:
        print("Error: "+str(human2sql_response))

    return response_df


def get_conditional_phrases(conditions, phrase1, phrase2):
    bool_array = []
    for condition in conditions:
        for op in ops:
            if op in condition:
                splitted = condition.split(' ' + op + ' ')
                operator = ops[op]
                bool_array.append(operator(splitted[0], splitted[1]))
        # bool_array.append(eval(condition))
    if False in bool_array:
        return phrase2
    else:
        return phrase1


def get_random_synonymous(synonyms):
    random.seed()
    nKeys = len(synonyms.keys())
    pickedItem = random.randint(0, nKeys - 1)
    synPicked = synonyms[pickedItem]
    return synPicked


def words_to_digits(phrase):
    words = phrase.split(" ")
    num = []
    for word in words:
        if "." in word:
            word = word.replace(".", "")
        if "," in word:
            word = word.replace(",", "")
        if word.isdigit():
            num.append(int(word))
    return num


def add_random_synonymous_to_sentence(phrase, placeholder, synonyms):
    random.seed()
    nKeys = len(synonyms.keys())
    pickedItem = random.randint(0, nKeys - 1)
    synPicked = synonyms[pickedItem]
    phrase = phrase.replace(placeholder, synPicked)
    return phrase


def data2nl(df, examples=None, max_tokens=64, fit_items=True):
    # The parameter "df" is a dataframe, but it will be converted into a dict, and called df in each case

    if examples is None:
        examples = [["player=Cristiano Ronaldo, goals=10, team=Juventus", "Cristiano Ronaldo scored 10 goals for Juventus"]]
        print("Using a default example: \n" + str(examples) + "\n")

    if not df.empty:
        headers = {
            "Content-Type": "application/json"
        }

        dict_df = df.to_dict()

        data = {
            "df": dict_df,
            "examples": examples,
            "fit_items": fit_items,
            "max_tokens": max_tokens
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_CFC_DEV'] + "/nlg"

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            df_response = pd.DataFrame.from_dict(r.json()['dict_df'])
            return df_response
        except Exception as e:
            logging.error(str(e))
    else:
        print("Input DataFrame is empty!")
        df_response = pd.DataFrame()
        return df_response


def query_to_sql(smartquery, driver):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_sql"

    stringed_smartquery = jsons.dumps(smartquery, strip_nulls=True)
    smartquery = json.loads(stringed_smartquery)

    data = {
        "smartquery": smartquery,
        "driver": driver
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        sql = dict_response['sql']
        return sql
    except Exception as e:
        logging.error(str(e))


def complex_field_calculator(smartquery, driver):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_sql"

    stringed_smartquery = jsons.dumps(smartquery, strip_nulls=True)
    smartquery = json.loads(stringed_smartquery)

    data = {
        "smartquery": smartquery,
        "driver": driver
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        sql = dict_response['sql']
        return sql
    except Exception as e:
        logging.error(str(e))


def complex_filter_calculator(smartquery, driver):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_sql"

    stringed_smartquery = jsons.dumps(smartquery, strip_nulls=True)
    smartquery = json.loads(stringed_smartquery)

    data = {
        "smartquery": smartquery,
        "driver": driver
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        sql = dict_response['sql']
        return sql
    except Exception as e:
        logging.error(str(e))
