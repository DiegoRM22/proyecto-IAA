import csv
import re
import string
from itertools import islice
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker

import nltk
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Convertir texto a minúsculas
    text = text.lower()
    # Eliminación de signos de puntuación
    text = re.sub('[' + string.punctuation + ']', '', text)
    # Tokenización de palabras
    tokens = word_tokenize(text)
    # Eliminación de stopwords
    stop_words = set(stopwords.words('english'))  # Puedes cambiar 'spanish' por otro idioma si es necesario
    tokens = [word for word in tokens if word not in stop_words]
    # Eliminación de URLs y etiquetas HTML
    tokens = [word for word in tokens if not re.match(r'^https?:\/\/.*[\r\n]*', word)]
    tokens = [word for word in tokens if not re.match(r'^<.*?>', word)]
    # Corrección ortográfica
    spell = SpellChecker(language='en')
    corrected_tokens = [spell.correction(word) for word in tokens]
    return corrected_tokens

def create_vocabulary(input_file, output_file):
    vocabulary = set()

    # Leer solo las primeras 10,000 líneas del archivo CSV
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la fila de encabezado si la hay
        line_count = 0  # Inicializar contador de línea
        for row in islice(reader, 10000):
            line_count += 1  # Incrementar el contador de línea
            if len(row) >= 2:
                text = row[1]  # Suponiendo que el texto está en la segunda columna
                tokens = preprocess_text(text)
                for word in tokens:
                    if word:
                        vocabulary.add(word)
            print("Procesando línea", line_count)  # Mostrar el número de línea actual

    # Ordenar el vocabulario alfabéticamente
    sorted_vocabulary = sorted(vocabulary)

    # Escribir el vocabulario en el archivo de salida
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Numero de palabras: {}\n".format(len(sorted_vocabulary)))
        for word in sorted_vocabulary:
            file.write(word + "\n")

# Llamar a la función para crear el vocabulario
create_vocabulary("PHI_train.csv", "vocabulary.txt")
