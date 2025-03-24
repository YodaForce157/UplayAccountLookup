import json
import re

import api

def main():
    mode = None
    modes = ["1", "2"]
    while mode not in modes:
        print("*********UBI TOOLS*********")
        print("Features:")
        print("[1] Account Lookup")
        print("[2] Inventory Lookup")
        print("***************************")

        mode = input("What tool would you like to use? ")

    email = None
    password = None

    valid = None

    while not valid:
        email = input("Email: ")
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

    while not password:
        password = input("Password: ")

    authRes = api.SessionRequest(email=email, password=password).send()
    ticket = authRes["ticket"]
    sessionId = authRes["sessionId"]
    userId = authRes["userId"]

    if not ticket:
        print("Error getting ticket!")

    if not sessionId:
        print("Error getting session id!")

    if mode == "1":
        userMode = None
        playerId = None

        while userMode not in ["1", "2"]:
            userMode = input("[1] Username\n[2] UUID: ")

        if userMode == "1":
            username = input("Username: ")
            playerId = json.loads(api.NameToUUIDRequest(ticket, username).send())["profiles"][0]["userId"]

            if not playerId:
                print("Error getting player id!")

        while not playerId:
            playerId = input("Player ID: ")

        res = api.AccountLookupRequest(playerId, ticket).send()
        if not res:
            print("Error getting player!")

        jRes = json.loads(res)

        if "errorCode" in jRes:
            print("Error getting player!")

        for profile in jRes["profiles"]:
            print(profile["platformType"])
            print("Platform ID: " + profile["idOnPlatform"])
            print("Platform Name: " + profile["nameOnPlatform"])

    if mode == "2":
        r = api.InventoryRequest(sessionId, userId, ticket).send()
        print(r)

    input("Press enter to exit...")

if __name__ == "__main__":
    main()