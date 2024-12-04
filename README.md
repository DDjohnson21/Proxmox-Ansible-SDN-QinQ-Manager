# proxmox_compatibility_to_Ansible

# Create Command 
- Command to create a one VM with SDN QINQ Zone and VNET(with subnets): ansible-playbook -i inventory qinq_isoNet.yml

# Delete Command
- Command to Delete all VM/s: ansible-playbook -i inventory delete_all_vms.yml
- Command to pick what VM/s to Delete: ansible-playbook delete_sel_vm.yml -e 'vmids_to_delete="[VM_ID, VM_ID]"'



# Copy Command - Make sure to already make VM a template:
- Command to selected what VM/s to copy: ansible-playbook -i inventory copy_vm.yml --extra-vars "source_vm_id=VM_ID"


# *Todo* to work  
* need to add an inventory file
* add .env for python scrips - Example provided 
* add vars.yml for yml scrips - Example provided 

# Notes: 

# Installation

## Install Ansible(if not done already-MacOS):
Install: brew install ansible
Verify: ansible --version
Upgrade: brew upgrade ansible

## Install Packges needed:
need to Install Proxmoxer:
python -m pip install proxmoxer 
pip install python-dotenv
pip install requests

# Debugging
Create a Virtual Environment: python3 -m venv venv
Activate the Virtual Environment: source venv/bin/activate
To turn off Virtual Environment run: deactivate

## Plan 1 
- add shutdown before trying to Delete online vms   
- addd Delete qinq snd -- added 
- Fix Readme to add eveything I installed and general overivew 

- added new repon 

 
