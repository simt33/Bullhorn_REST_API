from api_requests import *


# Number of days back to search for CV sends.
days_past = 1

# Gets all job submissions updated to reflect CV sends in the last n days
ids = get_cvs_jobsub_ids(days_past)

# Feeds jobSub ids back into API to pull back information on each job submission
jobsub_info = get_jobsub_info(ids)

# Extracts jobSub, candidate and jobOrder ids from the jobSubmission order, ready to feed again again through the API.
all_ids = data_extract_all_ids(jobsub_info)

get_candidate_info(all_ids['candidate_id'].tolist())