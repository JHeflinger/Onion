import os
import subprocess

def GetFileContent(filename):
    with open(filename, "r") as f:
    	return f.read()
    	
def SaveFile(saved, filecontent, filename):
    if not saved:
        try:
            with open(filename, "w") as f:
                f.write(filecontent)
        except:
            print("error. could not save.")
            return False
    return True

def RunScript(scriptcontent, scriptname, console):
    #currently supported script types:
    #python, Java, C++/C
    filetype = scriptname.split(".")[len(scriptname.split(".")) - 1]
    if filetype == "py":
        try:
            os.system("python3 " + scriptname)
            return True
        except:
            return False
    elif filetype == "java":
        console.consoleOutput("Compiling Java...")
        try:
            filename = scriptname.split("/")[len(scriptname.split("/")) - 1].split(".")[0]
            pathname = scriptname[0:len(scriptname) - len(filename) - 6]
            os.system("javac " + scriptname)
            console.consoleOutput("Compiled!")
            console.consoleOutput("Running java file")
            cmd = ['java', '-cp', pathname, filename]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
            console.consoleOutput(output.decode("utf-8"))
            return True
        except:
            console.consoleOutput(Exception)
            return False
    elif filetype == "cpp":
        print("cPP")
        try:
            filename = scriptname.split("/")[len(scriptname.split("/")) - 1].split(".")[0]
            pathname = scriptname[0:len(scriptname) - len(filename) - 5]
            cmd = ['g++', '-o', pathname + '/a.out', scriptname]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
            console.consoleOutput(output.decode("utf-8"))
            cmd = [pathname + '/a.out']
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
            console.consoleOutput(output.decode("utf-8"))
            return True
        except:
            console.consoleOutput(Exception)
            return False
    else:
        return False

def SettingsWrite_OPENED(files):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    print(currentdir)
    writestring = "openfiles:"
    for f in files:
        writestring += (f + "?")
    writestring = writestring[0:len(writestring) - 1] + ":\n"
    lines = []
    with open(currentdir + "/Settings/settings.fhist", "r") as f:
        lines = f.readlines()
    with open(currentdir + "/Settings/settings.fhist", "w") as f:
        lines[0] = writestring
        f.writelines(lines)

def SettingsGet_OPENED():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(currentdir + "/Settings/settings.fhist", "r") as f:
            return f.readlines()[0].split(":")[1].split("?")
    except:
        return []

def SettingsWrite_SELECTED(index):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    lines = []
    with open(currentdir + "/Settings/settings.fhist", "r") as f:
        lines = f.readlines()
    with open(currentdir + "/Settings/settings.fhist", "w") as f:
        lines[1] = "selectedfile:" + index.__str__() + ":\n"
        f.writelines(lines)

def SettingsGet_SELECTED():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    with open(currentdir + "/Settings/settings.fhist", "r") as f:
        return int(f.readlines()[1].split(":")[1])
        
def SettingsGet_PROJECT():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    with open(currentdir + "/Settings/settings.fhist", "r") as f:
        return f.readlines()[3].split(":")[1]
    
def SettingsWrite_PROJECT(path):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    lines = []
    with open(currentdir + "/Settings/settings.fhist", "r") as f:
        lines = f.readlines()
    with open(currentdir + "/Settings/settings.fhist", "w") as f:
        lines[3] = "openproj:" + path + ":\n"
        f.writelines(lines)

def SettingsGet_PROJLANG():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    with open(currentdir + "/Settings/settings.phist", "r") as f:
        return f.readlines()[0].split(":")[1]

def SettingsWrite_PROJLANG(txt):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    lines = []
    with open(currentdir + "/Settings/settings.phist", "r") as f:
        lines = f.readlines()
    with open(currentdir + "/Settings/settings.phist", "w") as f:
        lines[0] = "lang:" + txt + ":\n"
        f.writelines(lines)

def SettingsGet_PROJCONTENT():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    with open(currentdir + "/Settings/settings.phist", "r") as f:
        return f.readlines()[1].split(":")[1]

def SettingsWrite_PROJCONTENT(txt):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    lines = []
    with open(currentdir + "/Settings/settings.phist", "r") as f:
        lines = f.readlines()
    with open(currentdir + "/Settings/settings.phist", "w") as f:
        lines[1] = "files:" + txt.replace("\n", "?") + ":\n"
        f.writelines(lines)

def SettingsGet_PROJDEST():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    with open(currentdir + "/Settings/settings.phist", "r") as f:
        return f.readlines()[2].split(":")[1]

def SettingsWrite_PROJDEST(path):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    lines = []
    with open(currentdir + "/Settings/settings.phist", "r") as f:
        lines = f.readlines()
    with open(currentdir + "/Settings/settings.phist", "w") as f:
        lines[2] = "dest:" + path + ":\n"
        f.writelines(lines)

def RunProject(console):
    #currently supported project types:
    #C++, SDL2
    #'g++ TextureManager.cpp Vector2D.cpp Collision.cpp ECS/ECS.cpp Map.cpp Game.cpp main.cpp -lSDL2 -lSDL2main -lSDL2_image -o testme'
    files = SettingsGet_PROJCONTENT().split("?")
    flags = SettingsGet_PROJLANG().split(",")
    dest = SettingsGet_PROJDEST()
    for i in range(len(flags)):
        flags[i] = flags[i].strip()
    if "C++" in flags:
        console.consoleOutput("Compiling C++ project...")
        cmd = ["g++", "-o", dest + "/a.out"]
        if "SDL2" in flags:
            cmd.insert(1, "-lSDL2_image")
            cmd.insert(1, "-lSDL2main")
            cmd.insert(1, "-lSDL2")
        for f in files:
            if f != "":
                cmd.insert(1, f)
        console.consoleOutput("compiling project...")
        try:
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
            console.consoleOutput(output.decode("utf-8"))
            console.consoleOutput("Running project...")
            cmd = [".//a.out"]
            output = subprocess.Popen(cmd, cwd=dest, stdout=subprocess.PIPE).communicate()[0]
            console.consoleOutput(output.decode("utf-8"))
            console.consoleOutput("Finished project!")
            return True
        except:
            console.consoleOutput(Exception)
            return False
    else:
        return False