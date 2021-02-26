import display
import winreg
def search(registry, query, queryresult, string, type):
    #accessing registry through init HKEY
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    #opening registry 
    access_key = winreg.OpenKey(access_registry,registry)
    for i in range(20):
        try:
            #results based on registry keys
            asubkey_name=winreg.EnumKey(access_key,i)
            asubkey=winreg.OpenKey(access_key, asubkey_name)
            #searching all queries
            queryresult = winreg.QueryValueEx(asubkey, query)
        except:
            break
    #converting query output to string
    queryresult =''.join(str(queryresult))
    #checking query against possible keywords
    if string in queryresult:
        #virtual machine detected
        print(type + " " + display.detected())
    else:
        #'virtual machine not detected
        print(type + " " + display.undetected())
    #debugging
    #print("debug info " + colored(queryresult, 'yellow'))

def index(registry, string, type):
    #accessing registry through init HKEY
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    #opening registry 
    for i in range(1028):
        try:
            #results based on directory names
            access_key = winreg.OpenKey(access_registry,registry)
            x =winreg.EnumKey(access_key,i)
            if x == string:
                print(type+ " " + display.detected())
        except:
            break