#    _____  ____  _        _____   ____  
#   / ____|/ __ \| |      |  __ \ / __ \ 
#  | (___ | |  | | |      | |__) | |  | |
#   \___ \| |  | | |      |  ___/| |  | |
#   ____) | |__| | |____  | |    | |__| |
#  |_____/ \___\_\______| |_|     \____/ 

# Door Milan en Luuk.

# Voor dit PO moesten we een database maken die we vervolgens met en Python GUI konden bekijken.
# We hebben Qt gebruikt voor de GUI, Qt is een module die je kunt gebruiken om een GUI te maken in een hele hoop programeertalen.
# Met Qt kun je een programma gebruiken dat "Qt Designer" heet, met dit programma kun je gewoon een GUI teken en deze gelijk gebruiken in je code in de form van een .ui bestand.
# Qt heeft ondersteuning voor talen zoals C++, Rust en Go, maar ook voor Python.
# Qm Qt in python te kunnen gebruiken heb je PySide6 nodig. Dit is een module die een soort communicatielaag vormt tussen Python en Qt.

# hier importeren we alle nodige dingen. 
# Sys is nogidg om het scherm te kunne openen en ook weer af te sluiten.
# SQL is nodig om met de database te kunnen werken.
# PySide6 is een module die we nodig hebben om Qt te gebruiken in python.

import sys
import SQL
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QLineEdit, QListView, QTreeView
from PySide6.QtCore import QFile, QModelIndex, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont

# Dit is de lijst die we gebruiken om alle film ID's in op te slaan.
lijst_met_films = list(SQL.VraagFilmDataOp.vraagFilmIDsOp())

# Met deze functie vragen we de titels van alle films op. En voegen we deze toe aan een widget op de GUI.
def voegFilmsToeAanLijst():
    for i in (lijst_met_films):
        filmTitel = str(SQL.VraagFilmDataOp.vraagFilmTitelOp(i)).strip("[(',)]")
        if str(zoeken.text()).lower() in filmTitel.lower():
            filmItem = QStandardItem(filmTitel)
            filmItem.setEditable(False)
            filmItem.setData(i, Qt.UserRole)
            filmModel.appendRow(filmItem)

# Deze functie wordt aangeroepen waneer je een letter in de zoekbalk in typt, hierdoor veranderd de lijst met gevonden films terwijl je typt.
# Dit zorgt ervoor dat het programma dynamischer aanvoelt en beter te gebruiken is.
def zoekFilm():
    # Eerst verwijderen we alle films uit de widget om zo te voorkomen dat de zelfde film meerdere keren wordt toegevoegd.
    filmModel.clear()
    # Nu roepen we de voegFilmsToeAanLijst functie aan om zo de films die overeenkomen met de zoekcriteria weer toe te voegen.
    voegFilmsToeAanLijst()

# Deze functie wordt aangeroepen waneer je een film uit de lijst met gevonden films selecteerd, waneer deze functie wordt aangeroepen komt er aan de rechter van het scherm een lijst met informatie over de film.
def filmGeselecteerd(index:QModelIndex):
    # Eerst maken we de lijst aan de rechtekant leeg zodat er niet 2 dezelfde films komen te staan.
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

    # Nu veranderen we de font van elk van de items zodat de text kleiner is zodat het er beter uitziet.
    filmGenre.setFont(filmDetailFont)
    filmStudio.setFont(filmDetailFont)
    filmTaal.setFont(filmDetailFont)
    filmLengte.setFont(filmDetailFont)
    filmTrailer.setFont(filmDetailFont)

    # Nu voegen we de film informatie aan de geselecteerde film toe.
    filmTitel.setChild(0, filmGenre)
    filmTitel.setChild(1, filmStudio)
    filmTitel.setChild(2, filmTaal)
    filmTitel.setChild(3, filmLengte)
    filmTitel.setChild(4, filmTrailer)

    # Met setEditable(False) zorgen we ervoor dat je de titel niet kan veranderen door erop te dubbelklikken.
    filmTitel.setEditable(False)
    # Nu voegen we de geselecteerde film toe aan de lijstwidget aan de rechterkant.
    geselecteerdeFilmModel.appendRow(filmTitel)
    # Nu klappen we de lijst ook uit zodat je de informatie ook daadwerkelijk kan zien. :)
    geselecteerdeFilmLijst.expandAll()

# Hier defenieeren we een variabele voor de applicatie.
app = QApplication(sys.argv)
# Hier laden we het .ui bestand.
ui_file_name = "gui.ui"
ui_file = QFile(ui_file_name)
loader = QUiLoader()
# Hier defenieeren we een scherm met de .ui bestand.
window = loader.load(ui_file)

# Hier defenieeren we de font die we gaan gebruiken voor de informatie over de film.
filmDetailFont = QFont(QFont.defaultFamily(QFont()), 10)

# Hier koppelen we de zoek widget van de UI aan onze python code door het met een variabele te verbinden.
zoeken = window.findChild(QLineEdit, "zoekFilm")
# Hier doen we hetzelfde maar dan met de lijst met film resultaten.
filmLijst = window.findChild(QListView, "filmLijst")
# Hier maken we alvast een model aan voor de lijst met film resultaten
filmModel = QStandardItemModel()
# Hier koppelen we de lijst voor de geselecteerde film info.
geselecteerdeFilmLijst = window.findChild(QTreeView, "geselecteerdeFilmLijst")
# Hier maken we alvast een model aan voor de film info
geselecteerdeFilmModel = QStandardItemModel()

# Hier verbinden we de zoekFilm() functie aan de zoek widget zodat hij telkens waneer je typt de films laat zien die overeenkomen met wat je typt.
zoeken.textChanged.connect(zoekFilm) 
# hier verbinden we de filmGeselecteerd() functie aan de filmlijst zodat we weten waneer je op de film klikt.
filmLijst.clicked.connect(filmGeselecteerd) 
# Hier voegen we de film model aan de filmlijst toe.
filmLijst.setModel(filmModel)
# Hier voegen we de geselecteerde filmmodel toe aan de geselecteerde film lijst.
geselecteerdeFilmLijst.setModel(geselecteerdeFilmModel)

# Hier voegen we de films toe aan de lijst zodat je alvast de films kan zien.
voegFilmsToeAanLijst()

# Met deze code zorgen we ervoor dat het scherm ook te zien is. 
window.show()
# Deze regel zorgt ervoor dat we de aplicatie netjes kunnen sluiten.
sys.exit(app.exec())
