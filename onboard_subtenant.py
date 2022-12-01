import requests

# api key, host, and headers variables. api key should automatically be pulled from the morpheus user running the task/worflow.
api_key = morpheus['morpheus']['apiAccessToken']
host = morpheus['morpheus']['applianceHost']
headers = {
    "content-type": "application/json",
    "accept": "application/json",
    "authorization": f"Bearer {api_key}",
    }

# subtenant variables
subten_name = morpheus['customOptions']['subtenName']
subten_domain = morpheus['customOptions']['subtenDomain']
subten_currency = morpheus['customOptions']['subtenCurrency']

# creates subtenant and returns tenant id which is used for creating admin user and groups within subtenant.
def create_subtenant():
    url = f"https://{host}/api/accounts"
    payload = {"account": {
        "role": {"id": 2},
        "name": subten_name,
        "subdomain": subten_domain,
        "currency": subten_currency
        }
    }
    response = requests.post(url=url, json=payload, headers=headers, verify=False)
    data = response.json()
    tenant_id = data['account']['id']

    print(response.text)
    print(tenant_id)
    return tenant_id

# subtenant admin user variables
subten_admin_fname = morpheus['customOptions']['subtenAdminFirstName']
subten_admin_lname = morpheus['customOptions']['subtenAdminLastName']
subten_admin_uname = morpheus['customOptions']['subtenAdminUsername']
subten_admin_email = morpheus['customOptions']['subtenAdminEmail']
subten_admin_pw = morpheus['customOptions']['subtenAdminPw']

# creates new admin user with role of JAmultitenant (from morpheus administration > roles)
def create_admin_user(tenant_id):
    url = f"https://{host}/api/accounts/{tenant_id}/users"
    payload = {
        "user": {"receiveNotifications": True,
        "roles": [{"id": 7}],
        "firstName": subten_admin_fname,
        "lastName": subten_admin_lname,
        "username": subten_admin_uname,
        "email": subten_admin_email,
        "password": subten_admin_pw
        }
    }
    response = requests.post(url=url, json=payload, headers=headers, verify=False)
    print(response.text)

# creates and gets admin user's access token
def get_admin_token():
    url = f"https://{host}/oauth/token?client_id=morph-api&grant_type=password&scope=write"
    payload = f"username={new_tenant_id}\\{subten_admin_uname}&password={subten_admin_pw}"
    header = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded; charset=utf-8"
    }
    response = requests.post(url=url, data=payload, headers=header, verify=False)
    data = response.json()
    admin_token = data['access_token']
    print(response.text)
    return admin_token

# creates a default group within subtenant
def create_group(admin_token):
    url = f"https://{host}//groups"
    payload = {"group": {"name": "Default Group"}}
    header = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {admin_token}"
    }
    response = requests.post(url=url, json=payload, headers=header, verify=False)
    print(response.text)
    

new_tenant_id = create_subtenant()
new_admin_user = create_admin_user(new_tenant_id)
admin_token = get_admin_token()
create_group(admin_token)