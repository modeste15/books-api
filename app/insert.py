import csv

# Ouvrir le fichier CSV
with open('books.csv', mode='r', encoding='utf-8') as file:
    # Créer un lecteur CSV
    csv_reader = csv.reader(file)
    
    # Boucle sur chaque ligne du fichier CSV

    for index, row in enumerate(csv_reader, start=1):
        if index > 100:
            break
        print(f"Row {index}:")
        for col_index, column in enumerate(row, start=1):
            print(f"  Column {col_index}: {column}")