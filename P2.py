import csv
import sys
import math

# Aumentar el límite del tamaño del campo CSV
csv.field_size_limit(sys.maxsize)

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

def calculate_frequencies(emails, word):
    frequency = 0
    for email in emails:
        frequency += email[1].count(word)
    return frequency

safeCounter = 0
phishingCounter = 0

def generate_model_file(emails, corpus_type):
    output_file = f"modelo_{corpus_type}.txt"
    with open(output_file, 'w', encoding='utf-8') as out_file:
        words_count = 0
        filtered_emails = []
        for email in emails:
            if email[2] == corpus_type:
                words_count += len(email[1].split())
                filtered_emails.append(email)
                if corpus_type == "Phishing Email":
                    phishingCounter += 1
                else:
                    safeCounter += 1

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
                frequency = calculate_frequencies(filtered_emails, word)
                smoothed_prob = (frequency + 1) / (words_count + len(filtered_emails))
                smoothed_log_prob = math.log(smoothed_prob)
                out_file.write(f"Palabra: {word} Frec: {frequency} LogProb: {smoothed_log_prob}\n")

def generate_model_files(emails):
    for corpus_type in ["Phishing Email", "Safe Email"]:
        generate_model_file(emails, corpus_type)

# Llamada a la función para obtener los correos
emails = read_emails("PHI_train.csv")

# Eliminar el primer correo
emails.pop(0)

# Llamada a la función para generar los archivos modelo
# HAY QUE QUITAR EL PRIMER EMAIL -> ES LA DESCRIPCION
# generate_model_files(emails)


def probWordByModel(word, model):
    with open(model, 'r', encoding='utf-8') as file:
        next(file)
        next(file)
        for line in file:
            line = line.strip()
            if line.startswith(f"Palabra: {word}"):
                parts = line.split()
                # Retornar valor truncado a 2 decimales
                return round(float(parts[-1]), 2)
    return 0.0

def probEmailByModel(email, model):
    words = email.split()
    log_prob = 0.0  # Inicializar la probabilidad en 0.0 en forma logarítmica
    for word in words:
        log_prob_word = probWordByModel(word, model)
        # Si la palabra no está en el modelo, ignorarla
        log_prob += log_prob_word
    # Redondear la probabilidad final a 2 decimales
    return round(log_prob, 2)
    


print(probWordByModel("password", "modelo_Phishing Email.txt"))
print(probWordByModel("password", "modelo_Safe Email.txt"))

print ("numer de correos phishing: ", phishingCounter)
print ("numer de correos safe: ", safeCounter)

print(math.log(0.4088))
print(math.log(0.3106))

print(emails[4][2])
print(probEmailByModel(emails[4][1], "modelo_Phishing Email.txt") + (math.log(0.3106)))
print(probEmailByModel(emails[4][1], "modelo_Safe Email.txt") + (math.log(0.4088)))





# Ahora hay que clasificar los correos.
# Para ello, se debe calcular la probabilidad de que un correo sea phishing o seguro.
