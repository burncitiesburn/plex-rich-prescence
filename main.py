from pypresence import Presence
import time 
import asyncio
from plexauth import PlexAuth
import webbrowser
from plexapi.server import PlexServer
from pprint import pprint
import os

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
global plex
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
        with open('token.txt','w') as f:
            f.write(token)
    else:
        print("No token returned.")

if os.path.isfile('token.txt'):
    with open('token.txt') as f:
        token = f.read()
    plex = PlexServer(token=token)  
else:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




print(plex.account().username)


for session in plex.sessions():
    if session.type == 'movie':
        print(session.title)
    elif session.type == 'episode':
        print(session.title)
        print(session.parentTitle)
        print(session.grandparentTitle)
    pprint(vars(session.session[0]))

while True:
    time.sleep(15)
    for session in plex.sessions():
        pprint(vars(session))
        print(session.title)
       
        info1 = session.title
        info2 = ""
        info3 = ""
        if hasattr(session,'grandparentTitle'):
            info2 = session.grandparentTitle
            info3 = session.parentTitle
        print((int(session.duration) - int(session.viewOffset)))
        print(int(time.time()))
        end = int(time.time()) + ((int(session.duration) - int(session.viewOffset))/1000)
        RPC.update(
            state=" ▶ ",
            end=end,
            details="{}\n{}\n{}".format(info1,info2,info3)
        )