import pandas as pd

raw_text = b'{"requestId":2, "events":[{"eventId":"ID:JBM-61798579","eventType":"ENTITY","eventTimestamp":1608567046069,"eventMetadata":{"CHANGE_HISTORY_ID":"60130","PERSON_ID":"227004","TRANSACTION_ID":"b6ab4c53-d0d2-4c0d-967f-96260b87fc6b"},"entityName":"JobSubmission","entityId":94649,"entityEventType":"UPDATED","updatedProperties":["status"]},{"eventId":"ID:JBM-61798580","eventType":"ENTITY","eventTimestamp":1608567085482,"eventMetadata":{"CHANGE_HISTORY_ID":"60131","PERSON_ID":"227004","TRANSACTION_ID":"d4ac9259-b1bc-4233-ad9f-f3b11329c6d7"},"entityName":"JobSubmission","entityId":94649,"entityEventType":"UPDATED","updatedProperties":["status","comments"]}]}'

data = pd.read_json(raw_text)

df = data['events']

df = (pd.concat([pd.DataFrame.from_dict(item, orient='index').T for item in df]))

print (df['entityId'])