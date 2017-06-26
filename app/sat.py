# -*- coding: utf-8 -*-

import requests
import json
import re
from app.reserch import Coder
class API:
    api = {"apiKey": ""}
    url = 'http://urm.sat.ua/openws/hs/api/v1.0/calc/json'
def resp_add(city):
    response = requests.get('https://api.sat.ua/v1.0/main/json/getTowns?searchString={}'.format(city[0]))
    data = response.json()["data"][0]
    
    return data
def cost(d):
    
    cost = {
        "ID": "123",
        "townSender": resp_add(d["city_out"])["ref"],
        "townRecipient":  resp_add(d["city_in"])["ref"],
        "declaredCost":d["cost"]
        }
 
    if d["ServiceType"] == "DoorsDoors":
        cost.update({"departure":"true","delivery":"true"})
    if d["ServiceType"] == "DoorsWarehouse":
        cost.update({"departure":"true"})        
    if d["ServiceType"] == "WarehouseDoors":
        cost.update({"delivery":"true"})
                
    if d["cargoType"]=="TiresWheels":
        print("OK")
            
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
        elif int(d["weight"]) <= 10:
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
            
    resp = requests.post(
        API.url,
        json.dumps(cost),
        headers={'content-type': 'application/json'},
        ) 
    if resp.json()["success"]:
        data = resp.json()["data"][0]
        return data
    else:
        print("sat error")   