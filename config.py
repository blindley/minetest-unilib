import sys
if sys.version_info < (3, 0):
    print("python version >= 3.0 required")
    exit()

import os
import json

global_unilib_root = os.path.dirname(os.path.abspath(__file__))
global_cache_file = global_unilib_root + '/cache.json'

def load_cache():
    if not os.path.isfile(global_cache_file):
         return {'cmake_generators':[]}
    else:
        with open(global_cache_file) as f:
            return json.loads(f.read())

def do_menu(options):
    while True:
        print()
        for i in range(len(options)):
            print("  %s. %s" % (i + 1, options[i]))
        inp = input("> ")
        try:
            choice = int(inp)
            if choice > 0 and choice <= len(options):
                return options[choice - 1]
        except(e):
            pass

global_cache = load_cache()

while True:
    choice = do_menu(["Add Generator", "Remove Generator", "Print Cache", "Exit"])
    if choice == "Exit":
        break
    elif choice == "Add Generator":
        generator = input("Enter CMake Generator: ")
        if not generator in global_cache['cmake_generators']:
            global_cache['cmake_generators'].append(generator)
    elif choice == "Remove Generator":
        numgens = len(global_cache['cmake_generators'])
        if numgens == 0:
            print("no generators to remove")
        elif numgens == 1:
            global_cache['cmake_generators'] = []
        else:
            choice = do_menu(global_cache['cmake_generators'] + ["Cancel"])
            if not choice == "Cancel":
                global_cache['cmake_generators'].remove(choice)
    elif choice == "Print Cache":
        print(global_cache)

with open(global_cache_file, 'w') as f:
    f.write(json.dumps(global_cache))

