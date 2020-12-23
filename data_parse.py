import pandas as pd
import datetime

# Selects all jobsub changes where status was set to 'CV Sent' or 'CV send'. Returns a list of jobsub ids.
def data_extract_jobsub_ids_where_cvsent(input):

    data = pd.read_json(input)
    df = data['data']
    df = (pd.concat([pd.DataFrame.from_dict(item, orient='index').T for item in df]))
    df.info()
    df = df[(df['status'] == 'CV Sent') | (df['status'] == 'CV Send')]
    df = (pd.concat([pd.DataFrame.from_dict(item, orient='index').T for item in df['jobSubmission']]))
    df.info()
    jobsub_id_list = df['id'].to_list()

    return jobsub_id_list

def data_extract_all_ids(input):

    data = pd.read_json(input)
    jobsub_data = pd.DataFrame(data['data'].values.tolist())
    #print (jobsub_data)
    cand_data = pd.DataFrame(jobsub_data['candidate'].values.tolist())
    #print (cand_data)
    job_data = pd.DataFrame(jobsub_data['jobOrder'].values.tolist())

    all_ids = pd.concat((jobsub_data[['id', 'dateAdded']], cand_data['id'], job_data['id']), axis=1, join='inner')
    all_ids.columns = ['jobsub_id', 'jobsub_dateAdded','candidate_id', 'joborder_id']

    #print( all_ids)
    return (all_ids)


def data_flatten_nested_json(raw_df, level_to_drill):

    df = pd.DataFrame(raw_df[level_to_drill].values.tolist())
    return df


# Converts json to df and removes top 'data' level
def data_json_to_df(input):

    raw_df = pd.read_json(input)
    df = data_flatten_nested_json(raw_df,'data')
    return df

