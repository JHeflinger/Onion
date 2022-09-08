import os

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

def RunScript(scriptcontent, scriptname):
    #currently supported script types:
    #python
    filetype = scriptname.split(".")[len(scriptname.split(".")) - 1]
    if filetype == "py":
        try:
            os.system("python3 " + scriptname)
            return True
        except:
            return False
    else:
        return False
