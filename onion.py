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
