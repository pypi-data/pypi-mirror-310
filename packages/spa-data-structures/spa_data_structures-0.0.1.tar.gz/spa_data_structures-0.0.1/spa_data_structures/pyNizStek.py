import ctypes
import math


class NizStek():
   
    # Metoda kreira niz kapaciteta k -- ctypes --za dodatni info pogledati pyNizListe
    def kreiraj_niz(self, k):
        return (ctypes.py_object * k)()

    # Iniciranje steka
    def __init__(self, kapacitet):
        self.kapacitet = kapacitet
        self.vrh = -1
        self.Niz = self.kreiraj_niz(self.kapacitet)

    # U potpunosti briše stek
    def brisi(self):
        self.vrh = -1
        print("Stek u potpunosti obrisan!")

    # Ispistuje da li je stek PRAZAN (true - prazan)
    def jeLiPrazan(self):
        return self.vrh == -1
    
    # Ispistuje da li je stek PUN  (true - pun)
    def jeLiPun(self):
        return self.vrh == self.kapacitet-1

    # Vraća trenutnu dužinu steka tj. broj elemenata koji se nalazi u steku
    def duzina(self):
        return self.vrh + 1

    # Dodavanje elemenata u stek (LIFO)
    def dodajNaStek(self,x):
        if(self.jeLiPun()):
            print("Stek je pun! Nemoguće je dodatni nove elemente.")
        else:
            self.vrh += 1
            self.Niz[self.vrh] = x
            print("Element vrijednosti " + str(x) + " je dodan na stek.")

    # Uklanjanje elemenata sa stek (LIFO)
    def ukloniSaSteka(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan! Nema elemenata za uklanjanje.")
        else:
            self.vrh -= 1
            print("Element vrijednosti " + str(self.Niz[self.vrh+1]) + " je skinut na stek.") # Moguće ispisati vrijednost Niz[self.vrh+1] jer element i dalje ostaje u memoriji

    # Ispis elementa na vrhu steka
    def elementNaVrhu(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan! Nema elemenata za ispis.")
        else:
            print("Element na vrhu steka: " + str(self.Niz[self.vrh]))
   
    # Ispis sadržaja steka
    def prikazi(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan! Nema elemenata za ispis.")
        else:
            print("Sadržaj steka:\n")
            for i in range(self.vrh,-1,-1):
                print(str(i) + " : " + str(self.Niz[i]))
                i += 1

# UNZE PTF ASP 2021/2022 :: M.S. :: 01.12.2021

class prosireniPyNizStek(NizStek):

    def sumaElemenata(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan!")
            return
        suma = 0
        for i in range(self.duzina()):
            suma += int(self.Niz[i])
        print(f"Suma svih elemenata u steku je: {suma}")

    def dajMaksimum(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan!")
            return
        maks = int(self.Niz[0])
        for i in range(self.duzina()):
            if(maks < int(self.Niz[i])):
                maks = int(self.Niz[i])
        print(f"Najveći element u steku je: {maks}")

    def polovinaKorijena(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan!")
            return
        suma = 0
        for i in range(self.duzina()):
            suma += int(self.Niz[i])
        rezultat = math.sqrt(suma)/2
        print(f"Polovina korijena sume elemenata steka je: {rezultat}")

# Ispis menija
print("      ** TESTNI PROGRAM ZA pyStek **")
print("-------------------Menu--------------------")
print("1. Dodaje element na stek")
print("2. Ukloni element sa steka")
print("3. Element na vrhu steka")
print("4. Prikazi sadrzaj steka")
print("5. Da li je stek prazan?")
print("6. Da li je stek pun?")
print("7. Potpuno brisanje steka!")
print("8. Suma elemenata steka")
print("9. Maksimalni element steka")
print("10. Polovina korijena sume elemenata steka")
print("11. Testna funkcija")
print("99. Izlaz")

unos_izbor = input("--------------Izaberite opciju?---------------\n")
izbor = int(unos_izbor)

# Iniciranje Niz Steka
k = 15
Stek = prosireniPyNizStek(k)

# case petlja za definiranje opcija u meniju
def menu(izbor):
    match izbor:
        case 1:
            x = input("Unesite vrijednost elementa za dodavanje na stek?\n")
            Stek.dodajNaStek(x)
        case 2:
            Stek.ukloniSaSteka()
        case 3:
            Stek.elementNaVrhu()
        case 4:
            Stek.prikazi()
        case 5:
            print("Vrh: " + str(Stek.vrh))
            print("Kapacitet: " + str(Stek.kapacitet))
            if(Stek.jeLiPrazan()):
                print("Stek je prazan!")
            else:
                print("Stek NIJE prazan!")
        case 6:
            print("Vrh: " + str(Stek.vrh))
            print("Kapacitet: " + str(Stek.kapacitet))
            if(Stek.jeLiPun()):
                print("Stek je pun!")
            else:
                print("Stek NIJE pun!")
        case 7:
            Stek.brisi()
        case 8:
            Stek.sumaElemenata()
        case 9:
            Stek.dajMaksimum()
        case 10:
            Stek.polovinaKorijena()
        case 11:
            testni = [8,6,9,2,3,1,5,5,9,7]
            for i in range(len(testni)):
                Stek.dodajNaStek(testni[i])
            Stek.prikazi()
        case 99:
            print("Program završen!\n")
            exit()
        case _:
            print("Pogrešan izbor. Molimo ponovite unos izbora!")

# while petlja za kontinuiran odabir opcija u meniju
while (izbor):
    menu(izbor)
    unos_izbor = input("--------------Izaberite opciju?---------------\n")
    izbor = int(unos_izbor)

# UNZE PTF ASP 2021/2022 :: M.S. :: 01.12.2021