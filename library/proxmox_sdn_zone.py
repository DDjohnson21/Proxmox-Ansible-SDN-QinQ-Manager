#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Gabriel Morin
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: proxmox_sdn_zone
short_description: Management of SDN zones in a Proxmox VE cluster
version_added: "1.0.0"
description:
  - Allows you to create, update, and delete SDN zone configurations in a Proxmox VE cluster.
author: "Gabriel Morin (@Analepse129)"
options:
  state:
    description:
      - Define whether the zone should exist or not.
    choices: ['present', 'absent']
    type: str
    default: 'present'
  zone:
    description:
      - The unique ID of the SDN zone.
    required: true
    type: str
  type:
    description:
      - The type of the zone.
    choices: ['evpn', 'faucet', 'qinq', 'simple', 'vlan', 'vxlan']
    required: true
    type: str
  advertise_subnets:
    description:
      - Advertise EVPN subnets if you have silent hosts.
    required: false
    type: bool
  bridge:
    description:
      - Name of the bridge the zone is connected to.
    required: false
    type: str
  bridge_disable_mac_learning:
    description:
      - Disable auto MAC learning.
    required: false
    type: bool
  controller:
    description:
      - FRR router name.
    required: false
    type: str
  dhcp:
    description:
      - Type of the DHCP backend for this zone.
    required: false
    type: str
  disable_arp_nd_suppression:
    description:
      - Disable IPv4 ARP & IPv6 neighbor discovery suppression.
    required: false
    type: bool
  dns:
    description:
      - DNS API server.
    required: false
    type: str
  dnszone:
    description:
      - DNS domain zone, e.g., mydomain.com.
    required: false
    type: str
  dp_id:
    description: 
      - Faucet dataplane ID.
    required: false
    type: int
  exitnodes:
    description:
      - List of cluster node names.
    required: false
    type: str
  exitnodes_local_routing:
    description:
      - Allow exit nodes to connect to EVPN guests.
    required: false
    type: bool
  exitnodes_primary:
    description:
      - Force traffic to this exit node first.
    required: false
    type: str
  ipam:
    description:
      - Use a specific IPAM.
    required: false
    type: str
  mac:
    description:
      - Anycast logical router MAC address.
    required: false
    type: str
  mtu:
    description:
      - MTU.
    required: false
    type: int
  nodes:
    description:
      - List of cluster node names.
    required: false
    type: str
  peers:
    description:
      - Peers address list.
    required: false
    type: str
  reversedns:
    description:
      - Reverse DNS API server.
    required: false
    type: str
  rt_import:
    description:
      - Route-Target import.
    required: false
    type: str
  tag:
    description:
      - Service VLAN tag.
    required: false
    type: int
  vlan_protocol:
    description:
      - Protocol used for VLAN tagging. Can be either 802.1q or 802.1ad. Defaults to 802.1q.
    required: false
    type: str
  vrf_vxlan:
    description:
      - L3 VNI.
    required: false
    type: int
  vxlan_port:
    description:
      - VXLAN tunnel UDP port (default 4789).
    required: false
    type: int
requirements:
  - proxmoxer
  - requests
'''

EXAMPLES = r'''
- name: Create a QinQ zone
  proxmox_sdn_zone:
    state: present
    zone: "qinqzone"
    type: "qinq"
    bridge: "vmbr0"
    tag: 100
    vlan_protocol: "802.1q"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.general.plugins.module_utils.proxmox import (
    proxmox_auth_argument_spec, ProxmoxAnsible
)

class ProxmoxSdnZones(ProxmoxAnsible):
    
    def is_sdn_zone_empty(self, zone_id):
        """Check whether zone has vnets"""
        data = self.proxmox_api.cluster.sdn.vnets.get()
        for vnet in data:
            if vnet['zone'] == zone_id:
                return False
        return True
    
    def is_sdn_zone_existing(self, zone_id):
        """Check whether zone already exists"""
        try:
            zones = self.proxmox_api.cluster.sdn.zones.get()
            for zone in zones:
                if zone['zone'] == zone_id:
                    return True
            return False
        except Exception as e:
            self.module.fail_json(msg="Unable to retrieve zones: {0}".format(e))
    
    def create_update_sdn_zone(self, zone_id, zone_infos):
        """Create or update Proxmox VE SDN zone"""
        if self.is_sdn_zone_existing(zone_id):
            self.module.exit_json(changed=False, zone=zone_id, msg="Zone {0} already exists".format(zone_id))

        if self.module.check_mode:
            return

        try:
            self.proxmox_api.cluster.sdn.zones.post(**zone_infos)
        except Exception as e:
            self.module.fail_json(msg="Failed to create zone with ID {0}: {1}".format(zone_id, e))
      
    def delete_sdn_zone(self, zone_id):
        """Delete Proxmox VE zone"""
        if not self.is_sdn_zone_existing(zone_id):
            self.module.exit_json(changed=False, zone=zone_id, msg="Zone {0} doesn't exist".format(zone_id))

        if self.is_sdn_zone_empty(zone_id):
            if self.module.check_mode:
                return

            try:
                self.proxmox_api.cluster.sdn.zones(zone_id).delete()
            except Exception as e:
                self.module.fail_json(msg="Failed to delete zone with ID {0}: {1}".format(zone_id, e))
        else:
            self.module.fail_json(msg="Can't delete zone {0} with vnets. Please remove vnets from zone first.".format(zone_id))


def main():
    module_args = proxmox_auth_argument_spec()
    sdn_zone_args = {
        # Ansible
        'state': {'type': 'str', 'choices': ['present', 'absent'], 'default': 'present'},
        # Mandatory
        'zone': {'type': 'str', 'required': True},
        'type': {'type': 'str', 'choices': ['evpn', 'faucet', 'qinq', 'simple', 'vlan', 'vxlan'], 'required': True},
        # Optional
        'advertise_subnets': {'type': 'bool', 'required': False},
        'bridge': {'type': 'str', 'required': False},
        'bridge_disable_mac_learning': {'type': 'bool', 'required': False},
        'controller': {'type': 'str', 'required': False},
        'dhcp': {'type': 'str', 'required': False},
        'digest': {'type': 'str', 'required': False},
        'disable_arp_nd_suppression': {'type': 'bool', 'required': False},
        'dns': {'type': 'str', 'required': False},
        'dnszone': {'type': 'str', 'required': False},
        'dp_id': {'type': 'int', 'required': False},
        'exitnodes': {'type': 'str', 'required': False},
        'exitnodes_local_routing': {'type': 'bool', 'required': False},
        'exitnodes_primary': {'type': 'str', 'required': False},
        'ipam': {'type': 'str', 'required': False},
        'mac': {'type': 'str', 'required': False},
        'mtu': {'type': 'int', 'required': False},
        'nodes': {'type': 'str', 'required': False},
        'peers': {'type': 'str', 'required': False},
        'reversedns': {'type': 'str', 'required': False},
        'rt_import': {'type': 'str', 'required': False},
        'tag': {'type': 'int', 'required': False},
        'vlan_protocol': {'type': 'str', 'choices': ['802.1q', '802.1ad'], 'default': '802.1q'},
        'vrf_vxlan': {'type': 'int', 'required': False},
        'vxlan_port': {'type': 'int', 'required': False},
    }

    module_args.update(sdn_zone_args)

    module = AnsibleModule(
        argument_spec=module_args,
        required_together=[("api_token_id", "api_token_secret")],
        required_one_of=[("api_password", "api_token_id")],
        supports_check_mode=True
    )

    # Ansible parameters
    state = module.params['state']
    # Required parameters
    zone_id = module.params['zone']
    zone_type_param = module.params['type']  # Avoid using 'type' as variable name
    # Optional parameters
    advertise_subnets = module.params.get('advertise_subnets')
    bridge = module.params.get('bridge')
    bridge_disable_mac_learning = module.params.get('bridge_disable_mac_learning')
    controller = module.params.get('controller')
    dhcp = module.params.get('dhcp')
    digest = module.params.get('digest')
    disable_arp_nd_suppression = module.params.get('disable_arp_nd_suppression')
    dns = module.params.get('dns')
    dnszone = module.params.get('dnszone')
    dp_id = module.params.get('dp_id')
    exitnodes = module.params.get('exitnodes')
    exitnodes_local_routing = module.params.get('exitnodes_local_routing')
    exitnodes_primary = module.params.get('exitnodes_primary')
    ipam = module.params.get('ipam')
    mac = module.params.get('mac')
    mtu = module.params.get('mtu')
    nodes = module.params.get('nodes')
    peers = module.params.get('peers')
    reversedns = module.params.get('reversedns')
    rt_import = module.params.get('rt_import')
    tag = module.params.get('tag')
    vlan_protocol = module.params.get('vlan_protocol')
    vrf_vxlan = module.params.get('vrf_vxlan')
    vxlan_port = module.params.get('vxlan_port')

    # Build the zone_infos dictionary to send to the API
    zone_infos = {
        'zone': zone_id,
        'type': zone_type_param,
        'advertise-subnets': int(advertise_subnets) if advertise_subnets is not None else None,
        'bridge': bridge,
        'bridge-disable-mac-learning': int(bridge_disable_mac_learning) if bridge_disable_mac_learning is not None else None,
        'controller': controller,
        'dhcp': dhcp,
        'digest': digest,
        'disable-arp-nd-suppression': int(disable_arp_nd_suppression) if disable_arp_nd_suppression is not None else None,
        'dns': dns,
        'dnszone': dnszone,
        'dp-id': dp_id,
        'exitnodes': exitnodes,
        'exitnodes-primary': exitnodes_primary,
        'exitnodes-local-routing': int(exitnodes_local_routing) if exitnodes_local_routing is not None else None,
        'ipam': ipam,
        'mac': mac,
        'mtu': mtu,
        'nodes': nodes,
        'peers': peers,
        'reversedns': reversedns,
        'rt-import': rt_import,
        'tag': tag,
        'vlan-protocol': vlan_protocol,
        'vrf-vxlan': vrf_vxlan,
        'vxlan-port': vxlan_port,
    }

    # Remove None values from zone_infos
    zone_infos = {k: v for k, v in zone_infos.items() if v is not None}

    proxmox = ProxmoxSdnZones(module)

    if state == 'present':
        # API call to create/update a zone
        proxmox.create_update_sdn_zone(zone_id, zone_infos)
        module.exit_json(changed=True, message='Creating/updating zone ID: {}'.format(zone_id))
    elif state == 'absent':
        # API call to delete a zone
        proxmox.delete_sdn_zone(zone_id)
        module.exit_json(changed=True, message='Deleting zone ID: {}'.format(zone_id))
    else:
        module.fail_json(msg="Invalid state: {0}".format(state))

if __name__ == '__main__':
    main()
