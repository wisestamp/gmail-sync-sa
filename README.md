#  Running Gmail signature synchronization locally


## Step 1: Create a Google Cloud project.

1. [Open the Google Cloud Console.](https://console.cloud.google.com/)
2. At the top-left, click Menu icon > IAM & Admin > Create a Project.
![](https://d1n2mpfyq0bf3x.cloudfront.net/85b6dfcdd383687854fa079b443af881/create_preject.png)
3. In the Project Name field, enter a descriptive name for your project.
4. *Optional: To edit the Project ID, click Edit. The project ID can't be changed after the project is created, so choose an ID that meets your needs for the lifetime of the project.*
5. In the Location field, click Browse to display potential locations for your project. Then, click Select.
6. Click Create. The console navigates to the Dashboard page and your project is created within a few minutes.

## Step 2 Creating a service account.

1. Open the [Service accounts](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts) page.
2. If prompted, select your project.
3. Click add Create service account.
4. Under Service account details, type a **name**, **ID**, and **description** for the service account, then click Create and continue.
![](https://d1n2mpfyq0bf3x.cloudfront.net/85b6dfcdd383687854fa079b443af881/create_service_account1.png)
*Optional: Under Grant, this service account access to project, select the IAM roles to grant to the service account.*
5. Click Continue.
*Optional: Under Grant users access to this service account, add the users or groups that are allowed to use and manage the service account.*
6. Click Done.
**Next, create a service account key:**
1. Click the email address for the service account you created.
2. Click the **Keys** tab.
![](https://d1n2mpfyq0bf3x.cloudfront.net/85b6dfcdd383687854fa079b443af881/create_service_account_key.png)
3. In the Add key drop-down list, select Create new key.
4. Click Create.
5. Download JSON file to your machine. Rename it to service_account.json Will be needed in step #4

## Step 3 Delegating domain-wide authority to the service account.
1. From your Google Workspace domain’s Admin console, go to [**Main menu > Security > API Controls.**](https://admin.google.com/ac/owl)
2. In the Domain wide delegation pane, select **Manage Domain Wide Delegation.**
![](https://d1n2mpfyq0bf3x.cloudfront.net/85b6dfcdd383687854fa079b443af881/domain-wide-authority.png)
3. Click Add new.
![](https://d1n2mpfyq0bf3x.cloudfront.net/85b6dfcdd383687854fa079b443af881/cleant_id1.png)
4. In the Client ID field, enter the service account's **Client ID**. You can find your service account's client ID in the [service accounts](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts) page.
![](https://d1n2mpfyq0bf3x.cloudfront.net/85b6dfcdd383687854fa079b443af881/client_id.png)
In the **OAuth scopes** (comma-delimited) field, enter the list of scopes that your application should be granted access to:
* https://www.googleapis.com/auth/gmail.settings.basic
* https://www.googleapis.com/auth/gmail.settings.sharing
5. Click Authorize.

## Step 4 Running Gmail signature synchronization script locally.
1. Install python3. Make sure Python is added to your path and available from command prompt. Make sure pip is also installed
2. Get the project from [this repository](https://github.com/wisestamp/gmail-sync-sa).
3. Put service_account.json file inside root folder of the project.
4. Update config.json file with your credentials 

```json
{
    "SIGNATURE_TOKEN": "<teams_token>", 
    "SERVICE_ACCOUNT_FILE": "service_account.json"
}
```
5. Install necessary Python libraries.
`pip install --upgrade pip`
`pip install -r requirements.txt`
6. Run Gmail synchronization script. In command prompt execute 
`python sync_gmail.py`
