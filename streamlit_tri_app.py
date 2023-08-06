import streamlit as st
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import joblib
import os
import time

def main():
    st.set_page_config(page_title="Alerta Sísmica")
    link = 'Volver a :point_right: [Sistema de Notificación Sísmica](https://sismos-notificacion.streamlit.app/)'
    st.markdown(link, unsafe_allow_html=True)
    st.title(':blue[~ Clasificación de Terremotos en Tiempo Real :clipboard: ~]')

    st.subheader("¡ÚNETE al nuevo grupo de Telegram con alertas en tiempo real! :earth_americas: ")
    link2 = 'Grupo Telegram [Alertas Sismicas 2023](https://t.me/+af0DegBiO8E2ZTgx)'
    st.markdown(link2, unsafe_allow_html=True)

    # --- MEX --
    st.subheader('Últimos 5 Terremotos en México:')
    link = 'México - [Servicio Sismológico Nacional](http://www.ssn.unam.mx/)'
    st.markdown(link, unsafe_allow_html=True)

    # Ruta del archivo .pkl
    loaded_model = joblib.load('saved_dt_model_mx.pkl')
    url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr', class_='1days')

    # Define the output CSV file path
    output_file = 'earthquakes_mexico.csv'

    with open('earthquakes_mexico.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Magnitud', 'Fecha', 'Hora', 'Place', 'Latitud', 'Longitud', 'Profundidad'])

        for row in rows:
            magnitud = row.find('td', class_='latest-mag').text
            fecha = row.find('span', id=lambda x: x and x.startswith('date_')).text
            hora = row.find('span', id=lambda x: x and x.startswith('time_')).text
            place = row.find('span', id=lambda x: x and x.startswith('epi_')).text
            latitud = row.find('span', id=lambda x: x and x.startswith('lat_')).text
            longitud = row.find('span', id=lambda x: x and x.startswith('lon_')).text
            profundidad = row.find('td', class_='text-center', id=lambda x: x and x.startswith('prof_')).text

            writer.writerow([magnitud, fecha, hora, place, latitud, longitud, profundidad])

    filename = 'earthquakes_mexico.csv'
    data = []

    if os.path.isfile(filename):
        # Leer los datos existentes en el archivo CSV
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar la primera fila (encabezados)
            data = list(reader)
    else:
        # El archivo no existe, iniciar con una lista vacía
        data = []
    rows = soup.find_all('tr', class_='1days')

    # Define the output CSV file path
    output_file = 'earthquakes_mexico.csv'

    with open('earthquakes_mexico.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Magnitud', 'Fecha', 'Hora', 'Place', 'Latitud', 'Longitud', 'Profundidad'])

        for row in rows:
            magnitud = row.find('td', class_='latest-mag').text
            fecha = row.find('span', id=lambda x: x and x.startswith('date_')).text
            hora = row.find('span', id=lambda x: x and x.startswith('time_')).text
            place = row.find('span', id=lambda x: x and x.startswith('epi_')).text
            latitud = row.find('span', id=lambda x: x and x.startswith('lat_')).text
            longitud = row.find('span', id=lambda x: x and x.startswith('lon_')).text
            profundidad = row.find('td', class_='text-center', id=lambda x: x and x.startswith('prof_')).text

            writer.writerow([magnitud, fecha, hora, place, latitud, longitud, profundidad])

        # Verificar si el identificador único ya existe en los datos existentes
        # por ejemplo, si la fecha y hora coinciden
        if [fecha, hora] not in data:
            data.append([magnitud, fecha, hora, place, latitud, longitud, profundidad])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Magnitud', 'Fecha', 'Hora', 'Place', 'Latitud', 'Longitud', 'Profundidad'])
        writer.writerows(data)
    df = pd.read_csv('earthquakes_mexico.csv')
    df['Profundidad'] = df['Profundidad'].str.replace(' km', '').astype(float)

    # Realizando la predicción utilizando el modelo
    new_data = df
    predictions = loaded_model.predict(new_data)
    df['Earthquake_Classification'] = pd.Series(predictions)
    df = pd.concat([df['Earthquake_Classification'], df['Place'], df.drop(['Earthquake_Classification', 'Place'], axis=1)], axis=1)

    # Display the dataframe for Mexico
    with st.container():
        st.write(df.head(5))

    # -- USA --

    st.subheader('Últimos 5 Terremotos en USA:')
    link = 'USA - [United States Geological Survey](https://www.usgs.gov/)'
    st.markdown(link, unsafe_allow_html=True)

    # Load the ML model
    loaded_model_1 = joblib.load('saved_dt_model_us.pkl')

    # Function to process earthquake data and make predictions
    def process_earthquake_data():
        # URL of the earthquake feed
        url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the JSON data
        data = json.loads(response.text)

        # Access the earthquake data
        earthquakes = data['features']

        # Define the output CSV file path
        output_file = 'earthquake_data_us.csv'

        # Open the CSV file in write mode
        with open(output_file, 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Place', 'Ids', 'Magnitude', 'Tsunami', 'Time', 'Coordinates', 'Depth'])

            # Write the earthquake data
            for earthquake in earthquakes:
                properties = earthquake['properties']
                geometry = earthquake['geometry']
                place = properties['place']
                ids = properties['ids'].strip(',')
                magnitude = properties['mag']
                tsunami = properties['tsunami']
                time_string = properties['time']
                time = datetime.fromtimestamp(int(time_string) / 1000).strftime("%Y-%m-%d %H:%M")
                coordinates = geometry['coordinates'][:2]
                depth = round(geometry['coordinates'][2], 1)
                writer.writerow([place, ids, magnitude, tsunami, time, coordinates, depth])

        # Read the earthquake data from the CSV file
        df1 = pd.read_csv(output_file)

        # Make predictions using the loaded model
        predictions = loaded_model_1.predict(df1)

        # Add the predictions to the dataframe
        df1['Earthquake_Classification'] = pd.Series(predictions)
        df1 = pd.concat([df1['Earthquake_Classification'], df1['Place'], df1.drop(['Earthquake_Classification', 'Place'], axis=1)], axis=1)

        return df1

    # Process earthquake data and get the resulting dataframe
    df1 = process_earthquake_data()

    # Display the dataframe
    with st.container():
        st.write(df1.head(5))

    
    # -- JAPAN --

    st.subheader('Últimos 5 Terremotos en Japón:')
    link = 'Japan in Global - [United States Geological Survey ](https://www.usgs.gov/)'
    st.markdown(link, unsafe_allow_html=True)

    # Ruta del archivo .pkl
    loaded_model = joblib.load('saved_model_japan.pkl')

    # URL de la API para obtener sismos en Japón
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?minlatitude=20.961&maxlatitude=45.027&minlongitude=122.934&maxlongitude=153.986&minmagnitude=0.5&eventtype=earthquake&orderby=time&format=geojson'

    # Realizar la solicitud GET para obtener los datos
    response = requests.get(url)

    # Parsear los datos JSON
    data = json.loads(response.text)

    # Obtener los sismos
    earthquakes = data['features']

    # Ruta del archivo CSV de salida
    output_file = 'earthquake_japan.csv'

    # Abrir el archivo CSV en modo escritura
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        # Crear un escritor CSV
        writer = csv.writer(file)

        # Escribir la fila de encabezado
        writer.writerow(['ID', 'Location', 'Magnitude', 'Event_Time', 'Event_Type', 'Is_Tsunami', 'Longitude', 'Latitude', 'Depth'])

        # Escribir los datos de los sismos
        for earthquake in earthquakes[:15]:  # Utilizar slicing para tomar solo los primeros 15 elementos
            feature = earthquake['properties']
            event_id = feature.get('ids', '').strip(',')
            location = feature.get('place', '')
            magnitude = feature.get('mag', '')
            event_time = pd.to_datetime(feature.get('time', ''), unit='ms')
            event_type = feature.get('type', '')
            is_tsunami = feature.get('tsunami', '')
            geometry = earthquake['geometry']
            longitude = geometry['coordinates'][0]
            latitude = geometry['coordinates'][1]
            depth = geometry['coordinates'][2]
            writer.writerow([event_id, location, magnitude, event_time, event_type, is_tsunami, longitude, latitude, depth])

    # URL de la API para obtener sismos en Japón
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?minlatitude=20.961&maxlatitude=45.027&minlongitude=122.934&maxlongitude=153.986&minmagnitude=0.5&eventtype=earthquake&orderby=time&format=geojson'
    # Ruta al archivo CSV existente
    existing_file = 'earthquake_japan.csv'

    # Realizar una solicitud GET al servidor
    response = requests.get(url)

    # Analizar los nuevos datos JSON
    data = json.loads(response.text)
    earthquakes = data['features']

    # Leer los datos existentes del archivo CSV
    existing_data = []
    with open(existing_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Omitir la primera fila (encabezado)
        next(reader)
        existing_data = [row for row in reader]

    # Verificar duplicados y agregar solo los nuevos registros
    new_data = []
    for earthquake in earthquakes[:15]:  # Utilizar slicing para tomar solo los primeros 15 elementos
        feature = earthquake['properties']
        event_id = feature.get('ids', '').strip(',')
        location = feature.get('place', '')
        magnitude = feature.get('mag', '')
        event_time = pd.to_datetime(feature.get('time', ''), unit='ms')
        event_type = feature.get('type', '')
        is_tsunami = feature.get('tsunami', '')
        geometry = earthquake['geometry']
        longitude = geometry['coordinates'][0]
        latitude = geometry['coordinates'][1]
        depth = geometry['coordinates'][2]
        # Comprobar si el registro ya existe en los datos existentes
        if not any(pd.to_datetime(row[3]) == event_time and event_id == row[0] for row in existing_data):
            new_data.append([event_id, location, magnitude, event_time, event_type, is_tsunami, longitude, latitude, depth])

    # Combinar los datos existentes y los nuevos datos
    combined_data = existing_data + new_data

    # Escribir los datos combinados en un nuevo archivo CSV
    output_file = 'combined_earthquake_japan.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Location', 'Magnitude', 'Event_Ocurred', 'Type', 'Is_Tsunami', 'Longitude', 'Latitude', 'Depth'])
        writer.writerows(combined_data)

    df2 = pd.read_csv(r'combined_earthquake_japan.csv')

    # Realizando la predicción utilizando el modelo
    # Convertir la columna "Event_Ocurred" a datetime64
    df2['Event_Ocurred'] = pd.to_datetime(df2['Event_Ocurred'], errors='coerce')

    # Realizar las predicciones con el modelo cargado
    predictions = loaded_model.predict(df2)
    df2['Earthquake_Classification'] = pd.Series(predictions)
    df2 = pd.concat([df2['Earthquake_Classification'], df2['Location'], df2.drop(['Earthquake_Classification', 'Location'], axis=1)], axis=1)

    # Display the dataframe
    with st.container():
        st.write(df2.head(5))

    # ---------------------------------------------------------------------------------------------------

    # Send Telegram message if Strong classification is detected

    mensajes = []

    if 'Strong' in df['Earthquake_Classification'].values:
        for index, row in df[df['Earthquake_Classification'] == 'Strong'].iterrows():
            mensaje = f"Se detectó un sismo importante en la zona:\n"
            mensaje += f"Fecha: {row['Fecha']}\n"
            mensaje += f"Magnitud: {row['Magnitud']}\n"
            mensaje += f"Lugar: {row['Place']}\n"
            mensaje += "¡Tenga sumo cuidado y actúe prudentemente!"
            mensajes.append(mensaje)
    
    if 'Strong' in df1['Earthquake_Classification'].values:
        for index, row in df1[df1['Earthquake_Classification'] == 'Strong'].iterrows():
            mensaje = f"Se detectó un sismo importante en la zona:\n"
            mensaje += f"Fecha: {row['Time']}\n"
            mensaje += f"Magnitud: {row['Magnitude']}\n"
            mensaje += f"Lugar: {row['Place']}\n"
            mensaje += "¡Tenga sumo cuidado y actúe prudentemente!"
            mensajes.append(mensaje)

    if 'Strong' in df2['Earthquake_Classification'].values:
        for index, row in df2[df2['Earthquake_Classification'] == 'Strong'].iterrows():
            mensaje = f"Se detectó un sismo importante en la zona:\n"
            mensaje += f"Fecha: {row['Event_Ocurred']}\n"
            mensaje += f"Magnitud: {row['Magnitude']}\n"
            mensaje += f"Lugar: {row['Location']}\n"
            mensaje += "¡Tenga sumo cuidado y actúe prudentemente!"
            mensajes.append(mensaje)

    if mensajes:
        for mensaje in mensajes:
            base_url = 'https://api.telegram.org/bot6066809714:AAFx15-OwPqna2nAnlk7csgYlWVfb7Wc1Xc/sendMessage?chat_id=-917100777&text="{}"'.format(
                mensaje)
            requests.get(base_url)


if __name__ == "__main__":
    main()
