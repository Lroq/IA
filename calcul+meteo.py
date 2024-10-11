import requests
import re

API_KEY = '0fff8e1baad542fc4a4bc18d174634b6'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def obtenir_meteo(ville):
    try:
        url = f"{BASE_URL}?q={ville}&appid={API_KEY}&units=metric&lang=fr"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather = data['weather'][0]
            
            # info importantes
            temperature = main['temp']
            description = weather['description']
            humidity = main['humidity']
            wind_speed = data['wind']['speed']
            
            return (f"La météo à {ville.capitalize()} : {description.capitalize()}, "
                    f"{temperature}°C, Humidité: {humidity}%, Vent: {wind_speed} m/s.")
        else:
            return "Désolé, je n'ai pas pu obtenir la météo pour cette ville."
    
    except Exception as e:
        return "Erreur lors de la récupération de la météo."

def ia_repondre(question):
    if re.match(r'^meteo\s+\w+', question, re.IGNORECASE):
        ville = re.findall(r'^meteo\s+(\w+)', question, re.IGNORECASE)
        if ville:
            return obtenir_meteo(ville[0])
        else:
            return "Je ne connais pas cette ville."
    
    elif re.search(r'météo|temps', question, re.IGNORECASE):
        ville = re.findall(r'à\s(\w+)', question)
        if ville:
            return obtenir_meteo(ville[0])
        else:
            return "Je ne connais pas cette ville."
    
    elif re.search(r'calcule|calcul|additionne|soustrais|divise|multiplie', question, re.IGNORECASE):
        expression = re.findall(r'\d+[\+\-\*\/]\d+', question)
        if expression:
            return calculer(expression[0])
        else:
            return "Je ne comprends pas le calcul."

while True:
    question = input("Pose ta question : ")
    if question.lower() == "exit":
        break
    print(ia_repondre(question))
