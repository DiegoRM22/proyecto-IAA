def create_vocabulary(input_file, output_file):
    vocabulary = set()

    # Leer el archivo de vocabulario preprocesado
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()  # Eliminar espacios en blanco al principio y al final
            vocabulary.add(word)

    # Ordenar el vocabulario alfabéticamente
    sorted_vocabulary = sorted(vocabulary)

    # Escribir el vocabulario en el archivo de salida
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Numero de palabras: {}\n".format(len(sorted_vocabulary)))
        for word in sorted_vocabulary:
            file.write(word + "\n")

# Llamar a la función para crear el vocabulario
create_vocabulary("preprocessed_tokens.txt", "vocabulary.txt")