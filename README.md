# proxmox_compatibility_to_Ansible

# USE CASE:
This project leverages Ansible to automate the creation and management of Proxmox VMs within a QINQ zone and VNET. Key functionalities include:
- Creating Proxmox VMs with QINQ zones and VNETs, ensuring that a QINQ zone is created if it does not already exist.

- Automatically attaching new VMs to a new VNET within the QINQ zone and applying the necessary changes dynamically.

- Deleting specific VMs, all VMs, or all QINQ zones and VNETs as required.

- Naming VMs sequentially, starting from 100, for streamlined organization.

This automation simplifies the setup and management of Proxmox VMs and networking configurations, ensuring efficiency and consistency across deployments.


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



# Copy VM Command (Make sure to already make VM a template before attempting to copy VM):
- Command to selected what VM to copy (VM_ID = ID of VM to delete): 
```
ansible-playbook -i inventory copy_vm.yml --extra-vars "source_vm_id=VM_ID"
```


# Notes: 



# Installation:

## Install Ansible if not done already(I am using MacOS so I am installing ansible usig brew. Use the package manger of your choice):
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
If not made need to have an inventory file. 

## Install Packges needed:
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




#  <span style="color:red"> Important note: </span>
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


 
