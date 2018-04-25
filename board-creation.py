#!/usr/bin/env python
import json
import requests
import config

base_url = "https://api.trello.com/1/"

def create_board(board_name):
    board_url = base_url + 'boards'
    query_params = {
        "name" : board_name,
        "key" : config.api_key,
        "defaultLists" : "false",
        "defaultLabels" : "false",
        "token" : config.api_token
    }
    response = requests.request("POST", board_url, params=query_params)
    response_data = json.loads(response.content)
    return response_data['id']

print create_board("TESTING")
