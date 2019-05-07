import requests
import logging
import json


def nrPut(inurl, inlickey, inlogging, payload):

    headers = {}
    headers['X-Api-Key'] = inlickey
    headers['Content-Type'] = 'application/json'

    r = requests.put(inurl, headers=headers, data=payload)
    return r.text


def nrGet(inurl, inlickey, inlogging):

    headers = {}
    headers['X-Api-Key'] = inlickey
    headers['Accept'] = 'application/json'

    r = requests.get(inurl, headers=headers)
    return r.text






