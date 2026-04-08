import requests

url = "https://api.webflow.com/v2/collections/632c9383393497540313b702/items"
token = "ws-88fd54aae0908934096a1a930801b081e873d1bef3bd19e7e1ab2f298711115e"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {token}"
}

print("Fazendo a requisição para o Webflow...")
response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Resposta: {response.text}")
