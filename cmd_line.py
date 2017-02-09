import argparse
import cmd
from pprint import pprint

try:
    import readline
except ImportError:
    import pyreadline as readline

from powerview_api.powerview import PowerView


# def id_request(func):
#     def wrapper(self,*args,**kwargs):
#         _id = args[0]
#         if _id == '':
#             print ("a shade id is required.")
#             print("select an id from the list.")
#             for shade in self.pv.all_shades:
#                 print(PV.shadestring.format(shade.shade_id, shade.name, shade.shade_type))
#             self.stdout.write("testg")
#         else:
#             func(*args,**kwargs)
#     return wrapper


class Completer():
    def __init__(self, *args, formatstring="{:<8}{:<12}", headers=["id", "name"]):
        self.options = []
        self.formatstring = formatstring

    def prt(self):
        for _id in self.options:
            print(_id[0])

    def append(self, id, *obj):
        self.options.append((self.formatstring.format(id, *obj), str(id)))

    def complete(self, keyword):
        if not keyword:
            return [_a[0] for _a in self.options]
        else:
            rv = []
            first_match = None
            for _a in self.options:
                if _a[0].startswith(keyword):
                    if first_match is None:
                        first_match = _a[1]
                    rv.append(_a[0])

            if len(rv) == 1:
                # print("returning first match")
                # print(first_match)
                return [first_match]
            else:
                return rv


class PV(cmd.Cmd):
    intro = "Welcome"
    prompt = "pv command: "
    shadestring = "{:<8}{:<12}{}"
    scenestring = "{:<8}{:<12}"

    def __init__(self, ip_address):
        cmd.Cmd.__init__(self)
        self.pv = PowerView(ip_address)
        self.ids = None
        self.do_1_shades_get(None)

    def get_shade(self, shade_id):
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

    def _get_id_completions(self, text, line, begidx, endix):
        return self.ids.complete(text)

    def do_1_shades_get(self, arg):
        'Get all shades known by the hub: get_shades'
        self.pv.define_all_shades()
        print(PV.shadestring.format("ID", "NAME", "TYPE"))
        print(PV.shadestring.format("-------", "-----------", "----"))
        self.ids = Completer(PV.shadestring)
        for shade in self.pv.all_shades:
            self.ids.append(shade.shade_id, shade.name, shade.shade_type)
            # _shade = PV.shadestring.format(shade.shade_id, shade.name, shade.shade_type)
            # self.ids.append("{:_<8}{:<12}".format(shade.shade_id, shade.name))
            # print(_shade)
        self.ids.prt()

    def do_2_shade_get_info(self, shade_id):
        shade = self.get_shade(shade_id)
        if shade:
            pprint(shade.__repr__())

    def complete_2_shade_get_info(self, text, line, begidx, endix):
        # return self._get_id_completions(text, line, begidx, endix)
        return self.ids.complete(text)

    def do_open_shade(self, shade_id):
        'Open a shade: open_shade <shade_id>'
        shade = self.get_shade(shade_id)
        if shade:
            shade.open()

    def complete_open_shade(self, text, line, begidx, endix):
        return self.ids.complete(text)

    def do_open2_shade(self, shade_id):
        shade = self.get_shade(shade_id)
        if shade:
            shade.open2()

    def complete_open2_shade(self, text, line, begidx, endix):
        return self.ids.complete(text)

    def do_close_shade(self, shade_id):
        'Close a shade: close_shade <shade_id>'
        shade = self.get_shade(shade_id)
        if shade:
            shade.close()

    def complete_close_shade(self, text, line, begidx, endix):
        return self.ids.complete(text)


    def do_shade_update(self, shade_id):
        shade = self.get_shade(shade_id)
        if shade:
            shade.update()

    def do_shade_jog(self, shade_id):
        'Jog a shade: jog <shade_id>'
        shade = self.get_shade(shade_id)
        if shade:
            shade.jog()

    def do_scenes_get(self, arg):
        'Get all scenes stored in the hub'
        _sc = self.pv.get_scenes()
        for _scene in _sc['sceneData']:
            print(PV.scenestring.format(_scene['id'], _scene['name']))

    def do_scene_activate(self, scene_id):
        'Activate a scene stored in the hub'
        self.pv.activate_scene(scene_id)

    def do_exit(self, arg):
        'Exit this tool'
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ipaddress", help='the ip address of the PowerView hub')
    args = parser.parse_args()
    pv = PV(args.ipaddress)
    pv.cmdloop()
