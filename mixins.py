import requests
import json
from dataclasses import dataclass, asdict


class Model:
    def dict(self):
        return asdict(self)

@dataclass
class MyData(Model):
    def __init__(self, title, is_done=False) -> None:
        self.title = title
        self.is_done = is_done
        res = {'title': self.title, 'is_done': self.is_done}
        self.res = res

class Getallmixin:                                
    def get_all(self, url):
        response = requests.get(url + 'todo/all')
        if response.status_code == 200:
            return json.loads(response.text)
        return 'Server crashed' 


class Updatemixin:                                 
    def update(self, url, id_, name, status=False):
        updated = MyData(title=name, is_done=status)
        response = requests.put(url + f'todo/{id_}/update',data=json.dumps(updated.res))
        if response.status_code == 200:
            return 'Updated:)'
        elif response.status_code == 404:
            return 'ID not found!\n You can try again .'
        else:
            return 'You wrote wrong id!\nYou can try again'
        
class Createmixin:
    def create(self, url, title, status=False):                   
        created = MyData(title=title, is_done=status)
        response = requests.post(url + 'todo/create', data=json.dumps(created.res))
       
        if response.status_code == 200:
            return '1'
        elif response.status_code == 422:
            return '422'
        return 0
    
class Deletemixin:                              
    def delete(self, url, id_):
        response = requests.delete(url + f'todo/{id_}/delete')
        if response.status_code == 200:
            return 'Deleted'
        elif response.status_code == 404:
            return 'ID not found!'
        return 'Only numbers'

