import os
import platform
import sys


if __name__ == "__main__":
    import thirdparty.getBoost as getBoost
    import thirdparty.getRelic as getRelic
else:
    from .thirdparty import getBoost
    from .thirdparty import getRelic

#import thirdparty


def Setup(boost, relic, install, prefix):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path + "/thirdparty")

    if boost:
        getBoost.getBoost(install,prefix)
    if relic:
        getRelic.getRelic(install,prefix)


def Build(mainArgs, cmakeArgs,install, prefix):

    osStr = (platform.system())
    buildDir = ""
    args = sys.argv[1:]
    config = ""
    buildType = ""
    if len(args) > 0 and args[0] == "--Debug":
        buildType = "Debug"
        args = args[1:]
    else:
        buildType = "Release"


    if osStr == "Windows":
        buildDir = "out/build/x64-{0}".format(buildType)
        config = "--config {0}".format(buildType)
        args.append("-DCOMMON_FLAGS=/MP /Qpar")
    else:
        buildDir = "out/build/linux"

    if len(prefix) > 0:
        cmakeArgs.append("-DCMAKE_INSTALL_PREFIX={0}".format(prefix))
        

    cmakeArgs.append("-DCMAKE_BUILD_TYPE={0}".format(buildType))

    argStr = ""
    for a in cmakeArgs:
        argStr = argStr + " " + a

    parallel = ""
    if "--noPar" not in sys.argv:
        parallel = "--parallel"

    mkDirCmd = "mkdir -p {0}".format(buildDir); 
    CMakeCmd = "cmake -S . -B {0} {1}".format(buildDir, argStr)
    BuildCmd = "cmake --build {0} {1} {2} ".format(buildDir, config, parallel)

    print("Build Cmd:\n  {0}\n  {1}\n  {2}".format(mkDirCmd, CMakeCmd, BuildCmd))


    InstallCmd = ""
    sudo = ""
    if "--sudo" in sys.argv:
        sudo = "sudo "

    if install:
        InstallCmd = sudo
        InstallCmd += "cmake --install {0} {1} ".format(buildDir, config)

        if len(prefix):
            InstallCmd += " --prefix {3} ".format(prefix)

        print("  {0}".format(InstallCmd))

    print("")

    os.system(mkDirCmd)
    os.system(CMakeCmd)
    os.system(BuildCmd)

    if len(sudo) > 0:
        print("installing libraries: {0}".format(InstallCmd))

    os.system(InstallCmd)


def getInstallArgs(args):
    install = ""
    for x in args:
        if x.startswith("--install="):
            install = x.split("=",1)[1]
            return (True, install)
        if x == "--install":
            return (True, "")
    return (False, "")


def parseArgs():
    
    
    hasCmakeArgs = "--" in sys.argv
    mainArgs = []
    cmakeArgs = []

    if hasCmakeArgs:
        idx = sys.argv.index("--")
        mainArgs = sys.argv[:idx]
        cmakeArgs = sys.argv[idx+1:]

    else:
        mainArgs = sys.argv


    return (mainArgs, cmakeArgs)

def help():
    print(" --setup    \n\tfetch, build and optionally install the dependencies. \
    Must also pass --relic and/or --boost to specify which to build. Without \
    --setup, the main library is built.")

    print(" --install \n\tInstructs the script to install whatever is currently being built to the default location.")
    print(" --install=prefix  \n\tinstall to the provided predix.")
    print(" --sudo  \n\twhen installing, use sudo. May require password.")
    print(" --noPar  \n\twhen building do not use parallel builds.")
    print(" --  \n\tafter the \"--\" argument, all command line args are passed to cmake")

    print("\n\nExamples:")
    print("-fetch the dependancies and dont install")
    print("     python build.py --setup --boost --relic")
    print("-fetch the dependancies and install with sudo")
    print("     python build.py --setup --boost --relic --install --sudo")
    print("-fetch the dependancies and install to a specified location")
    print("     python build.py --setup --boost --relic --install=~/my/install/dir")
    print("")
    print("-build the main library")
    print("     python build.py")
    print("-build the main library with cmake configurations")
    print("     python build.py -- -DCMAKE_BUILD_TYPE=Debug -DENABLE_SSE=ON")
    print("-build the main library and install with sudo")
    print("     python build.py --install --sudo")
    print("-build the main library and install to prefix")
    print("     python build.py --install=~/my/install/dir ")




def main():
    (mainArgs, cmake) = parseArgs()
    if "--help" in mainArgs:
        help()
        return 

    relic = ("--relic" in mainArgs)
    boost = ("--boost" in mainArgs)
    setup = ("--setup" in mainArgs)
    install, prefix = getInstallArgs(mainArgs)
    
    if(setup):
        Setup(boost, relic,install, prefix)
    else:
        Build(mainArgs, cmake,install, prefix)

if __name__ == "__main__":

    main()