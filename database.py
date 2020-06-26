from firebase import firebase
 
def update_status(id): 
    firebase = firebase.FirebaseApplication('https://green-planet-team.firebaseio.com', None)
    result = firebase.put('/green-planet-team/booking/' + id, 'status', '2')
    print(result)
    return result