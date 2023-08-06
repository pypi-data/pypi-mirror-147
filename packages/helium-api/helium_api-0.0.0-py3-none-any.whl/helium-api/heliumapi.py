from urllib.request import Request, urlopen
import json
import requests
from time import sleep, time


class HotspotNotAvailable(Exception):
    def __init__(self, hotspot):
        super().__init__(hotspot+" is not a valid hotspot.")

def getlink(link):
    return requests.get(link, headers = {'User-agent': 'pythonhelium'})



class Name():
    def get(address):
        """The address of the hotspot with the name."""
        return getlink("https://api.helium.io/v1/hotspots/"+address).json()["data"]["name"]
    
    def transactions(name):
        """Every transaction of the hotspot with the name."""
        return Address.get_transactions(Address.get(name))

    def search(term):
        """Data of hotspots with the search term."""
        req = getlink("https://api.helium.io/v1/hotspots/name?search="+term)
        return req.json()["data"]

    def is_valid(name):
        """Returns boolean for if the name is a hotspot."""
        try:
            Name.data(name)
            return True
        except Exception:
            return False

    def data(name):
        """Data of the hotspot with the name."""
        req = getlink("https://api.helium.io/v1/hotspots/name/"+name)
        jason = req.json()
        if jason == {'data': []}:
            raise HotspotNotAvailable(name)
        datajson = jason["data"]
        data = dict(datajson[0])
        return data


    
    
class Address():
    def get(name):
        """The name of the hotspot with the given address."""
        return Name.data(name)["address"]

    def transactions(address):
        """Every transaction of the hotspot with the address."""
        req = getlink("https://api.helium.io/v1/hotspots/"+address+"/activity")
        jason = req.json()["cursor"]
        
        req2 = getlink("https://api.helium.io/v1/hotspots/"+address+"/activity?cursor="+jason)
        jason2 = req2.json()["data"]
        return jason2
    



def distance_search(lat,lon,distance):
    """Every hotspot within the radius of the distance from the point."""
    req = getlink("https://api.helium.io/v1/hotspots/location/distance?lat="+str(lat)+"&lon="+str(lon)+"&distance="+str(distance))
    return req.json()["data"]
    

