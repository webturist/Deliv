# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import hashlib
from xml.dom import minidom
from app.recipe import XmlDictConfig
import re


class API:
    login = "AkhtyrtsevHennadiyAnatoliyovych"
    password = "VDV5$$@da34s184FL"
    UID = "06a0e5be-ab88-11e4-b90b-003048d2b473"
    url = 'http://api1c.meest-group.com/services/1C_Query.php'
    urlcalck = 'http://api1c.meest-group.com/services/1C_Document.php'
def resp_add(city):
    ###################### формируем xml  ############
    # создаем документ
    root = ET.Element("param") # рутовый элемент 
    login = ET.SubElement(root, "login") # добавляем дочерний элемент к root 
    login.text = API.login # добавляем значение элемента
    function = ET.SubElement(root, "function") # добавляем дочерний элемент к root 
    function.text = "City" # добавляем значение элемента
    where = ET.SubElement(root, "where") # добавляем дочерний элемент к root 
    where.text = "DescriptionUA = \"{}\" and RegionDescriptionUA=\"{}\"".format(city[0],city[2]) # добавляем значение элемента 
    order = ET.SubElement(root, "order")
    order.text = ""
    sign = ET.SubElement(root, "sign")
    m = hashlib.md5(API.login.encode('utf-8'))
    m.update(API.password.encode('utf-8'))
    m.update(function.text.encode('utf-8'))
    m.update(where.text.encode('utf-8'))
    m.update(order.text.encode('utf-8'))
    sign.text = m.hexdigest()
    message = ET.tostring(root) # формируем XML документ в строку message
    
    reparsed = minidom.parseString(message)
    dataXml = reparsed.toxml("utf-8").decode('utf-8')
    #print (dataXml)
    
    resp = requests.post(
        API.url,
        dataXml.encode('utf-8'),
        headers={'Content-Type': 'application/xml'},
        ) 
    #print(resp.text)
    root = ET.XML(resp.text)
    xmldict = XmlDictConfig(root) 
    print(xmldict)
    if xmldict["result_table"] == "\n" or not xmldict["result_table"]:
        return None
    else:
        return xmldict["result_table"]["items"]

def cost(d):
    city_out = resp_add(d["city_out"])
    city_in = resp_add(d["city_in"])
    try:
        city_out = city_out[0]
    except:
        city_out = city_out
    try:
        city_in = city_in[0]
    except:
        city_in = city_in    
    print(city_out)
    print(city_in)
    
    if not city_out:
        #print("З цього місця не можливо зробити відправку")
        return "З цього місця не можливо зробити відправку"
    elif not city_in:
        #print("В це місце не можливо зробити доставку")
        return "В це місце не можливо зробити доставку"
    else:
        root = ET.Element("param")
        login = ET.SubElement(root, "login") 
        login.text = API.login 
        function = ET.SubElement(root, "function")  
        function.text = "CalculateShipments"
        request = ET.SubElement(root, "request")
        CalculateShipment = ET.SubElement(request, "CalculateShipment")
        ClientUID = ET.SubElement(CalculateShipment, "ClientUID")
        ClientUID.text = API.UID
        SenderService = ET.SubElement(CalculateShipment, "SenderService")
        ReceiverService = ET.SubElement(CalculateShipment, "ReceiverService")
            
        if d["ServiceType"] == "DoorsDoors":
            SenderService.text = "1"
            SenderCity_UID = ET.SubElement(CalculateShipment, "SenderCity_UID")
            SenderCity_UID.text = city_out["uuid"]
            ReceiverService.text = "1"
            ReceiverCity_UID = ET.SubElement(CalculateShipment, "ReceiverCity_UID")
            ReceiverCity_UID.text = city_in["uuid"]
            
        elif d["ServiceType"] == "DoorsWarehouse":
            SenderService.text = "1"
            SenderСity_UID = ET.SubElement(CalculateShipment, "SenderCity_UID")
            SenderСity_UID.text = city_out["uuid"]
            ReceiverService.text = "0"
            ReceiverBranch_UID = ET.SubElement(CalculateShipment, "ReceiverBranch_UID")
            ReceiverBranch_UID.text = city_in["Branchuuid"]
                  
        elif d["ServiceType"] == "WarehouseDoors":
            SenderService.text = '0'
            SenderBranch_UID = ET.SubElement(CalculateShipment, "SenderBranch_UID")
            SenderBranch_UID.text = city_out["Branchuuid"]
            ReceiverService.text = '1'
            ReceiverCity_UID = ET.SubElement(CalculateShipment, "ReceiverCity_UID")
            ReceiverCity_UID.text = city_in["uuid"]
        else:
            SenderService.text = '0'
            SenderBranch_UID = ET.SubElement(CalculateShipment, "SenderBranch_UID")
            SenderBranch_UID.text = city_out["Branchuuid"]
            ReceiverService.text = '0'
            ReceiverBranch_UID = ET.SubElement(CalculateShipment, "ReceiverBranch_UID")
            ReceiverBranch_UID.text = city_in["Branchuuid"]
        
        if d["cargoType"]=="TiresWheels":
            
            for data in d:
                if re.search("[-]{1}[0-9]{10}[a-z]{2}$", data):
                    Places_items = ET.SubElement(CalculateShipment, "Places_items")
                    SendingFormat = ET.SubElement(Places_items, "SendingFormat")
                    Quantity = ET.SubElement(Places_items, "Quantity")
                    Volume = ET.SubElement(Places_items, "Volume")
                    Weight = ET.SubElement(Places_items, "Weight")
                    Insurance  =  ET.SubElement(Places_items, "Insurance")
                    #if data == "20f7b625-9add-11e3-b441-0050568002cf" or data == "d7c456cd-aa8b-11e3-9fa0-0050568002cf":
                        #вантажна R 22,5
                    #elif data == "20f7b628-9add-11e3-b441-0050568002cf" or data == "d7c456cc-aa8b-11e3-9fa0-0050568002cf":
                        #вантажна R 20
                    #elif data == "20f7b627-9add-11e3-b441-0050568002cf" or data == "d7c456cb-aa8b-11e3-9fa0-0050568002cf":
                        #вантажна R 19,5
                    #elif data == "20f7b626-9add-11e3-b441-0050568002cf" or data == "d7c456ca-aa8b-11e3-9fa0-0050568002cf":
                        #вантажна R 17,5
                    if data == "d7c456c5-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456cf-aa8b-11e3-9fa0-0050568002cf": 
                        SendingFormat.text = "R14"   #легкова R 13-14
                        Volume.text = "0.001"
                        Weight.text = "6"
                        Quantity.text = d[data]
                        Insurance.text = str(int(d[data])*int(d["cost"])/len(d) + 0.01)
                    elif data == "d7c456d0-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456c6-aa8b-11e3-9fa0-0050568002cf":
                        SendingFormat.text = "R3"#легкова R 15-16
                        Volume.text = "0.1"
                        Weight.text = "10"
                        Quantity.text = d[data]
                        Insurance.text = str(int(d[data])*int(d["cost"])/len(d) + 0.01)
                    elif data == "d7c456c7-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456d1-aa8b-11e3-9fa0-0050568002cf": 
                        SendingFormat.text = "R6" #легковые R18-19
                        Volume.text = "0.1"
                        Weight.text = "11"
                        Quantity.text = d[data]
                        Insurance.text = str(int(d[data])*int(d["cost"])/len(d) + 0.01)
                    elif data == "d7c456c8-aa8b-11e3-9fa0-0050568002cf" or data == "d7c456d2-aa8b-11e3-9fa0-0050568002cf": 
                        SendingFormat.text = "R7" #легковые R19,5-22      
                        Volume.text = "0.1"
                        Weight.text = "12"
                        Quantity.text = d[data]
                        Insurance.text = str(int(d[data])*int(d["cost"])/len(d) + 0.01)
        else:    
            Places_items = ET.SubElement(CalculateShipment, "Places_items")
            SendingFormat = ET.SubElement(Places_items, "SendingFormat")
            Quantity = ET.SubElement(Places_items, "Quantity")
            Volume = ET.SubElement(Places_items, "Volume")
            Weight = ET.SubElement(Places_items, "Weight")
            Insurance  =  ET.SubElement(Places_items, "Insurance")
                    
            if d["cargoType"]=="Pallet":
                try:
                    v = int(d["seats_amount"])*int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
                    w = int(d["seats_amount"])*int(d["weight"])
                except:
                    v = 0 
                if int(d["weight"]) > 200 and int(d["weight"]) <= 500:
                    SendingFormat.text = "PL5"
                elif int(d["weight"]) > 500 and int(d["weight"]) <= 750:     
                    SendingFormat.text = "PL7"
                elif int(d["weight"]) > 750 and int(d["weight"]) <= 1000:     
                    SendingFormat.text = "PL1" 
                elif  int(d["weight"]) > 1000:
                    SendingFormat.text = "NST"      
                if int(d["cost"])*int(d["seats_amount"]) < 5000*int(d["seats_amount"]):
                    Insurance.text = str(5000*int(d["seats_amount"]))
                Volume.text = str(v)
                Weight.text = str(w)
            Quantity.text = d["seats_amount"]
            
            if d["cargoType"]=="Documents":
                SendingFormat.text = "DOX"
                Weight.text = str(float(d["weight"])*int(d["seats_amount"]))
                Insurance.text = str(int(d["cost"]) + 1)
                Volume.text = "0.001" 
                
            if d["cargoType"]=="Cargo":
                try:
                    v = int(d["volumetricWidth"])*int(d["volumetricLength"])*int(d["volumetricHeight"])/1000000
                except:
                    v = 0
                if v/int(d["seats_amount"]) <= 1.44 and int(d["weight"])/int(d["seats_amount"]) <= 250:
                    SendingFormat.text = "PAX"
                    Volume.text = str(v)
                    Weight.text =  d["weight"]
                else:
                    SendingFormat.text = "NST"
                    Volume.text = str(v)
                    Weight.text = d["weight"]  
                Insurance.text = str(int(d["cost"]) + 0.01)
                
        sign = ET.SubElement(root, "sign")
        m = hashlib.md5(API.login.encode('utf-8'))
        m.update(API.password.encode('utf-8'))
        m.update(function.text.encode('utf-8'))
        m.update(ET.tostring(CalculateShipment))
        
        sign.text = m.hexdigest()
        message = ET.tostring(root) # формируем XML документ в строку message
        #print(message)
        reparsed = minidom.parseString(message)
        dataXml = reparsed.toxml("utf-8").decode('utf-8')
        print (dataXml)
        
        resp = requests.post(
            API.urlcalck,
            dataXml.encode('utf-8'),
            headers={'Content-Type': 'application/xml'},
            ) 
        
        root = ET.XML(resp.text)
        xmldict = XmlDictConfig(root) 
        print(xmldict)
        if xmldict["result_table"] == "\n":
            #print(xmldict["errors"]["name"].partition("ua:")[2].replace("]",""))
            return xmldict["errors"]["name"].partition("ua:")[2].replace("]","")
        else:
            return xmldict["result_table"]["items"]["PriceOfDelivery"]+" грн. *"
        
if __name__ == '__main__':
    cost({'city_out': ['Суми', 'Сумська', 'Сумська'], 'city_in': ['Київ', 'Київ', 'Київська'], 'ServiceType': 'DoorsDoors', 'cargoType': 'Cargo', 'weight': '10', 'volumetricLength': '100', 'volumetricWidth': '100', 'volumetricHeight': '100', 'seats_amount': '20', 'cost': '100000'}
)