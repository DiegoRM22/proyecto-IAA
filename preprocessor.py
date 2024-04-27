import csv
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Eliminar caracteres no imprimibles
    text = ''.join(filter(lambda x: x in string.printable, text))
    # Convertir texto a minúsculas
    text = text.lower()
    # Eliminación de URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Eliminación de etiquetas HTML
    text = re.sub(r'<.*?>', '', text)
    # Eliminación de hashtags
    text = re.sub(r'#\w+', '', text)
    # Agregar signos de puntuación adicionales
    additional_punctuation = "?!,;:–…´¸¿¡\"“”‘’«»„†‡•·¨˜¬ˆ"
    # Concatenar los signos de puntuación estándar con los adicionales
    all_punctuation = string.punctuation + additional_punctuation
    # Usar en la función re.sub()
    text = re.sub('[' + all_punctuation + ']', '', text)
    # Tokenizar el texto
    tokens = word_tokenize(text)
    # Eliminación de stopwords
    stop_words = set(stopwords.words('english'))
    # Eliminación de palabras que contienen 'html', 'http' o 'https'
    tokens = [word for word in tokens if not re.search(r'(html|http[s]?)', word)]
    # Eliminación de stopwords
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def truncate_words(tokens):
    lemmatizer = WordNetLemmatizer()
    truncated_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return truncated_tokens

def preprocess_and_truncate(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la fila de encabezado si la hay
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for row in reader:
                if len(row) >= 2:
                    text = row[1]  # Suponiendo que el texto está en la segunda columna
                    tokens = preprocess_text(text)
                    for token in tokens:
                        truncated_token = truncate_words([token])[0]
                        out_file.write(truncated_token + '\n')

# Llamar a la función para preprocesar y truncar el texto
preprocess_and_truncate("PHI_train.csv", "preprocessed_tokens.txt")
