from api_requests import *

# Number of days back to search for CV sends.
days_past = 3



# Gets all job submissions updated to reflect CV sends in the last n days
ids = get_cvs_jobsub_ids(days_past)

# Feeds jobSub ids back into API to pull back information on each job submission
jobsub_info = get_jobsub_info(ids)

# Extracts jobSub, candidate and jobOrder ids from the jobSubmission order, ready to feed again again through the API.
all_ids = data_extract_all_ids(jobsub_info)

cand_info = get_candidate_info(all_ids['candidate_id'].tolist())
joborder_info = get_jobOrder_info(all_ids['joborder_id'].tolist())

cand_info_df = data_json_to_df(cand_info)
job_info_df = data_json_to_df(joborder_info)

client_name = data_flatten_nested_json(job_info_df, 'clientCorporation')['name']

job_info_all = pd.concat([job_info_df[['id', 'title']],client_name],axis = 1, join='inner')
job_info_all.columns = ['id','job_title', 'client_name']

all_data = all_ids.merge(cand_info_df, left_on='candidate_id', right_on='id', suffixes=('_all', '_candidate'))
all_data = all_data.merge(job_info_all, left_on='joborder_id', right_on='id', suffixes=('_all', '_jobOrder'))

print (all_data)


