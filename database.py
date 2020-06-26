from firebase import firebase
 
firebase = firebase.FirebaseApplication('https://green-planet-team.firebaseio.com', None)
data =  { 'Name': 'John Doe',
          'RollNo': 3,
          'Percentage': 70.02
          }
result = firebase.post('/green-planet-team/Students/',data)
print(result)