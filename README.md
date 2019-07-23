---
services: active-directory
platforms: python
author: abpati
level: 200
client: Python Web App
service: Microsoft Graph
endpoint: AAD v1.0
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

```Shell
git clone https://github.com/Azure-Samples/https://github.com/Azure-Samples/active-directory-python-webapp-graphapi.git
```

> To avoid file name length limitations in Windows, clone the repo close to your root directory.

### Step 2.  Register the app 

There is one project in this sample. To register it, you can:

- either follow the steps [Step 2: Register the sample with your Azure Active Directory tenant](#step-2-register-the-sample-with-your-azure-active-directory-tenant) and [Step 3:  Configure the sample to use your Azure AD tenant](#choose-the-azure-ad-tenant-where-you-want-to-create-your-applications)
- or use PowerShell scripts that:
  - **automatically** creates the Azure AD applications and related objects (passwords, permissions, dependencies) for you
  - modify the configuration file of your project.

If you want to use this automation:
1. On Windows run PowerShell and navigate to the root of the cloned directory
1. In PowerShell run:
   ```PowerShell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
   ```
1. Run the script to create your Azure AD application and configure the code of the sample application accordingly. 
   ```PowerShell
   .\AppCreationScripts\Configure.ps1
   ```
   > Other ways of running the scripts are described in [App Creation Scripts](./AppCreationScripts/AppCreationScripts.md)

#### Choose the Azure AD tenant where you want to create your applications

As a first step you'll need to:

1. Sign in to the [Azure portal](https://portal.azure.com) using either a work or school account or a personal Microsoft account.
1. If your account is present in more than one Azure AD tenant, select your profile at the top right corner in the menu on top of the page, and then **switch directory**.
   Change your portal session to the desired Azure AD tenant.

#### Register the webApp app (PythonWebApp)

1. Navigate to the Microsoft identity platform for developers [App registrations](https://go.microsoft.com/fwlink/?linkid=2083908) page.
1. Select **New registration**.
1. When the **Register an application page** appears, enter your application's registration information:
   - In the **Name** section, enter a meaningful application name that will be displayed to users of the app, for example `PythonWebApp`.
   - Leave **Supported account types** on the default setting of **Accounts in this organizational directory only**.
   - In the Redirect URI (optional) section, select **Web** in the combo-box and enter the following redirect URIs: `http://localhost:5000/getAToken`.
1. Select **Register** to create the application.
1. On the app **Overview** page, find the **Application (client) ID** value and record it for later. You'll need it to configure the Visual Studio configuration file for this project.
<!-- 1. From the app's Overview page, select the **Authentication** section.
   - In the **Advanced settings** | **Implicit grant** section, check **ID tokens** as this sample requires
     the [Implicit grant flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-implicit-grant-flow) to be enabled to
     sign-in the user, and call an API.-->
6. Select **Save**.
1. From the **Certificates & secrets** page, in the **Client secrets** section, choose **New client secret**:

   - Type a key description (of instance `app secret`),
   - Select a key duration of either **In 1 year**, **In 2 years**, or **Never Expires**.
   - When you press the **Add** button, the key value will be displayed, copy, and save the value in a safe location.
   - You'll need this key later to configure the project in Visual Studio. This key value will not be displayed again, nor retrievable by any other means,
     so record it as soon as it is visible from the Azure portal.
1. Select the **API permissions** section
   - Click the **Add a permission** button and then,
   - Ensure that the **Microsoft APIs** tab is selected
   - In the *Commonly used Microsoft APIs* section, click on **Microsoft Graph**
   - In the **Delegated permissions** section, ensure that the right permissions are checked: **User.Read**. Use the search box if necessary.
   - Select the **Add permissions** button

### Step 3:  Configure the sample to use your Azure AD tenant

In the steps below, "ClientID" is the same as "Application ID" or "AppId".

Open the config.py file to configure the project

#### Configure the webApp project

> Note: if you used the setup scripts, the changes below will have been applied for you

1. Open the `config.py` file
1. Find the app key `TENANT` and replace the existing value with your Azure AD tenant name.
1. Find the app key `CLIENT_SECRET` and replace the existing value with the key you saved during the creation of the `PythonWebApp` app, in the Azure portal.
1. Find the app key `CLIENT_ID` and replace the existing value with the application ID (clientId) of the `PythonWebApp` application copied from the Azure portal.

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
The sample first starts sign in by redirecting the application from `@app.route("/")`  to  `@app.route("/login")`. It forms an authorization url that goes to the Authorization endpoint here:

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
## How to deploy this sample to Azure

This project has one WebApp / Web API projects. To deploy them to Azure Web Sites, you'll need, for each one, to:

- create an Azure Web Site
- publish the Web App / Web APIs to the web site, and
- update its client(s) to call the web site instead of IIS Express.

### Create and publish the `PythonWebApp` to an Azure Web Site

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Click `Create a resource` in the top left-hand corner, select **Web** --> **Web App**, and give your web site a name, for example, `PythonWebApp-contoso.azurewebsites.net`.
1. Thereafter select the `Subscription`, `Resource Group`, `App service plan and Location`. `OS` will be **Windows** and `Publish` will be **Code**.
1. Click `Create` and wait for the App Service to be created.
1. Once you get the `Deployment succeeded` notification, then click on `Go to resource` to navigate to the newly created App service.
1. Once the web site is created, locate in the **Dashboard** and click it to open **App Services** **Overview** screen.

<!--
## Review and delete the following two lines if not applicable end ##

1. From the **Overview** tab of the App Service, download the publish profile by clicking the **Get publish profile** link and save it.  Other deployment mechanisms, such as from source control, can also be used.
1. Switch to Visual Studio and go to the PythonWebApp project.  Right click on the project in the Solution Explorer and select **Publish**.  Click **Import Profile** on the bottom bar, and import the publish profile that you downloaded earlier.
1. Click on **Configure** and in the `Connection tab`, update the Destination URL so that it is a `https` in the home page url, for example [https://PythonWebApp-contoso.azurewebsites.net](https://PythonWebApp-contoso.azurewebsites.net). Click **Next**.
1. On the Settings tab, make sure `Enable Organizational Authentication` is NOT selected.  Click **Save**. Click on **Publish** on the main screen.
1. Visual Studio will publish the project and automatically open a browser to the URL of the project.  If you see the default web page of the project, the publication was successful.
 -->

### Update the Active Directory tenant application registration for `PythonWebApp`

1. Navigate back to to the [Azure portal](https://portal.azure.com).
In the left-hand navigation pane, select the **Azure Active Directory** service, and then select **App registrations**.
1. In the resultant screen, select the `PythonWebApp` application.
1. From the *Branding* menu, update the **Home page URL**, to the address of your service, for example [https://PythonWebApp-contoso.azurewebsites.net](https://PythonWebApp-contoso.azurewebsites.net). Save the configuration.
1. Add the same URL in the list of values of the *Authentication -> Redirect URIs* menu. If you have multiple redirect urls, make sure that there a new entry using the App service's Uri for each redirect url.


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

For more information about how OAuth 2.0 protocols work in this scenario and other scenarios, see [Authentication Scenarios for Azure AD](http://go.microsoft.com/fwlink/?LinkId=394414).
