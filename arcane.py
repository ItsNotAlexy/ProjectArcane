import requests, colorama, os, time, psutil
from datetime import datetime, timedelta


def getOs():
    getOSType = os.name

    if getOSType == "nt":
        return "Windows"
    else:
        return "Linux"


def CheckDependencies():
    try:
        import requests, colorama, psutil
    except ImportError:
        print("Missing dependencies, installing...")
        osType = getOs()
        if osType == "Windows":
            os.system("python -m pip install -r requirements.txt")
        else:
            os.system("python3 -m pip install -r requirements.txt")
        print("Dependencies installed! Please restart the program.")
        exit()


def Clear():
    getOSType = os.name

    if getOSType == "nt":
        os.system("cls")
    else:
        os.system("clear")


def Start():
    colorama.init()
    Clear()
    print(" -- [ PROJECT ARCANE ] -- ")
    print("Author       : alexy.dev")
    print("OS Type      : " + getOs())
    print("CPU Usage    : " + str(psutil.cpu_percent()) + "%")
    print("RAM Usage    : " + str(psutil.virtual_memory()[2]) + "%")
    print("Version      : 1.0.0 ")
    print("-------------------------")

    inputId = input("Enter Roblox ID: ")

    try:
        int(inputId)
        print("Fetching data...")
        print("-------------------------")
        Clear()
        data = getAccount(int(inputId))
        groups = getGroups(int(inputId))
        check_alt = isAlt(int(inputId))
        getPrecense = getCurrentStatus(int(inputId))

        print(" -- [ USER FOUND ] --")
        print("Username: " + data["name"])
        print("ID: " + str(data["id"]))
        print("Is Banned: " + str(data["isBanned"]))
        print("Last Online: " + getPrecense["userPresences"][0]["lastOnline"])
        print(
            "Last Accessed Roblox on: "
            + getPrecense["userPresences"][0]["lastLocation"]
        )
        print("Roblox Creation Date: " + data["created"])
        print(
            "Roblox profile link: " + "https://www.roblox.com/users/" + str(data["id"])
        )
        if not check_alt:
            print("Alt Check: " + colorama.Fore.GREEN + "Passed")
        else:
            print("Alt Check: " + colorama.Fore.RED + "Failed (Possible Alt)")

        print(colorama.Fore.RESET + "-------------------------")
        IfGroupCheck = input("Would you like to run a Group Check? [Y/N]: ")
        IfGroupCheckLower = IfGroupCheck.lower()

        if IfGroupCheckLower == "y":
            CheckForBlacklist = input(
                "Would you like to search for blacklisted Groups only? [Y/N]: "
            )
            if CheckForBlacklist.lower() == "y":
                blacklistedGroups = []
                InputBlacklistedGroups = input(
                    "Enter the blacklisted groups seperate each one with a (','): "
                )
                InputBlacklistedGroupsSplit = InputBlacklistedGroups.split(",")
                for i in InputBlacklistedGroupsSplit:
                    blacklistedGroups.append(int(i))

                groups = getGroups(int(inputId), blacklistedGroups)
                if len(groups) == 0:
                    print("No blacklisted groups found!")
                    exit()
                else:
                    print("Running group check...")
                    time.sleep(0.5)
                    print(
                        "A total of "
                        + str(len(groups))
                        + " blacklisted groups were found!"
                    )
                    for i in groups:
                        print(f"{i}\n")

            else:
                groups = getGroups(int(inputId))

                print("Running group check...")
                time.sleep(0.5)
                for i in groups:
                    print(f"{i}\n")

        else:
            Clear()
            print("Group check not required, exiting...")
            exit()

    except ValueError:
        print("Roblox ID must be an integer!")
        exit()


def getAccount(rblxId: int):
    url = "https://users.roblox.com/v1/users/" + str(rblxId)
    response = requests.get(url)
    restoJson = response.json()
    return restoJson


def getGroups(rblxId: int, blacklistedGroups: list = None):
    url = "https://groups.roblox.com/v1/users/" + str(rblxId) + "/groups/roles"
    response = requests.get(url)
    restoJson = response.json()
    groupNames = []

    if not blacklistedGroups:
        for group in restoJson["data"]:
            groupNames.append(
                group["group"]["name"] + " " + "[" + str(group["group"]["id"]) + "]"
            )

        return groupNames
    else:
        for group in restoJson["data"]:
            if group["group"]["id"] in blacklistedGroups:
                groupNames.append(
                    group["group"]["name"] + " " + "[" + str(group["group"]["id"]) + "]"
                )

        return groupNames


def isAlt(rblxId: int):
    url = "https://users.roblox.com/v1/users/" + str(rblxId)
    response = requests.get(url)
    restoJson = response.json()

    dateOfCreation = restoJson["created"]
    creation_datetime = datetime.strptime(dateOfCreation, "%Y-%m-%dT%H:%M:%S.%fZ")
    current_time = datetime.now()
    allowed_time = current_time - timedelta(days=30)

    if creation_datetime > allowed_time:
        get_badges = (
            "https://badges.roproxy.com/v1/users/"
            + str(rblxId)
            + "/badges?limit=100&sortOrder=Asc"
        )
        response = requests.get(get_badges)
        restoJson = response.json()
        if restoJson["total"] <= 50:
            return True
        else:
            return False
    else:
        return False


def getCurrentStatus(rblxId: int):
    url = "https://presence.roblox.com/v1/presence/users/"
    data = {"userIds": [rblxId]}
    response = requests.post(url, json=data)
    restoJson = response.json()
    return restoJson


def main():
    CheckDependencies()
    Start()


if __name__ == "__main__":
    main()
