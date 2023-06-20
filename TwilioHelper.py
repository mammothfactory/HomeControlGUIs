# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import dotenv_values    # Load environment variables for things usernames, passwords, and API keys

def send_otp_code(code):
    pass

if __name__ == "__main__":
    twilioEnvironmentVariables = dotenv_values()
    accountSid = twilioEnvironmentVariables['TWILIO_ACCOUNT_SID']
    twilioAuthToken = twilioEnvironmentVariables['TWILIO_AUTH_TOKEN']
    verifySid = twilioEnvironmentVariables['VERIFY_SID']
    twilioPhoneNumber = "+18559661260"
    verifiedNumberForFirstUser = "+17196390839"
    #TODO twilioClient = Client(accountSid, twilioAuthToken)

    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    #account_sid = "ACf845a12b2beb2f345ddfe3008ab69d4e"
    #auth_token = "ac380a9596b4b8c52718bc14908f82c2"
    #twilioPhoneNumber = "+18559661260"
    #verified_number = "+17196390839"

    client = Client(accountSid, twilioAuthToken)

    verification = client.verify.v2.services(verifySid) \
    .verifications \
    .create(to=verifiedNumberForFirstUser, channel="sms")
    print(verification.status)

    otp_code = input("Please enter the OTP:")

    verification_check = client.verify.v2.services(verifySid) \
    .verification_checks \
    .create(to=verifiedNumberForFirstUser, code=otp_code)
    print(verification_check.status)
    