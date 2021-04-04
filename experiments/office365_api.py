# O365 library
from O365 import Account
client_id = '1e0327a2-c117-45e0-a5d7-d87aceb563e2'
client_secret = 'mqOeR7u6JYswffm.KQt-60UjD.C8R.El3g'
credentials = (client_id, client_secret)
account = Account(credentials, scopes=['basic'])
if not account.is_authenticated:
    account.authenticate(redirect_uri='https://127.0.0.1:5500/auth/redirect')
