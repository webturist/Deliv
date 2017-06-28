# -*- coding: utf-8 -*-

import requests
import json
import re

class API:
    api = {"apiKey": ""}
    url2 = 'https://api.sat.ua/v1.0/calc/json'
    url = "http://urm.sat.ua/openws/hs/api/v1.0/calc/json"
    regionru = {"Івано-Франківська":    "Ивано-Франковская область",
"Волинська"    :"Волынская область",
"Вінницька":    "Винницкая область",
"Дніпропетровська":    "Днепропетровская область",
"Донецька"    :"Донецкая область",
"Житомирська"    :"Житомирская область",
"Закарпатська"    :"Закарпатская область",
"Запорізька"    :"Запорожская область",
"Київська"    :"Киевская область",
"Кіровоградська":    "Кировоградская область",
"Луганська":    "Луганская область",
"Львівська"    :"Львовская область",
"Миколаївська":    "Николаевская область",
"Одеська"    :"Одесская область",
"Полтавська"    :"Полтавськая область",
"Рівненська"    :"Ровенская область",
"Сумська"    :"Сумская область",
"Тернопільська":    "Тернопольская область",
"Харківська":    "Харьковская область",
"Херсонська":    "Херсонская область",
"Хмельницька":    "Хмельницкая область",
"Черкаська"    :"Черкасская область",
"Чернівецька":    "Черновицкая область",
"Чернігівська":    "Черниговская область"}
def resp_add(city):
    response = requests.get('https://api.sat.ua/v1.0/main/json/getTowns?searchString={}'.format(city[0]))
    if response.json()["success"]:
        data = response.json()["data"]
        for cur in data:
            for i in API.regionru.values():
                if cur["region"] == i:
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
            "ID": "123",
            "townSender": city_out["ref"],
            "townRecipient":  city_in["ref"],
            "declaredCost":d["cost"]
            }
     
        if d["ServiceType"] == "DoorsDoors":
            cost.update({"departure":"true","delivery":"true"})
        if d["ServiceType"] == "DoorsWarehouse":
            cost.update({"departure":"true"})        
        if d["ServiceType"] == "WarehouseDoors":
            cost.update({"delivery":"true"})
                    
        if d["cargoType"]=="TiresWheels":
            
            for data in d:
                if re.search("[-]{1}[0-9]{10}[a-z]{2}$", data):
                    if data == "20f7b625-9add-11e3-b441-0050568002cf" or data == "d7c456cd-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"cargoType":"гКолеса22",
                                                  "seatsAmount": d[data],}) #вантажна R 22,5
                    elif data == "20f7b628-9add-11e3-b441-0050568002cf" or data == "d7c456cc-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"cargoType":"гКолеса20",
                                                  "seatsAmount": d[data],}) #вантажна R 20
                    elif data == "20f7b627-9add-11e3-b441-0050568002cf" or data == "d7c456cb-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"cargoType":"гКолеса19",
                                                  "seatsAmount": d[data],})#вантажна R 19,5
                    elif data == "20f7b626-9add-11e3-b441-0050568002cf" or data == "d7c456ca-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"cargoType":"гКолеса17",
                                                  "seatsAmount": d[data],}) #вантажна R 17,5
                    elif data == "d7c456c5-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456cf-aa8b-11e3-9fa0-0050568002cf": 
                        cost.update({"cargoType":"лКолеса10",
                                                  "seatsAmount": d[data],}) #легкова R 13-14
                    elif data == "d7c456d0-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456c6-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"cargoType":"лКолеса15",
                                                  "seatsAmount": d[data],}) #легкова R 15-16
                    elif data == "d7c456c7-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456d1-aa8b-11e3-9fa0-0050568002cf": 
                        cost.update({"cargoType":"лКолеса18",
                                                  "seatsAmount": d[data],}) #легковые R17,5-19
                    else:
                        cost.update({"cargoType":"лКолеса19",
                                                  "seatsAmount": d[data],}) #легковые R19,5-22    
            
        
                
        if d["cargoType"]=="Cargo":
            try:
                v = int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            except:
                v = 0 
            cost.update({"volumeGeneral": v,
                        "width": d["volumetricWidth"],
                        "length": d["volumetricLength"],
                        "height": d["volumetricHeight"],
                        "weight": d["weight"],
                        "seatsAmount":d["seats_amount"],
                     })   
                  
            if int(d["weight"]) <= 2:
                cost.update({
                    "cargoType":"ПосылкаS"
                })
            elif int(d["weight"]) <= 5:
                cost.update({
                    "cargoType":"ПосылкаM"
                }) 
            elif int(d["weight"]) < 10:
                cost.update({
                    "cargoType":"ПосылкаL"
                })
            else:        
                cost.update({
                        "cargoType":"Стандарт"
                    })
      
        if d["cargoType"]=="Pallet":
             
            try:
                width = int(d["volumetricWidth"])*int(d["seats_amount"])
                weight = int(d["weight"])*int(d["seats_amount"])
                v = width*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            except:
                v = 0   
            cost.update({
                    "volumeGeneral": v,
                    "width": str(width),
                    "length": d["volumetricLength"],
                    "height": d["volumetricHeight"],
                    "weight": str(weight),
                    "cargoType":"Стандарт",
                    "seatsAmount":d["seats_amount"]
                })   
        if d["cargoType"]=="Documents":
            
            cost.update({"weight": d["weight"],"cargoType":"Документы"})       
        print(cost)        
        resp = requests.post(
            API.url,
            json.dumps(cost),
            headers={'content-type': 'application/json'},
            ) 
        if resp.json()["success"]:
            data = resp.json()["data"][0]["cost"]
            print (str(data)+" грн. *")
            return str(data)+" грн. *"
            
        else:
            print("sat error")  
            
if __name__ == '__main__':
    cost({'city_out': ['Суми', 'Сумська', 'Сумська'], 'city_in': ['Полтава', 'Полтавська', 'Полтавська'], 'ServiceType': 'DoorsDoors', 'cargoType': 'TiresWheels', 'd7c456c7-aa8b-11e3-9fa0-0050568002cf': '1', 'cost': '1'}
)           