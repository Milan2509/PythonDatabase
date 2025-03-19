### --------- Bibliotheken en globale variabelen ----------------
import sqlite3

with sqlite3.connect("FilmDatabase.db") as db:
    # cursor is object waarmee je data uit de database kan halen
    cursor = db.cursor()

### --------- Functie definities -----------------
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

# met deze functie kan je een film verwijderen uit de database, gebaseerd op de filmID
def verwijderFilm(ID:int):
    cursor.execute("DELETE FROM tbl_films WHERE filmID = ?", (ID,))
    db.commit()

# met deze functie kan je een film toevoegen aan de database
def voegFilmToe(titel:str, genre:str, studio:str, taal:str, lengte:str, trailer:str, ondertitels:str):
    print("Begonnen met Film ", titel, " Toevoegen")
    
    cursor.execute("SELECT titel FROM tbl_films")
    data = cursor.fetchall()

    #for loop die checkt of de titel al bestaat in de database
    db_heeft_titel = False
    for i in range(len(data)):
        if str(data[i]) == "('" + titel + "',)":
            db_heeft_titel = True
            continue #Gaat verder uit de for loop naar het volgende if statement: if(db_heeft_titel), zodat de for loop niet verder gaat met checken
    
    # if statement die checkt of de titel al bestaat in de database
    if(db_heeft_titel):
        print("Kan ", titel, " Niet Toevoegen: Bestaat Al!")   
    else:     
        cursor.execute("INSERT INTO tbl_films VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (titel, genre, studio, taal, lengte, trailer, '[' + ondertitels +']'))
        db.commit()  # gegevens naar de database wegschrijven
        print("Film ", titel, " Succesvol Toegevoegd")

# in deze class worden alle functies gemaakt die data uit de database halen
class VraagFilmDataOp():
    # vraagt alle filmID's op en returned deze
    def vraagFilmIDsOp():
        cursor.execute("SELECT filmID FROM tbl_films")
        resultaat = cursor.fetchall()
        return resultaat
    # vraagt alle titels op en returned deze
    def vraagFilmTitelOp(ID:int):
        cursor.execute("SELECT titel FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat
    # vraagt alle genres op en returned deze
    def vraagFilmGenreOp(ID:int):
        cursor.execute("SELECT genre FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat
    # vraagt alle studios op en returned deze
    def vraagFilmStudioOp(ID:int):
        cursor.execute("SELECT studio FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat
    # vraagt alle talen op en returned deze
    def vraagFilmTaalOp(ID:int):
        cursor.execute("SELECT taal FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat
    # vraagt alle lengtes op en returned deze
    def vraagFilmLengteOp(ID:int):
        cursor.execute("SELECT lengte FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat
    # vraagt alle trailers op en returned deze
    def vraagFilmTrailerOp(ID:int):
        cursor.execute("SELECT trailer FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat
    # vraagt alle ondertitelingen op en returned deze
    def vraagFilmOndertitelingOp(ID:int):
        cursor.execute("SELECT ondertitels FROM tbl_films WHERE filmID = ?", (ID))
        resultaat = cursor.fetchall()
        return resultaat

# voegt de films toe aan de database
def voegAlleFilmsToe():
    cursor.execute("SELECT COUNT(*) FROM tbl_films") # telt het aantal films in de database
    count = cursor.fetchone()[0] # zet het aantal films in de variabele count, fetchone haalt de eerste rij uit de query met de type tuple. De [0] zorgt er voor dat het eerste element uit de tuple word gehaald. Dit is nodig omdat Python bijna niks kan met tuples.
    
    # als er nog geen films in de database staan, worden de films toegevoegd
    if count == 0:    
        voegFilmToe("Deadpool & Wolverine", "Actie Comedy", "Disney", "Engels", "128", "https://www.youtube.com/watch?v=73_1biulkYk", '"Engels", "Spaans", "Duits"')
        voegFilmToe("Logan", "Actie", "Fox Studios", "Engels", "137", "https://www.youtube.com/watch?v=Div0iP65aZo", '"Nederlands"')
        voegFilmToe("Iron Man", "Actie", "Marvel Studios", "Engels", "126", "https://www.youtube.com/watch?v=X9Twk9v2g_0", '"Engels", "Spaans"')
        voegFilmToe("Spiderman 3", "Actie", "Sony Pictures Entertainment", "Engels", "148", "https://www.youtube.com/watch?v=JfVOs4VSpmA", '"Spaans", "Japans"')
    # als er al films in de database staan, wordt er een melding gegeven
    else:
        print("Voorbeeld films worden niet toegevoegd, omdat er al films in de database staan.")
### --------- Hoofdprogramma -----------------
maakHoofdTabelAan()
voegAlleFilmsToe()
