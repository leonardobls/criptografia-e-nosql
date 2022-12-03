from cryptography.fernet import Fernet
from os.path import exists
import csv

if not(exists('chave.key')):
    chave = Fernet.generate_key()
    with open('chave.key', 'wb') as filekey: 
        filekey.write(chave)

with open('chave.key', 'rb') as filekey:
    chave = filekey.read()

fernet = Fernet(chave)

arquivo = csv.reader(open('firstContry.csv'), delimiter=',')

encriptado = open('encrypted.csv', 'w', newline='', encoding='utf-8')

write = csv.writer(encriptado, delimiter=',')
header = ['country', 'city', 'accentCity', 'region', 'population', 'latitude', 'longitude']
write.writerow(header)

for [country, city, accentCity, region, population, latitude, longitude] in arquivo:
    city = fernet.encrypt(city.encode())

    write.writerow([country, city, accentCity, region, population, latitude, longitude])