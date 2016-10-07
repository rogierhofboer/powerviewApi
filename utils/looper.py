import argparse
import json
import time

from powerview import PowerView
import logging
WAIT_BETWEEN_SHADES=1
logging.basicConfig(level=logging.DEBUG)

def cycleshade(_shades):
    for shade in _shades:
        yield shade

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    args = parser.parse_args()
    with open(args.config_file, 'r') as fl:
        js = json.load(fl)

    shade_ids = js['shade_ids']
    ip = js['pv_hub_ip']
    cycletime = js['cycletime']

    pv = PowerView(ip)
    pv.define_all_shades()
    _shades = []
    for _shade_id in shade_ids:
        _shades.append(next((shade for shade in pv.all_shades if shade.shade_id == _shade_id)))

    cycle = 0

    while 1:
        cycle += 1
        logging.debug("entering cycle {}".format(cycle))
        for shade in cycleshade(_shades):
            shade.open()
            time.sleep(WAIT_BETWEEN_SHADES)
        time.sleep(cycletime)
        for shade in cycleshade(_shades):
            shade.close()
            time.sleep(WAIT_BETWEEN_SHADES)
        time.sleep(cycletime)
