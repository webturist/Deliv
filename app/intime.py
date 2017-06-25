# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import hashlib
from xml.dom import minidom
from app.recipe import XmlDictConfig
import re
from app.reserch import Coder
from zeep import Client


class API:
    key = "94726845460001224437"
    url = 'https://ws.intime.ua/API/ws/API20/?wsdl'
    
def resp_add(city):
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
   """
    resp = requests.post(
        API.url,"""
     <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api2="http://www.reality.sh/in-time/Api20" xmlns:int="http://inr.intime.ua/in-time/integration20">
   <soapenv:Header/>
   <soapenv:Body>
      <api2:AllCatalog>
         <api2:AllCatalogRequest>
            <int:Auth>
               <int:ID>380503273621</int:ID>
               <int:KEY>94726845460001224437</int:KEY>
            </int:Auth>
         </api2:AllCatalogRequest>
      </api2:AllCatalog>
   </soapenv:Body>
</soapenv:Envelope>""",
        headers={"Accept-Encoding": "gzip,deflate",
            'Content-Type': 'application/soap+xml',
                 "SOAPAction":"http://www.reality.sh/in-time/Api20#API20:AllCatalog",
                 "Connection": "Keep-Alive"},
        ) 
    #print(resp.text)
    root = ET.XML(resp.text)
    xmldict = XmlDictConfig(root) 
    print(xmldict)
    

if __name__ == '__main__':
    resp_add(1)