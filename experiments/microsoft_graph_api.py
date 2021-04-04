import msal
from office365.graph_client import GraphClient
def acquire_token():
    """
    Acquire token via MSAL
    """
    authority_url = f'https://login.microsoftonline.com/b9fac4ac-dde5-4983-a2bc-ab447e7cfb6f'
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id='17910ef6-8644-48b7-8dbb-a98e16298d76',
        client_credential='mt14z3d-TsLyZe_uN2aQZ_jb1PKyMNVF~G'
    )
    token = app.acquire_token_for_client(scopes=['onedrive.readwrite', "https://graph.microsoft.com/.default"])
    return token


## CreditMate (majid@marketojo.com): https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/Overview/appId/17910ef6-8644-48b7-8dbb-a98e16298d76/isMSAApp/
client_id = '17910ef6-8644-48b7-8dbb-a98e16298d76'
client_secret = 'mt14z3d-TsLyZe_uN2aQZ_jb1PKyMNVF~G'
tenant_id = 'b9fac4ac-dde5-4983-a2bc-ab447e7cfb6f'
# ## creditmate (majid.ubc@live.com): https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/Overview/appId/17910ef6-8644-48b7-8dbb-a98e16298d76/isMSAApp/
# client_id = '1e0327a2-c117-45e0-a5d7-d87aceb563e2'
# client_secret = 'mqOeR7u6JYswffm.KQt-60UjD.C8R.El3g'
# tenant_id = '3d08ea4d-479e-42b3-9cd1-249532a218b4'

# token = acquire_token()
client = GraphClient(acquire_token)
dir(client)
client.service_root_url()
[drive for drive in client.drives]
[user for user in client.users]
[group for group in client.groups]
drives = client.drives
dir(drives)
drives.properties
drives.to_json()
drives.add_child()
client.load(drives)
[drive for drive in drives]
client.execute_query()

[user for user in client.users]
[site for site in client.sites]
dir(client.me)
client.me.to_json()