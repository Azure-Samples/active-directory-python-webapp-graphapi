---
services: active-directory
platforms: python
author: abpati
level: 200
client: Python Web App
service: Microsoft Graph
endpoint: AAD V1
---
# Calling Microsoft Graph from a web app using ADAL Python

<!--![Build badge](https://travis-ci.org/AzureAD/azure-activedirectory-library-for-python/builds/358958147?utm_source=github_status&utm_medium=notification#)-->

## About this sample

### Overview

This sample demonstrates how to build a Python (Flask) web application that authorizes Azure Active Directory users and access data from the Microsoft Graph.

1. The app uses the Active Directory Authentication Library (ADAL) to acquire a JWT access token for the Microsoft Graph.  
2. The app then uses the access token to get data about the user from the Microsoft Graph. 

![Overview](./ReadmeFiles/topology.png)

## How to run this sample

To run this sample, you'll need:

- [Python 2.7+](https://www.python.org/downloads/release/python-2713/) or [Python 3+](https://www.python.org/downloads/release/python-364/)
- [Flask](http://flask.pocoo.org/)
- [ADAL Python](https://github.com/AzureAD/azure-activedirectory-library-for-python#install) 
- [An Azure AD tenant](https://azure.microsoft.com/en-us/documentation/articles/active-directory-howto-tenant/)
- [An Azure AD user](https://docs.microsoft.com/en-us/azure/active-directory/add-users-azure-active-directory). Note: this sample does not support Microsoft accounts. 

### Step 1.  Clone or download this repository

From your shell or command line:

`git clone https://github.com/Azure-Samples/active-directory-python-webapp-graphapi`

> To avoid file name length limitations in Windows, clone the repo close to your root directory.

### Step 2.  Register the app 

To register the sample, you can:

- either follow the steps in the paragraphs below ([Step 2](#step-2--register-the-sample-with-your-azure-active-directory-tenant) and [Step 3](#step-3--configure-the-sample-to-use-your-azure-ad-tenant))
- or use PowerShell scripts that:
  - **automatically** create for you the Azure AD applications and related objects (passwords, permissions, dependencies)
  - modify the configuration file of your project.

If you want to use this automation, read the instructions in [App Creation Scripts](./AppCreationScripts/AppCreationScripts.md)

#### Choose your tenant

1. Sign in to the [Azure portal](https://portal.azure.com).
1. On the top bar, click on your account, and then on **Switch Directory**. 
1. Once the *Directory + subscription* pane opens, choose the Active Directory tenant where you wish to register your application, from the *Favorites* or *All Directories* list.
1. Click on **All services** in the left-hand nav, and choose **Azure Active Directory**.

> In the next steps, you might need the tenant name (or directory name) or the tenant ID (or directory ID). These are presented in the **Properties**
of the Azure Active Directory window respectively as *Name* and *Directory ID*

#### Register the app

1. In the  **Azure Active Directory** pane, click on **App registrations** and choose **New application registration**.
1. Enter a friendly name for the application, for example 'PythonWebApp' and select 'Web app / API' as the *Application Type*.
1. For the *sign-on URL*, enter the base URL for the sample.  By default, this sample uses `http://localhost:5000/`.
1. Click **Create** to create the application.
1. In the succeeding page, Find the *Application ID* value and record it for later. 
1. Then click on **Settings**, and choose **Properties**.
1. For the App ID URI, replace the guid in the generated URI 'https://\<your_tenant_name\>/\<guid\>', with the name of your service, for example, 'https://\<your_tenant_name\>/App' (replacing `<your_tenant_name>` with the name of your Azure AD tenant)
1. From the **Settings** | **Reply URLs** page for your application, update the Reply URL for the application to be `http://localhost:5000/getAToken`
1. From the Settings menu, choose **Keys** and add a new entry in the Password section:

   - Type a key description (of instance `app secret`),
   - Select a key duration of either **In 1 year**, **In 2 years**, or **Never Expires**.
   - When you save this page, the key value will be displayed, copy, and save the value in a safe location.
   - You'll need this key later to configure the project. This key value will not be displayed again, nor retrievable by any other means,
     so record it as soon as it is visible from the Azure portal.
1. Configure Permissions for your application. In the Settings menu, choose the 'Required permissions' section and then,
   click on **Add**, then **Select an API**, and type `Microsoft Graph` in the textbox. Then, click on  **Select Permissions** and underneath **Delegated Permissions** select **Sign in and read user profile**.

### Step 3.  Configure the sample 

In the steps below, ClientID is the same as Application ID or AppId.

Open the config.py file to configure the project

#### Configure the app project

1. Open the `config.py` file
1. Find the app key `TENANT` and replace the existing value with your AAD tenant name.
1. Find the app key `CLIENT_SECRET` and replace the existing value with the key you saved during the creation of the `PythonWebApp` app in the Azure portal.
1. Find the app key `CLIENT_ID` and replace the existing value with the application ID (client ID) of the `PythonWebApp` application from the Azure portal.

### Step 4. Run the sample

- You will need to install Flask framework and the ADAL Python library using pip as follows:

  ```Shell
  $ pip install flask
  $ pip install adal
  ```
  
- If the environment variable for Flask is already set:

  Run app.py from shell or command line:

  ```Shell
  $ python app.py
  ```
- If the environment variable for Flask is not set:

  Type the following commands on shell or command line by navigating to the project directory:

  ```Shell
  $ export FLASK_APP=app.py
  $ export FLASK_DEBUG=1
  $ flask run
  ```
Follow the sign-in process to complete the logging.

## About the code

The code acquiring a token is located in `app.py` file.
The sample first starts sign in by redirecting the application from `@app.route("/")`  to  `@app/route("/login")`. It forms an authorization url that goes to the Authorization endpoint here:

```Python
authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
resp = Response(status=307)
resp.headers['location']= authorization_url
return resp
```

After the user logs in, the authorization code is used acquire a token in `@app.route("/getAToken")`.
The `AuthenticationContext` is created here:

```Python

auth_context = AuthenticationContext(AUTHORITY_URL, api_version=None)
```

The acquire_token_with_authorization_code() function requests for an access token using the authorization code here:

```Python

token_response = auth_context.acquire_token_with_authorization_code(code,REDIRECT_URI,config.RESOURCE, config.CLIENT_ID, config.CLIENT_SECRET)
```

This token is then used to call the Graph API in `@app.route("/graphcall")`:

```Python
graph_data = SESSION.get(endpoint,headers = http_headers, stream=False).json()
```

## Community Help and Support

Use [Stack Overflow](https://stackoverflow.com/questions/tagged/adal+python) to get support from the community.
Ask your questions on Stack Overflow first and browse existing issues to see if someone has asked your question before.
Make sure that your questions or comments are tagged with [`adal` `python`].

If you find a bug in the sample, please raise the issue on [GitHub Issues](../../issues).

To provide a recommendation, visit the following [User Voice page](https://feedback.azure.com/forums/169401-azure-active-directory).

## Contributing

If you'd like to contribute to this sample, see [CONTRIBUTING.MD](/CONTRIBUTING.md).

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## More information

<!--
For more information, see ADAL Python's conceptual documentation:

> Provide links to the flows from the conceptual documentation
> for instance:
- [Recommended pattern to acquire a token](https://github.com/AzureAD/azure-activedirectory-library-for-dotnet/wiki/AcquireTokenSilentAsync-using-a-cached-token#recommended-pattern-to-acquire-a-token)
- [Acquiring tokens interactively in public client applications](https://github.com/AzureAD/azure-activedirectory-library-for-dotnet/wiki/Acquiring-tokens-interactively---Public-client-application-flows)
-->
For more information about how OAuth 2.0 protocols work in this scenario and other scenarios, see [Authentication Scenarios for Azure AD](http://go.microsoft.com/fwlink/?LinkId=394414).
