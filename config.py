import pyrebase
config={
     "apiKey": "AIzaSyApH3WQJd3-IUlD4hqWa1GiMT_sT8UOZrE",
    "authDomain": "appi-ecf0e.firebaseapp.com",
    "databaseURL": "https://appi-ecf0e.firebaseio.com",
    "projectId": "appi-ecf0e",
    "storageBucket": "appi-ecf0e.appspot.com",
    "messagingSenderId": "168592718623",
    "appId": "1:168592718623:web:c82100b13c16a1f0e44e2a",
    "measurementId": "G-L9LJK2XBFC"
        }
#Iniciando los servicios de FB
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()
st=firebase.storage()