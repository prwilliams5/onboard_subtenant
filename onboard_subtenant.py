import requests

# api key, host, and headers variables. api key pulled should be from the morpheus user running the task/worflow.
api_key = morpheus['morpheus']['apiAccessToken']
host = morpheus['morpheus']['applianceHost']
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {api_key}",
    }

# subtenant variables
subten_name = morpheus['customOptions']['subtenName']
subten_domain = morpheus['customOptions']['subtenDomain']
subten_currency = morpheus['customOptions']['subtenCurrency']

# creates subtenant and returns tenant id which is used for creating admin user and groups within subtenant.
def create_tenant():
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

# instantiate tenant id variable
new_tenant_id = create_tenant()

# subtenant admin user variables
subten_admin_fname = morpheus['customOptions']['subtenAdminFirstName']
subten_admin_lname = morpheus['customOptions']['subtenAdminLastName']
subten_admin_uname = morpheus['customOptions']['subtenAdminUsername']
subten_admin_email = morpheus['customOptions']['subtenAdminEmail']
subten_admin_pw = morpheus['customOptions']['subtenAdminPw']

# creates new admin user with role of JAmultitenant (from morpheus roles)
def create_admin_user(tenant_id):
    tenant_id = new_tenant_id
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
    
create_admin_user(new_tenant_id)

# subten_group = morpheus['customOptions']['subgroupname']
# def create_group(tenant_id):
#     tenant_id = new_tenant_id


