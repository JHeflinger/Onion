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
    #python
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