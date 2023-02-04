from flask import Flask,redirect,url_for, request, render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from google.cloud import firestore
import statistics

import json

# creazione dell'istanza db google
db = firestore.Client.from_service_account_json('client.json')

# classe utente
class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {}

# inizializzazione dell'applicazione FLASK
app = Flask(__name__)

# inserimento della chiave segreta per l'autenticazione
app.config['SECRET_KEY'] = "secret_key_SuperComplex$$$$$"

# inizializzazione di flask login
login = LoginManager(app)
# dichiarazione del percorso della pagina di login
login.login_view = '/static/login.html'

# utenti che hanno accesso alla pagina
usersdb = {
    # ----- qua è possibile aggiungere utenti per l'app
    'marco': 'marco',
    'matteo': 'matteo',
    'luca': 'luca'
}

# caricatore di utenti
@login.user_loader
def load_user(username):
    # se l'utente è nel dizionario userdb allora l'utente esiste
    if username in usersdb:
        return User(username)
    return None

# pagina inziale
@app.route('/')
def root():
    return redirect('/static/login.html')

# pagina di visualizzazione dei dati
@app.route('/data')
@login_required
def index():
    return redirect('/static/data.html')

# api per il login
@app.route('/login', methods=['POST'])
def login():
    # se l'utente è già autenticato allora indirizzalo alla pagina dei dati
    if current_user.is_authenticated:
        return redirect('data')
    # recupera username e password dalla richiesta api
    username = request.values['u']
    password = request.values['p']
    # se l'utente è in userdb e la password è corretta
    if username in usersdb and password == usersdb[username]:
        # fai il login dell'utente con Flask Login
        login_user(User(username))
        # se nella richiesta è specificata una pagina successiva in cui indirizzare l'utente
        next_page = request.values['next']
        # altrimenti
        if not next_page:
            next_page = 'data'
        return redirect(next_page)
    # se l'utente o la password non sono corretti allora rimanda alla pagina di login
    return redirect('/')

# logout utente e indirizzamento a pagina iniziale
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# api per restituire al frontend i dati di google
@app.route('/getpoint', methods=['GET'])
def get_points():

    # se l'utente non è autenticato all'ora l'api non restituisce i dati
    if current_user.is_authenticated == False:
        return json.dumps("Year must be authenticated")

    # se l'anno non è specificato allora richiedere di inserirlo
    if request.args.get('year') == "":
        return json.dumps("One year must be selected")

    # recupera l'anno
    year = int(request.args.get('year'))

    # se la specie non è compilata
    if request.args.get('specie') == "":
       
        # inserisci il limite sul numero di risultati
        if request.args.get('limit') == "":
            limit = 1000
        else:
            limit = int(request.args.get('limit'))

        # chiedi i dati di tutte le specie di quell'anno
        google_data = db.collection('kellogg_biological_process').where('year', '==', year).limit(limit)
        

    else:
        # ottieni la specie

        specie = request.args.get('specie')

        # aggiungi il limite di default se non è specificato
        if request.args.get('limit') == "":
            limit = 1000
        else:
            limit = int(request.args.get('limit'))

        # ottieni i dati
        google_data = db.collection('kellogg_biological_process').where('year', '==', year).where('species', "==", specie).limit(limit)


    data = []
    # controlla se ci sono dati
    if sum(1 for _ in google_data.stream()) == 0:
        return json.dumps("No data for input")

    # se ci sono dati
    for doc in google_data.stream():    
        res = doc.to_dict()
        data.append(res)

    # rispondi con i dati
    return json.dumps(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)