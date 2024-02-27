import os.path
from datetime import date

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from doviz_sinifi import DovizKurlari

import sys
import os
from PyQt5.QtWidgets import *

class Pencere(QMainWindow):
    veriler = {}

    def __init__(self, parent=None):
        super().__init__(parent)

        self.resim_yolu = os.path.join(os.getcwd(), "img")

        self.setFixedWidth(320)
        self.setFixedHeight(660)
        self.setObjectName('AnaPencere')
        self.setWindowTitle("dövizler")
        self.setWindowIcon(QIcon(os.path.join(self.resim_yolu, "logo.png")))

        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(0, 0, self.width(), self.height())
        self.setCentralWidget(self.mainWidget)

        font = QFont()
        font.setFamily('Segoe UI')

        self.mainWidget.setFont(font)

        baslik = QLabel(self.mainWidget)
        baslik.setText('TCMB Döviz Kurları')
        baslik.setGeometry(0, 10, self.mainWidget.width(), 40)
        baslik.setAlignment(Qt.AlignCenter)

        font.setBold(True)
        font.setPointSize(12)
        baslik.setFont(font)

        font.setBold(False)
        font.setPointSize(8)

        self.txt_tarih = QDateEdit(self.mainWidget)
        self.txt_tarih.setGeometry(80, 60, 80, 20)
        self.txt_tarih.setMaximumDate(date.today())
        self.txt_tarih.setDate(date.today())
        self.txt_tarih.setFont(font)

        self.btn_getir = QPushButton(self.mainWidget)
        self.btn_getir.setText('Kurları Getir')
        self.btn_getir.setGeometry(165, 59, 80, 22)
        self.btn_getir.setFont(font)
        self.btn_getir.clicked.connect(self.veriCek)

        self.tablo = QTableWidget(self.mainWidget)
        baslangic = self.btn_getir.y() + self.btn_getir.height() + 10
        self.tablo.setGeometry(10, baslangic, self.mainWidget.width() - 20, self.mainWidget.height() - baslangic - 10)

        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["#", "Kod", "Döviz Adı", "alış", "satış"])

        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.horizontalHeader().setFixedHeight(36)
        self.tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.tablo.setSelectionMode(QTableWidget.NoSelection)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tablo.verticalHeader().setVisible(False)

        self.showEvent = lambda _, : self.veriCek()

        bilgi = QPushButton(self.mainWidget)
        bilgi.setText("")
        bilgi.setIcon(QIcon(QPixmap(os.path.join(self.resim_yolu, "information.png"))))
        bilgi.setStyleSheet("background-color: transparent; border: none;")
        bilgi.setGeometry(self.mainWidget.width() - 10 - 24, 10, 24, 24)
        bilgi.clicked.connect(self.bilgi_ver)

    def bilgi_ver(self):
        box = QMessageBox()
        box.setWindowTitle("Program Hakkında")
        box.setWindowIcon(QIcon(QPixmap(os.path.join(self.resim_yolu, "information.png"))))
        box.setText("Bu program Erdem Arslan'ın yardımıyla Uras Gezici tarafından Biga Bilsem'de(Bilim ve Sanat Merkezi) yazılmıştır")

        box.exec_()

    def tablo_temizle(self):
        self.tablo.clearContents()
        self.tablo.setRowCount(0)

    def tabloya_icerik_ekle(self):
        if len(self.veriler) > 0:
            row = 0
            for key, value in self.veriler.items():
                self.tablo.insertRow(row)

                bayrak = QLabel()
                resim = os.path.join(self.resim_yolu, str(key).lower() + ".png")
                bayrak.setPixmap(QPixmap(resim))
                bayrak.setAlignment(Qt.AlignCenter)
                self.tablo.setCellWidget(row, 0, bayrak)

                kod = QTableWidgetItem()
                kod.setText(str(key))
                kod.setTextAlignment((Qt.AlignCenter))

                doviz_adi = QTableWidgetItem()
                doviz_adi.setText(str(value["isim"]))
                doviz_adi.setTextAlignment((Qt.AlignCenter))

                alis = QTableWidgetItem()
                alis.setText(str(value["alis"]))
                alis.setTextAlignment((Qt.AlignCenter))

                satis = QTableWidgetItem()
                satis.setText(str(value["satis"]))
                satis.setTextAlignment((Qt.AlignCenter))

                self.tablo.setItem(row, 1, kod)
                self.tablo.setItem(row, 2, doviz_adi)
                self.tablo.setItem(row, 3, alis)
                self.tablo.setItem(row, 4, satis)
                row += 1




    def veriCek(self):
        kurlar = DovizKurlari()
        tarihHam = self.txt_tarih.text()

        tarih = tarihHam.split(".")

        veriler = kurlar.doviz_kurlari(int(tarih[0]), int(tarih[1]), int(tarih[2]))


        self.tablo_temizle()

        if veriler["durum"] == "ok":
            self.veriler = veriler['veri']
            self.tabloya_icerik_ekle()
        else:
            box = QMessageBox()

            box.setWindowTitle("bir hata oluştu")
            box.setWindowIcon(QIcon(QPixmap(os.path.join(self.resim_yolu, "warning.png"))))
            box.setIconPixmap(QPixmap(os.path.join(self.resim_yolu, "error.png")))
            box.setText(veriler["mesaj"])
            box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = Pencere()
    pencere.show()
    sys.exit(app.exec_())
