### --------- Bibliotheken en globale variabelen ----------------
import sqlite3 

with sqlite3.connect("FilmDatabase.db") as db:
    # cursor is object waarmeWe je data uit de database kan halen
    cursor = db.cursor()

### --------- Functie definities -----------------
def maakHoofdTabelAan():
    # Maak een nieuwe tabel met de naam 'tbl_films' als deze nog niet bestaat
    # met de kolommen: filmID, titel, genre, studio, taal, lengte, trailer, ondertitels
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_films(
        filmID INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT NOT NULL UNIQUE,
        studio TEXT NOT NULL,
        taal TEXT NOT NULL,
        genreID INTEGER,
        lengte INTEGER NOT NULL,
        trailer TEXT NOT NULL,
        ondertitels JSON NOT NULL,
        FOREIGN KEY (genreID) REFERENCES tbl_genre_id(genreID)
        );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_genre_id(
        genreID INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT NOT NULL
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
    
    genre = genre.lower() # lowercase genre zodat de genre niet hoofdlettergevoelig is, en 2x dezelfde genre niet wordt toegevoegd

    # checkt of de titel al bestaat in de database
    db_heeft_titel = any(str(row) == f"('{titel}',)" for row in data)
    
    cursor.execute("SELECT genre FROM tbl_genre_id")

    if db_heeft_titel:
       print("Kan ", titel, " Niet Toevoegen: Bestaat Al!")   
    else:     
        # selcteer genreID van de genre die je wilt toevoegen
        cursor.execute("SELECT genreID FROM tbl_genre_id WHERE genre = ?", (genre,))
        genre_data = cursor.fetchone()
        
        # checkt of de genre id al bestaat, zo niet dan wordt deze toegevoegd
        if genre_data is None:
            cursor.execute("INSERT INTO tbl_genre_id (genre) VALUES (?)", (genre,))
            db.commit()
            cursor.execute("SELECT genreID FROM tbl_genre_id WHERE genre = ?", (genre,))
            genreID = cursor.fetchone()[0]
        else:
            genreID = genre_data[0]
        
        # Insert the film into tbl_films with the retrieved genreID
        cursor.execute("INSERT INTO tbl_films VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (titel, studio, taal, genreID, lengte, trailer, '[' + ondertitels + ']'))
        db.commit()
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
        cursor.execute("SELECT genreID FROM tbl_films WHERE filmID = ?", (ID))
        genreID = cursor.fetchone()[0]
        cursor.execute("SELECT genre FROM tbl_genre_id WHERE genreID = ?", (genreID,))
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
    count = cursor.fetchone()[0] # zet het aantal films in de variabele count
    
    # als er nog geen films in de database staan, worden de films toegevoegd
    if count == 0:    
        voegFilmToe("Deadpool & Wolverine", "Actie Comedy", "Disney", "Engels", "128", "https://www.youtube.com/watch?v=73_1biulkYk", '"Engels", "Spaans", "Duits"')
        voegFilmToe("Logan", "Actie", "Fox Studios", "Engels", "137", "https://www.youtube.com/watch?v=Div0iP65aZo", '"Nederlands"')
        voegFilmToe("Iron Man", "Actie", "Marvel Studios", "Engels", "126", "https://www.youtube.com/watch?v=X9Twk9v2g_0", '"Engels", "Spaans"')
        voegFilmToe("Spiderman 3", "Actie", "Sony Pictures Entertainment", "Engels", "148", "https://www.youtube.com/watch?v=JfVOs4VSpmA", '"Spaans", "Japans"')
    # als er al films in de database staan, wordt er een melding gegeven
    else:
        print("Voorbeeld films worden niet toegevoegd, omdat er al films in de database staan.")

# main functies
maakHoofdTabelAan()
voegAlleFilmsToe()
