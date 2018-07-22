#!/usr/bin/env python
import json
import requests
import config
from datetime import timedelta
from datetime import datetime


# Default Vars
start_day = datetime.now()
end_day = datetime.now() + timedelta(days=5)
base_url = "https://api.trello.com/1/"


# Default Dictionaries
query_params = {
        "key" : config.api_key,
        "token" : config.api_token
}

default_labels = {
    "Done" : "green",
    "In Progress": "yellow",
    "Pending Outside Interaction" : "red",
    "Work Task" : "blue",
    "Personal Task" : "black",
    "Unexpected Personal Task" : "pink",
    "Unexpected Work Task" : "orange"
}

default_lists = {
    "Planned Tasks" : "128",
    "Unplanned Tasks" : "192",
    "In Progress" : "256",
    "Done" : "384",
    "Carry-Over" : "512",
    "Won't Do" : "4096"
}


##########


def reset_params():
    """
    quick way to reset the default parameters
    """
    query_params = {
            "key" : config.api_key,
            "token" : config.api_token
    }


def find_board_id_by_name(board_name, params=query_params, board_status='open'):
    """
    find an any board by name
    """
    url = base_url + 'members/me/boards/'
    params['filter'] = board_status
    response = requests.get(url, params)
    board_data = json.loads(response.content)
    for board in board_data:
        if board_name == board['name']:
            return board['id']
    reset_params


def create_board(board_name, params=query_params):
    """
    Create the initial board
    This creates a clean board with no Labels or Lists
    """
    board_url = base_url + 'boards'
    params['name'] = board_name,
    params['defaultLists'] = "false",
    params['defaultLabels'] = "false",
    params['prefs_background'] = "grey"
    try:
        response = requests.request("POST", board_url, params=params)
        response_data = json.loads(response.content)
        reset_params
        print "%s Created!" % (board_name)
        return True
    except: 
        print "Something went wrong, please try again"
        return


def add_labels(board_id, labels_dict):
    """
    add expected labels
    """
    labels_url = base_url + 'boards/' + board_id + '/labels'
    for label_name, label_color in labels_dict.iteritems():
        query_params = {
            "key" : config.api_key,
            "token" : config.api_token,
            "name" : label_name,
            "color" : label_color
        }
        response = requests.request("POST", labels_url, params=query_params)
        print "%s Label Added" % label_name
    return True


def add_lists(board_id, list_dict):
    """
    add expected lists
    """
    lists_url = base_url + 'boards/' + board_id + '/lists'
    for list_name, list_position in list_dict.iteritems():
        query_params = {
            "key" : config.api_key,
            "token" : config.api_token,
            "name" : list_name,
            "pos" : list_position
        }
        response = requests.request("POST", lists_url, params=query_params)
        print "%s List Added" % list_name
    return True


def run_tasks(board_name):
    create_response = create_board(board_name)
    label_response = add_labels(find_board_id_by_name(board_name), default_labels)
    list_response = add_lists(find_board_id_by_name(board_name), default_lists)
    if create_response is True and label_response is True and list_response is True:
        print "[o] All Tasks Successful"
    else: 
        print "[X] ERROR: One or more Tasks Failed"
    

def main():
    board_name =  "Week of " + start_day.strftime("%b %d") + " - " + end_day.strftime("%b %d")
    run_tasks(board_name)



if __name__ == '__main__':
    main()
