import requests

ip = ""

# response = requests.get(f"http://ip-api.com/json/{ip}?fields=proxy,mobile,country,city,hosting,org,regionName")
# print(response.json())

response = requests.get(f"https://registro.br/v2/ajax/whois/?qr={ip}&recaptchaResponse=", headers={"x-xsrf-token": "D8A03071793BC75FEC61098D78FB65ACEBAAE488"})
print(response.json()["IPNetwork"]["Owner"])