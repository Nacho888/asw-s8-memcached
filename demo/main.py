from pymemcache.client.base import Client
import requests
import json

keyName = 'POKEMON_'
cacheTime = 10
client = Client(('ts.josecurioso.space', 11211))

def getFromSource(queryName):
    r = requests.get("https://pokeapi.co/api/v2/pokemon/" + queryName)
    return r.content

def getData(queryName):
    result = client.get(keyName + queryName)
    if result is None:
        print('Data not cached, caching...')
        result = getFromSource(queryName)
        client.set(keyName + queryName, result)
        client.touch(keyName + queryName, cacheTime)
    return json.loads(result)

def printData(data):
    print()
    print('Name: ', data['name'])
    print('Types: ')
    for n in data['types']:
        print('   ', n['type']['name'])
    print('Abilities:')
    for n in data['abilities']:
        print('   ', n['ability']['name'])
    print()

while True: 
    queryName = input("Pokemon name (e to exit): ")
    if(queryName == 'e'):
        exit()
    try:
        data = getData(queryName)
        printData(data)
    except:
        print("That's not a pokemon you dumbass")
