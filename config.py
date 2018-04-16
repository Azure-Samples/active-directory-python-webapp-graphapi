RESOURCE = "https://graph.microsoft.com"  # Add the resource you want the access token for
TENANT = "Your tenant"  # Enter tenant name, e.g. contoso.onmicrosoft.com
AUTHORITY_HOST_URL = "https://login.microsoftonline.com"
CLIENT_ID = "Your client id "  # copy the Application ID of your app from your Azure portal
CLIENT_SECRET = "Your client secret"  # copy the value of key you generated when setting up the application

# These settings are for the Microsoft Graph API Call
API_VERSION = 'v1.0'
SCOPES = ['User.Read']  # Add other scopes/permissions as needed.
# This scope allows users to sign-in to the app, and allows the app to read the profile of signed-in users.
# It also allows the app to read basic company information of signed-in users.
# List of scopes/permissions - https://developer.microsoft.com/en-us/graph/docs/concepts/permissions_reference
