from firebase import firebase 
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("green-planet-team-firebase-adminsdk-a4hhi-52e15807ab.json")
firebase_admin.initialize_app(cred)
store = firestore.client()  
 
def update_status(id): 
    # xxx = firebase.FirebaseApplication('https://green-planet-team.firebaseio.com', None)
    # result = xxx.put('/green-planet-team/booking/' + id, 'status', '2')
    # print(result)

    doc_ref = store.collection(u'booking').document(u'' + id)
    doc_ref.update({u'status': '2'})

    return True