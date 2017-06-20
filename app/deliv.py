# -*- coding: utf-8 -*-

import requests
import json
import re
from app.reserch import Code
class API:
    api = {"apiKey": ""}
    url = 'http://www.delivery-auto.com/api/v4/Public/PostReceiptCalculate'

def resp_add(city):
    response = requests.get('http://www.delivery-auto.com/api/v4/Public/GetAreasList?culture=uk-UA&fl_all=true&country=1')
    if response.json()["status"]:
        data = response.json()["data"]
        if city[1] == "Київ":
            city[2] = city[0]
        for more in data:
            if more["IsWarehouse"] and (more["name"] == city[0] or more["name"].lower() == city[0]) and more["regionName"].split(" ")[0] == city[2]:
                data = more
            else:
                more.clear()
        try:
                       
            return data
        except:
            return None
        

def cost(d):
    if d["cost"] and (int(d["cost"]) > 0 and int(d["cost"])) <1001:
        d["cost"] = 1001
    cost = {        
         "culture": "uk-UA",
         "areasSendId": resp_add(d["city_out"])["id"],
         "areasResiveId": resp_add(d["city_in"])["id"],
         "InsuranceValue": d["cost"]
        }
   
    if d["ServiceType"] == "DoorsDoors":
        cost.update({"deliveryScheme":1})
    elif d["ServiceType"] == "DoorsWarehouse":
        cost.update({"deliveryScheme":3})        
    elif d["ServiceType"] == "WarehouseDoors":
        cost.update({"deliveryScheme":2})
    else:
        cost.update({"deliveryScheme":0})    
    
    if d["cargoType"]=="TiresWheels":
        cost.update({"category": []})
        for data in d:
            if re.search(Code.tires, data):
                if data == "20f7b625-9add-11e3-b441-0050568002cf" or data == "d7c456cd-aa8b-11e3-9fa0-0050568002cf":
                    cost["category"].append({"categoryId": "f35b5c7d-0cbc-40a0-9713-005142732fc8",
                                              "countPlace": d[data],}) #вантажна R 22,5
                elif data == "20f7b628-9add-11e3-b441-0050568002cf" or data == "d7c456cc-aa8b-11e3-9fa0-0050568002cf":
                    cost["category"].append({"categoryId": "b9cdeb6b-ea2b-48c9-94a1-ef40d426503c",
                                              "countPlace": d[data],}) #вантажна R 20
                elif data == "20f7b627-9add-11e3-b441-0050568002cf" or data == "d7c456cb-aa8b-11e3-9fa0-0050568002cf":
                    cost["category"].append({"categoryId": "87c83a1e-bb1d-4fc2-b047-8600fc60df16",
                                              "countPlace": d[data],})#вантажна R 19,5
                elif data == "20f7b626-9add-11e3-b441-0050568002cf" or data == "d7c456ca-aa8b-11e3-9fa0-0050568002cf":
                    cost["category"].append({"categoryId": "83d6f316-94a2-446f-8966-a4eb240be3ba",
                                              "countPlace": d[data],}) #вантажна R 17,5
                elif data == "d7c456c5-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456cf-aa8b-11e3-9fa0-0050568002cf": 
                    cost["category"].append({"categoryId": "ef32f833-e648-e211-ab75-00155d012d0d",
                                              "countPlace": d[data],}) #легкова R 13-14
                elif data == "d7c456d0-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456c6-aa8b-11e3-9fa0-0050568002cf":
                    cost["category"].append({"categoryId": "38475e48-e648-e211-ab75-00155d012d0d",
                                              "countPlace": d[data],}) #легкова R 15-16
                elif data == "d7c456c7-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456d1-aa8b-11e3-9fa0-0050568002cf": 
                    cost["category"].append({"categoryId": "3556f95e-e648-e211-ab75-00155d012d0d",
                                              "countPlace": d[data],}) #легковые R17,5-19
                else:
                    cost["category"].append({"categoryId": "112ead71-e648-e211-ab75-00155d012d0d",
                                              "countPlace": d[data],}) #легковые R19,5-22    
                        
        
    if d["cargoType"]=="Pallet":
        try:
            v = int(d["seats_amount"])*int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            w = int(d["seats_amount"])*int(d["weight"])
        except:
            v = 0 
        if int(d["volumetricWidth"]) <= 80 or int(d["volumetricLength"]) <= 80:
            categoryId = "07dd5789-e648-e211-ab75-00155d012d0d"
        elif int(d["volumetricWidth"]) <= 100 or int(d["volumetricLength"]) <= 100:     
            categoryId = "62c7b796-e648-e211-ab75-00155d012d0d"
        else:
            categoryId = "e9e885b1-e648-e211-ab75-00155d012d0d"    
            
        cost.update({"category": 
                    [{
             "categoryId": categoryId,
             "countPlace": d["seats_amount"],
            "helf": w,
            "size": v
             }]    
             })          
                  
    if d["cargoType"]=="Cargo":
        try:
            v = int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
            #d["weight"]=int(d["weight"])/int(d["seats_amount"])
        except:
            v = 0
        cost.update({"category": 
                    [{
             "categoryId": "00000000-0000-0000-0000-000000000000",
             "countPlace": d["seats_amount"],
            "helf": d["weight"],
            "size": v
             }]    
             })   
        
    if d["cargoType"]=="Documents":
        cost.update({"category": 
                    [{
             "categoryId": "ebe885b1-e648-e211-ab75-00155d012d0d",
             "helf": d["weight"]
             }]    
             })   
              
            
    
    print(cost)
    resp = requests.post(
        API.url,
        json.dumps(cost),
        headers={'content-type': 'application/json'},
        ) 
    if resp.json()["status"]:
        data = resp.json()["data"]
        print(data)
        return data
    else:
        return None
        print("delyvery error")      
            

    
    