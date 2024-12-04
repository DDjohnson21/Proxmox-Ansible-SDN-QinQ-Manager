import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Proxmox server details
PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PORT = os.getenv("PORT")
VERIFY_SSL = os.getenv("VERIFY_SSL") == "True"

# API Token Details
TOKEN_ID = os.getenv("TOKEN_ID")
SECRET = os.getenv("SECRET")

# API Endpoint URL
BASE_URL = f"{PROXMOX_HOST}:{PORT}/api2/json"
SDN_APPLY_URL = f"{BASE_URL}/cluster/sdn"

# Headers for API Token Authentication
headers = {
    "Authorization": f"PVEAPIToken={TOKEN_ID}={SECRET}"
}

def apply_sdn_changes():
    try:
        # Make the PUT request to apply SDN changes
        response = requests.put(SDN_APPLY_URL, headers=headers, verify=VERIFY_SSL)

        # Check if the request was successful
        if response.status_code == 200:
            print("SDN changes applied successfully.")
        else:
            print(f"Failed to apply SDN changes: {response.status_code}")
            print(response.text)

    except Exception as e:
        print("An error occurred:", str(e))

apply_sdn_changes()
