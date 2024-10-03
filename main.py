from fastapi import FastAPI, UploadFile
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, db
from fastapi.middleware.cors import CORSMiddleware
import json
from dotenv import load_dotenv

import os
import json
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://hackathon-project-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


bucket_name = "invoices-from-user"
service_account_info = os.getenv('SERVICE_ACCOUNT_JSON')
if not service_account_info:
    raise ValueError("SERVICE_ACCOUNT_JSON environment variable is not set")

# Parse the JSON string
try:
    service_account_info = json.loads(service_account_info)
except json.JSONDecodeError as e:
    print(f"Error decoding SERVICE_ACCOUNT_JSON: {e}")
    print(f"SERVICE_ACCOUNT_JSON value: {service_account_info[:100]}...")  # Print first 100 chars
    raise

credentials = service_account.Credentials.from_service_account_info(service_account_info)
# Initialize storage client
storage_client = storage.Client(credentials=credentials)
bucket = storage_client.get_bucket(bucket_name)
# initialise firebase
firebase_config_json = os.getenv('FIREBASE_JSON')
firebase_config = json.loads(firebase_config_json)

# Initialize Firebase app with config that includes the databaseURL
firebase_admin.initialize_app(options=firebase_config)



@app.get("/test/gemini-analysis")
async def get_gemini_output():
    return json.load(open("gemini-dummy.json", "r"))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/file")
async def get_file():
    blobs = bucket.list_blobs()
    return [blob.name for blob in blobs]


@app.post("/api/upload-file")
async def upload_file(file: UploadFile):
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file.file)
    # and updates in the firestore also
    return {"message": "File uploaded successfully"}


@app.post("/api/create-user/{user_name}")
async def add_user(user_name: str):
    # store the user in the user collection
    return True


# TODO : change products to invoices
"""

CHange the schema of what we store in invoices this way:

    {
        "invoices": ...everything in the product, file_name
    }

{ 
 users: ["harsha": {invoices: [..., file_name]}, "hemanth": {invoices: [.... filename]}]

 users: [..., user: {files: [file_name1, file_name2], invoices:
                     [invoice_output_from_gemini, filename]}]

"""


def exists_in_firebase(file_name):
    ref = db.reference("/products")  # should be invoices
    products = ref.get()
    if not products:
        return False
    products = products.strip("```json")
    products = products.strip("```")
    products = json.loads(products)

    if products:
        for product in products:
            # should be file_name
            if product["product_name"] == file_name:
                return product
    return False


# TODO: Change from products to invoices
@app.get("/api/process/{file_name}")
async def process_file(file_name: str):
    # This is where we check in firebase if the file is processed
    # if file is processed, we retrun the response stored in firebase.

    product_in_firebase = exists_in_firebase(file_name)
    if product_in_firebase:
        return product_in_firebase

    file = bucket.get_blob("test.txt")
    return "...generating from gemini"

    # extract from gemini
    # get the file from the bucket with the file_name using google cloud
    # send the file contents to gemini prompt
    # get the response and store it in firebase .set() !! WITHOUT OVERRIDING
    # THE EXISING
    # send the response as the output of gemini

    # store in firebase invoices

    ## Then we call the gemini api
    ## step 1:  WE get an output from gemini, store it in firebase
    ## step 2: We return the output to the client
