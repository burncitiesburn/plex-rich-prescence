from pypresence import Presence
import time 

client_id = "908912285563641888"

RPC = Presence(client_id)

RPC.connect()

RPC.update(state="Testing Rich Presence")

while True:
    time.sleep(15)