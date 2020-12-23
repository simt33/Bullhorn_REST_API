import pandas as pd
import datetime


def get_jobsub_ids_from_cvsends(input):

    data = pd.read_json(input)
    df = data['data']
    df = (pd.concat([pd.DataFrame.from_dict(item, orient='index').T for item in df]))
    df.info()
    print (df)
    df = df[(df['status'] == 'CV Sent') | (df['status'] == 'CV Send')]
    df = (pd.concat([pd.DataFrame.from_dict(item, orient='index').T for item in df['jobSubmission']]))
    df.info()
    jobsub_id_list = df['id'].to_list()

    return jobsub_id_list

def list_to_str():

    list = [13, 14, 3351]
    string = ','.join(str(e) for e in list)

    print (string)

list_to_str()