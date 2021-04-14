import requests
import json
import re

class Location:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Avenue:
    
    locations = list()

    def __init__(self, wkid, latestWkid):
        self.wkid = wkid
        self.latestWkid = latestWkid

class House:

    def __init__(self, houseId, pstladdress, pstlcity, ownername, proptype, currvalue, saledate, saleprice, classdscrp,stories,beds,baths):
        self.houseId = houseId
        self.pstladdress = pstladdress
        self.pstlcity = pstlcity
        self.ownername = ownername
        self.proptype = proptype
        self.currvalue = currvalue
        self.saledate = saleprice
        self.classdscrp = classdscrp
        self.stories = stories
        self.beds = beds
        self.baths = baths
    


def main():
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
    # for location in avenue.locations:
    #     print("X: ", location.x, "Y: ", location.y) 
    #Loop through all houses
    filename = 'Rugby'+ '.csv'
    f = open(filename,'w')
    f.write('PSTLADDRESS,PSTLCITY,OWNERNME1,PROPERTYTYPE,CURRENT_TOTAL_VALUE,SALE_DATE,SALE_PRICE,CLASSDSCRP\n')
    for location in avenue.locations:

        url = "https://maps.cityofrochester.gov/arcgis/rest/services/App_PropertyInformation/ROC_Parcel_Query_RPS/MapServer/0/query"
        payload = "f=json&where=&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometry=%7B%22x%22%3A%22"+str(location.x)+"%22%2C%22y%22%3A%22"+str(location.y)+"%22%2C%22spatialReference%22%3A%7B%22wkid%22%3A"+str(avenue.wkid)+"%2C%22latestWkid%22%3A"+str(avenue.latestWkid)+"%7D%7D&geometryType=esriGeometryPoint&inSR="+str(avenue.wkid)+"&outFields=PARCELID&outSR="+str(avenue.wkid)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "private, must-revalidate, max-age=0"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        file = open("query_first.txt", "w")
        file.write(response.text)
        file.close()

        file = open('query_first.txt', mode = 'r', encoding = 'utf-8-sig')
        l1 = file.read().split('{')
        l2 = l1[len(l1)-1].split(',')
        l3 = l2[0].split(':')
        l4 = l3[1].split('}')
        houseId = l4[0]
        # print(houseId)
        
        # url = "https://maps.cityofrochester.gov/arcgis/rest/services/App_PropertyInformation/ROC_Parcel_Query_RPS/MapServer/0/query"
        # payload = "f=json&where=PARCELID%20%3D%20%27"+str(houseId)+"%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&outSR="+ str(avenue.wkid)
        # headers = {
        #     'Content-Type': "application/x-www-form-urlencoded",
        #     'cache-control': "private, must-revalidate, max-age=0"
        #     }
        url = "https://maps.cityofrochester.gov/arcgis/rest/services/App_PropertyInformation/ROC_Parcel_Query_RPS/MapServer/0/query"
        payload = "f=json&where=&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometry=%7B%22x%22%3A%22"+str(location.x)+"%22%2C%22y%22%3A%22"+str(location.y)+"%22%2C%22spatialReference%22%3A%7B%22wkid%22%3A"+str(avenue.wkid)+"%2C%22latestWkid%22%3A"+str(avenue.latestWkid)+"%7D%7D&geometryType=esriGeometryPoint&inSR="+str(avenue.wkid)+"&outFields=PSTLADDRESS,PSTLCITY,OWNERNME1,PROPERTYTYPE,CURRENT_TOTAL_VALUE,SALE_DATE,SALE_PRICE,CLASSDSCRP&outSR="+str(avenue.wkid)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "private, must-revalidate, max-age=0"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        file = open("query_second.txt", "w")
        file.write(response.text)
        file.close()

        file = open('query_second.txt', mode = 'r', encoding = 'utf-8-sig')
        l1 = file.read().split('[')
        # print(l1[len(l1)-1])
        l2 = l1[len(l1)-1].split('{')
        l3 = l2[2].split(',')
        # print(l3)
        l4 = l3[0].split(':')
        pstladdress = l4[1]
        l5 = l3[1].split(':')
        pstlcity = l5[1] + l3[2]
        l6 = l3[3].split(':')
        ownername = l6[1]
        l7 = l3[4].split(':')
        proptype = l7[1]
        l8 = l3[5].split(':')
        currvalue = l8[1]
        l9 = l3[6].split(':')
        saledate = l9[1]
        l10 = l3[7].split(':')
        saleprice = l10[1]
        l11 = l3[8].split(':')
        l12 = l11[1].split('}')
        classdscrp = l12[0]

        f.write(str(pstladdress)+','+str(pstlcity)+','+str(ownername)+','+str(proptype)+','+str(currvalue)+','+str(saledate)+','+str(saleprice)+','+str(classdscrp)+ '\n')

    f.close()

    file.close()
    print(type(response))

main()