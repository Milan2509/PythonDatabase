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
    # Maak een nieuwe tabel met 3 kolommen: id, naam, prijs ondertitelID INTEGER,
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_films(
        filmID INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT NOT NULL UNIQUE,
        genre TEXT NOT NULL,
        studio TEXT NOT NULL,
        taal TEXT NOT NULL,
        lengte INTEGER NOT NULL,
        trailer TEXT NOT NULL,
        ondertitels JSON NOT NULL
        );
    """)
    print("Tabel 'tbl_films' aangemaakt.")

def voegFilmToe(titel:str, genre:str, studio:str, taal:str, lengte:str, trailer:str, ondertitels:str):
    print("Begonnen met Film ", titel, " Toevoegen")
    
    #Maakt van de booleans een bit (int)
    # if type(heeft_engels) == bool and type(heeft_nederlands) == bool and type(heeft_spaans) == bool:
    #     heeft_engels = 0 if heeft_engels == False else 0
    #     heeft_nederlands = 0 if heeft_nederlands == False else 0
    #     heeft_spaans = 0 if heeft_spaans == False else 0

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
        # cursor.execute("INSERT INTO tbl_ondertitels VALUES(NULL, ?, ?, ?)", (heeft_engels, heeft_nederlands, heeft_spaans))
        
        # ondertitel_tbl_link = cursor.lastrowid
        
        cursor.execute("INSERT INTO tbl_films VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (titel, genre, studio, taal, lengte, trailer, '[' + ondertitels +']'))
        db.commit()  # gegevens naar de database wegschrijven
        print("Film ", titel, " Succesvol Toegevoegd")
            
    # else:
    #     print('Invalide Ondertitel Input! Needs typeof(bool)')

#class

class VraagFilmDataOp():
    def vraagFilmIDsOp():
        cursor.execute("SELECT filmID FROM tbl_films")
        resultaat = cursor.fetchall()
        return resultaat

    def vraagFilmTitelOp(ID:int):
        cursor.execute("SELECT titel FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat

    def vraagFilmGenreOp(ID:int):
        cursor.execute("SELECT genre FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat

    def vraagFilmStudioOp(ID:int):
        cursor.execute("SELECT studio FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat

    def vraagFilmTaalOp(ID:int):
        cursor.execute("SELECT taal FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat

    def vraagFilmLengteOp(ID:int):
        cursor.execute("SELECT lengte FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat

    def vraagFilmTrailerOp(ID:int):
        cursor.execute("SELECT trailer FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat

    def vraagFilmOndertitelingOp(ID:int):
        cursor.execute("SELECT ondertitels FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat
    
def voegAlleFilmsToe():
    voegFilmToe("Deadpool & Wolverine", "Actie", "Disney", "Engels", "300", "youtube", '"Engels", "Spaans", "Afrikaans", "Duits"')
    voegFilmToe("Logan", "Actie", "Disney", "Engels", "300", "youtube", '"Nederlands"')
    voegFilmToe("Iron Man", "Actie", "Disney", "Engels", "300", "youtube", '"Engels", "Spaans"')
    voegFilmToe("Spiderman 3", "Actie", "Disney", "Engels", "300", "youtube", '"Spaans", "Japans')

### --------- Hoofdprogramma -----------------
maakOndertitelTabelAan()
maakHoofdTabelAan()
voegAlleFilmsToe()
