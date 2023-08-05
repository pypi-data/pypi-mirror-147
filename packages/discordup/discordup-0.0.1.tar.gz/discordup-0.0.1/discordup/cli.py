import shlex
import requests
from subprocess import Popen, PIPE
import os
import tempfile

def main():
    #if os.geteuid() != 0:
    #    exit("You need to have root privileges to run discordup.\nPlease try again, this time using 'sudo discordup'.")

    def getLatestVersion(type, version):
        if type == "stable":
            resp = requests.get("https://discord.com/api/download?platform=linux&format=deb")
            latestVersion = resp.url.split("/")[5]
            if latestVersion != version:
                completeName = os.path.join(tempfile.gettempdir(), resp.url.split("/")[-1])

                if os.path.exists(completeName):
                    os.remove(completeName)

                with open(completeName, "wb") as f:
                    f.write(resp.content)

                command = shlex.split(f"sudo apt install '{completeName}'")
                process = Popen(command, stdout=PIPE, stderr=PIPE)
                process.communicate()

                os.remove(completeName)
                return "Has just been updated"
            return "Already up to date"

        elif type == "ptb":
            resp = requests.get("https://discord.com/api/download/ptb?platform=linux&format=deb")
            latestVersion = resp.url.split("/")[5]
            if latestVersion != version:
                completeName = os.path.join(tempfile.gettempdir(), resp.url.split("/")[-1])

                if os.path.exists(completeName):
                    os.remove(completeName)

                with open(completeName, "wb") as f:
                    f.write(resp.content)

                command = shlex.split(f"sudo apt install '{completeName}'")
                process = Popen(command, stdout=PIPE, stderr=PIPE)
                process.communicate()

                os.remove(completeName)
                return "Has just been updated"
            return "Already up to date"

        elif type == "canary":
            resp = requests.get("https://discord.com/api/download/canary?platform=linux")
            latestVersion = resp.url.split("/")[5]
            if latestVersion != version:
                completeName = os.path.join(tempfile.gettempdir(), resp.url.split("/")[-1])

                if os.path.exists(completeName):
                    os.remove(completeName)

                with open(completeName, "wb") as f:
                    f.write(resp.content)

                command = shlex.split(f"sudo apt install '{completeName}'")
                process = Popen(command, stdout=PIPE, stderr=PIPE)
                process.communicate()

                os.remove(completeName)
                return "Has just been updated"
            return "Already up to date"

        elif type == "development":
            resp = requests.get("https://discord.com/api/download/development?platform=linux")
            latestVersion = resp.url.split("/")[5]
            if latestVersion != version:
                completeName = os.path.join(tempfile.gettempdir(), resp.url.split("/")[-1])

                if os.path.exists(completeName):
                    os.remove(completeName)

                with open(completeName, "wb") as f:
                    f.write(resp.content)

                command = shlex.split(f"sudo apt install '{completeName}'")
                process = Popen(command, stdout=PIPE, stderr=PIPE)
                process.communicate()

                os.remove(completeName)
                return "Has just been updated"
            return "Already up to date"

    command = shlex.split('sudo apt list --installed')
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    installations = {"stable": {"installed": False, "version": -1, "needs_update": False}, "ptb": {"installed": False, "version": -1, "needs_update": False}, "canary": {"installed": False, "version": -1, "needs_update": False}, "development": {"installed": False, "version": -1, "needs_update": False}}
    for line in stdout.decode().split("\n"):
        if "discord/now" in line:
            installations["stable"]["installed"] = True
            installations["stable"]["version"] = line.split(" ")[1]
        elif "discord-ptb/now" in line:
            installations["ptb"]["installed"] = True
            installations["ptb"]["version"] = line.split(" ")[1]
        elif "discord-canary/now" in line:
            installations["canary"]["installed"] = True
            installations["canary"]["version"] = line.split(" ")[1]
        elif "discord-development/now" in line:
            installations["development"]["installed"] = True
            installations["development"]["version"] = line.split(" ")[1]

    for installation, details in installations.items():
        if details["installed"]:
            updateStatus = getLatestVersion(installation, details["version"])
            print("\033[1m"+installation.upper()+":\033[0m", updateStatus)
        else:
            print("\033[1m"+installation.upper()+":\033[0m", "Not installed")