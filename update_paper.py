#!/usr/bin/python3


# NOTE: 3rd party modules are imported in the main() function.

import re
import os
import sys
import json


base_download_url = "https://papermc.io/api/v1/paper/{}/latest/download"
base_version_url = "https://papermc.io/api/v1/paper/{}"


class PaperUpdateData:
    def __init__(self, filepath, download_url, buildnum, size):
        self.filepath = filepath
        self.download_url = download_url
        self.buildnum = buildnum
        self.size = size


def cls():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def chk_update(cfg, ask_before_update):
    global base_download_url

    print("Checking for updates ...")

    download_url = base_download_url.format(cfg["paper-version"])

    headers = requests.head(download_url)

    buildnum_pattern = r"^paper-(.*).jar$"

    latest_filename = headers.headers['Content-Disposition'].split("filename=",1)[1]
    latest_download_size = int(headers.headers['Content-Length'])
    latest_buildnum = int(re.search(buildnum_pattern, latest_filename).group(1))

    # Find newest existing build jar in script dir
    current_buildnum = -1
    for filename in os.listdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))):
        if not re.match(buildnum_pattern, filename):
            # file is not a Paper jar file
            continue

        try:
            buildnum = int(re.search(buildnum_pattern, filename).group(1))
        except ValueError:
            continue

        if buildnum > current_buildnum:
            current_buildnum = buildnum


    if latest_buildnum <= current_buildnum:
        print("No updates are available (current build: {})".format(current_buildnum))
        return None


    print("An update is available!\n")

    print("New Build:         {}".format(latest_buildnum))
    if current_buildnum > -1:
        print("Installed Build:   {}".format(current_buildnum))
    else:
        print("Installed Build:   No installed build was found")
    print("Download Size:     {}".format(sizeof_fmt(latest_download_size)))
    print("\n\n")

    if ask_before_update:
        sel = input("Download and Install Update? (y/n) ")

        if sel.lower() != "y":
            return None

    return PaperUpdateData(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), latest_filename), download_url, latest_buildnum, latest_download_size)


def download_update(update_data):
    print("\n\nDownloading update...")

    # Download and save jar
    jar = requests.get(update_data.download_url, allow_redirects=True)
    with open(update_data.filepath, 'wb') as file:
        file.write(jar.content)


def update_server_script(cfg, update_data):
    jar_pattern = r"paper-(.*).jar"

    print("Updating server script...")

    if not os.path.isfile(cfg["start-script-path"]):
        print("ERROR: Start script path '{}' cannot be found. Please update your server script manually.".format(cfg["start-script-path"]))
        return

    with open(cfg["start-script-path"], 'r') as file:
        filedata = file.read()

    # replace Paper jar filename in script with the filename of the new jar
    filedata = re.sub(jar_pattern, os.path.basename(update_data.filepath), filedata)

    with open(cfg["start-script-path"], 'w') as file:
        file.write(filedata)


def print_title(s):
    """Prints a nice looking title for menus, where 's' is a string consisting of the title text"""

    cls()
    print(s.upper())
    print("=" * len(s))
    print("")


def generate_config(json_cfg_path):
    def set_paper_version():
        global base_version_url
        while True:
            print_title("Set Paper version")
            print("You can exit at any time by answering EXIT at any question.\n")

            ver = input("Enter the version you want to use (eg. '1.15.2'):   ")

            if ver.upper() == "EXIT":
                return None
            
            req = requests.get(base_version_url.format(ver))
            if ver == "" or req.status_code == 404:
                print("\n\nERROR: The Paper version you specified does not exist. Make sure the version is available here: https://papermc.io/downloads")
                _ = input("\nPress ENTER to retry ...")
                continue
            
            cls()
            return ver

    if not os.path.isfile(json_cfg_path):
        print_title("Paper Updater Configuration")

        ver = set_paper_version()

        if ver is None:
            cls()
            sys.exit(0)

        cfg = {"paper-version" : ver,
        "start-script-path" : os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "start_noupdate.sh")}
        return cfg
    else:
        return None


def change_config(cfg):
    def change_paper_version():
        global base_version_url
        while True:
            print_title("Change Paper version")
            print("You can exit at any time by answering EXIT at any question.\n")

            new_ver = input("Change from '{}' --> ".format(cfg["paper-version"]))

            if new_ver.upper() == "EXIT":
                break
            
            req = requests.get(base_version_url.format(new_ver))
            if req.status_code == 404:
                print("\n\nERROR: The Paper version you specified does not exist. Make sure the version is available here: https://papermc.io/downloads")
                _ = input("\nPress ENTER to retry ...")
                continue
            
            cfg["paper-version"] = new_ver
            break

    def change_start_script_path():
        while True:
            print_title("Change start script path")
            print("You can exit at any time by answering EXIT at any question.\n")

            new_path = input("Change from '{}' --> ".format(cfg["start-script-path"]))

            if new_path.upper() == "EXIT":
                break

            if not os.path.isfile(new_path):
                print("\n\nERROR: The path you specified does not exist.")
                _ = input("\nPress ENTER to retry ...")
                continue

            cfg["start-script-path"] = new_path
            break

    sel = None
    while True:
        print_title("Paper Updater Configuration")

        print("Select an option:")
        print("\n")
        print("(1) Change Paper version")
        print("(2) Change start script path")
        print("")
        print("(8) Exit without Saving")
        print("(9) Save and Exit")
        print("\n\n")

        ssel = input("> ")
        try:
            sel = int(ssel)
        except ValueError:
            continue

        if sel == 1:
            change_paper_version()
        elif sel == 2:
            change_start_script_path()
        elif sel == 8:
            print_title("Paper Updater Configuration")
            do_not_save_confirmation = input("Are you sure you want to exit WITHOUT saving? (y/n) ").lower()
            if do_not_save_confirmation != "y":
                continue
            return False
        elif sel == 9:
            return True


def save_cfg(cfg, json_cfg_path):
    with open(json_cfg_path, 'w') as outfile:
        json.dump(cfg, outfile)


def main():
    try:
        global requests
        import requests
    except ImportError:
        print("Python module 'requests' is required to use this program. Please install it with 'pip install requests' and run this program again.\n\n")
        _ = input("Press ENTER to exit ...")
        return


    json_cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'update_paper_config.json')

    cfg = generate_config(json_cfg_path)
    if cfg is None:
        with open(json_cfg_path) as json_data_file:
            cfg = json.load(json_data_file)
    else:
        save_cfg(cfg, json_cfg_path)

    ask_before_update = True
    if len(sys.argv) > 1:
        if sys.argv[1] == "-c" or sys.argv[1] == "--conf" or sys.argv[1] == "--config" or sys.argv[1] == "--configure":
            if change_config(cfg):
                save_cfg(cfg, json_cfg_path)
            cls()
            return
        if "-y" in sys.argv:
            ask_before_update = False

    update_data = chk_update(cfg, ask_before_update)
    if update_data is None:
        return
    
    download_update(update_data)
    update_server_script(cfg, update_data)

    print("\nDone!\n------------------\n\n")

main()