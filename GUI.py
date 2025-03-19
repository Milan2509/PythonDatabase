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
        filmTitel = str(SQL.VraagFilmDataOp.vraagFilmTitelOp(i)).strip("[(',)]")
        # Hier kijken we of de zoektext voorkomt in de titel van de film.
        if str(zoeken.text()).lower() in filmTitel.lower():
            # Hier maken we een item om aan de film lijst toe te voegen.
            filmItem = QStandardItem(filmTitel)
            filmItem.setEditable(False)
            filmItem.setData(i, Qt.UserRole)
            filmModel.appendRow(filmItem)

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
    filmModel.clear()
    # Nu roepen we de voegFilmsToeAanLijst functie aan om zo de films die overeenkomen met de zoekcriteria weer toe te voegen.
    voegFilmsToeAanLijst()

# Deze functie wordt aangeroepen wanneer je een film uit de lijst met gevonden films selecteert, wanneer deze functie wordt aangeroepen komt er aan de rechterkant van het scherm een lijst met informatie over de film.
def filmGeselecteerd(index: QModelIndex):
    # Eerst maken we de lijst aan de rechterkant leeg zodat er niet 2 dezelfde films komen te staan.
    geselecteerdeFilmModel.clear()
    # Nu geven we de geselecteerde film een unieke ID zodat we de juiste data kunnen opvragen.
    ID = index.data(Qt.UserRole)

    # Nu maken we voor elk stukje informatie over de film een item zodat we deze aan de geselecteerde film kunnen toevoegen.
    filmTitel = QStandardItem(str(SQL.VraagFilmDataOp.vraagFilmTitelOp(ID)).strip("[(',)]"))
    filmGenre = QStandardItem("Genre: " + str(SQL.VraagFilmDataOp.vraagFilmGenreOp(ID)).strip("[(',)]"))
    filmStudio = QStandardItem("Studio: " + str(SQL.VraagFilmDataOp.vraagFilmStudioOp(ID)).strip("[(',)]"))
    filmTaal = QStandardItem("Taal: " + str(SQL.VraagFilmDataOp.vraagFilmTaalOp(ID)).strip("[(',)]"))
    filmLengte = QStandardItem("Duur: " + str(SQL.VraagFilmDataOp.vraagFilmLengteOp(ID)).strip("[(',)]"))
    filmTrailer = QStandardItem("Trailer: " + str(SQL.VraagFilmDataOp.vraagFilmTrailerOp(ID)).strip("[(',)]"))
    filmOnderTiteling = QStandardItem("Ondertiteling: " + str(SQL.VraagFilmDataOp.vraagFilmOndertitelingOp(ID)).strip("[(',)]").replace('"', ""))

    # Nu veranderen we de font van elk van de items zodat de tekst kleiner is en het er beter uitziet.
    filmGenre.setFont(filmDetailFont)
    filmStudio.setFont(filmDetailFont)
    filmTaal.setFont(filmDetailFont)
    filmLengte.setFont(filmDetailFont)
    filmTrailer.setFont(filmDetailFont)
    filmOnderTiteling.setFont(filmDetailFont)

    # Nu voegen we de film informatie aan de geselecteerde film toe.
    filmTitel.setChild(0, filmGenre)
    filmTitel.setChild(1, filmStudio)
    filmTitel.setChild(2, filmTaal)
    filmTitel.setChild(3, filmLengte)
    filmTitel.setChild(4, filmTrailer)
    filmTitel.setChild(5, filmOnderTiteling)

    # Met setEditable(False) zorgen we ervoor dat je de titel niet kan veranderen door erop te dubbelklikken.
    filmTitel.setEditable(False)
    # Nu voegen we de geselecteerde film toe aan de lijstwidget aan de rechterkant.
    geselecteerdeFilmModel.appendRow(filmTitel)
    # Nu klappen we de lijst ook uit zodat je de informatie ook daadwerkelijk kan zien. :)
    geselecteerdeFilmLijst.expandAll()

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
filmLengteVeld = None
filmOndertitelingTabel = None

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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Niet alle velden zijn ingevuld!")
        msg.setInformativeText('Vul alle velden in om een film toe te voegen!')
        msg.setWindowTitle("Fout melding!")
        msg.exec()
    else:
        # Hier voegen we de film toe aan de database.
        SQL.voegFilmToe(titel, genre, studio, taal, lengte, trailer, ondertitels)
        filmModel.clear()
        voegFilmsToeAanLijst()
        second_window.close()

# Hier definiëren we de functie die wordt aangeroepen wanneer je een film uit de database verwijdert.
def filmUitDBVerwijderen(ID:int):
    # Hier verwijderen we de film uit de database.
    SQL.verwijderFilm(ID)
    # Hier verwijderen we de film uit de lijst met films omdat er anders dubbele films in komen te staan.
    filmModel.clear()
    # Hier voegen we de films weer toe aan de lijst zodat je de films kan zien.
    voegFilmsToeAanLijst()

# Hier definiëren we de functie die wordt aangeroepen wanneer je op de voeg film toe knop drukt.
def voegFilmToeAanDB():
    # Hier koppelen we de locale variable aan de globale variabelen.
    global second_window
    global filmLengteVeld
    global filmOndertitelingTabel
    
    # Hier definieren we de gui popup file en openen we deze.
    ui_file_2 = QFile("gui_popup.ui")
    ui_file_2.open(QFile.ReadOnly)

    # Hier laden we de popup gui
    loader = QUiLoader()
    second_window = loader.load(ui_file_2)
    
    # Hier sluiten we de gui popup file.
    ui_file_2.close()
    
    # Hier koppelen we de gui elementen aan de locale variabelen.
    filmTitelVeld = second_window.findChild(QTextEdit, "filmTitelVeld")
    filmGenreVeld = second_window.findChild(QTextEdit, "filmGenreVeld")
    filmStudioVeld = second_window.findChild(QTextEdit, "filmStudioVeld")
    filmTaalVeld = second_window.findChild(QTextEdit, "filmTaalVeld")
    filmLengteVeld = second_window.findChild(QLineEdit, "filmLengteVeld")
    filmTrailerVeld = second_window.findChild(QTextEdit, "filmTrailerVeld")
    filmOndertitelingVeld = second_window.findChild(QTextEdit, "filmOndertitelingVeld")
    
    cancelKnop = second_window.findChild(QPushButton, "cancelKnop")
    accepteerKnop = second_window.findChild(QPushButton, "accepteerKnop")
    filmOndertitelingTabel = second_window.findChild(QTableWidget, "filmOndertitelingTabel")
    filmOndertitelingKnop = second_window.findChild(QPushButton, "voegOndertitelingToeKnop")

    # Hier zorgen we ervoor dat de lengte van de film alleen maar cijfers kan bevatten.
    filmLengteVeld.setInputMask("000;")
    
    # Hier voegen we de ondertiteling toe aan de tabel.
    filmOndertitelingKnop.clicked.connect(lambda: voegToeAanTabel(filmOndertitelingVeld.toPlainText(), filmOndertitelingTabel))    
    # Hier zorgen we ervoor dat de knoppen werken.
    cancelKnop.clicked.connect(lambda: second_window.close())
    accepteerKnop.clicked.connect(lambda: filmDataInDBZetten(filmTitelVeld.toPlainText(), filmGenreVeld.toPlainText(), filmStudioVeld.toPlainText(), filmTaalVeld.toPlainText(), filmLengteVeld.text(), filmTrailerVeld.toPlainText(), ondertitels))

    # Hier zorgen we ervoor dat het scherm ook te zien is.
    second_window.show()
    
# Hier definiëren we de font die we gaan gebruiken voor de informatie over de film.
filmDetailFont = QFont(QFont.defaultFamily(QFont()), 10)

# Hier koppelen we de zoek widget van de UI aan onze Python code door het met een variabele te verbinden.
zoeken = window.findChild(QLineEdit, "zoekFilm")
# Hier doen we hetzelfde maar dan met de lijst met film resultaten.
filmLijst = window.findChild(QListView, "filmLijst")
# Hier maken we alvast een model aan voor de lijst met film resultaten.
filmModel = QStandardItemModel()
# Hier definieren we de geselecteerde film lijst (de rechter blok) en koppelen we het aan het ui element
geselecteerdeFilmLijst = window.findChild(QTreeView, "geselecteerdeFilmLijst")
# Hier definieren we de voeg film toe knop en koppelen we het aan het ui element
voegFilmToeKnop = window.findChild(QPushButton, "voegFilmToeKnop")
# Hier definieren we de verwijder film knop en koppelen we het aan het ui element
verwijder_film_knop = window.findChild(QPushButton, "verwijderFilmKnop")

# Hier maken we alvast een model aan voor de film info.
geselecteerdeFilmModel = QStandardItemModel()

# Hier verbinden we de zoekFilm() functie aan de zoek widget zodat hij telkens wanneer je typt de films laat zien die overeenkomen met wat je typt.
zoeken.textChanged.connect(zoekFilm) 
# Hier verbinden we de filmGeselecteerd() functie aan de filmlijst zodat we weten wanneer je op de film klikt.
filmLijst.clicked.connect(filmGeselecteerd) 
# Hier voegen we de functie toe aan de voeg .
voegFilmToeKnop.clicked.connect(voegFilmToeAanDB)
# Hier voegen we de functie toe aan de verwijder film knop.
verwijder_film_knop.clicked.connect(lambda: filmUitDBVerwijderen(int(filmLijst.currentIndex().data(Qt.UserRole)[0])))
# Hier voegen we het film model aan de filmlijst toe.
filmLijst.setModel(filmModel)
# Hier voegen we het geselecteerde filmmodel toe aan de geselecteerde film lijst.
geselecteerdeFilmLijst.setModel(geselecteerdeFilmModel)

# Hier voegen we de films toe aan de lijst zodat je alvast de films kan zien.
voegFilmsToeAanLijst()

# Met deze code zorgen we ervoor dat het scherm ook te zien is. 
window.show()
# Deze regel zorgt ervoor dat we de applicatie netjes kunnen sluiten.
sys.exit(app.exec())
