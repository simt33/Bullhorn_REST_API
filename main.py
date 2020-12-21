from passcodes import *
import requests
import webbrowser
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import date
import json


# Fetches authorization code from BH API. Passcodes and private details are stored in passcodes file (not in repository)
def request_auth_code():

    url = f"https://auth.bullhornstaffing.com/oauth/authorize?client_id={client_id}" \
          f"&response_type=code&action=Login&username={username}&password={password}" \
          f"&state={state_val}"

    print(url)

    response = requests.get(url)

    parsed = urlparse.urlparse(response.url)
    print(response.url)
    auth_code = (parse_qs(parsed.query)['code'])[0]
    print("Authorisation code is: " + auth_code)

    return auth_code


# Fetches access token from BH API
def get_token():

    url = f"https://auth.bullhornstaffing.com/oauth/token?" \
          "grant_type=authorization_code" \
          f"&code={auth}" \
          f"&client_id={client_id}" \
          f"&client_secret={client_secret}"

    response = requests.post(url)
    data = json.loads(response.content)
    token = data['access_token']
    print("Access token is: " + token)

    return token


# Logs into REST API with access token and returns session details
def rest_login():

    url = f"https://rest.bullhornstaffing.com/rest-services/login?version=*&access_token={token}"

    response = requests.post(url)
    data = json.loads(response.content)

    return data


def get_candidate_info(candidate_id):
      url = (restURL + f"entity/Candidate/{candidate_id}?BhRestToken={BhRestToken}&fields=firstName,lastName,email")

      response = requests.get(url)
      print(response.content)

def get_jobsub_info(jobsub_id):
    url = (restURL + f"entity/JobSubmission/{jobsub_id}?BhRestToken={BhRestToken}&fields=id, candidate, status")
    print(url)
    response = requests.get(url)
    print(response.content)


def get_jobsub_history(jobsub_id):
    url = (restURL + f"query/JobSubmissionHistory?where=dateAdded=&BhRestToken={BhRestToken}&fields=id")
    response = requests.get(url)
    print(response.content)


def get_jobsub_history_by_date(date):
    url = (restURL + f"query/JobSubmissionHistory?where=dateAdded>20201220&BhRestToken={BhRestToken}&fields=id,jobSubmission,status,dateAdded&count=100")
    print(url)
    response = requests.get(url)
    print(response.content)


def get_events(sub_id,max_events):
    url = (restURL + f"event/subscription/{sub_id}?BhRestToken={BhRestToken}&maxEvents={max_events}")
    response = requests.get(url)
    print(response.content)



def create_event_subscription(sub_id):
    url = (restURL + f"event/subscription/{sub_id}?BhRestToken={BhRestToken}&type=entity&names=JobSubmissionHistory&eventTypes=INSERTED,UPDATED,DELETED")

    response = requests.put(url)
    print (response.content)

# Authenticates and logs into REST API. Fetches sessions details into BhRestToken and restURL
auth = request_auth_code()
token = get_token()
session_details = rest_login()
BhRestToken = session_details['BhRestToken']
restURL = session_details['restUrl']

#create_event_subscription(104)

#get_events(103, 100)

#get_jobsub_info(94649)

get_jobsub_history_by_date('[20201213]')

