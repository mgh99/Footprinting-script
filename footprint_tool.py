import requests
from bs4 import BeautifulSoup
import dns.resolver

# Realizamos la petición HTTP a la página web
response = requests.get('https://www.bodasorganizadas.es')

# Obtenemos la información del encabezado HTTP de la respuesta
header_info = response.headers

# Mostramos la información del encabezado HTTP
print(header_info)

# Analizamos el contenido HTML de la respuesta
soup = BeautifulSoup(response.content, 'html.parser')

# Obtenemos el título de la página
title = soup.title.string
print(title)

# Obtenemos las etiquetas meta de la página
meta_tags = soup.find_all('meta')
for tag in meta_tags:
    print(tag)

# Obtenemos los enlaces externos de la página
links = soup.find_all('a')
for link in links:
    print(link.get('href'))

# Realizamos una consulta DNS para obtener el servidor de nombres de la página
answers = dns.resolver.query('bodasorganizadas.es', 'NS')

# Mostramos la información del servidor de nombres
for rdata in answers:
    print(rdata)

# Realizamos la petición a la API de Shodan
response = requests.get(
    'https://api.shodan.io/shodan/host/search',
    params={
        'query': 'hostname:bodasorganizadas.es',
        'key': 'TU_API_KEY'
    }
)

# Obtenemos la información del escaneo de puertos del resultado de la petición
scan_info = response.json()

# Mostramos la información del escaneo de puertos
for result in scan_info['matches']:
    print('Host:', result['ip_str'])
    for service in result['data']:
        print('Protocol:', service['transport'])
        print('Port:', service['port'])
        print('State:', service['state'])
        print('Product:', service['product'])
        print('Version:', service['version'])
        print('Extra info:', service['extra'])
