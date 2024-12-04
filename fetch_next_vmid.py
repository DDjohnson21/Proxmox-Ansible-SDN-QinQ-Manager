from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch credentials and configurations from .env
proxmox_host = os.getenv("API_HOST")
proxmox_user = os.getenv("API_USER")
proxmox_password = os.getenv("API_PASSWORD")
proxmox_port = int(os.getenv("API_PORT", 443))  # Default to port 443 if not specified
verify_ssl = os.getenv("VERIFY_SSL", "False").lower() == "true"  # Convert to boolean

try:
    # Connect to Proxmox API
    proxmox = ProxmoxAPI(
        host=proxmox_host,
        user=proxmox_user,
        password=proxmox_password,
        verify_ssl=verify_ssl,
        port=proxmox_port,
    )
    # Fetch the next available VM ID
    vmid = proxmox.cluster.nextid.get()
    print(vmid)

except Exception as e:
    print(f"Error: {e}")