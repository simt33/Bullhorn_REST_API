import requests
import urllib.parse as urlparse
import json
import datetime
from passcodes import *
from data_parse import *
from urllib.parse import parse_qs


# Fetches authorization code from BH API. Passcodes and private details are stored in passcodes file (not in repository)
def request_auth_code():

    url = f"https://auth.bullhornstaffing.com/oauth/authorize?client_id={client_id}" \
          f"&response_type=code&action=Login&username={username}&password={password}" \
          f"&state={state_val}"

    response = requests.get(url)

    parsed = urlparse.urlparse(response.url)
    auth_code = (parse_qs(parsed.query)['code'])[0]

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

# Fetches candidate info from id or list of ids
def get_candidate_info(candidate_id):
    if isinstance(candidate_id, str):
        candidate_id_string = candidate_id
    elif isinstance(candidate_id, list):
        candidate_id_string = ','.join(str(e) for e in candidate_id)

    url = (restURL + f"entity/Candidate/{candidate_id_string}?BhRestToken={BhRestToken}&fields=id,firstName,lastName,email")

    response = requests.get(url)
    return response.content

# Fetches job info from id or list of ids
def get_jobOrder_info(joborder_id):
    if isinstance(joborder_id, str):
        joborder_id_string = joborder_id
    elif isinstance(joborder_id, list):
        joborder_id_string = ','.join(str(e) for e in joborder_id)

    url = (restURL + f"entity/JobOrder/{joborder_id_string}?BhRestToken={BhRestToken}&fields=id,title,clientCorporation")

    response = requests.get(url)

    return response.content

# Fetches jobsub info from id or list of ids
def get_jobsub_info(jobsub_id):
    if isinstance(jobsub_id, str):
        jobsub_id_string = jobsub_id
    elif isinstance(jobsub_id, list):
        jobsub_id_string = ','.join(str(e) for e in jobsub_id)

    url = (restURL + f"entity/JobSubmission/{jobsub_id_string}?BhRestToken={BhRestToken}&fields=id, candidate, status, jobOrder, dateAdded")

    response = requests.get(url)

    return response.content


# Fetches jobsub_history info by jobsub id
def get_jobsub_history(jobsub_id):
    url = (restURL + f"query/JobSubmissionHistory?where=dateAdded=&BhRestToken={BhRestToken}&fields=id")
    response = requests.get(url)


#Fetches all jobsub
def get_cvs_jobsub_ids(days):

    # Fetches jobsub_history since n number of days ago
    def get_jobsub_history_by_date(days):

        # Returns date, backdated by n days, in UNIX Epoch time
        def get_previous_date(days):
            date = datetime.datetime.today() - datetime.timedelta(days=days)
            date_adj = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second,
                                         date.microsecond).timestamp()
            date_adj = int(date_adj * 1000)
            return date_adj

        date = get_previous_date(days)
        url = (restURL + f"query/JobSubmissionHistory?where=dateAdded>{date}&BhRestToken={BhRestToken}&fields=id,jobSubmission,status,dateAdded&count=500")

        response = requests.get(url)

        return response.content

    jobsub_hist_response = get_jobsub_history_by_date(days)

    print (jobsub_hist_response)

    jobsub_ids = data_extract_jobsub_ids_where_cvsent(jobsub_hist_response)

    print (jobsub_ids)
    return (jobsub_ids)


auth = request_auth_code()
token = get_token()
session_details = rest_login()
BhRestToken = session_details['BhRestToken']
restURL = session_details['restUrl']