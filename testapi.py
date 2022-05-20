import requests

URL = "https://maas-printer.azure-api.net/printer-gateway/v1/orders/label/00000261"

r = requests.get(url = URL, headers={"Ocp-Apim-Subscription-Key":"2b8f2197a7da4414a96c2c03335eaaa9"})
  
# extracting data in json format
data = r.json()

print(data)

print(data['order_code'])
'''
# extracting latitude, longitude and formatted address 
# of the first matching location
latitude = data['results'][0]['geometry']['location']['lat']
longitude = data['results'][0]['geometry']['location']['lng']
formatted_address = data['results'][0]['formatted_address']
  
# printing the output
print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
      %(latitude, longitude,formatted_address))

'''