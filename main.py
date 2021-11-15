from pypresence import Presence
import time 
import asyncio
from plexauth import PlexAuth
import webbrowser
from plexapi.server import PlexServer

PAYLOAD = {
    'X-Plex-Product': 'Test Product',
    'X-Plex-Version': '0.0.1',
    'X-Plex-Device': 'Test Device',
    'X-Plex-Platform': 'Test Platform',
    'X-Plex-Device-Name': 'Test Device Name',
    'X-Plex-Device-Vendor': 'Test Vendor',
    'X-Plex-Model': 'Test Model',
    'X-Plex-Client-Platform': 'Test Client Platform'
}

client_id = "908912285563641888"

RPC = Presence(client_id)

RPC.connect()


global tokenRequested
tokenRequested = False
global token

async def main():
    async with PlexAuth(PAYLOAD) as plexauth:
        await plexauth.initiate_auth()
        global tokenRequested
        global token
        print("Complete auth at URL: {}".format(plexauth.auth_url()))
        if tokenRequested == False:
            webbrowser.open(plexauth.auth_url())
            tokenRequested = True
        token = await plexauth.token()
    
    if token:
        print("Token: {}".format(token))
    else:
        print("No token returned.")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

plex= PlexServer(token=token)

print(plex.account().username)

for client in plex.clients():
    print(client.title)

for session in plex.sessions():
    print(session.title)
    print(session.parentTitle)
    print(session.grandparentTitle)


while True:
    time.sleep(15)
    for session in plex.sessions():
        print(session.title)
        print(session.parentTitle)
        print(session.grandparentTitle)
        RPC.update(state="{} - {} - {}".format(session.grandparentTitle,session.parentTitle,session.title))