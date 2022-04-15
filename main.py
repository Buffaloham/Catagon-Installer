import time
from time import gmtime, strftime
import os
import requests
import json
import zlib
import base64
import hashlib

if (not (os.name == 'nt')): #Windows only sorry fellas :<
    print("This program can only run on windows!")
    exit(0)

os.system("cls")
os.system("color")
print('''
   \033[35m   _____      _                            _____           _        _ _           
     / ____|    | |                          |_   _|         | |      | | |          
    | |     __ _| |_ __ _  __ _  ___  _ __     | |  _ __  ___| |_ __ _| | | ___ _ __ 
    | |    / _` | __/ _` |/ _` |/ _ \| '_ \    | | | '_ \/ __| __/ _` | | |/ _ \ '__|
    | |___| (_| | || (_| | (_| | (_) | | | |  _| |_| | | \__ \ || (_| | | |  __/ |   
     \_____\__,_|\__\__,_|\__, |\___/|_| |_| |_____|_| |_|___/\__\__,_|_|_|\___|_|   
                           __/ |                                                     
                          |___/                                                      
                       

                              Catagon modpack installer!
                                      version 1
               
    \033[33m           
    By continuing to use this program, you agree to it's license...
    
    install     -> Installs the modpack
    license     -> Prints the program license
\033[0m
''')

def printLicense():
    print('''
    Catagon modpack installer for automated Minecraft mod installation
    Copyright (C) 2022 Buffaloham

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    ''')

startTime = time.time()
    
def fprint(x, opt):
    temp = ""
    if (opt == "error"):
        temp = "\033[31m"
    elif (opt == "warning"):
        temp = "\033[33m"
    elif (opt == "notice"):
        temp = "\033[36m"
    elif (opt == "success"):
        temp = "\033[32m"
    print(temp + "[" + strftime("%H:%M:%S] ", gmtime(time.time()-startTime)) + x + "\033[0m")
        
def base64ToJson(x):
    return json.loads(zlib.decompress(base64.b64decode(x.encode('utf-8'))).decode('utf-8'))

def jsonToBase64(x):
    return base64.b64encode(zlib.compress(json.dumps(x).encode('utf-8'), 9)).decode('utf-8')
    
################################################################################################################################
################################################################################################################################

class CurseGoblin:
    def __init__(self):
        self.operational = (requests.get("https://google.com").status_code == 200)
        self.historicalData = []
        
    def findDownloadUrlAndFilename(self, idt, version):
        url = "https://addons-ecs.forgesvc.net/api/v2/addon/" + str(idt)
        r = requests.get(url, headers={'User-agent': 'joemama'})
        if (r.status_code != 200):
            return ["", "", ""]
        else:
            try:
                rejson = r.json()
                destinationUrl = rejson["latestFiles"][0]["downloadUrl"]
                destinationUrl = destinationUrl[:destinationUrl.rfind('/')]
                
                tempFilename = ""
                
                foundDesiredFile = False
                for x in rejson["gameVersionLatestFiles"]:
                    if (x["gameVersion"] == version):
                        destinationUrl += x["projectFileName"]
                        tempFilename = x["projectFileName"]
                        foundDesiredFile = True
                        break
                
                if not foundDesiredFile:
                    return ["", "", ""]
                
                return [rejson["name"], destinationUrl, tempFilename]
            except:
                return ["", "", ""]
   
################################################################################################################################
################################################################################################################################
    
    
def installNow():
    global startTime
    startTime = time.time()
    os.system("cls")
    key = base64ToJson(input("\033[36mInsert Modlist key to install:\033[0m\n\n"))
    os.system("cls")
    fprint("Preparing to install...", "notice")
    #print(key)
    
    if (type(key) != type([])):
        fprint("Key was invalid or corrupted! (Invalid json)", "error")
        input()
        exit()
        
    try:
        if (key[0][0] != "CatagonInstaller1"):
            fprint("Key was invalid or corrupted! (Json data was incorrect)", "error")
            input()
            exit()
        
        hashTemp = ""
        for x in key[1]:
            hashTemp += x
    
        if (key[0][3] != hashlib.md5(hashTemp.encode()).hexdigest()):
            fprint("Checksum doesn't match! (try again)", "error")
            input()
            exit()
    
    except:
        fprint("Key was invalid or corrupted! (Json structure was incorrect)", "error")
        input()
        exit()
    
    fprint("Checksum matched!", "success")
    
    minecraft = os.getenv('APPDATA') + "\\.minecraft"
    
    if (not os.path.isdir(minecraft)):
        fprint("Couldn't find minecraft directory!", "error")
        input()
        exit()
        
    desiredVersion = key[0][2]
    
    fprint("Installing mods....", "notice")
    
    if (not os.path.isdir(minecraft + "\\mods\\.cache")):
        os.mkdir(minecraft + "\\mods\\.cache")
    for file in os.listdir(minecraft+"\\mods"):
        if file.endswith(".jar"):
            if (not (os.path.isfile(minecraft + "\\mods\\.cache\\" + file))):
                os.rename(minecraft + "\\mods\\" + file, minecraft + "\\mods\\.cache\\" + file)
            else:
                os.remove(minecraft + "\\mods\\" + file)
    
    modcount = len(key[1])
    success = 0
    
    cursed = CurseGoblin()
    
    for x in key[1]:
        particle = cursed.findDownloadUrlAndFilename(x, desiredVersion)
        if (particle[1] == ""):
            fprint("Couldn't connect to curseforge servers!", "error")
            continue
        if True:
            if (os.path.isfile(minecraft + "\\mods\\.cache\\" + particle[2])):
                os.rename(minecraft + "\\mods\\.cache\\" + particle[2], minecraft + "\\mods\\" + particle[2])
                fprint("Receive file from cache: " + particle[0], "notice")
            else:
                r = requests.get(particle[1], headers={'User-agent': 'joemama'})
                open(minecraft + "\\mods\\" + particle[2], 'wb').write(r.content)
                fprint("Successfully installed " + particle[0], "success")
            success += 1
        #except:
            #fprint("Failed to install " + particle[0], "error")
    
    
    fprint("\033[35mInstalled: " + str(success) + "/" + str(modcount), "")
    
    fprint("Preparing to install forge...", "notice")
    
    if True:
        r = requests.get("https://maven.minecraftforge.net/net/minecraftforge/forge/" + key[0][1], headers={'User-agent': 'joemama'})
        open(os.getenv('APPDATA') + "\\.minecraft\\mods\\.cache\\forge.jar", 'wb').write(r.content)
        os.system('java -jar "' + os.getenv('APPDATA') + '\\.minecraft\\mods\\.cache\\forge.jar"')
    #except:
       # fprint("Failed to install forge!", "error")
    
    fprint("\033[35mFINISHED INSTALLATION!", "")
    input()
    
    if (cursed == None or not cursed.operational):
        fprint("Failed to connect to the internet!", "error")


################################################################################################################################
################################################################################################################################
    
pickedCommand = False
while (not pickedCommand):
    x = input("> ")
    if (x == "install"):
        installNow()
        pickedCommand = True
    if (x == "clearcache"):
        if (os.path.isdir(os.getenv('APPDATA') + "\\.minecraft\\mods\\.cache")):
            for file in os.listdir(os.getenv('APPDATA') + "\\.minecraft\\mods\\.cache"):
                os.remove(os.getenv('APPDATA') + "\\.minecraft\\mods\\.cache\\" + file)
        fprint("Cleared cache!", "success")
    if (x == "license"):
        printLicense()
        pickedCommand = True