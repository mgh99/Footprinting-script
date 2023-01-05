# HERRAMIENTA DE FOOTPRINTING
# https://www.bodasorganizadas.es/

# 1. Nombre del dominio: bodasorganizadas.es
# 2. Dirección IP:
# 3. Registros Whois:
# 4. Correos electrónicos:
# 5. Sistema operativo del servidor:
# 6. Numeros de telefono:
# 7. Mapa de red
# 8. URLs de la web
# 9. Cortafuegos
# 10. Información de la web

import re
import socket
import urllib.parse
import requests
from bs4 import BeautifulSoup
import networkx as nx
import json

url = "http://www.bodasorganizadas.es"
url2 = "www.bodasorganizadas.es"
domain = "bodasorganizadas.es"

# 1. Nombre del dominio: bodasorganizadas.es 
def get_domain_name(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        return domain
    except:
        return "No se ha podido obtener el nombre del dominio"

print("1. Nombre del dominio: " + get_domain_name(url))

# 2. Dirección IP: 
def get_ip_address(url2):
    try:
        ip_address = socket.gethostbyname(url2)
        return ip_address
    except:
        return "No se ha podido obtener la dirección IP"

print("2. Direccion IP: " +get_ip_address(url2))

# 3. Registros Whois: # FUNCIONA
def get_whois_info (domain):
    
    api_key = 'at_QnMUAXz2MOljPmDJyhc1pbrjrQylE'
    url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={domain}&outputFormat=JSON'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = json.loads(r.text)
            return data
        else:
            return "No se ha podido obtener la información Whois"
    except:
        return "No se ha podido obtener la información Whois un error ha ocurrido"

print("3. Registros Whois: " + str(get_whois_info(domain)))

# 4. Correos electrónicos: # FUNCIONA
def get_emails(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', soup.prettify())
        return emails
    except:
        return "No se ha podido obtener los correos electrónicos"

print("4. Correos electrónicos: " + str(get_emails(url)))

# 5. Sistema operativo del servidor: # FUNCIONA
def get_os_info(url):
  try:
    r = requests.get(url)
    headers = r.headers
    server = headers['Server']
    if 'Windows' in server:
      os_info = 'Windows'
    elif 'Linux' in server:
      os_info = 'Linux'
    else:
      os_info = 'Other'
    return os_info
  except:
        return "No se ha podido obtener la información del sistema operativo"

print("5. Sistema operativo del servidor: " + get_os_info(url)) ## Sale other -> significa que no se puede determinar con certeza, 
#porque puede deberse a que el servidor no está utilizando un os conocido o que no hay la suficente información en la respuesta del servidor

# 6. Numeros de telefono: # FUNCIONA
def get_phone_numbers(url):
  try:
    r = requests.get(url)
    phone_numbers = re.findall(r'\d{3} \d{3} \d{4}', r.text)
    return phone_numbers
  except:
    return  "No se ha podido obtener los números de teléfono"

print("6. Numeros de telefono: " + str(get_phone_numbers(url)))
# Si no aparecen numeros de movil puede ser por que el servidor no los muestra en la web

# 7. Mapa de red: #FUNCIONA
def get_network_map(url):
  try:
    r = requests.get(url)
    links = re.findall(r'(?<=href=")[^"]*', r.text)
    G = nx.Graph()
    for link in links:
      G.add_edge(url, link)
    return G
  except:
    return "No se ha podido obtener el mapa de red"

print("7. Mapa de red: " + str(get_network_map(url)))

# 8. URLs de la web: # FUNCIONA
def get_urls(url):
  try:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    urls = []
    for link in soup.find_all('a'):
      href = link.get('href')
      urls.append(href)
    return urls
  except:
    return "No se ha podido obtener las URLs"

print("8. URLs de la web: " + str(get_urls(url)))

# 9. Cortafuegos: # FUNCIONA
def get_firewall(url):
  try:
    r = requests.get(url)
    headers = r.headers
    if 'Server' in headers:
        server = headers['Server']
        if 'cloudflare' in server.lower():
            firewall = 'Cloudflare'
        elif 'incapsula' in server.lower():
            firewall = 'Incapsula'
        elif 'apache' in server.lower():
            firewall = 'Apache'
        elif 'akamai' in server.lower():
            firewall = 'Akamai'
        elif 'F5 BIG-IP' in server.lower():
            firewall = 'F5 BIG-IP'
        elif 'barracuda' in server.lower():
            firewall = 'Barracuda'
        else:
            firewall = 'Other'
    else:
      firewall = 'None'
    return firewall
  except:
    return "No se ha podido obtener la información del cortafuegos"

print("9. Cortafuegos: " + get_firewall(url))

# 10. Información de la web: # FUNCIONA
def get_info(url):
  try:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('title').text
    description = soup.find('meta', attrs={'name':'description'}).get('content')
    keywords = soup.find('meta', attrs={'name':'keywords'}).get('content')
    return f'Title: {title}\nDescription: {description}\nKeywords: {keywords}'
  except:
    return "No se ha podido obtener la información de la web"

print("10. Información de la web: " + get_info(url))
