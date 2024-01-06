# Imports
from consolemenu.format import *
from modified_console_menu.menu_borders import MenuBorderStyleType as CustomBorderStyleType
from modified_console_menu.console_menu import *
from modified_console_menu.function_item import FunctionItem
from colors import color, strip_color
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

UUID = "" # Enter your ubisoft connect id if you know it. (located as a folder in C:\Users\(your name)\Documents\My Games\Rainbow Six - Siege)

R6SPATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Tom Clancy\'s Rainbow Six Siege\\RainbowSix.exe" # Replace with your R6S path

# A custom Menu object taken from 
# Functions

def generateOptions():
    serverOptions = []
    for server in SERVER_LIST:

        # Find each option's index number
        item_number =list( SERVER_LIST.keys()).index(server) + 1

        # Making a separator with padding
        separator = "|"

        separator = separator.rjust( 
            ( len( str( len(SERVER_LIST) ) ) + 1 ) - ( len( str( item_number ) ) ) + 1
        )
        
        separator = separator.ljust( len(separator) + 1 )

        # crop and color the server names
        server_name = server[8:] if server != "default" else server
        server_name = color(server_name, SERVER_LIST[server])

        serverOptions.append(
            FunctionItem(
                server_name, switchServer, args=[strip_color(server)],
                menu_char=color( item_number, fg=SERVER_LIST[server] ),
                index_item_separator= separator
            )
        )
    return serverOptions

def switchServer(server:str):

    settingsDir = path.expanduser('~') + r"\Documents\My Games\Rainbow Six - Siege" # this is where the folders of each account's ubisoft uuid are stored as a directory. inside them, are the config folders

    if not path.exists(settingsDir):
        print(f"Error: {settingsDir} does not exist")
        input()
        exit(1)

    if not UUID:
        ubi_ids = get_ubisoft_ids(settingsDir)

        if not ubi_ids: 
            print(color(f"Error: There were no ubisoft ID directories found in {settingsDir}", fg="red"))
            input()
            exit(1)

        if len(ubi_ids) > 1:
            print(color("You have more than 1 ubisoft IDs connected to your R6S documents. The first one found will be used, please delete the folders of the accounts you do not use or modify the code to use your UUID.", fg="red"))
        
        settingsDir = ubi_ids[0] # pick the first one, even if there are many they are ignored.
    
    else:
        settingsDir += rf"\{UUID}"

    configPath = rf"{settingsDir}\GameSettings.ini"

    with open(configPath, "r") as f: # Open and read the file first

        text = f.readlines()
        updated_text = text.copy()

        for line in text:
            if re.match( re.compile(r'DataCenterHint=[a-zA-Z\/\\]+'), line ): # If we find a line that fits the regex of DataCenterHint=(some server)
                updated_text[ updated_text.index(line) ] = f"DataCenterHint={server}\n" # We update it and put it in updated_text
                break
    
    with open(configPath, "w") as f: # Open and rewrite the file.

        f.writelines(updated_text)

    print(color(f"Successfully changed your server to {server}", fg="green"))
    
    input(color("> Press enter to start Rainbow Six Siege\n", fg="blue"))
    try: startR6()
    except: print("Could not start siege! The siege executable path is incorrect.")
    exit(0)


def get_ubisoft_ids(directory_path):
    ubi_id_dirs = []
    uuid_pattern = re.compile(r'\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b') # all ubi ids are UUIDs, so we regex search the folders with UUID patterns.
    all_items = listdir(directory_path)

    # Get all items in the dir
    for item in all_items:
        item_path = path.join(directory_path, item)

        # If the item is a directory and it matches the uuid pattern
        if path.isdir(item_path) and re.match(uuid_pattern, item):
            ubi_id_dirs.append(item_path)

    return ubi_id_dirs
    

def startR6(): # Does not start with vulkan- If you want vulkan, change R6SPATH executable to RainbowSix_Vulkan.exe + You will also need to change the drive folder to wherever you have steam installed.
    startfile(R6SPATH)

def main():

    menu_format = MenuFormatBuilder()
    menu_format.set_border_style_type(CustomBorderStyleType.ZERO_BORDER)
    menu_format.set_subtitle_align('centre')

    # Create the menu
    menu = ConsoleMenu(NAME_ASCII, "Select a server with it's number", show_exit_option=False, formatter=menu_format)

    # Add all the servers to the menu
    for option in generateOptions():
        menu.append_item(option)

    # Show the menu
    menu.show()

if __name__ == "__main__":
    main()