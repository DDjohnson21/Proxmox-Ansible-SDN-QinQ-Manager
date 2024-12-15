# proxmox_compatibility_to_Ansible

# USE CASE:

This project leverages Ansible to automate the creation and management of Proxmox VMs within a QINQ zone and VNET. Key functionalities include:

- Creating Proxmox VMs with QINQ zones and VNETs, ensuring that a QINQ zone is created if it does not already exist.

- Automatically attaching new VMs to a new VNET within the QINQ zone and applying the necessary changes dynamically.

- Deleting specific VMs, all VMs, or all QINQ zones and VNETs as required.

- Naming VMs sequentially, starting from 100, for streamlined organization.

- Easy set up of custom VM outline templates for QINQ zone and VNET. Select the desired VM outline in by replacing "vm_outline.yml" file in qinq_isoNet.yml to a new custom VM outline.

This automation simplifies the setup and management of Proxmox VMs and networking configurations, ensuring efficiency and consistency across deployments.

# Academic Use Case:

This project is particularly useful for professors and educators who need to provide students with the same isolated virtual environments for learning and experimentation.

- Professors can create multiple VMs, each isolated within its own QINQ zone and VNET, ensuring a secure and independent environment for every student.

- Using VM outline templates, professors can replicate the same infrastructure setup for all students while maintaining isolation. These outline templates can include custom configurations tailored to the course requirements.

- The VM specifications are defined in vm_outline.yml, and professors can easily select the desired VM outline in by replacing "vm_outline.yml" in qinq_isoNet.yml to a diffent custom environments for their classes.

- This setup allows for rapid development of consistent environments, reducing time spent on manual configuration and enabling.

# Create Command

- Command to create a one VM with SDN QINQ Zone and VNET(with subnets): ansible-playbook -i inventory qinq_isoNet.yml

```
ansible-playbook -i inventory qinq_isoNet.yml
```

# Delete Command

- Command to Delete all VM/s and QINQ Config:

```
ansible-playbook -i inventory delete_qinqsdn.yml
```

- Command to Delete all VM/s:

```
ansible-playbook -i inventory delete_all_vms.yml
```

- Command to pick what VMs you want to Delete (VM_ID = ID of VM to delete):

```
ansible-playbook delete_sel_vm.yml -e 'vmids_to_delete="[VM_ID, VM_ID]"'
```

# Copy VM Command

NOTE: Make sure to already make VM a template before attempting to copy VM

- Command to selected what VM to copy (VM_ID = ID of VM to delete):

```
ansible-playbook -i inventory copy_vm.yml --extra-vars "source_vm_id=VM_ID"
```

# Installation:

Install Ansible if not done already (I am using MacOS so I am installing ansible using brew. Use the package manger of your choice):

Install: brew install ansible

```
brew install ansible
```

Verify: brew install ansible

```
brew install ansible
```

Upgrade(optional):

```
brew upgrade ansible
```

### Install Packges needed:

Need to Install Proxmoxer:

```
python -m pip install proxmoxer
```

Need to Install python-dotenv:

```
pip install python-dotenv
```

Need to Install requests:

```
pip install requests
```

### Add variable files .env and vars.yml:

create a file Called -->**.env** <-- and paste the template and fill in your information. The .env file will hold varables for python Scripts

**.env template:**

```
# ========================
# Proxmox Server Details
# ========================
PROXMOX_HOST=
PORT=443
VERIFY_SSL=False  # Set to True if SSL certificates should be verified

# ========================
# Proxmox API Credentials
# ========================
API_USER=root@pam
API_PASSWORD=
API_HOST=

# ========================
# Proxmox API URLs
# ========================
BASE_URL=${PROXMOX_HOST}:${PORT}/api2/json
SDN_APPLY_URL=${BASE_URL}/cluster/sdn

# ========================
# VM Configuration
# ========================
VM_NAME=testvm #
VM_MEMORY=1024  # Memory allocation in MB
VM_CORES=1      # Number of CPU cores
VM_SOCKETS=1    # Number of CPU sockets
VM_CPU_TYPE=host
VM_DISK_SIZE=32 # Disk size in GB
VM_OS_TYPE=l26  # Linux OS type
VM_ISO_PATH= # path to ISO

# ========================
# SDN Configuration
# ========================
SDN_ZONE_NAME=qinqzone        # SDN zone name
SDN_TYPE=qinq                # SDN zone type
SDN_MTU=1496                 # Maximum Transmission Unit (MTU)
SDN_BRIDGE=vmbr0             # Network bridge to use
SDN_TAG=100                  # VLAN tag for QinQ zone
SDN_VLAN_PROTOCOL=802.1ad    # VLAN protocol for QinQ zone

# ========================
# Token Details
# ========================
TOKEN_ID=
SECRET=

```

create a file Called -->**vars.yml** <-- and paste the template and fill in your information. The vars.yml file will hold varables for yml Scripts.

**vars.yml template**

```
### VM and Proxmox API Configuration
vm_name: "testvm"
api_host: ""
api_user: "root@pam"
api_password: ""
api_port: 443
node: ""

### SDN Zone Parameters
sdn_zone_params:
  zone: "qinqzone"
  type: "qinq"
  mtu: 1496
  bridge: "vmbr0"
  tag: 100
  vlan_protocol: "802.1ad"

### Proxmox Server Details
proxmox_host: ""
port: 443
verify_ssl: false

### API Token Details
token_id: ""
secret: ""

### API Endpoint URL
base_url: "{{ proxmox_host }}:{{ port }}/api2/json"
sdn_apply_url: "{{ base_url }}/cluster/sdn"

```

# <span style="color:red"> Important note: </span>

Python Scripts are running with <span style="color:red">**python3(Common for MacOS)**.</span> You may need to change the command to run with your system perfered python. Python Scripts are run in qinq_isoNet.yml, delete_qinqsdn.yml, copy_vm.yml files.

Occurrences in **qinq_isoNet.yml** :

```
LINE #14: command: "python3 {{ playbook_dir }}/fetch_next_vmid.py"
LINE #77: command: "python3 {{ playbook_dir }}/apply_sdn_changes.py"
```

Occurrences in **delete_qinqsdn.yml** :

```
LINE #90: command: "python3 {{ playbook_dir }}/apply_sdn_changes.py"
```

Occurrences in **copy_vm.yml** :

```
LINE #19: command: "python3 {{ playbook_dir }}/fetch_next_vmid.py"
```

# Debugging(if running into issues on MacOS)

To run this program and manage dependencies, it is recommended to create a virtual environment. This ensures that package installations do not interfere with your global environment, particularly if you are using Homebrew.

Important Note: Direct usage of pip commands without a virtual environment may cause conflicts with your Homebrew setup. Homebrew is designed to safeguard its environment, which could lead to errors when running commands if packages like Proxmoxer, python-dotenv, or requests—installed via pip—are not found.

Follow these steps to set up a virtual environment and avoid these issues:

Create a Virtual Environment:

```
python3 -m venv venv
```

Activate the Virtual Environment:

```
source venv/bin/activate
```

To turn off Virtual Environment run: deactivate

```
deactivate
```
