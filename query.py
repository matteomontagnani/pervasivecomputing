from google.cloud import firestore
import statistics

year = 2009
species = "soybeans"

db = firestore.Client.from_service_account_json('client.json')

data = []

for doc in db.collection('kellogg_biological_process').where('year', '==', year).where('species', "==", species).limit(10).stream():
    res = doc.to_dict()
    data.append(res)




