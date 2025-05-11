import json
import requests

def get_home_page():
    url = "http://localhost:8000/"

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

def create_user():
    url = "http://localhost:8000/user/create/"

    payload = json.dumps({
                    "room_id": "string",
                    "patient_details": {},
                    "patient_name": "string",
                    "gender": "string",
                    "dob": "string",
                    "visit_reason": "string",
                    "environment": "dev"
                    })
    headers = {
            'Content-Type': 'application/json',
            'auth_token': 'auth_key'
            }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

def update_user(patient_id: str):
    url = "http://localhost:8000/user/update/"

    payload = json.dumps({
            "patient_id": patient_id,
            "patient_details": {}
            })
    headers = {
            'Content-Type': 'application/json',
            'auth_token': 'auth_key'
            }

    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response.text

def view_all_users():
    url = "http://localhost:8000/user/view_all/"

    payload = {}
    headers = {
    'auth_token': 'auth_key'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

def delete_user(patient_id: str):


    url = "http://localhost:8000/user/delete/"

    payload = json.dumps({
            "patient_id": patient_id
            })
    headers = {
        'Content-Type': 'application/json',
        'auth_token': 'auth_key'
        }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    return response.text

# home page display (HTML)
print(get_home_page())

# user creation
creation_response = create_user()
print(creation_response)
patient_id = creation_response[25:]

# user update
print(update_user(patient_id))

# view all users
print(view_all_users())

# delete user
print(delete_user(patient_id))