import os
import requests
from bs4 import BeautifulSoup
from datetime import date

class DovizKurlari:
    
    __sonuc = {"durum" : "ERROR", "mesaj" : "bilinmeyen hata oluştu.", "veri" : {}}
    
    def __init__(self, onbellek_klasoru="onbellek"):
        
        self.onbellek_klasoru = os.path.join(os.getcwd(), onbellek_klasoru)
        
    def bugunun_kurlari(self):
        bugun = date.today()
        return self.doviz_kurlari(bugun.day, bugun.month, bugun.year)
    
    def doviz_kurlari(self, gun, ay, yil):
        bugun = date.today()
        
        klasor = str(yil) + self.__basta_sifir(ay)
        dosya = self.__basta_sifir(gun) + self.__basta_sifir(ay) + str(yil) + ".xml"
        
        if bugun.day == gun and bugun.month == ay and bugun.year == yil:
            url = "https://www.tcmb.gov.tr/kurlar/today.xml"
            onbellek_kullan = False
        else :
            url = "https://www.tcmb.gov.tr/kurlar/" + klasor + "/" + dosya
            onbellek_kullan = True
            
        if onbellek_kullan:
            sonuc = self.___onbellekten_oku(klasor, dosya)
            if sonuc["durum"] == "ok":
                return self.__verileri_cozumle(sonuc["veri"])
            else:
                sunucudan_veri = self.__sunucudan_veri_cek(url)
                if sunucudan_veri != None:
                    self.__onbellege_yaz(klasor, dosya,  sunucudan_veri)
                    return self.__verileri_cozumle(sunucudan_veri)
                else:
                    self.__sonuc["durum"] = "ERROR"
                    self.__sonuc["mesaj"] = "sunucudan veri çekilemedi. Ön bellek oluşturulamadı."
                    self.__sonuc["veri"] = {}
                    return self.__sonuc
        else :
            veri = self.__sunucudan_veri_cek(url)
            if veri != None:
                return self.__verileri_cozumle(veri)
            else:
                self.__sonuc["durum"] = "ERROR"
                self.__sonuc["mesaj"] = "sunucudan veri çekilemedi."
                self.__sonuc["veri"] = {}
                return self.__sonuc
    
    def __sunucudan_veri_cek(self, url):
        try:
            istek = requests.get(url)
            
            if istek.status_code == 200:
                return istek.content
            else :
                print("sunucu 200 istek kodu göndermedi")
                
    
        except Exception as e:
            print("sunucudan veri çekerken hata oldu. bu da hata mesajı:", e)
            return None 
    
    def __verileri_cozumle(self, veri):
        self.__sonuc["veri"] = {}
        
        try:
            icerik = BeautifulSoup(veri, "xml")
            
            kurlar = icerik.find_all("Currency")
            
            for kur in kurlar:
                kod = kur.get("CurrencyCode")
                
                if kod == "XDR":
                    continue
                
                isim = kur.find("Isim").text
                alis = kur.find("ForexBuying").text
                satis = kur.find("ForexSelling").text
                
                self.__sonuc["veri"][kod] = {"kod" : kod, "isim" : isim, "alis" : alis, "satis" : satis}
                
            self.__sonuc["durum"] = "ok"
            self.__sonuc["mesaj"] = "Veriler basarıyla çekildi ve yorumlandı"
            return self.__sonuc
                
        except Exception as e:
            self.__sonuc["durum"] = "ERROR"
            self.__sonuc["mesaj"] = "Verilerin getitilmesi sırasında sorun oluştu. hata: " + str(e)
            self.__sonuc["veri"] = {}
            return self.__sonuc
    
    def ___onbellekten_oku(self, klasor, dosya):
        #return {"durum" : "ERROR"}
        okunacak_dosya = os.path.join(self.onbellek_klasoru, klasor, dosya)
        if os.path.exists(okunacak_dosya):
            try:
                with open(okunacak_dosya, "rb") as dosya:
                    self.__sonuc["durum"] = "OK"
                    self.__sonuc["mesaj"] = "ön bellek dosyasından okuma başarılı"
                    self.__sonuc["veri"] = dosya.read()
                    return self.__sonuc
            except Exception as e:
                    self.__sonuc["durum"] = "ERROR"
                    self.__sonuc["mesaj"] = "ön bellek dosyası bulunamadı"
                    self.__sonuc["veri"] = {}
                    return self.__sonuc
        else:
            self.__sonuc["durum"] = "ERROR"
            self.__sonuc["mesaj"] = "ön bellek dosyası bulunamadı"
            self.__sonuc["veri"] = {}
            return self.__sonuc
    
    def __onbellege_yaz(self, klasor, dosya, veri):
        if not os.path.exists(os.path.join(self.onbellek_klasoru, klasor)):
            os.mkdir(os.path.join(self.onbellek_klasoru, klasor))
            
            try:
                with open(os.path.join(self.onbellek_klasoru, klasor, dosya), "wb") as dosya:
                    dosya.write(veri)
            except Exception as e:
                print("hata", e)
    
    def __basta_sifir(self, sayi):
        if sayi < 10:
            return "0" + str(sayi)
        else :
            return str(sayi)
    