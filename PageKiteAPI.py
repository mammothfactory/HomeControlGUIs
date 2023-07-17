#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.1.0"
"""

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name

# Standard Python libraries
import subprocess
from time import sleep
import xmlrpc.client

import GlobalConstants as GC

API_URL = 'https://pagekite.net/xmlrpc/'

# Error Codes
# https://pagekite.net/support/service_api_reference/#error_codes
bad_value = "Bad value for"
bad_key = "Invalid key"
bad_users = "Invalid e-mails or kite names"
bad_group = "Invalid group ID"
dns_error = "DNS Error"
domain = "Domain unavailable"
domaintaken = "Domain is already in use"
email = "Invalid e-mail address"
emailtaken = "E-mail is already in use"
error = "Internal Error"
kite_gone = "No such kite, was it already deleted?"
no_account = "No such account exists"
no_groups = "You cannot create any more groups"
no_members = "That would exceed your membership limit!"
no_root_ns = "Could not find root nameserver"
no_service = "Not a service domain"
not_cname = "CNAME record not found"
not_in_group = "You are not in a group"
pass_mismatch = "Passwords do not match"
pass_short = "Passwords is too short"
pleaselogin = "Please log in"
subdomain = "Invalid kite name"
terms = "Please accept the terms and conditions"
unauthorized = "Access Denied"
unchanged = "Nothing has changed"
undo_key = "Invalid Undo Key"
unregistered = "Not a registered kite"

class PageKiteAPI():
    """Log into base pagekite.me domains and add & remove subdomains for each house updating the .pagekite.rc file in home directory
    """

    def __init__(self, pagekiteDomain: str, configuration):
        """Create session credentials for base Page Kite domain names
           See https://pagekite.net/support/service_api_reference
 
        Args:
            pagekiteDomain (String): Base URL to add subdomains to
        """
        self.ActiveSubdomain = ''
        self.processCode  = -1
        self.pagekiteDomain = pagekiteDomain
        
        #pagekiteEnvironmentVariables = dotenv_values()
        pagekiteUserName = configuration['PAGE_KITE_EMAIL']
        pagekitePassword = configuration['PAGE_KITE_PASSWORD']
        pagekiteKey = configuration['PAGE_KITE_KEY']
        
        self.proxy = xmlrpc.client.ServerProxy(API_URL)
        ok, creds = self.proxy.login(pagekiteDomain, pagekitePassword, '')
        
        self.accountIdentifer, self.accessCredential = creds
        
        print(creds)
        
        if ok == 'unauthorized':
            print(f'Login in failed')
        else:
            pass
        
    def logout(self):
        """If the revoke_all variable is True, all temporary access credentials will be revoked. 
           Otherwise, only the credential in use by this session will be revoke
        """
        revokeAll = False
        self.proxy.logout(self.accountIdentifer, self.accessCredential, revokeAll)

    def run_kite(self):
        url = f'{self.ActiveSubdomain.lower()}.{self.pagekiteDomain}'
        
        command = ['python3', 'pagekite.py', f'{GC.LOCAL_HOST_PORT_FOR_GUI}', url]
        backgroundPageKiteProcess = subprocess.Popen(command)
        self.processCode = backgroundPageKiteProcess.pid
        print(f'PID = {self.processCode}')

    def stop_kite(self):
        subprocess.call(['kill', '-9', f'{self.processCode}'])

    def get_kite_flying_status(self):
        statusCode, data = self.proxy.get_kite_stats(self.accountIdentifer, self.accessCredential)
        print(f'Current running URLs are {data}')
        return data
        
    def remove_subdomain_kite(self, homeNameSubDomain: str) -> str:
        """_summary_
           data = 'No such kite, was it already deleted?
           data = 'Deleted: apitest.litehouse.pagekite.me'
        """
        url  = f'{homeNameSubDomain.lower()}.{self.pagekiteDomain}'
        forceDelete = True
        statusCode, data = self.proxy.admin_delete_kites(self.accountIdentifer, self.accessCredential, [url], forceDelete)

        print(data)
        
        # Check API Error Code returned by admin_delete_kites()
        if data == kite_gone:
            return "Subdomain doesn't exist or the URL has a typo"

    def add_subdomain_kite(self, homeNameSubDomain: str) -> bool:
        """_summary_
       
        """
        # Check kite status (if it already exists) and  proxy.get_kite_stats(a, c)
        newUrlAdded = False
        
        statusDictionary = self.get_kite_flying_status()
        url  = f'{homeNameSubDomain.lower()}.{self.pagekiteDomain}'
        
        if url in statusDictionary:
            print("URL already exists")
        else:
            checkCnames = False   # Change to True if using a fully custom domain
            statusCode, data = self.proxy.add_kite(self.accountIdentifer, self.accessCredential, url, checkCnames)
            self.ActiveSubdomain = homeNameSubDomain
            newUrlAdded = True
        
        return newUrlAdded

if __name__ == "__main__":
    litehousePageKiteDomain = 'litehouse.pagekite.me'
    homeName = "7196390839"

    apiObject = PageKiteAPI(litehousePageKiteDomain)
    sleep(5)
    apiObject.add_subdomain_kite(homeName)
    apiObject.get_kite_flying_status()
    sleep(5)
    apiObject.add_subdomain_kite(homeName)
    sleep(5)
    apiObject.run_kite()
    #apiObject.remove_subdomain_kite(homeName)
    sleep(10)
    apiObject.get_kite_flying_status()
    sleep(5)
    apiObject.logout()


"""
# Add services to foo.pagekite.me:
$ pagekite.py --add /var/www foo.pagekite.me # Publish a folder
$ pagekite.py --add 80 http:foo.pagekite.me:8080 # A local webserver
$ pagekite.py --add 22 ssh:foo.pagekite.me # Enable SSH tunneling

# Disabling a service:
$ pagekite.py --disable ssh:foo.pagekite.me

# Disabling an entire kite (all services):
$ pagekite.py --disable foo.pagekite.me

# Removing kites or services completely:
$ pagekite.py --remove ssh:foo.pagekite.me
$ pagekite.py --remove foo.pagekite.me


>>> headers = {'Authorization': f'Basic {PAGE_KITE_EMAIL}:{PAGE_KITE_PASSWORD=}', 'Content-Type': 'application/json'}
>>> payload = {'name': 'testapi.litehouse.pagekite.me'}
>>> response = requests.post('https://api.pagekite.net/' + 'subdomains', headers=headers, json=payload)
>>> response = requests.post('https://pagekite.net/xmlrpc/' + 'subdomains', headers=headers, json=payload)
>>> print(response)
<Response [403]>
>>> exit()
"""      