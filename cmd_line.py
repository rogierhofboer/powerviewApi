import argparse
import cmd

from model.powerview import PowerView


class PV(cmd.Cmd):
    intro = "Welcome"
    prompt = "pv command: "

    def __init__(self, ip_address):
        cmd.Cmd.__init__(self)
        self.pv = PowerView(ip_address)

    def get_shade(self,shade_id):
        try:
            shade_id = int(shade_id)
        except:
            print("wrong shade id: {}".format(shade_id))
            return False
        try:
            shade = next((shade for shade in self.pv.all_shades if shade.shade_id == shade_id))
        except StopIteration:
            print("no shade found with id: {}".format(shade_id))
            return False
        return shade

    def do_get_shades(self, arg):
        self.pv.define_all_shades()
        for shade in self.pv.all_shades:
            print ("{:<8}{}".format(shade.shade_id,shade.name))

    def do_open_shade(self,shade_id):
        shade = self.get_shade(shade_id)
        if shade:
            shade.open()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ipaddress")
    args = parser.parse_args()
    pv = PV(args.ipaddress)
    pv.cmdloop()
