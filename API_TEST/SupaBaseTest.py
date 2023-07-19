# Open source plaform for NoSQL databases, authentication, file storage, and auto-generated APIs
# https://github.com/supabase-community/supabase-py
from supabase.client import create_client, Client

# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values   

      
config = dotenv_values()
url = config['SUPABASE_URL']
key = config['SUPABASE_KEY']
supabase: Client = create_client(url, key)

user = supabase.auth.sign_in_with_otp({"phone": "17196390839",})
#user.session
#res = supabase.auth.verify_otp({"phone": "17196390839", "token": str(sanitizedOtpCode), "type": 'sms'})