import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyCHvuRhRcCzGQ_PPMQUGpDZ9PIxgAlX4x8",
    'authDomain': "expensetrackerpy-cbe98.firebaseapp.com",
    'projectId': "expensetrackerpy-cbe98",
    'storageBucket': "expensetrackerpy-cbe98.appspot.com",
    'messagingSenderId': "797554454730",
    'appId': "1:797554454730:web:47c56bfc3aa9b71b354433",
    'measurementId': "G-7N77XNB7RR",
    'databaseURL': "https://expensetrackerpy-cbe98-default-rtdb.firebaseio.com"
    # 'databaseURL': "https://expensetrackerpy-cbe98.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
