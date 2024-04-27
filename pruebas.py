import csv

import os
from collections import Counter
import math

# Aumentar el límite del tamaño del campo CSV
csv.field_size_limit(sys.maxsize)

def count_words(emails):
    word_count = Counter()
    for _, email_text, _ in emails:
        tokens = preprocess_text(email_text)
        word_count.update(tokens)
    return word_count

def calculate_smoothed_log_probability(word_count, total_words):
    vocab_size = len(word_count)
    smoothed_log_probs = {}
    for word, count in word_count.items():
        smoothed_prob = (count + 1) / (total_words + vocab_size)
        smoothed_log_prob = math.log(smoothed_prob)
        smoothed_log_probs[word] = smoothed_log_prob
    return smoothed_log_probs

def write_model_file(corpus_type, num_documents, total_words, smoothed_log_probs, output_dir):
    file_path = os.path.join(output_dir, f"modelo_{corpus_type}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Numero de documentos (noticias) del corpus: {num_documents}\n")
        file.write(f"Número de palabras del corpus: {total_words}\n")
        for word, count in sorted(smoothed_log_probs.items()):
            file.write(f"Palabra: {word} Frec: {word_count[word]} LogProb: {count}\n")

def generate_model_files(emails, vocabulary_file, output_dir):
    with open(vocabulary_file, 'r', encoding='utf-8') as vocab_file:
        vocabulary = [line.strip() for line in vocab_file]

    num_documents = len(emails)
    word_count = count_words(emails)
    total_words = sum(word_count.values())
    smoothed_log_probs = calculate_smoothed_log_probability(word_count, total_words)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for corpus_type in ['P', 'S']:
        write_model_file(corpus_type, num_documents, total_words, smoothed_log_probs, output_dir)

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

# Llamada a la función para obtener los correos
emails = read_emails("PHI_train.csv")

# Llamada a la función para generar los archivos modelo
generate_model_files(emails, "vocabulary.txt", "model_files")
