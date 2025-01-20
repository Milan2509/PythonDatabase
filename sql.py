### --------- Bibliotheken en globale variabelen ----------------
import sqlite3

with sqlite3.connect("FilmDatabase.db") as db:
    # cursor is object waarmee je data uit de database kan halen
    cursor = db.cursor()

### --------- Functie definities -----------------
def maakOndertitelTabelAan():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_ondertitels(
        ondertitelID INTEGER PRIMARY KEY AUTOINCREMENT,
        engels BIT NOT NULL,
        nederlands BIT NOT NULL,
        spaans BIT NOT NULL
    );
    """)

def maakHoofdTabelAan():
    # Maak een nieuwe tabel met 3 kolommen: id, naam, prijs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_films(
        filmID INTEGER PRIMARY KEY AUTOINCREMENT,
        ondertitelID INTEGER,
        titel TEXT NOT NULL UNIQUE,
        genre TEXT NOT NULL,
        studio TEXT NOT NULL,
        taal TEXT NOT NULL,
        lengte INTEGER NOT NULL,
        trailer TEXT NOT NULL
        );
    """)
    print("Tabel 'tbl_films' aangemaakt.")

def voegFilmToe(titel, genre, studio, taal, lengte, trailer, heeft_engels, heeft_nederlands, heeft_spaans):
    print("Begonnen met Film ", titel, " Toevoegen")
    
    cursor.execute("SELECT titel FROM tbl_films")
    data = cursor.fetchall()

    #for loop die checkt of de titel al bestaat in de database
    db_heeft_titel = False
    for i in range(len(data)):
        if str(data[i]) == "('" + titel + "',)":
            db_heeft_titel = True
            continue #Gaat verder uit de for loop naar het volgende if statement (if(db_heeft_titel))
        
    
    if(db_heeft_titel):
        print("Kan ", titel, " Niet Toevoegen: Bestaat Al!")
        
    else:
        # voegt de ondertiteling talen toe aan de database
        cursor.execute("INSERT INTO tbl_ondertitels VALUES(NULL, ?, ?, ?)", (heeft_engels, heeft_nederlands, heeft_spaans))
        
        ondertitel_tbl_link = cursor.lastrowid
        
        cursor.execute("INSERT INTO tbl_films VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (ondertitel_tbl_link, titel, genre, studio, taal, lengte, trailer))
        db.commit()  # gegevens naar de database wegschrijven
        print("Film ", titel, " Succesvol Toegevoegd")
### --------- Hoofdprogramma -----------------
maakHoofdTabelAan()
maakOndertitelTabelAan()

voegFilmToe("Deadpool & Wolverine", "Actie", "Disney", "Engels", "300", "youtube", 1, 1, 0)
voegFilmToe("Test", "Actie", "Disney", "Engels", "300", "youtube", 1, 1, 0)
voegFilmToe("Deadpool 2", "Actie", "Disney", "Engels", "300", "youtube", 1, 1, 0)
voegFilmToe("Deadpool", "Actie", "Disney", "Engels", "300", "youtube", 1, 1, 0)
voegFilmToe("Test 2", "Actie", "Disney", "Engels", "300", "youtube", 1, 1, 0)

