# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from app.recipe import XmlDictConfig
import re

from zeep import Client


class API:
    key = "94726845460001224437"
    url = 'http://esb.intime.ua:8080/services/intime_api_3.0?wsdl'
    
    
def resp_add(city):
    session = requests.Session()
    response = session.get('https://intime.ua/ua-calc')
    if not response:
        return None
    else:
        try:
            response = session.get('https://intime.ua/get-cities/{}'.format(city[0]),timeout=(2, 2))
        except requests.exceptions.ReadTimeout:
            return "Помилка серверу ReadTimeout"
        except requests.exceptions.ConnectTimeout:
            return "Помилка серверу ConnectTimeout" 
        except requests.exceptions.ConnectionError:
            return "Помилка серверу ConnectionError"
        except requests.exceptions.HTTPError:  
            return "Помилка серверу HTTPError"    
        data = response.json()
        if not data:
            return None
        else:
            for cur in data:
                if cur["name"] == city[0] and cur["area"].partition(" область")[0] == city[2]: 
                    return cur    
                    print(cur)
 
def cost(d):
    city_out = resp_add(d["city_out"])
    city_in = resp_add(d["city_in"])
    print(city_out)
    print(city_in)
    client = Client(API.url)
    response = client.service['declaration_calculate'](api_key=API.key)
    
    
        
    """
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
   
    
    root = ET.XML(resp.text)
    xmldict = XmlDictConfig(root) 
    print(xmldict)
    """
    

if __name__ == '__main__':
    cost( {'cargoType': 'Pallet', 'volumetricWidth': '80', 'city_in': ['Суми', 'Сумська', 'Сумська'], 'weight': '500', 'cost': '4999', 'volumetricLength': '100', 'city_out': ['Одеса', 'Одеська', 'Одеська'], 'ServiceType': 'WarehouseWarehouse', 'seats_amount': '1', 'volumetricHeight': '150'})