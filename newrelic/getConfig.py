import configparser


def parseConfig(InFile):
    confDict = {}
    config= configparser.ConfigParser()
    config.read(InFile)
    options = config.options("NRCONFIG")
    for option in options:
        try:
            confDict[option] = config.get("NRCONFIG",option)
           
        except:
            print("Missing Config  values")
    return confDict