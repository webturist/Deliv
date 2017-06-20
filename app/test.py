import re 
from app.reserch import Code

d= {'city_out': ['Суми', 'Сумська', 'Сумська'],
     'city_in': ['Київ', 'Київ', 'Київська'],
      'ServiceType': 'DoorsDoors', 
      'cargoType':'TiresWheels', 
      '20f7b625-9add-11e3-b441-0050568002cf': '',
       '20f7b626-9add-11e3-b441-0050568002cf': '',
        '20f7b627-9add-11e3-b441-0050568002cf': '', 
        '20f7b628-9add-11e3-b441-0050568002cf': '', 
        'd7c456c5-aa8b-11e3-9fa0-0050568002cf': '', 
        'd7c456c6-aa8b-11e3-9fa0-0050568002cf': '1', 
        'd7c456c7-aa8b-11e3-9fa0-0050568002cf': '1', 
        'd7c456c8-aa8b-11e3-9fa0-0050568002cf': '', 
        'd7c456c9-aa8b-11e3-9fa0-0050568002cf': '', 
        'd7c456ca-aa8b-11e3-9fa0-0050568002cf': '', 
        'd7c456cb-aa8b-11e3-9fa0-0050568002cf': '', 
        'd7c456cc-aa8b-11e3-9fa0-0050568002cf': '',
         'd7c456cd-aa8b-11e3-9fa0-0050568002cf': '', 
         'd7c456cf-aa8b-11e3-9fa0-0050568002cf': '', 
         'd7c456d0-aa8b-11e3-9fa0-0050568002cf': '', 
         'd7c456d1-aa8b-11e3-9fa0-0050568002cf': '', 
         'd7c456d2-aa8b-11e3-9fa0-0050568002cf': '', 
         'd7c456d3-aa8b-11e3-9fa0-0050568002cf': '', 
         'cost': '120'}


if d["cargoType"]=="TiresWheels":
            k={}
            for data in d:
                if not re.search(Code.tires, data):
                    k.update({data:d[data]})
                elif d[data]:
                    k.update({data:d[data]})
            d=k
            del k   
print(d)
            