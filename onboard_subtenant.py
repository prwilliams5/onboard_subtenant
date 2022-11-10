import requests

# api key, host, and headers variables. api key pulled should be from the morpheus user running the task/worflow.
api_key = morpheus['morpheus']['apiAccessToken']
host = morpheus['morpheus']['applianceHost']
morphheaders = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {api_key}",
    }

# subtenant variables.
subten_name = morpheus['customOptions']['subtenName']
# subten_group = morpheus['customOptions']['subgroupname']
subten_domain = morpheus['customOptions']['subtenDomain']
subten_currency = morpheus['customOptions']['subtenCurrency']

# subtenant admin user variable.
# subtenant_admin = morpheus['customOptions']['subtenAdminUsername']


def createTenant():
    url = f"https://{host}/api/accounts"
    payload = {"account": {
        "role": {"id": 2},
        "name": f"{subten_name}",
        "subdomain": f"{subten_domain}",
        "currency": f"{subten_currency}"
    }}

    response = requests.post(url=url, json=payload, headers=morphheaders, verify=False) 
    data = response.json()
    tenant_id = data['account']['id']

    print(tenant_id)
    return tenant_id

createTenant()