import csv
import sys
import math
import re
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

csv.field_size_limit(sys.maxsize)

# def separate_emails(file_path):
#     emails = []
#     number_found = False
#     message_found = False
#     type_found = False
#     message = ""
#     kind = ""
#     number = ""
#     with open(file_path, 'r') as file:
#         # Lee todo el documento entero y mételo en un string
#         data = file.read()
    
#     # Cada vez que aparezca un número en data y un ;, así 1001; convertir en ;1001;
#     er = re.compile(r'^(\d+);')
#     data = er.sub(r';\1;', data)
#     data = data.split(';')
#     # Eliminar los 3 primeros elementos de la lista
#     data = data[3:]

#     counter = 1
#     number = 0
#     email = ""
#     kind = ""
#     for word in data:
#         #esperar entrada del usuario
#         # print("contador: ", counter)
#         if counter == 1:
#             # print("cogiendo email")
#             email = word
#             counter += 1
#         elif counter == 2:
#             # print("cogiendo tipo")
#             kind = word
#             # Eliminar los 2 ultimos caracteres
#             # Buscar la palabra Safe o Phishing
#             er = re.compile(r'Safe')
#             if er.search(kind):
#                 kind = "Safe Email"
#             else:
#                 kind = "Phishing Email"
#             counter = 1
#             # Añadir el correo a la lista de correos
#             # print("Añadiendo correo")
#             emails.append((number, email, kind))
#             number += 1

#     return emails

def read_emails(file_path):
    emails = []
    total_words = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if len(row) >= 3:
                email_info = (row[0].strip(), row[1].strip(), row[2].strip())
                word_count = len(row[1].strip().split())  # Contar palabras en el mensaje
                total_words += word_count
                emails.append(email_info)
    print("Total de palabras en todos los correos:", total_words)
    return emails

def addAleatoryKinf(file_path):
    # Añadir al final de cada linea ;Phishing Email
    with open(file_path, 'r') as file:
        data = file.read()
        data = data.split('\n')
        with open("PH_test_actualizado.csv", 'w') as out_file:
            for line in data:
                out_file.write(line + ";Phishing Email\n")


def calculate_frequencies(emails, word):
    frequency = 0
    for email in emails:
        frequency += email[1].count(word)
    return frequency

import math


def generate_model_file(emails, corpus_type):
    phishingCounter = 0
    output_file = f"modelo_{corpus_type}.txt"
    with open(output_file, 'w', encoding='utf-8') as out_file:
        words_count = 0
        filtered_emails = {}
        count = 0
        for email in emails:
            count += 1
            if email[2] == corpus_type:
                words_count += len(email[1].split())
                filtered_emails[email[0]] = email
                if corpus_type == "Phishing Email":
                    phishingCounter += 1

        out_file.write(f"Numero de documentos (noticias) del corpus: {len(filtered_emails)}\n")
        out_file.write(f"Número de palabras del corpus: {words_count}\n")

        input_file = "vocabulary.txt"
        with open(input_file, 'r', encoding='utf-8') as vocab_file:
            next(vocab_file)
            line_counter = 0
            for line in vocab_file:
                line_counter += 1
                print(f"Procesando palabra {line_counter}")
                word = line.strip()
                frequency = calculate_frequencies(emails, word)
                smoothed_prob = (frequency + 1) / (words_count + len(filtered_emails))
                smoothed_log_prob = math.log(smoothed_prob)
                out_file.write(f"Palabra: {word} Frec: {frequency} LogProb: {smoothed_log_prob}\n")

# Función calculate_frequencies() no proporcionada en tu código, asegúrate de incluirla


def generate_model_files(emails):
    for corpus_type in ["Phishing Email", "Safe Email"]:
        generate_model_file(emails, corpus_type)

#emails = separate_emails("PHI_train.csv")
#imprimir los numeros de correos
test_emails = read_emails("PH_test_actualizado.csv")

# addAleatoryKinf("PHtest_final.csv")

print(test_emails[-2])

# original_emails = separate_emails("PHI_train_original.csv")
# print("Originales: ", len(original_emails))


# generate_model_files(emails)

def create_model_hash(model_file):
    model_hash = {}
    with open(model_file, 'r', encoding='utf-8') as file:
        next(file)
        next(file)
        for line in file:
            line = line.strip()
            parts = line.split()
            word = parts[1]  # La palabra está en el segundo campo
            log_prob = float(parts[-1])  # El log está en el último campo
            # Sumar la probabilidad de la clase Safe o Phishing
            if model_file == "modelo_Phishing Email.txt":
                log_prob += math.log(5914 / 15000)
            else:
                log_prob += math.log(9086 / 15000)
            model_hash[word] = log_prob
    return model_hash

# Crear hash para el modelo phishing
phishing_model_hash = create_model_hash("modelo_Phishing Email.txt")

# Crear hash para el modelo safe
safe_model_hash = create_model_hash("modelo_Safe Email.txt")


def probWordByModel(word, model_hash):
    if word in model_hash:
        return round(model_hash[word], 2)
    return 0.0


def probEmailByModel(email, model):
    words = email.split()
    log_prob = 0.0
    for word in words:
        if model == "modelo_Phishing Email.txt":
            log_prob += probWordByModel(word, phishing_model_hash)
        else:
            log_prob += probWordByModel(word, safe_model_hash)
    return round(log_prob, 2)

classifications = []

with open("clasificacion_alu0101464992.txt", 'a', encoding='utf-8') as out_file:
    count = 0
    for test_email in test_emails:
        count += 1
        print(f"Procesando email {count}")
        phishing_prob = probEmailByModel(test_email[1], "modelo_Phishing Email.txt")
        safe_prob = probEmailByModel(test_email[1], "modelo_Safe Email.txt")
        clasification = "Phishing Email" if phishing_prob > safe_prob else "Safe Email"
        words = test_email[1].split()[:10]
        text = ' '.join(words)
        classifications.append(clasification)
        out_file.write(f"{text}, {safe_prob}, {phishing_prob}, {clasification}\n")

def calculate_accuracy(test_emails, classifications):
    correct = 0
    for i in range(len(test_emails)):
        # print(f"Comparando {test_emails[i][2]} con {classifications[i]}")
        if test_emails[i][2] == classifications[i]:
            correct += 1
    return correct / len(test_emails)

def print_results(classifications):
    with open("resumen_alu0101464992_control.txt", 'w', encoding='utf-8') as out_file:
        for classification in classifications:
            out_file.write(f"{classification[0]}\n")
    

accuracy = calculate_accuracy(test_emails, classifications)
print_results(classifications)
# print(f"Accuracy: {accuracy}")
# print("Percent accuracy: ", accuracy * 100, "%")



# print(len(emails)