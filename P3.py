import csv
import sys
import math

csv.field_size_limit(sys.maxsize)

def read_emails(file_path, max_emails=10000):
    emails = {}
    total_words = 0
    last_line = None  # Variable para almacenar la última línea
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Saltar la primera fila
        email_count = 0
        for row in reader:
            if email_count >= max_emails:
                break
            if len(row) >= 3:
                email_info = {"subject": row[0].strip(), "message": row[1].strip(), "type": row[2].strip()}
                word_count = len(row[1].strip().split())
                total_words += word_count
                emails[email_info["subject"]] = email_info
                email_count += 1
            last_line = row  # Almacenar la última línea en cada iteración
    print("Total de palabras en los primeros 10,000 correos electrónicos:", total_words)
    print("Número de correos electrónicos capturados:", len(emails))
    if last_line:
        print("Última línea del archivo CSV:", last_line)
    else:
        print("El archivo CSV está vacío o no se capturaron correos electrónicos.")
    return emails



def calculate_frequencies(emails, word):
    frequency = 0
    for email in emails.values():
        frequency += email["message"].count(word)
    return frequency

def generate_model_file(emails, corpus_type):
    phishingCounter = 0
    output_file = f"modelo_{corpus_type}.txt"
    with open(output_file, 'w', encoding='utf-8') as out_file:
        words_count = 0
        filtered_emails = {}
        for email in emails.values():
            if email["type"] == corpus_type:
                words_count += len(email["message"].split())
                filtered_emails[email["subject"]] = email
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
                word = line.strip()
                frequency = calculate_frequencies(filtered_emails, word)
                smoothed_prob = (frequency + 1) / (words_count + len(filtered_emails))
                smoothed_log_prob = math.log(smoothed_prob)
                out_file.write(f"Palabra: {word} Frec: {frequency} LogProb: {smoothed_log_prob}\n")

def generate_model_files(emails):
    for corpus_type in ["Phishing Email", "Safe Email"]:
        generate_model_file(emails, corpus_type)

emails = read_emails("PHI_train.csv")
#imprimir los numeros de correos
for number in emails.keys():
    print(number)
# test_emails
print("train", len(emails))
# print("test", len(test_emails))


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

# with open("clasificacion_alu0101464992.txt", 'a', encoding='utf-8') as out_file:
#     count = 0
#     for email_info in test_emails.values():
#         count += 1
#         print(f"Procesando email {count}")
#         phishing_prob = probEmailByModel(email_info["message"], "modelo_Phishing Email.txt")
#         safe_prob = probEmailByModel(email_info["message"], "modelo_Safe Email.txt")
#         clasification = "Phishing Email" if phishing_prob > safe_prob else "Safe Email"
#         words = email_info["message"].split()[:10]
#         text = ' '.join(words)
#         out_file.write(f"{text} {safe_prob}, {phishing_prob}, {clasification}\n")

if emails:  # Verifica si el diccionario no está vacío
    ultima_clave = list(emails.keys())[3673]  # Obtiene la última clave (asunto del correo)
    ultimo_correo = emails[ultima_clave]  # Obtiene la información del último correo
    print("Último correo:")
    print("Asunto:", ultimo_correo["subject"])
    print("Mensaje:", ultimo_correo["message"])
    print("Tipo:", ultimo_correo["type"])
else:
    print("El diccionario de correos está vacío.")


print(len(emails))

