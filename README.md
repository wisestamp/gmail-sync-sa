#  Running Gmail signature synchronization locally


### Step #1: Create a Google Cloud project.
    * Open the Google Cloud Console.
    * At the top-left, click Menu icon > IAM & Admin > Create a Project.
    * In the Project Name field, enter a descriptive name for your project.
    * Optional: To edit the Project ID, click Edit. The project ID can't be changed after the project is created, so choose an ID that meets your needs for the lifetime of the project.
    * In the Location field, click Browse to display potential locations for your project. Then, click Select.
    * Click Create. The console navigates to the Dashboard page and your project is created within a few minutes.
### Step # 2 Creating a service account.
    * Open the Service accounts page.
    * If prompted, select your project.
    * Click add Create service account.
    * Under Service account details, type a name, ID, and description for the service account, then click Create and continue.
    * Optional: Under Grant, this service account access to project, select the IAM roles to grant to the service account.
    * Click Continue.
    * Optional: Under Grant users access to this service account, add the users or groups that are allowed to use and manage the service account.
    * Click Done.
    * Click add Create key, then click Create.
    * Next, create a service account key:
    * Click the email address for the service account you created.
    * Click the Keys tab.
    * In the Add key drop-down list, select Create new key.
    * Click Create.
    * Download JSON file to your machine. Rename it to service_account.json Will be needed in step #4
### Step #3 Delegating domain-wide authority to the service account.
    * From your Google Workspace domain’s Admin console, go to Main menu > Security > API Controls.
    * In the Domain wide delegation pane, select Manage Domain Wide Delegation.
    * Click Add new.
    * In the Client ID field, enter the service account's Client ID. You can find your service account's client ID in the Service accounts page.
    * In the OAuth scopes (comma-delimited) field, enter the list of scopes that your application should be granted access to. For example, if your application needs domain-wide full access to the Google Drive API and the Google Calendar API, enter:
    * https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/gmail.settings.basic
    * Click Authorize.
 
### Step #4 Running gmail signature synchronization script locally.
    * Install python3. Make sure python is added to your path and available from command prompt. Make sure pip is also installed
    * Get the project from this repository.
    * Put service_account.json file inside root folder of the project.
    * Open command prompt inside root folder.
    * Install necessary python libraries. 
        ``` pip install -r requirements.txt ```
    * Edit config.json file.
        domain: The primary domain in google workspace 
        admin_email: Email of one of user with super admin role from google workspace 
    * Run gmail synchronization script. In command prompt execute 
        ``` python sync_gmail.py ```
