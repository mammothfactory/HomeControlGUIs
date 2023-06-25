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


Steps to setup a IT for new hosue:
1) Follow https://docs.zimaboard.com/docs/index.html at install Plex, UniFi Controller, PiHole, and HomeAssistant onto CasaOS
2) Install Python 3.9 (specifically) onto CasaOs using sudo apt install python3.9 python3-pip
3) Install git onto CasaOS using "sudo apt install git"
3) Install git onto CasaOS using "sudo apt install gh" then run "gh auth login" can follow terminal instrictions usins github.com and HTTPS 