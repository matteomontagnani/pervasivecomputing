from google.cloud import firestore
import time

# anno dei dati
year = 2012

# variabile del database
db = firestore.Client.from_service_account_json('client.json')

# batch to load all data in one time
batch = db.batch()

# leggi il file
file = open('{}.txt'.format(year), 'r')

# ottieni le righe
lines = file.readlines()

# conta le righe
count = 1
# per ogni riga
for l in lines:
    # pulisci gli spazi bianchi
    data = l.strip()

    # esempio di dati
    #longitude,latitude,yield,species,moisture,year,
    #-85.3726570729292,42.4123191318918,38.56,soybeans,0.03,2012

    batch.set(db.collection('kellogg_biological_process').document(), 
    {
        u"moisture": data.split(",")[4],
        u"posizione_lat":  data.split(",")[1],
        u"posizione_long": data.split(",")[0],
        u"species": data.split(",")[3],
        u"year": int(data.split(",")[5]),
        u"yield": data.split(",")[2]
    })
    # load and wait 1 second until new load
    if count == 499:
        batch.commit()
        count = 1
        time.sleep(1)
    else:
        count = count + 1

batch.commit()
