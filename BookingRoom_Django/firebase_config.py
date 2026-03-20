import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('BookingRoom_Django/firebase-creds.json')
firebase_admin.initialize_app(cred)
