#!/usr/bin/env python3

import json
from datetime import datetime
import uuid


dateNow = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
locationType = ['PORT', 'QUAY', 'BERTH']

# UUID generator for every location
def randomUUID():
    UUID = str(uuid.uuid4())
    return UUID


# Get details for each location
def get_port_details():
    global portName, portCode, quayNo
    portName = input("Enter port name: ").title()
    portCode = input("Enter the UNLOCODE: ").replace(" ", "").upper()
    quayNo = int(input("How many quays does the port have? "))
    portUUID = randomUUID()
    return portName, portCode, quayNo, portUUID


def get_quay_details(quayNo):
    quayName = input("What is quay {} called? ".format(quayNo + 1)).title()
    berthNo = int(input("How many berths does {} have? ".format(quayName)))
    quayUUID = randomUUID()
    return quayName, berthNo, quayUUID


def get_berth_details(berthNo):
    berthName = input(
        "What is the name of berth {}? ".format(berthNo + 1)).title()
    berthUUID = randomUUID()
    return berthName, berthUUID


def generate_quayPath(portName, quayName):
    locationPath = "{}/{}".format(portName, quayName)
    return locationPath


def generate_berthPath(portName, quayName, berthName):
    locationPath = "{}/{}/{}".format(portName, quayName, berthName)
    return locationPath

#Create location dicts
def create_port_location(portName, portCode, portUUID, dateNow):
    portLocation = []
    mapPortLocation = {'__typename': {'S': 'Location'}, 'number': {'N': 0}, 'dockable': {'BOOL': False},
                       'allocatable': {'BOOL': False}, '_lastChangedAt': {'N': '1500000000000'},
                       'createdAt': {'S': dateNow}, 'updatedAt': {'S': dateNow},
                       '_version': {'N': '1'}, 'name': {'S': portName}, 'type': {'S': locationType[0]},
                       'path': {'S': portName}, 'portUnlocode': {'S': portCode},
                       'portCode': {'S': portCode}, 'id': {'S': portUUID}
                       }
    portLocation.append(mapPortLocation)
    return portLocation


def create_quay_location(quayName, quayUUID, portName, portCode, portUUID, dateNow, quayLocation):
    locationPath = generate_quayPath(portName, quayName)
    mapQuayLocation = {'__typename': {'S': 'Location'}, 'number': {'N': 0}, 'dockable': {'BOOL': False},
                       'allocatable': {'BOOL': True}, '_lastChangedAt': {'N': '1500000000000'},
                       'createdAt': {'S': dateNow}, 'updatedAt': {'S': dateNow},
                       '_version': {'N': '1'}, 'name': {'S': quayName}, 'type': {'S': locationType[1]},
                       'path': {'S': locationPath}, 'portUnlocode': {'S': portCode},
                       'portCode': {'S': portCode}, 'id': {'S': quayUUID},
                       'parentName': {'S': portName}, 'locationParentId': {'S': portUUID}
                       }
    quayLocation.append(mapQuayLocation)
    return quayLocation


def create_berth_location(portName, portCode, quayName, quayUUID, berthName, berthUUID, dateNow, berthLocation):
    locationPath = generate_berthPath(portName, quayName, berthName)
    mapBerthLocation = {'__typename': {'S': 'Location'}, 'number': {'N': 0}, 'dockable': {'BOOL': True},
                        'allocatable': {'BOOL': True}, '_lastChangedAt': {'N': '1500000000000'},
                        'createdAt': {'S': dateNow}, 'updatedAt': {'S': dateNow},
                        '_version': {'N': '1'}, 'name': {'S': berthName}, 'type': {'S': locationType[2]},
                        'path': {'S': locationPath}, 'portUnlocode': {'S': portCode},
                        'portCode': {'S': portCode}, 'id': {'S': berthUUID},
                        'parentName': {'S': quayName}, 'locationParentId': {'S': quayUUID}
                        }
    berthLocation.append(mapBerthLocation)
    return berthLocation


#Combine dicts into list
def complete_location(portLocation, quayLocation, berthLocation):
    location = [*portLocation, *quayLocation, *berthLocation]
    return location


#Add unique number to each location
def add_number(location):
    n = 0
    while n < (len(location)):
        location[n]['number']['N'] = int(n)
        n = n + 1
    return location


def write_to_json(location):
    with open('Location.json', 'w') as json_file:
        json.dump(location, json_file)


def main():
    portName, portCode, quayNo, portUUID = get_port_details()
    portLocation = create_port_location(portName, portCode, portUUID, dateNow)
    quayLocation = []
    berthLocation = []
    for i in range(quayNo):
        quayName, berthNo, quayUUID = get_quay_details(i)
        quayLocation = create_quay_location(
            quayName, quayUUID, portName, portCode, portUUID, dateNow, quayLocation)
        for i in range(berthNo):
            berthName, berthUUID = get_berth_details(i)
            berthLocation = create_berth_location(
                portName, portCode, quayName, quayUUID, berthName, berthUUID, dateNow, berthLocation)
    location = complete_location(portLocation, quayLocation, berthLocation)
    location = add_number(location)
    write_to_json(location)


if __name__ == '__main__':
    main()
