# Imports
import random
from modified_console_menu.menu_borders import MenuBorderStyleType
from modified_console_menu.console_menu import ConsoleMenu, MenuFormatBuilder
from modified_console_menu.function_item import FunctionItem
from colors import color
from os import listdir, path, startfile
import re

# Name of the server
NAME_ASCII = f"""

 ██████████                               ██        
░░███░░░░███                             ███        
 ░███   ░░███  ██████   ██████   ███████░░░   █████ 
 ░███    ░███ ███░░███ ███░░███ ███░░███     ███░░  
 ░███    ░███░███ ░███░███ ░███░███ ░███    ░░█████ 
 ░███    ███ ░███ ░███░███ ░███░███ ░███     ░░░░███
 ██████████  ░░██████ ░░██████ ░░███████     ██████ 
░░░░░░░░░░    ░░░░░░   ░░░░░░   ░░░░░███    ░░░░░░  
                                ███ ░███            
                               ░░██████             
                                ░░░░░░              

    {color("R6S", fg="dodgerblue")}  {color("Server Changer", fg="lightsteelblue")}
"""

# Data centre list
SERVER_LIST = {
    "default": "lightgray",
    "playfab/australiaeast": "mediumseagreen",
    "playfab/brazilsouth": "lightcoral",
    "playfab/centralus": "lightsteelblue",
    "playfab/eastasia": "darkkhaki",
    "playfab/eastus": "lightpink",
    "playfab/japaneast": "lightskyblue",
    "playfab/northeurope": "thistle",
    "playfab/southafricanorth": "darkseagreen",
    "playfab/southcentralus": "lightseagreen",
    "playfab/southeastasia": "darkorchid",
    "playfab/uaenorth": "palegoldenrod",
    "playfab/westeurope": "mediumslateblue",
    "playfab/westus": "darksalmon"
}

# Enter your ubisoft connect id if you know it. (located as a folder in C:\Users\(your name)\Documents\My Games\Rainbow Six - Siege), probably. Also check your onedrive.
UUID = ""

# Replace with your R6S path
R6SPATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Tom Clancy\'s Rainbow Six Siege\\RainbowSix.exe" 

# Enter your R6S settings file path if you know it. Defaults to {UserProfile}/Documents/My Games/Rainbow Six - Siege/
SETTINGS_PATH = "" 

# Asks if you want to start r6s after changing your server.
START_R6S = False 


# Functions

def switchServer(configPath, server):

    try:
        with open(configPath, "r") as f: # Open and read the file first

            text = f.readlines()
            updated_text = text.copy()

            for line in text:
                if re.match( re.compile(r'DataCenterHint=[a-zA-Z\/\\]+'), line ): # If we find a line that fits the regex of DataCenterHint=(some server)
                    updated_text[ updated_text.index(line) ] = f"DataCenterHint={server}\n" # We update it and put it in updated_text
                    break

    except FileNotFoundError: # If the file doesn't exist
        input(color("Could not find your config file!", fg="red"))
        exit()
    
    with open(configPath, "w") as f: # Open and rewrite the file.
        f.writelines(updated_text)

    print(color(f"Successfully changed your server to {server}", fg="green"))

    startR6()

    exit(0)

def getUbisoftIds(directory_path):

    ubi_id_dirs = []

    # All ubisoft ids are UUIDs, so we regex search the folders with UUID patterns.
    uuid_pattern = re.compile(r'\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b')

    all_items = listdir(directory_path)

    # Get all items in the directory
    for item in all_items:
        item_path = path.join(directory_path, item)

        # If the item is a directory and it matches the uuid pattern
        if path.isdir(item_path) and re.match(uuid_pattern, item):
            ubi_id_dirs.append( re.search(uuid_pattern, item).group(0) )

    return ubi_id_dirs

def makeSeparatorWithPadding(separator, item_number, item_list):

        separator = separator.rjust( 
            len( str(len(item_list)) ) - len( str(item_number) ) + 2
            # Length of the stringified of the biggest number in the item list - Length of the stringified version of the item number + 2 (To add space after calculations)
            # For example, 12 items in a list, String of that is '12', Length of that is 2.
        )
        
        separator = separator.ljust( len(separator) + 1 )

        return separator

def generateUbisoftIDOptions(settingsDir, server):

    ubiIdOptions = []
    ubiIds = getUbisoftIds(settingsDir)

    for ubiId in ubiIds:

        # Find each option's index number
        item_number = ubiIds.index(ubiId) + 1

        separator = makeSeparatorWithPadding("|", item_number, ubiIds)
                
        id_name = color(ubiId, applyColor(item_number))

        configPath = settingsDir + rf"\{ubiId}\GameSettings.ini"
    
        ubiIdOptions.append(
            FunctionItem(
                id_name, switchServer, args=[configPath, server],
                menu_char=color( item_number, applyColor(item_number) ),
                index_item_separator= separator
            )
        )
        
    return ubiIdOptions

def pickUbisoftID(settingsDir, server):
    
    menu_format = MenuFormatBuilder()
    menu_format.set_border_style_type(MenuBorderStyleType.ZERO_BORDER)
    menu_format.set_subtitle_align('centre')

    menu = ConsoleMenu (
        NAME_ASCII,
        f"You have multiple accounts with R6S. Choose the UUID of the account you want.\nThis is located in {settingsDir}",
        show_exit_option=False, formatter=menu_format
    )

    for option in generateUbisoftIDOptions(settingsDir, server):
        menu.append_item(option)
    
    menu.show()

def startR6(): 
        try: # Attempt to start r6s
            if START_R6S:
                input(color("> Press enter to start Rainbow Six Siege or close this window.\n", fg="blue"))
                startfile(R6SPATH)
                # Does not start with vulkan- If you want vulkan, change R6SPATH executable to RainbowSix_Vulkan.exe
                # You will also need to change the drive folder to wherever you have steam installed.
            else:
                input()
        except: print("Siege failed to start. Is your executable path correct? Ignore this if you didn't want to start siege.")

def applyColor(item_number):
    try:
        return list(SERVER_LIST.values())[item_number - 1]
    except IndexError:
        return random.choice( list(SERVER_LIST.values()) )
    
def findConfigFile(server:str):

    if not SETTINGS_PATH:

        # This is where the folders of each account's ubisoft uuid are stored as a directory. inside them, are the config folders. A OneDrive alternative is also included just in case.
        standard_path = r"\Documents\My Games\Rainbow Six - Siege" 
        onedrive_path = r"\OneDrive\Documents\My Games\Rainbow Six - Siege"

        settingsDir = path.expanduser('~') + standard_path 

        if not path.exists(settingsDir): # If the path does not exist, it's probably stored in OneDrive?
            settingsDir = path.expanduser('~') +  onedrive_path
        
        if not path.exists(settingsDir): # If the path still does not exist, that's a problem
            print(f"Error: {path.expanduser('~') + standard_path} (and the onedrive counterpart) does not exist.")
            input()
            exit(1)
            
    else:
        settingsDir = SETTINGS_PATH

    if not UUID: # If there's no preset UUID

        ubi_ids = getUbisoftIds(settingsDir)
        chosen_ubi_id = None

        if not ubi_ids: # If there were no UUIDs found 
            print(color(f"Error: There were no ubisoft ID directories found in {settingsDir}", fg="red"))
            input()
            exit(1)

        if len(ubi_ids) > 1: # If there's more than 1 ubisoft ID
            pickUbisoftID(settingsDir, server)
            return
        
        else:
            chosen_ubi_id = ubi_ids[0]
        
        settingsDir += rf"\{chosen_ubi_id}" # pick the first one, even if there are many they are ignored.
    
    else:
        settingsDir += rf"\{UUID}"

    configPath = rf"{settingsDir}\GameSettings.ini"

    switchServer(configPath, server)

def generateServerOptions():
    serverOptions = []
    for server in SERVER_LIST:

        # Find each option's index number
        item_number =list( SERVER_LIST.keys()).index(server) + 1

        # Making a separator with padding

        separator = makeSeparatorWithPadding("|", item_number, SERVER_LIST)

        # crop and color the server names
        server_name = server[8:] if server != "default" else server
        server_name = color(server_name, SERVER_LIST[server])

        serverOptions.append(
            FunctionItem(
                server_name, findConfigFile, args=[server],
                menu_char=color( item_number, fg=SERVER_LIST[server] ),
                index_item_separator= separator
            )
        )

    return serverOptions

# Main function

def main():

    menu_format = MenuFormatBuilder()
    menu_format.set_border_style_type(MenuBorderStyleType.ZERO_BORDER)
    menu_format.set_subtitle_align('centre')

    # Create the menu
    menu = ConsoleMenu (
        NAME_ASCII, "Select a server with it's number",
        show_exit_option=False, formatter=menu_format
    )

    # Add all the servers to the menu
    for option in generateServerOptions():
        menu.append_item(option)

    # Show the menu
    menu.show()

if __name__ == "__main__":
    main()

"""
A little map of how things work:
> main (gets options from generateServerOptions) -> sends selected option to findConfigFile
> findConfigFile -> Sends selected option and the config file either directly to switchServer or pickUbisoftId depending on whether there are many ubisoft IDs logged in the system or not
> pickUbisoftId (gets options from generateUbisoftIdOptions) -> Sends selected option to switchServer
> switchServer ends the process.
"""