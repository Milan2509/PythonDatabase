#    _____  ____  _        _____   ____  
#   / ____|/ __ \| |      |  __ \ / __ \ 
#  | (___ | |  | | |      | |__) | |  | |
#   \___ \| |  | | |      |  ___/| |  | |
#   ____) | |__| | |____  | |    | |__| |
#  |_____/ \___\_\______| |_|     \____/ 

# Door Milan en Luuk.

# Voor dit PO moesten we een database maken die we vervolgens met een Python GUI konden bekijken.
# We hebben Qt gebruikt voor de GUI, Qt is een module die je kunt gebruiken om een GUI te maken in een hele hoop programmeertalen.
# Met Qt kun je een programma gebruiken dat "Qt Designer" heet, met dit programma kun je gewoon een GUI tekenen en deze gelijk gebruiken in je code in de vorm van een .ui bestand.
# Qt heeft ondersteuning voor talen zoals C++, Rust en Go, maar ook voor Python.
# Om Qt in Python te kunnen gebruiken heb je PySide6 nodig. Dit is een module die een soort communicatielaag vormt tussen Python en Qt.

# Hier importeren we alle nodige dingen. 
# Sys is nodig om het scherm te kunnen openen en ook weer af te sluiten.
# SQL is het is script SQL.py zodat we de functies kunnen gebruiken die we daar hebben gemaakt.
# PySide6 is een module die we nodig hebben om Qt te gebruiken in Python.

import sys
import SQL
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QLineEdit, QListView, QTreeView, QPushButton, QTableWidget, QTextEdit, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile, QModelIndex, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont

# Dit is de lijst die we gebruiken om alle film ID's in op te slaan.
# lijst_met_films = list(SQL.VraagFilmDataOp.vraagFilmIDsOp())

# Met deze functie vragen we de titels van alle films op en voegen we deze toe aan een widget op de GUI.
def voegFilmsToeAanLijst():
    # Eerst halen we alle films op uit de database.
    # De film ID wordt opgeslalgen in de "i" variabele
    for i in list(SQL.VraagFilmDataOp.vraagFilmIDsOp()):
        film_titel = str(SQL.VraagFilmDataOp.vraagFilmTitelOp(i)).strip("[(',)]")
        # Hier kijken we of de zoektext voorkomt in de titel van de film.
        if str(zoeken.text()).lower() in film_titel.lower():
            # Hier maken we een item om aan de film lijst toe te voegen.
            film_item = QStandardItem(film_titel)
            film_item.setEditable(False)
            film_item.setData(i, Qt.UserRole)
            film_model.appendRow(film_item)

# Deze variabele houden we bij zodat we de ondertitels van een film kunnen toevoegen aan de database.
ondertitels = ""
# Deze functie wordt aangeroepen wanneer je een ondertitel toevoegt aan een film.
def voegToeAanTabel(tekst:str, tabel:QTableWidget):
    global ondertitels
    
    # Hier kijken we of de ondertitels leeg is of niet.
    if ondertitels == "":
        # Hier voegen we de ondertitels toe als de ondertitels leeg zijn.
        ondertitels = '"'+tekst+'"'
    else:
        # Hier voegen we de ondertitels toe als de ondertitels niet leeg zijn.
        ondertitels = ondertitels + ', "' + tekst + '"'
        
    # Hier voegen we de ondertitels toe aan de tabel zodat je ze kan zien.
    tabel.insertRow(tabel.rowCount())
    item = QTableWidgetItem()
    tabel.setItem(tabel.rowCount()-1, 0, item)
    item = QTableWidgetItem(tekst)
    tabel.setVerticalHeaderItem(tabel.rowCount()-1, item)

# Deze functie wordt aangeroepen wanneer je een letter in de zoekbalk intypt, hierdoor verandert de lijst met gevonden films terwijl je typt.
# Dit zorgt ervoor dat het programma dynamischer aanvoelt en beter te gebruiken is.
def zoekFilm():
    # Eerst verwijderen we alle films uit de widget om zo te voorkomen dat dezelfde film meerdere keren wordt toegevoegd.
    film_model.clear()
    # Nu roepen we de voegFilmsToeAanLijst functie aan om zo de films die overeenkomen met de zoekcriteria weer toe te voegen.
    voegFilmsToeAanLijst()

# Deze functie wordt aangeroepen wanneer je een film uit de lijst met gevonden films selecteert, wanneer deze functie wordt aangeroepen komt er aan de rechterkant van het scherm een lijst met informatie over de film.
def filmGeselecteerd(index: QModelIndex):
    # Eerst maken we de lijst aan de rechterkant leeg zodat er niet 2 dezelfde films komen te staan.
    geselecteerdefilm_model.clear()
    # Nu geven we de geselecteerde film een unieke ID zodat we de juiste data kunnen opvragen.
    ID = index.data(Qt.UserRole)

    # Nu maken we voor elk stukje informatie over de film een item zodat we deze aan de geselecteerde film kunnen toevoegen.
    film_titel = QStandardItem(str(SQL.VraagFilmDataOp.vraagFilmTitelOp(ID)).strip("[(',)]"))
    film_studio = QStandardItem("Studio: " + str(SQL.VraagFilmDataOp.vraagFilmStudioOp(ID)).strip("[(',)]"))
    film_taal = QStandardItem("Taal: " + str(SQL.VraagFilmDataOp.vraagFilmTaalOp(ID)).strip("[(',)]"))
    film_lengte = QStandardItem("Duur: " + str(SQL.VraagFilmDataOp.vraagFilmTaalOp(ID)).strip("[(',)]"))
    film_trailer = QStandardItem("Trailer: " + str(SQL.VraagFilmDataOp.vraagFilmLengteOp(ID)).strip("[(',)]"))
    film_ondertiteling = QStandardItem("Ondertiteling: " + str(SQL.VraagFilmDataOp.vraagFilmOndertitelingOp(ID)).strip("[(',)]").replace('"', ""))
    film_genre = QStandardItem("Genre: " + str(SQL.VraagFilmDataOp.vraagFilmGenreOp(ID)).strip("[(',)]"))

    # Nu veranderen we de font van elk van de items zodat de tekst kleiner is en het er beter uitziet.
    film_genre.setFont(film_detail_font)
    film_studio.setFont(film_detail_font)
    film_taal.setFont(film_detail_font)
    film_lengte.setFont(film_detail_font)
    film_trailer.setFont(film_detail_font)
    film_ondertiteling.setFont(film_detail_font)

    # Nu voegen we de film informatie aan de geselecteerde film toe.
    film_titel.setChild(0, film_genre)
    film_titel.setChild(1, film_studio)
    film_titel.setChild(2, film_taal)
    film_titel.setChild(3, film_lengte)
    film_titel.setChild(4, film_trailer)
    film_titel.setChild(5, film_ondertiteling)

    # Met setEditable(False) zorgen we ervoor dat je de titel niet kan veranderen door erop te dubbelklikken.
    film_titel.setEditable(False)
    # Nu voegen we de geselecteerde film toe aan de lijstwidget aan de rechterkant.
    geselecteerdefilm_model.appendRow(film_titel)
    # Nu klappen we de lijst ook uit zodat je de informatie ook daadwerkelijk kan zien. :)
    geselecteerde_film_lijst.expandAll()

# Hier definiëren we een variabele voor de applicatie.
app = QApplication(sys.argv)
# Hier laden we het .ui bestand.
ui_file_name = "gui_main.ui"
ui_file = QFile(ui_file_name)
ui_file.open(QFile.ReadOnly)
loader = QUiLoader()
# Hier definiëren we een scherm met het .ui bestand.
window = loader.load(ui_file)
ui_file.close()

# Variabele om het tweede scherm bij te houden
second_window = None
film_lengte_veld = None
film_ondertiteling_tabel = None

# Hier definiëren we de functie die wordt aangeroepen wanneer je een film toevoegt.
def filmDataInDBZetten(titel:str, genre:str, studio:str, taal:str, lengte:int, trailer:str, ondertitels:str):
    # Hier kijken we of de lengte van de film leeg is of niet.
    if lengte == "":
        lengte = 0
    else:
        lengte = int(lengte)
        
    # Hier kijken we of alle velden zijn ingevuld.
    if titel == "" or genre == "" or studio == "" or taal == "" or lengte == 0 or trailer == "" or ondertitels == "":
        # Hier geven we een foutmelding als niet alle velden zijn ingevuld.
        msg = QMessageBox() # hier koppelt de variabele msg aan de QMessageBox class
        msg.setIcon(QMessageBox.Critical) # hier zetten we de icoon van de messagebox
        msg.setText("Niet alle velden zijn ingevuld!") # hier zetten we de tekst van de messagebox
        msg.setInformativeText('Vul alle velden in om een film toe te voegen!') # hier zetten we de extra informatie van de messagebox
        msg.setWindowTitle("Fout melding!") # hier zetten we de titel van de messagebox
        msg.exec() # hier laten we de messagebox zien
    else:
        # Hier voegen we de film toe aan de database.
        SQL.voegFilmToe(titel, genre, studio, taal, lengte, trailer, ondertitels)
        film_model.clear()
        voegFilmsToeAanLijst()
        second_window.close()

# Hier definiëren we de functie die wordt aangeroepen wanneer je een film uit de database verwijdert.
def filmUitDBVerwijderen(ID):
    # Hier verwijderen we de film uit de database.
    SQL.verwijderFilm(ID)
    # Hier verwijderen we de film uit de lijst met films omdat er anders dubbele films in komen te staan.
    film_model.clear()
    # Hier voegen we de films weer toe aan de lijst zodat je de films kan zien.
    voegFilmsToeAanLijst()

# Hier definiëren we de functie die wordt aangeroepen wanneer je op de voeg film toe knop drukt.
def voegFilmToeAanDB():
    # Hier koppelen we de locale variable aan de globale variabelen. 
    # Dit is perse nodig omdat anders de variabelen niet in andere en deze functie correct gebruikt kunnen worden.
    global second_window
    global film_lengte_veld
    global film_ondertiteling_tabel
    
    # Hier definieren we de gui popup file en openen we deze.
    ui_file_2 = QFile("gui_popup.ui")
    ui_file_2.open(QFile.ReadOnly)

    # Hier laden we de popup gui
    loader = QUiLoader()
    second_window = loader.load(ui_file_2)
    
    # Hier sluiten we de gui popup file.
    ui_file_2.close()
    
    # Hier koppelen we de gui elementen aan de locale variabelen.
    film_titel_veld = second_window.findChild(QTextEdit, "filmTitelveld")
    film_genre_veld = second_window.findChild(QTextEdit, "filmGenreVeld")
    film_studio_veld = second_window.findChild(QTextEdit, "filmStudioVeld")
    film_taal_veld = second_window.findChild(QTextEdit, "filmTaalVeld")
    film_lengte_veld = second_window.findChild(QLineEdit, "filmLengteVeld")
    film_trailer_veld = second_window.findChild(QTextEdit, "filmTrailerVeld")
    film_ondertiteling_veld = second_window.findChild(QTextEdit, "filmOndertitelingVeld")
    
    cancelKnop = second_window.findChild(QPushButton, "cancelKnop")
    accepteerKnop = second_window.findChild(QPushButton, "accepteerKnop")
    film_ondertiteling_tabel = second_window.findChild(QTableWidget, "filmOndertitelingTabel")
    film_ondertitelingKnop = second_window.findChild(QPushButton, "voegOndertitelingToeKnop")

    # Hier zorgen we ervoor dat de lengte van de film alleen maar cijfers kan bevatten.
    film_lengte_veld.setInputMask("000;")
    
    # Hier voegen we de ondertiteling toe aan de tabel.
    film_ondertitelingKnop.clicked.connect(lambda: voegToeAanTabel(film_ondertiteling_veld.toPlainText(), film_ondertiteling_tabel))    
    # Hier zorgen we ervoor dat de knoppen werken.
    cancelKnop.clicked.connect(lambda: second_window.close())
    accepteerKnop.clicked.connect(lambda: filmDataInDBZetten(film_titel_veld.toPlainText(), film_genre_veld.toPlainText(), film_studio_veld.toPlainText(), film_taal_veld.toPlainText(), film_lengte_veld.text(), film_trailer_veld.toPlainText(), ondertitels))

    # Hier zorgen we ervoor dat het scherm ook te zien is.
    second_window.show()
    
# Hier definiëren we de font die we gaan gebruiken voor de informatie over de film.
film_detail_font = QFont(QFont.defaultFamily(QFont()), 10)

# Hier koppelen we de zoek widget van de UI aan onze Python code door het met een variabele te verbinden.
zoeken = window.findChild(QLineEdit, "zoekFilm")
# Hier doen we hetzelfde maar dan met de lijst met film resultaten.
film_lijst = window.findChild(QListView, "filmLijst")
# Hier maken we alvast een model aan voor de lijst met film resultaten.
film_model = QStandardItemModel()
# Hier definieren we de geselecteerde film lijst (de rechter blok) en koppelen we het aan het ui element
geselecteerde_film_lijst = window.findChild(QTreeView, "geselecteerdeFilmLijst")
# Hier definieren we de voeg film toe knop en koppelen we het aan het ui element
voeg_film_toe_knop = window.findChild(QPushButton, "voegFilmToeKnop")
# Hier definieren we de verwijder film knop en koppelen we het aan het ui element
verwijder_film_knop = window.findChild(QPushButton, "verwijderFilmKnop")

# Hier maken we alvast een model aan voor de film info.
geselecteerdefilm_model = QStandardItemModel()

# Hier verbinden we de zoekFilm() functie aan de zoek widget zodat hij telkens wanneer je typt de films laat zien die overeenkomen met wat je typt.
zoeken.textChanged.connect(zoekFilm) 
# Hier verbinden we de filmGeselecteerd() functie aan de film_lijst zodat we weten wanneer je op de film klikt.
film_lijst.clicked.connect(filmGeselecteerd) 
# Hier voegen we de functie toe aan de voeg .
voeg_film_toe_knop.clicked.connect(voegFilmToeAanDB)
# Hier voegen we de functie toe aan de verwijder film knop.
# we gebruiken hier lambda omdat we een argument mee willen geven aan de functie.
verwijder_film_knop.clicked.connect(lambda: filmUitDBVerwijderen(film_lijst.currentIndex().data(Qt.UserRole)[0]))
# Hier voegen we het film model aan de film_lijst toe.
film_lijst.setModel(film_model)
# Hier voegen we het geselecteerde film_model toe aan de geselecteerde film lijst.
geselecteerde_film_lijst.setModel(geselecteerdefilm_model)
# Hier voegen we de films toe aan de lijst zodat je alvast de films kan zien.
voegFilmsToeAanLijst()

# Met deze code zorgen we ervoor dat het scherm ook te zien is. 
window.show()
# Deze regel zorgt ervoor dat we de applicatie netjes kunnen sluiten.
sys.exit(app.exec())
