# -*- coding: utf-8 -*-
import requests
import json
import re


class API:
    api = {"apiKey": "8c4d695c530e963968190af84ded7bc8"}
    url = 'https://api.novaposhta.ua/v2.0/json/'
def resp_add(city):
    
    address = {
        "modelName": "Address",
        "calledMethod": "searchSettlements",
        "methodProperties": {
        "CityName": city[0],
        "Limit": 5
            }
        }    
    address.update(API.api)
    resp = requests.post(
        API.url,
        json.dumps(address),
        headers={'content-type': 'application/json'},
        ) 
    data = resp.json()["data"][0]["Addresses"]
    for cur in data:
        
        if cur["MainDescription"] == city[0] and cur["Area"] == city[2]: 
            
            return cur
    return None        
            
    
def cost(d):
    city_out = resp_add(d["city_out"])
    city_in = resp_add(d["city_in"])
    if not city_out:
        #print("З цього місця не можливо зробити відправку")
        return "З цього місця не можливо зробити відправку"
    elif not city_in:
        #print("В це місце не можливо зробити доставку")
        return "В це місце не можливо зробити доставку"
    else:
        cost = {
            "modelName": "InternetDocument",
            "calledMethod": "getDocumentPrice",
            "methodProperties": {
            "CitySender": city_out["DeliveryCity"],
            "CityRecipient": city_in["DeliveryCity"],
            
            "ServiceType": d["ServiceType"],
            "Cost": d["cost"],
            "CargoType": d["cargoType"],
            
            
                },
            }
        if d["cargoType"]=="TiresWheels":
            k=[]
            for data in d:
                if re.search("[-]{1}[0-9]{10}[a-z]{2}$", data):
                    k.append({"CargoDescription":data,"Amount": d[data]})           
            
            cost["methodProperties"].update({"CargoDetails": k})
            
        if d["cargoType"]=="Pallet":
            k=[]
            try:
                v = int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            except:
                v = 0    
            for i in range(int(d["seats_amount"])):
                k.append({
                    "volumetricVolume": v,
                    "volumetricWidth": d["volumetricWidth"],
                    "volumetricLength": d["volumetricLength"],
                    "volumetricHeight": d["volumetricHeight"],
                    "weight": d["weight"]
                })           
            
              
            cost["methodProperties"].update({"OptionsSeat": k})
            
        if d["cargoType"]=="Cargo":
            try:
                v = int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            except:
                v = 0   
            cost["methodProperties"].update({"OptionsSeat": [{
                    "volumetricVolume": v,
                    "volumetricWidth": d["volumetricWidth"],
                    "volumetricLength": d["volumetricLength"],
                    "volumetricHeight": d["volumetricHeight"],
                    "weight": d["weight"]
                }]})
        if d["cargoType"]=="Documents":
            
            cost["methodProperties"].update({"Weight": d["weight"]})       
                
        cost.update(API.api)
        #print(cost)
        resp = requests.post(
            API.url,
            json.dumps(cost),
            headers={'content-type': 'application/json'},
            ) 
        
        if resp.json()["success"]:
            data = resp.json()["data"][0]["Cost"]
            #print(str(data)+" грн. *")
            return str(data)+" грн. *"
            
        else:
            #print("pochta error")
            return "На сервері помилка"
             
if __name__ == '__main__':
    cost({'city_out': ['Львівські Отруби', 'Бериславський', 'Херсонська'], 'city_in': ['Волиця', 'Турійський', 'Волинська'], 'ServiceType': 'DoorsDoors', 'cargoType': 'Cargo', 'weight': '20', 'volumetricLength': '100', 'volumetricWidth': '100', 'volumetricHeight': '100', 'seats_amount': '20', 'cost': '12'}
)    