import sys
import json
import os

def is_python3():
    return sys.version_info >= (3,0)

def unilib_root_directory():
    return os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

def cache_file_name():
    return unilib_root_directory() + "/cache.json"

def load_cache():
    if not os.path.isfile(cache_file_name()):
         return {'cmake_generators':[]}
    else:
        with open(cache_file_name()) as f:
            return json.loads(f.read())

def save_cache(cache_object):
    with open(cache_file_name(), 'w') as f:
        f.write(json.dumps(cache_object))


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
        except ValueError:
            print("please enter an integer")

