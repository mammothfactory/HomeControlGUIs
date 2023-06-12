import subprocess

class PageKiteStartUp():
    
    def __init__(self, homeName):
        subprocess.call(['python3', 'pagekite.py', '8080', f'{homeName}.pagekite.me'])   # Run command in backgroud using &
#curl -O https://pagekite.net/pk/pagekite.py    -> subprocess.call(['curl', '-O', 'https://pagekite.net/pk/pagekite.py'])
#python3 pagekite.py 8080 yourname.pagekite.me  -> f'python3 pagekite.py 8080 {homeName}.pagekite.me' -> subprocess.call(['python3', 'pagekite.py', '8080', f'{homeName}.pagekite.me'])
# python3 pagekite.py 8080 mammothlitehouse.pagekite.me    