# IMPORTS
import os
import json
import hashlib
import logging
import pendulum
from fastapi import Depends
from fastapi import FastAPI
from pydantic import BaseModel
from dependencies.auth import get_api_key
from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import TimedRotatingFileHandler
from fastapi.responses import HTMLResponse, JSONResponse

# FOLDERS INITIALIZATION
try:
    os.mkdir("logs")
except:
    pass 

try:
    os.mkdir("user_data")
except:
    pass 

# LOGGING CONFIGURATION
logging.getLogger("uvicorn.error").disabled = True

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a TimedRotatingFileHandler that rotates daily
log_filename = './logs/logfile.log'
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = TimedRotatingFileHandler(log_filename, when='H', interval=1, backupCount=24)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# generate patient ID
def generate_int_identifier(list: list) -> int:
    data = ''
    for l in list:
        data += str(l)
    return int(str(int(hashlib.sha1(data.encode("utf-8")).hexdigest(), 32))[:9])

# API INITIALIZATION
logger.info("API Initialized.")
environment = "dev"

tags_metadata = [   {
                        "name": "Home Page",
                        "description": "Home Page of Patient Checkin API."
                    },
                    {
                        "name": "Backend",
                        "description": "Retrieve user and related information."
                    }
                ]

app = FastAPI(title = "Patient Checkin API",
             version = environment,
             contact = {'name':'API Team',
                       'email':'support@api.team.com'},
             openapi_tags = tags_metadata,
             root_path = "")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

# HOME PAGE
@app.get("/", status_code = 200, tags= ["Home Page"], response_class = HTMLResponse)
async def home_page():
    html_content =  """
                        <h1>Patient Checkin API</h1> <br>
                        <p> Email: support@api.team.com </p>
                    """

    logger.info("Home page invoked.")
    return HTMLResponse(content=html_content, status_code=200)

class create(BaseModel):
    room_id: str
    patient_details: dict
    patient_name: str
    gender: str
    dob: str
    visit_reason: str
    environment: str = environment
@app.post("/user/create/", status_code = 200, tags= ["Backend"])
async def create_user(user: create, key = Depends(get_api_key)):
    
    insertion_ts = pendulum.now('UTC')
    patient_id = generate_int_identifier([insertion_ts, user.patient_name, user.gender, user.visit_reason])

    user_data = user.model_dump()
    user_data['insertion_ts'] = insertion_ts.to_iso8601_string()
    user_data['updated_at_ts'] = insertion_ts.to_iso8601_string()
    user_data['patient_id'] = patient_id

    json_file_path = "./user_data/%s.json" %patient_id
    with open(json_file_path, "w") as f:
        json.dump(user_data, f, indent=4)

    logger.info("Patient Created with ID: %s" %patient_id)
    return HTMLResponse(content = "Patient Created with ID: %s" %patient_id, status_code = 200)

class update(BaseModel):
    patient_id: str
    patient_details: dict
@app.patch("/user/update/", status_code = 200, tags= ["Backend"])
async def update_user(user: update, key = Depends(get_api_key)):

    try:
        json_file_path = "./user_data/%s.json" %user.patient_id
        with open(json_file_path, "r") as f:
            user_data = json.load(f)

        user_data['updated_at_ts'] = pendulum.now('UTC').to_iso8601_string()
        user_data['patient_details'] = user.patient_details

        with open(json_file_path, "w") as f:
            json.dump(user_data, f, indent=4)

        logger.info("Patient with ID: %s updated successfully" %user.patient_id)
        return HTMLResponse(content = "Patient with ID: %s updated successfully" %user.patient_id, status_code = 200)
    
    except Exception as E:
        logger.error("Patient with ID: %s does not exist. Error: %s" %(user.patient_id, str(E)))
        return HTMLResponse(content = "Patient with ID: %s does not exist. Error: %s" %(user.patient_id, str(E)), status_code = 406)
    
class delete(BaseModel):
    patient_id: str
@app.delete("/user/delete/", status_code = 200, tags= ["Backend"])
async def delete_user(user: delete, key = Depends(get_api_key)):

    try:
        os.remove("./user_data/%s.json" %user.patient_id)
        logger.info("Patient with ID: %s deleted successfully" %user.patient_id)
        return HTMLResponse(content = "Patient with ID: %s deleted successfully" %user.patient_id, status_code = 200)
    except Exception as E:
        logger.error("Patient with ID: %s does not exist, could not delete. Error: %s" %(user.patient_id, str(E)))
        return HTMLResponse(content = "Patient with ID: %s does not exist, could not delete. Error: %s" %(user.patient_id, str(E)), status_code = 406)

@app.get("/user/view_all/", status_code = 200, tags= ["Backend"])
async def view_users(key = Depends(get_api_key)):

    all_users = []
    folder_path = "./user_data"
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as f:
                    data = json.load(f)
                    all_users.append(data)

    return JSONResponse(content = all_users, status_code=200)