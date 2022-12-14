import requests

endpoint = "http://127.0.0.1:8000/api/products/25/update" 

data = {
    "title":"Hello World",
    "price":70.70
}

get_response = requests.put(endpoint, json = data) 
print(get_response.json())