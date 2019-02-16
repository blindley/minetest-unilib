from util import *

if not is_python3():
    print("python version >= 3.0 required")
    exit()

def validate_generator(generator):
    genlist = [
        "Visual Studio 15 2017", "Visual Studio 15 2017 Win64", "Visual Studio 15 2017 ARM",
        "Visual Studio 14 2015", "Visual Studio 14 2015 Win64", "Visual Studio 14 2015 ARM",
        "Visual Studio 12 2013", "Visual Studio 12 2013 Win64", "Visual Studio 12 2013 ARM",
        "Visual Studio 11 2012", "Visual Studio 11 2012 Win64", "Visual Studio 11 2012 ARM",
        "Visual Studio 10 2010", "Visual Studio 10 2010 Win64", "Visual Studio 10 2010 ARM",
        "Visual Studio 9 2008", "Visual Studio 9 2008 Win64", "Visual Studio 9 2008 ARM",
        "Visual Studio 8 2005", "Visual Sudio 8 2005 Win64",
        "Visual Studio 7 .NET 2003",
        "Borland Makefiles", "NMake Makefiles", "NMake Makefiles JOM", "Green Hills MULTI",
        "MSYS Makefiles", "MinGW Makefiles", "Unix Makefiles", "Ninja", "Watcom WMake",
        "CodeBlocks - MinGW Makefiles", "CodeBlocks - NMake Makefiles", "CodeBlocks - NMake Makefiles JOM",
        "CodeBlocks - Ninja", "CodeBlocks - Unix Makefiles",
        "CodeLite - MinGW Makefiles", "CodeLite - NMake Makefiles", "CodeLite - Ninja",
        "CodeLite - Unix Makefiles",
        "Sublime Text 2 - MinGW Makefiles", "Sublime Text 2 - NMake Makefiles",
        "Sublime Text 2 - Ninja", "Sublime Text 2 - Unix Makefiles",
        "Kate - MinGW Makefiles", "Kate - NMake Makefiles", "Kate - Ninja", "Kate - Unix Makefiles",
        "Eclipse CDT4 - NMake Makefiles", "Eclipse CDT4 - MinGW Makefiles", "Eclipse CDT4 - Ninja",
        "Eclipse CDT4 - Unix Makefiles"
    ]

    if generator in genlist:
        return generator

    genlower = generator.lower()
    for g in genlist:
        if g.lower() == genlower:
            return g

    print("Unrecognized generator")
    choice = do_menu(["I meant what I typed", "My bad", "Show me the list"])
    if choice == "My bad":
        return False
    elif choice == "I meant what I typed":
        return generator
    else:
        choice = do_menu(["nevermind"] + genlist)
        if choice == "nevermind":
            return False
        else:
            return choice

global_cache = load_cache()

while True:
    choice = do_menu(["Add Generator", "Remove Generator", "Print Cache", "Exit"])
    if choice == "Exit":
        break
    elif choice == "Add Generator":
        generator = input("Enter CMake Generator: ").strip()
        generator = validate_generator(generator)
        if generator and not generator in global_cache['cmake_generators']:
            print("Adding generator '%s'" % generator)
            global_cache['cmake_generators'].append(generator)
    elif choice == "Remove Generator":
        numgens = len(global_cache['cmake_generators'])
        if numgens == 0:
            print("no generators to remove")
        elif numgens == 1:
            print("removing '%s'" % global_cache['cmake_generators'][0])
            global_cache['cmake_generators'] = []
        else:
            choice = do_menu(global_cache['cmake_generators'] + ["Cancel"])
            if not choice == "Cancel":
                print("removing '%s'" % choice)
                global_cache['cmake_generators'].remove(choice)
    elif choice == "Print Cache":
        print(global_cache)

save_cache(global_cache)
