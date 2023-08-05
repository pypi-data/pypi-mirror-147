import aiohttp
import re

class antifish:
    def __init__(self, client):
        self.client = client
    
    async def check_message(self, message):
        if not self.client:
            raise Exception("You haven't linked your client! Please do `antifish(client)` so we can get your bot's username for the User-Agent header.")

        if len(self.client.application) < 1:
            raise Exception("You haven't linked your client! Please do `antifish(client)` so we can get your bot's username for the User-Agent header.")

        if not re.search("(?:[A-z0-9](?:[A-z0-9-]{0,61}[A-z0-9])?\.)+[A-z0-9][A-z0-9-]{0,61}[A-z0-9]", message.content):
            return { "match": False }

        headers = {
            "User-Agent":f"{self.client.application} - via Antifish-py module"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://anti-fish.bitflow.dev/check") as response:

                async def is_scam():
                    res = response.json()
                    if res.match is True and res.matches[0]["trust_rating"] >= 0.95:
                        return { "match":True, "match":{ "followed":res.matches[0]["followed"], "domain":res.matches[0]["domain"], "source":res.matches[0]["source"], "type":res.matches[0]["type"], "trust_rating":res.matches[0]["trust_rating"] } }
                    else:
                        return { "match":False }

                return await response.json()
        
        