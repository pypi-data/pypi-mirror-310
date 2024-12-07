import ctypes
import math


class NizLista():
   
    def kreiraj_niz(self, k):
        return (ctypes.py_object * k)()
    
    def __init__(self, kapacitet):
        self.kapacitet = kapacitet
        self.duzina = 0
        self.tekuci = 0
        self.Niz = self.kreiraj_niz(self.kapacitet)

    def idiNaPocetak(self):
        self.tekuci = 0
        print("Pokazivač tekući postavljen na POČETAK liste!")

    def idiNaKraj(self):
        self.tekuci = self.duzina
        print("Pokazivač tekući postavljen na KRAJ liste!")

    def idiNaSljedeci(self):
        if(self.tekuci < self.duzina):
            self.tekuci += 1
            print("Pokazivač tekući postavljen na SLJEDEĆI ELEMENT liste!")
        else:
            print("Pokazivač tekući je na kraju liste!")

    def idiNaPrethodni(self):
        if(self.tekuci != 0):
            self.tekuci -= 1
            print("Pokazivač tekući postavljen na PRETHODNI ELEMENT liste!")
        else:
            print("Pokazivač tekući je na početku liste!")

    def idiNaPoziciju(self, pozicija):
        if((pozicija < 0) or (pozicija > self.duzina)):
            print("Zadata poziciaj je izvan raspona!")
        else:
            self.tekuci = pozicija
            print("Pokazivač tekući postavljen na poziciju:" + str(pozicija))

    def dodaj(self,x):
        if(self.duzina < self.kapacitet):
            self.Niz[self.duzina] = x
            self.duzina += 1
            print("Uspješno dodan element!")
        else:
            print("Kapacitet popunjen!")

    def lDuzina(self):
        return self.tekuci

    def dDuzina(self):
        return self.duzina - self.tekuci

    def umetni(self, x):
        if(self.duzina < self.kapacitet):
            for i in range(self.duzina,self.tekuci,-1):
                self.Niz[i] = self.Niz[i-1]            
            self.Niz[self.tekuci] = x
            self.duzina += 1
            print("Uspješno umetnut element " + str(x) + " na poziciju pokazivača " + str(self.tekuci))
        else:
            print("Kapacitet popunjen!")

    def izbaci(self):
        if (self.dDuzina() <= 0):
            print("nema elemenata za izbacivanje/brisanje! Tekući na kraju liste!")
        else:
            izbacei = self.Niz[self.tekuci]
            for i in range (self.tekuci,self.duzina-1): 
                self.Niz[i] = self.Niz[i+1]             
            self.duzina -= 1
            print("izvršeno je izbacivanje elementa vrijednosti: " + str(izbacei))

    def ispisiTekuci(self):
        if (self.dDuzina() <= 0):
            print("Nema elemnata za ispis! Pokazivač je na kraju liste!")
        else:
            print("Vrijednost elementa na tekućoj poziciji je: " + str(self.Niz[self.tekuci]))

    def prikazi(self):
        print("Dužina liste:" + str(self.duzina))
        for i in range(0,self.duzina):
            print("Element " + str(i+1) + " - pozicija(" + str(i) + ") :" + str(self.Niz[i]))

# UNZE PTF ASP 2021/2022 :: M.S. :: 10.11.2021

class prosirenaPyNizLista(NizLista):

    def sumaElemenata(self):
        if(self.duzina == 0):
            print("Lista je prazna!")
            return
        sum = 0
        for i in range(self.duzina):
            sum += int(self.Niz[i])
        print(f"Suma svih elemenata u listi je: {sum}")

    def dajMaksimum(self):
        if(self.duzina == 0):
            print("Lista je prazna!")
            return
        maks = int(self.Niz[0])
        for i in range(self.duzina):
            if(maks < int(self.Niz[i])):
                maks = int(self.Niz[i])
        print(f"Najveći element u listi je: {maks}")

    def polovinaKorijena(self):
        if(self.duzina == 0):
            print("Lista je prazna!")
            return
        sum = 0
        for i in range(self.duzina):
            sum += int(self.Niz[i])
        rezultat = math.sqrt(sum)/2
        print(f"Polovina korijena sume elemenata liste je: {rezultat}")

print("      ** TESTNI PROGRAM ZA pyListe **")
print("-------------------Menu--------------------")
print("1. Idi na početak")
print("2. idi na kraj")
print("3. Idi na prethodni")
print("4. Idi na sljedeći")
print("5. Idi na poziciju")
print("6. Dodavanje elemenata na kraj liste")
print("7. Umetanje elmenta na tekuću poziciju")
print("8. Izbacivanje tekućeg elementa")
print("9. Ispis vrijednosti tekućeg elementa")
print("10. Prikaz sadržaja liste")
print("11. Suma elemenata liste")
print("12. Maksimalni element u listi")
print("13. Polovina korijena sume elemenata liste")
print("14. Testna funkcija")
print("99. Izlaz")

unos_izbor = input("--------------Izaberite opciju?---------------\n")
izbor = int(unos_izbor)

k = 20
Lista = prosirenaPyNizLista(k)

def menu(izbor):
    match izbor:
        case 1:
            Lista.idiNaPocetak()
        case 2:
            Lista.idiNaKraj()
        case 3:
            Lista.idiNaPrethodni()
        case 4:
            Lista.idiNaSljedeci()
        case 5:
            pozicija = input("Unesite poziciju za dislokaciju pokazivača tekući!\n")
            Lista.idiNaPoziciju(int(pozicija))
        case 6:
            x = input("Unesite vrijednost elementa!\n")
            Lista.dodaj(x)
        case 7:
            x = input("Unesite vrijednost elementa!\n")
            Lista.umetni(x)
        case 8:
            Lista.izbaci()
        case 9:
            Lista.ispisiTekuci()
        case 10:
            print("** ELEMENTI U LISTI **")
            Lista.prikazi()
        case 11:
            Lista.sumaElemenata()
        case 12:
            Lista.dajMaksimum()
        case 13:
            Lista.polovinaKorijena()
        case 14:
            testni = [8,6,9,2,3,1,5,5,9,7]
            for i in range(len(testni)):
                Lista.dodaj(testni[i])
            Lista.prikazi()
        case 99:
            print("Program završen!\n")
            exit()
        case _:
            print("Pogrešan izbor. Molimo ponovite unos izbora!")

while (izbor):
    menu(izbor)
    unos_izbor = input("--------------Izaberite opciju?---------------\n")
    izbor = int(unos_izbor)

# UNZE PTF ASP 2021/2022 :: M.S. :: 10.11.2021