from firebase import firebase
 
def update_status(id): 
    firebase = firebase.FirebaseApplication('https://green-planet-team.firebaseio.com', None)
    data =  { 'id': 'xxx'}
    result = firebase.put('/green-planet-team/booking/3ckOjcgHN2Mrpm3VzI3z',data)
    print(result)