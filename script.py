import requests
import json

class Location:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Avenue:
    
    locations = list()

    def __init__(self, wkid, latestWkid):
        self.wkid = wkid
        self.latestWkid = latestWkid



url = "https://maps.cityofrochester.gov/arcgis/rest/services/App_PropertyInformation/AppPropInfo_locator_280/GeocodeServer/findAddressCandidates"
payload = "Single%20Line%20Input=RUGBY&f=json&outSR=%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D&outFields=Shape"
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "private, must-revalidate, max-age=0"
    }
response = requests.request("POST", url, data=payload, headers=headers)
file = open("resp_content.txt", "w")
file.write(response.text)
file.close()

file = open('resp_content.txt', mode = 'r', encoding = 'utf-8-sig')
# file = open("parse_content.txt", "w")
l1 = file.read().split('}')
l2 = list()
for item in l1:
    if "spatialReference" in item:

        l2.append(item)
    elif "x" in item:
        l2.append(item)

l3 = l2[0].split('{')
l4 = l3[2].split('[:,]')
l5 = l4[0].split(',')
l6 = l5[0].split(':')
l7 = l5[1].split(':')

avenue = Avenue(l6[1], l7[1])
houses = list()
for i in range(3, len(l2)):
    l8 = l2[i].split(',')
    l9 = l8[2].split(':')
    l10 = l8[3].split(':')
    location = Location(l9[2], l10[1])
    houses.append(location)
avenue.locations = houses

print("Wkid: ",avenue.wkid, "latestWkid: ", avenue.latestWkid)
for location in avenue.locations:
    print("X: ", location.x, "Y: ", location.y)

file.close()
print(type(response))