# HomeControlGUIs
Graphical User Interfaces for any browser, mobile (iOS &amp; Android) apps, Desktop apps, and embedded house hardware <br>

To start the Progressive Web App (PWA) run the following command: "python3 MainHouse.py" <br>

To delpoy the PWA to the global internet run the following command: "python3 pagekite.py 8080 mammothlitehouse.pagekite.me" <br>

External libraries to install: <br>
pip3 install paramiko <br>
pip3 install supabase <br>~~~
pip3 install nicegui <br>
pip3 install python-dotenv <br> MIGHT COME WITH Python3.9 on CasaOS running debain but not Raspberry Pi CM4
pip3 install bcrypt <br> MIGHT COME WITH Python3.9 on CasaOS running debain but not Raspberry Pi CM4
pip3 install pysqlitecipher <br>


Steps to setup the full IT system for a new house:
1) Go to http://casaos.local/#/ on a development computer on the same physical Ethernet network as the ZimaBoard to setup. Create a new account on the ZimaBoard with the username and password linked to match QR code on ZimaBoard.
2) Follow instructions at https://docs.zimaboard.com/docs/index.html to install Plex, UniFi Controller, PiHole, and HomeAssistant onto CasaOS
3) Install Python 3.9 (specifically) onto CasaOs running the "sudo apt install python3.9 python3-pip" command
4) Install git onto CasaOS running "sudo apt install git" comamnd
5) Install git onto CasaOS running "sudo apt install gh" then run "gh auth login" can follow terminal instructions using github.com and HTTPS. Clone the full HomeControlGUIs repo using the "gh repo clone mammothfactory/HomeControlGUIs" conmand. 
6) pip3 intall the 6 libraraies above running the "Python3 PipInstall.py" or "yes | pip install -r requirements.txt" command
7) Copy the .env file over to CasaOS running the Files app inside the http://casaos.local/#/ Dashboard on a dev computer
8) Change into HomeControlGUI's directory using "cd HomeControlGUIs" then setup PageKite using the two following commands "curl -O https://pagekite.net/pk/pagekite.py" and "python3 pagekite.py 8080 mammothlitehouse.pagekite.me"

https://www.reddit.com/r/Python/comments/10d6ugv/nicegui_let_any_browser_be_the_frontend_for_your/

Command to count lines of code in a directory / git repo:
git ls-files | xargs wc -l


Commands used to define Dockerfile for dependency installs:
pip freeze  > requirements.txt
yes | pip install -r requirememts.txt  


Use a VPC instead of PageKite longterm: ttps://www.linode.com/blog/networking/go-private-with-vlans-and-vpcs/