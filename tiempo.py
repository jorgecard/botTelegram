import requests


#url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"

url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/1"

querystring = {"api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYW5pZWxtb3Jlbm9AaWVzcmFtb25sbHVsbC5uZXQiLCJqdGkiOiJhNDBmYTc1ZC0yZTU1LTQxMjAtYWNiNy1mOWU3YjM1NDc5YjIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYzMzcwMjExOSwidXNlcklkIjoiYTQwZmE3NWQtMmU1NS00MTIwLWFjYjctZjllN2IzNTQ3OWIyIiwicm9sZSI6IiJ9.oq6YOiDrykoKMyyzDcr_A0ZcKYhOiphFZuRENqV4_T4"}

headers = {
    'cache-control': "no-cache"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
