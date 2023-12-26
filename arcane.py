import requests, colorama, os
from datetime import datetime, timedelta


def CheckDependencies():
    try:
        import requests, colorama
    except ImportError:
        print("Missing dependencies, installing...")
        os.system("pip install requests")
        os.system("pip install colorama")
        print("Dependencies installed! Please restart the program.")
        exit()


def Start():
    colorama.init()

    print(" -- [ PROJECT ARCANE ] -- ")
    print(" Created By: alexy.dev")
    print(" Version: 1.0.0 ")
    print("-------------------------")

    inputId = input("Enter Roblox ID: ")

    try:
        int(inputId)
        print("Fetching data...")
        print("-------------------------")
        os.system("cls")
        data = getAccount(int(inputId))
        groups = getGroups(int(inputId))
        check_alt = isAlt(int(inputId))

        print(" -- [ USER FOUND ] --")
        print(" Username: " + data["name"])
        print(" ID: " + str(data["id"]))
        print(" Roblox Creation Date: " + data["created"])
        if not check_alt:
            print(" Alt Check: " + colorama.Fore.GREEN + "Passed")
        else:
            print(" Alt Check: " + colorama.Fore.RED + "Failed (Possible Alt)")

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
                for i in groups:
                    print(f"{i}\n")

        else:
            os.system("cls")
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


def main():
    CheckDependencies()
    Start()


if __name__ == "__main__":
    main()
