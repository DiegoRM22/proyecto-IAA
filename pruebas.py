import re

def separate_emails(file_path):
    emails = []
    number_found = False
    message_found = False
    type_found = False
    message = ""
    kind = ""
    number = ""
    with open(file_path, 'r') as file:
        # Lee todo el documento entero y mételo en un string
        data = file.read()
    
    # Cada vez que aparezca un número en data y un ;, así 1001; convertir en ;1001;
    er = re.compile(r'^(\d+);')
    data = er.sub(r';\1;', data)
    data = data.split(';')
    # Eliminar los 3 primeros elementos de la lista
    data = data[3:]

    counter = 1
    number = 0
    email = ""
    kind = ""
    for word in data:
        #esperar entrada del usuario
        # print("contador: ", counter)
        if counter == 1:
            # print("cogiendo email")
            email = word
            counter += 1
        elif counter == 2:
            # print("cogiendo tipo")
            kind = word
            # Eliminar los 2 ultimos caracteres
            # Buscar la palabra Safe o Phishing
            er = re.compile(r'Safe')
            if er.search(kind):
                kind = "Safe Email"
            else:
                kind = "Phishing Email"
            counter = 1
            # Añadir el correo a la lista de correos
            # print("Añadiendo correo")
            emails.append((number, email, kind))
            number += 1

    return emails


    
def main():
    file_path = "PHI_train.csv"
    emails = separate_emails(file_path)
    counter = 0
    for email in emails:
        counter += 1
        print(email[2])
    
    print("Total de correos: ", counter)


if __name__ == "__main__":
    main()
