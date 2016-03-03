import json
import os

SCRIPT_FOLDER = "scripts"

from powerview import PowerView


def create_scripts(pvs):
    check_for_folder()
    empty_scripts_folder()
    for hub in hubs:
        for scene in hub['scenes']['sceneData']:
            with open("{}/script_{}_{}.py".format(SCRIPT_FOLDER,
                                                  hub["hubname"],
                                                  scene['name']), 'w') as fl:
                fl.write("import requests\n")
                # requests.get("http://192.168.0.117/api/scenes?sceneid=58509")
                fl.write("\n")
                fl.write("# executes a scenario\n")
                fl.write("requests.get('http://{}/api/scenes?sceneid={}')".format(hub['address'],
                                                                                  str(scene['id'])))


def check_for_folder():
    try:
        os.mkdir("scripts")
    except FileExistsError:
        print("folder already exists. Proceeding...")


def empty_scripts_folder():
    filelist = [f for f in os.listdir(SCRIPT_FOLDER) if f.startswith("script")]
    for f in filelist:
        os.remove(os.path.join(SCRIPT_FOLDER, f))


if __name__ == "__main__":
    with open("addresses.json") as fl:
        addresses = json.load(fl)
    hubs = []
    for address in addresses:
        _pv = PowerView(address)
        hubs.append({"address": address,
                     "scenes": _pv.get_scenes(),
                     "hubname": _pv.get_user_data()["userData"]["hubName"]})

    with open("scenes.json", 'w') as fl:
        json.dump(hubs, fl, indent=4)
    create_scripts(hubs)
