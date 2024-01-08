# r6server
 A server changer tool for Rainbow Six Siege
 <br>
 Just a silly little tool I made to change the r6s server for my friends and I, it speeds up my process. 

![Screenshot of the application running in a terminal](readme_images/image.png)

<hr>
<br>

# How to install
Download the .exe from https://github.com/SuppliedOrange/r6server/releases/tag/latest if you want to use the executable. You may also run it with python or build it yourself if you like.

# How to use
- Start the .exe and choose the server you want to use.
- Select your Ubisoft ID incase you have multiple.
- You may choose to make the app automatically start siege.
- It's recommend you change and customize the constants like your Ubisoft ID and R6S Path to speed up the app's process even more.

# Running as python
Download the repository. Run `pip install -r requirements.txt` to install all prequisites. Then run `py r6server.py`

# Building
I used Python 3.10.10. You'll need to get PyInstaller for this. You can change the name and favicon to anything you like.
<br>
<br>
PyInstaller Command:
```
pyinstaller r6server.py -F -n "R6 Server Changer" -i "favicon.ico"
```
<br>
You should see it in `/dist` after it's completed.
