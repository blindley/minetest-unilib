import json, os, subprocess, sys
assert(sys.version_info >= (3,0))

def unilib_root():
    root = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(root, "unilib.root")):
        newroot = os.path.dirname(root)
        if newroot == root:
            raise Exception("unable to find unilib.root")
        root = newroot
    return root

def cache_file_name():
    return os.path.join(unilib_root(), "cache.json")

def load_cache():
    if not os.path.isfile(cache_file_name()):
         return {}
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

    choice = "Show me the list"
    if generator:
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

def generator_build_directory(generator):
    return "%s/lib/build/%s" % (unilib_root(), generator.replace(" ","-"))

def install_directory(generator):
    return "%s/install" % generator_build_directory(generator)

def library_build_directory(generator, libname):
    return "%s/%s" % (generator_build_directory(generator), libname)

def library_source_directory(libname):
    return "%s/lib/%s" % (unilib_root(), libname)

def configure_and_build_and_install(generator, libname, config_options):
    builddir = os.path.normpath(library_build_directory(generator, libname))
    if os.path.exists(builddir):
        print("to rebuild %s, delete '%s'" % (libname, builddir))
        return True

    print("building %s" % libname)
    os.makedirs(builddir)
    if not os.path.exists(builddir):
        print("could not make %s" % builddir)
        return False

    libsource = library_source_directory(libname)

    with open("%s/stdout.log" % unilib_root(), "a") as stdout_log:
        with open("%s/stderr.log" % unilib_root(), "a") as stderr_log:
            result = subprocess.run(
                ["cmake", libsource, "-G", generator,
                "-DCMAKE_INSTALL_PREFIX=%s" % install_directory(generator)
                ]
                + config_options,
                cwd=builddir,
                stdout=stdout_log, stderr=stderr_log
            )

            if not result.returncode == 0:
                print(result.args)
                print("failed to configure %s" % libname)
                return False

    with open("%s/stdout.log" % unilib_root(), "a") as stdout_log:
        with open("%s/stderr.log" % unilib_root(), "a") as stderr_log:
            result = subprocess.run(
                ["cmake", "--build", builddir, "--config", "release", "--target", "install"],
                stdout=stdout_log, stderr=stderr_log
            )

            if not result.returncode == 0:
                print("failed to build %s" % libname)
                return False

    return True


def build_irrlicht(generator):
    libname = "irrlicht"
    return configure_and_build_and_install(generator, libname, [])

def build_zlib(generator):
    libname = "zlib"
    result = configure_and_build_and_install(generator, libname, [])

    # undo zlib/CMakeLists.txt renaming zconf.h, to keep the repository unmodified
    zlib_source = library_source_directory("zlib")
    oldname = "%s/zconf.h.included" % zlib_source
    newname = "%s/zconf.h" % zlib_source
    if os.path.exists(oldname):
        os.replace(oldname, newname)
    return result
    
def build_ogg(generator):
    libname = "ogg"
    return configure_and_build_and_install(generator, libname, [
        "-DBUILD_SHARED_LIBS=TRUE"
    ])
    
def build_vorbis(generator):
    libname = "vorbis"
    install = install_directory(generator)
    return configure_and_build_and_install(generator, libname, [
        "-DBUILD_SHARED_LIBS=TRUE",
        "-DOGG_ROOT=%s" % install
    ])
    
def build_openal(generator):
    libname = "openal"
    return configure_and_build_and_install(generator, libname, [
        "-DALSOFT_UTILS=OFF",
        "-DALSOFT_NO_CONFIG_UTIL=ON",
        "-DALSOFT_EXAMPLES=OFF",
        "-DALSOFT_TESTS=OFF",
        "-DALSOFT_CONFIG=OFF",
        "-DALSOFT_HRTF_DEFS=OFF",
        "-DALSOFT_AMBDEC_PRESETS=OFF"
    ])
    
def build_sqlite3(generator):
    libname = "sqlite3"
    return configure_and_build_and_install(generator, libname, [])

def do_build_all(generator):
    print("building with '%s'" % generator)
    return (build_irrlicht(generator) and
           build_zlib(generator) and
           build_ogg(generator) and
           build_vorbis(generator) and
           build_openal(generator) and
           build_sqlite3(generator)
        )

def build_libraries():
    generator = input("Select generator: ")
    generator = validate_generator(generator)
    if generator:
        if do_build_all(generator):
            print("build succeeded")
        else:
            print("build failed")


def main():
    while True:
        choice = do_menu(["exit", "print cache", "build libraries"])
        if choice == "exit":
            break
        elif choice == "print cache":
            print(load_cache())
        elif choice == "build libraries":
            build_libraries()

if __name__ == "__main__":
    main()