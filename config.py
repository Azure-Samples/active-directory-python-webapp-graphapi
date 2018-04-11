RESOURCE = "https://graph.microsoft.com"  # Add the resource you want the access token for
TENANT =  "Your tenant" # Enter your tenant
AUTHORITY_HOST_URL = "https://login.microsoftonline.com"
CLIENT_ID = "Your client id " # copy the Application ID of your app from your Azure portal
CLIENT_SECRET = "Your client secret" #copy the value of key you generated when setting up the application



#These settings are for the Microsoft Graph API Call
API_VERSION = 'v1.0'
SCOPES = ['User.Read'] #Add other scopes/permissions as needed.
