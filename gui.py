# File: main.py
import sys
import sqlite3
import SQL
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QLineEdit, QListView, QTreeView
from PySide6.QtCore import QFile, QModelIndex, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont

with sqlite3.connect("FilmDatabase.db") as db:
    cursor = db.cursor()

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

lijst_met_films = list(VraagFilmDataOp.vraagFilmIDsOp())

def voegFilmsToeAanLijst():
    for i in (lijst_met_films):
        filmTitel = str(VraagFilmDataOp.vraagFilmTitelOp(i)).strip("[(',)]")
        if str(zoeken.text()).lower() in filmTitel.lower():
            filmItem = QStandardItem(filmTitel)
            filmItem.setEditable(False)
            filmItem.setData(i, Qt.UserRole)
            filmModel.appendRow(filmItem)

def zoekFilm():
    filmModel.clear()
    voegFilmsToeAanLijst()

def filmGeselecteerd(index:QModelIndex):
    geselecteerdeFilmModel.clear()
    ID = index.data(Qt.UserRole)
    itemFont = QFont("Segui UI", 15)

    filmTitel = QStandardItem(str(VraagFilmDataOp.vraagFilmTitelOp(ID)).strip("[(',)]"))
    filmGenre = QStandardItem("Genre: " + str(VraagFilmDataOp.vraagFilmGenreOp(ID)).strip("[(',)]"))
    filmStudio = QStandardItem("Studio: " + str(VraagFilmDataOp.vraagFilmStudioOp(ID)).strip("[(',)]"))
    filmTaal = QStandardItem("Taal :" + str(VraagFilmDataOp.vraagFilmTaalOp(ID)).strip("[(',)]"))
    filmLengte = QStandardItem("Duur: " + str(VraagFilmDataOp.vraagFilmLengteOp(ID)).strip("[(',)]"))
    filmTrailer = QStandardItem("Trailer: " + str(VraagFilmDataOp.vraagFilmTrailerOp(ID)).strip("[(',)]"))

    filmGenre.setFont(itemFont)
    filmStudio.setFont(itemFont)
    filmTaal.setFont(itemFont)
    filmLengte.setFont(itemFont)
    filmTrailer.setFont(itemFont)

    filmTitel.setChild(0, filmGenre)
    filmTitel.setChild(1, filmStudio)
    filmTitel.setChild(2, filmTaal)
    filmTitel.setChild(3, filmLengte)
    filmTitel.setChild(4, filmTrailer)

    filmTitel.setEditable(False)
    geselecteerdeFilmModel.appendRow(filmTitel)
    geselecteerdeFilmLijst.expandAll()
    

app = QApplication(sys.argv)
ui_file_name = "gui.ui"
ui_file = QFile(ui_file_name)
loader = QUiLoader()
window = loader.load(ui_file)

zoeken = window.findChild(QLineEdit, "zoekFilm")
filmLijst = window.findChild(QListView, "filmLijst")
filmModel = QStandardItemModel()
geselecteerdeFilmLijst = window.findChild(QTreeView, "geselecteerdeFilmLijst")
geselecteerdeFilmModel = QStandardItemModel()

zoeken.textChanged.connect(zoekFilm) 
filmLijst.clicked.connect(filmGeselecteerd) 
filmLijst.setModel(filmModel)
geselecteerdeFilmLijst.setModel(geselecteerdeFilmModel)

voegFilmsToeAanLijst()

window.show()
sys.exit(app.exec())
