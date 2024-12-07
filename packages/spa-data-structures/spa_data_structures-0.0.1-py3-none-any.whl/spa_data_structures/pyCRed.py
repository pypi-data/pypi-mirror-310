import ctypes

class CRed():
   
    # Metoda kreira niz kapaciteta k -- ctypes --za dodatni info pogledati pyNizListe
    def kreiraj_niz(self, k):
        return (ctypes.py_object * k)()

    # Iniciranje reda
    def __init__(self, kapacitet):
        self.kapacitet = kapacitet
        self.pocetak = -1
        self.kraj = -1
        self.Niz = self.kreiraj_niz(self.kapacitet)

    # U potpunosti briše red
    def brisi(self):
        self.pocetak = -1
        self.kraj = -1        
        print("Red u potpunosti obrisan!")

    # Ispistuje da li je red PRAZAN (true - prazan)
    def jeLiPrazan(self):
        return self.pocetak == -1
    
    # Ispistuje da li je red PUN  (true - pun)
    def jeLiPun(self):
        return self.pocetak == (self.kraj+1) % self.kapacitet

    # Vraća trenutnu dužinu reda tj. broj elemenata koji se nalazi u redu
    def duzina(self):
        if (self.pocetak == -1):
            return 0
        else:
            return ((self.kraj + self.kapacitet) - self.pocetak) % self.kapacitet + 1

    # Dodavanje elemenata u red
    def dodajURed(self,x):
        if(self.jeLiPun()):
            print("Red je pun! Nemoguće je dodatni nove elemente.")
        else:
            self.kraj = (self.kraj + 1) % self.kapacitet
            self.Niz[self.kraj] = x
            if(self.pocetak == -1):  # Ukoliko je Red bio prazan, potrebno je i promjeniti pokazivač početak
                self.pocetak = 0
            print("Element vrijednosti " + str(x) + " je dodan u red.")

    # Izbacivanje elemenata siz rada (FIFO)
    def izbaciIzReda(self):
        if(self.jeLiPrazan()):
            print("Red je prazan! Nema elemenata za izbacivanje!")
        else:
            x = self.Niz[self.pocetak]
           
            if (self.pocetak == self.kraj):     # samo jedan element u redu
                self.pocetak = self.kraj = -1   # prazan red
            else:
                self.pocetak = (self.pocetak + 1) % self.kapacitet

            print("Element vrijednosti " + x + " je izbačen iz reda.") 

    # Ispis elementa na početku reda
    def elementNaCelu(self):
        if(self.jeLiPrazan()):
            print("Red je prazan! Nema elemenata za ispis.")
        else:
            print("Element na početku reda: " + str(self.Niz[self.pocetak]))
   
    # Ispis sadržaja reda
    def prikazi(self):
        if(self.jeLiPrazan()):
            print("Red je prazan! Nema elemenata za ispis.")
        else:
            print("Sadržaj reda:\n")

            i = self.pocetak
            # U pythonu ne postoji klasična do-while petlja
            while True:
                print(str(i) + " : " + str(self.Niz[i]))
                i = (i +1) % self.kapacitet

                if (i == (self.kraj + 1) % self.kapacitet):
                    break           

# UNZE PTF ASP 2021/2022 :: M.S. :: 01.12.2021

import pyCRed

class prosireniPyCRed(pyCRed.CRed):

    def ariSredina(self):
        if (self.jeLiPrazan()):
            print("Red je prazan!")
            return
        sum = 0
        i = self.pocetak
        while True:
            sum += int(self.Niz[i])
            i = (i + 1) % self.kapacitet
            if(i == (self.kraj+1) % self.kapacitet):
                break
        ariSredina = sum/float(self.duzina())
        print(f"Aritmeticka sredina svih elemenat u strukturi je: {ariSredina}")

    def dajMinimum(self):
        if(self.jeLiPrazan()):
            print("Red je prazan!")
            return
        i = self.pocetak
        minimum = int(self.Niz[i])
        while True:
            if(minimum > int(self.Niz[i])):
                minimum = int(self.Niz[i])
            i = (i+1) % self.kapacitet
            if(i == (self.kraj + 1) % self.kapacitet):
                break
        print(f"Najmanji element u strukturi je: {minimum}")

# Ispis menija
print("      ** TESTNI PROGRAM ZA pyRed **")
print("-------------------Menu--------------------")
print("1. Dodaje element u red")
print("2. Ukloni element iz reda")
print("3. Element na početku reda")
print("4. Prikazi sadržaj reda")
print("5. Da li je red prazan?")
print("6. Da li je red pun?")
print("7. Potpuno brisanje reda!")
print("8. Aritmeticka sredina elemenata reda")
print("9. Minimalni element reda")
print("10. Testna funkcija")
print("99. Izlaz")

unos_izbor = input("--------------Izaberite opciju?---------------\n")
izbor = int(unos_izbor)

# Iniciranje Cirkularnog Reda
k = 10
Red = prosireniPyCRed(k)

# case petlja za definiranje opcija u meniju
def menu(izbor):
    match izbor:
        case 1:
            x = input("Unesite vrijednost elementa za dodavanje na red?\n")
            Red.dodajURed(x)
        case 2:
            Red.izbaciIzReda()
        case 3:
            Red.elementNaCelu()
        case 4:
            Red.prikazi()
        case 5:
            if(Red.jeLiPrazan()):
                print("Red je prazan!")
            else:
                print("Red NIJE prazan!")
        case 6:
            if(Red.jeLiPun()):
                print("Red je pun!")
            else:
                print("Red NIJE pun!")
        case 7:
            Red.brisi()
        case 8:
            Red.ariSredina()
        case 9:
            Red.dajMinimum()
        case 10:
            testni = [8,6,9,2,3,1,5,5,9,7]
            for i in range(len(testni)):
                Red.dodajURed(str(testni[i]))
            Red.prikazi()
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