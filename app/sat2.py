# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup


class API:
    url = "https://www.sat.ua/new/ru/services/calculate/"
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
"Полтавська"    :"Полтавская область",
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
            for i in API.regionru:
                if city[2] == i and cur["region"] == API.regionru[i]:
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
            "guidfrom": city_out["ref"],
            "guidto":  city_in["ref"],
            "cost":d["cost"]
            }
     
        if d["ServiceType"] == "DoorsDoors":
            cost.update({'sklad':"1",'doors':"1"})
        elif d["ServiceType"] == "DoorsWarehouse":
            cost.update({'sklad':"1",'doors':"0"})        
        elif d["ServiceType"] == "WarehouseDoors":
            cost.update({'sklad':"0",'doors':"1"})
        else: 
            cost.update({'sklad':"0",'doors':"0"})   
                    
        if d["cargoType"]=="TiresWheels":
            
            for data in d:
                if re.search("[-]{1}[0-9]{10}[a-z]{2}$", data):
                    if data == "20f7b625-9add-11e3-b441-0050568002cf" or data == "d7c456cd-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"tyres": d[data],"radius":"29", "type":"5"}) #вантажна R 22,5
                    elif data == "20f7b628-9add-11e3-b441-0050568002cf" or data == "d7c456cc-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"tyres": d[data],"radius":"27", "type":"5"}) #вантажна R 20
                    elif data == "20f7b627-9add-11e3-b441-0050568002cf" or data == "d7c456cb-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"tyres": d[data],"radius":"26", "type":"5"})#вантажна R 19,5
                    elif data == "20f7b626-9add-11e3-b441-0050568002cf" or data == "d7c456ca-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"tyres": d[data],"radius":"24", "type":"5"}) #вантажна R 17,5
                    elif data == "d7c456c5-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456cf-aa8b-11e3-9fa0-0050568002cf": 
                        cost.update({"tyres": d[data],"radius":"17", "type":"3"}) #легкова R 13-14
                    elif data == "d7c456d0-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456c6-aa8b-11e3-9fa0-0050568002cf":
                        cost.update({"tyres": d[data],"radius":"18", "type":"3"}) #легкова R 15-16
                    elif data == "d7c456c7-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456d1-aa8b-11e3-9fa0-0050568002cf": 
                        cost.update({"tyres": d[data],"radius":"20", "type":"3"}) #легковые R17,5-19
                    else:
                        cost.update({"tyres": d[data],"radius":"21", "type":"3"}) #легковые R19,5-22    
            
        
                
        if d["cargoType"]=="Cargo":
            try:
                v = int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            except:
                v = 0 
            cost.update({"shape": v,
                        "shw": d["volumetricWidth"],
                        "shl": d["volumetricLength"],
                        "shh": d["volumetricHeight"],
                        "weight": d["weight"]
                        
                     })   
                  
            if int(d["weight"]) < 10:
                cost.update({
                    "type":"4"
                })
            else:        
                cost.update({
                        "type":"2"
                    })
      
        if d["cargoType"]=="Pallet":
             
            try:
                width = int(d["volumetricWidth"])*int(d["seats_amount"])
                weight = int(d["weight"])*int(d["seats_amount"])
                v = width*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            except:
                v = 0   
            cost.update({
                    "shape": v,
                    "shw": str(width),
                    "shl": d["volumetricLength"],
                    "shh": d["volumetricHeight"],
                    "weight": str(weight),
                    "type":"2"
                                    })   
        if d["cargoType"]=="Documents":
            
            cost.update({"weight": d["weight"],"type":"1"}) 
            
                 
        print(cost)
        
        headers = {    
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }     
        querystring = {"do":"calculate"}  
        response = requests.request("POST", API.url, data=cost, headers=headers, params=querystring)
        if response:
            soup = BeautifulSoup(response.text, "lxml")
            try:
                cost = re.findall('\d+', soup.find('h3', {'class': 'subHead'}).text)[0]
                if cost:                
                    print (str(cost)+" грн. *")
                    return str(cost)+" грн. *"
            except:
                raise("sat error")     
        else:
            raise("sat error") 
             
            
if __name__ == '__main__':
    cost({'city_out': ['Суми', 'Сумська', 'Сумська'], 'city_in': ['Львів', 'Львівська', 'Львівська'], 'ServiceType': 'DoorsDoors', 'cargoType': 'Cargo', 'weight': '20', 'volumetricLength': '100', 'volumetricWidth': '100', 'volumetricHeight': '100', 'seats_amount': '20', 'cost': '12'}
)           