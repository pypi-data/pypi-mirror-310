
class Cvor:
    def __init__(self, element=None):
        self.element = element
        self.sljedeci = None
    
    def __str__(self):
        return str(self.element)

class JPlista():
    def __init__(self):
        self.pocetak = None
        self.kraj = None
        self.tekuci = None
        self.dduzina = 0
        self.lduzina = 0

    def idiNaPocetak(self):
        self.tekuci = self.pocetak
        self.dduzina += self.lduzina
        self.lduzina = 0
        print("Pokazivač tekući postavljen na POČETAK liste!")
    
    def idiNaKraj(self):
        self.tekuci = self.kraj
        self.lduzina += self.dduzina
        self.dduzina = 0
        print("Pokazivač tekući postavljen na KRAJ liste!")

    def idiNaSljedeci(self):
        if(self.dduzina != 0):
            if(self.tekuci == None):
                self.tekuci = self.pocetak
                print("Pokazivač je postavljen an POČETAK liste!")
            else:
                self.tekuci = self.tekuci.sljedeci
            self.lduzina += 1
            self.dduzina -= 1
            print("Pokazivač tekući postavljen na SLJEDEĆI ELEMENT liste!")
        else:
            print("Pokazivač tekući je na kraju liste!")

    def idiNaPrethodni(self):
        if(self.lduzina != 0):
            if(self.lduzina == 1):
                self.tekuci = self.pocetak
                print("Pokazivač je postavljen na POČETAK liste!")
            else:
                privremeni = self.pocetak
                while(privremeni.sljedeci != self.tekuci):
                    privremeni = privremeni.sljedeci
                self.tekuci = privremeni
                print("Pokazivač tekući je postavljen na PRETHODNI ELEMENT liste!")
            self.lduzina -= 1
            self.dduzina += 1
        else:
            print("Pokazivač tekući je na početku liste!")

    def idiNaPoziciju(self, pozicija):
        if((pozicija < 0) or (pozicija > (self.lduzina + self.dduzina))):
            print("Zadata pozicija je izvan raspona!")
        else:
            self.dduzina = self.dduzina + self.lduzina - pozicija
            self.lduzina = pozicija
            if(pozicija == 0):
                self.tekuci = self.pocetak
                print("Pokazivač tekući pokazuje na POČETAK liste")
            else:
                self.tekuci = self.pocetak
                for i in range(0,pozicija-1):
                    self.tekuci = self.tekuci.sljedeci
            print("Pokazivač tekući postavljen na poziciju:" + str(pozicija))

    def dodaj(self, x):
        novicvor = Cvor(x)
        
        if(self.dduzina+self.lduzina == 0):
            self.pocetak = novicvor
            self.kraj = novicvor
            print("Lista je bila prazna. Početak i kraj liste su sada isti novi čvor!")
        else:                               
            self.kraj.sljedeci = novicvor      
            self.kraj = novicvor                
            print("Uspješno dodan element na kraj liste!")
        
        self.dduzina += 1

    def umetni(self, x):
        privremen = Cvor(x)

        if (self.lduzina == 0):
            privremen.sljedeci = self.pocetak
            self.pocetak = privremen
            if(self.lduzina+self.dduzina == 0):
                self.kraj = privremen
            print("Uspješno umetnut element " + str(x) + " na početak liste")
        else:
            privremen.sljedeci = self.tekuci.sljedeci
            self.tekuci.sljedeci = privremen
            if(self.dduzina == 0):
                self.kraj = self.tekuci.sljedeci
            print("Uspješno umetnut element " + str(x) + " na poziciju pokazivača " + str(self.tekuci))
        
        self.dduzina += 1    

    def izbaci(self):
        if (self.dduzina <= 0):
            print("Nema elemenata za izbacivanje/brisanje! Tekući na kraju liste!")
        
        privremen = Cvor()
        
        if(self.lduzina == 0):                      
            privremen = self.pocetak
            self.pocetak = privremen.sljedeci
            print("Izvršeno je izbacivanje elementa!")
        else:
           privremen = self.tekuci.sljedeci        
           self.tekuci.sljedeci = privremen.sljedeci
           print("izvršeno je izbacivanje elementa!")
        
        if(self.dduzina == 1):                  
            self.kraj = self.tekuci
        
        self.dduzina -= 1

    def ispisiTekuci(self):
        if (self.dduzina == 0):
            print("Nema elemnata za ispis! Pokazivač je na kraju liste!")
        elif(self.tekuci == None):
            print("Vrijednost elementa na početku liste je: " + str(self.pocetak.element))
        else:
            print("Vrijednost elementa na tekućoj poziciji je: " + str(self.tekuci.element))

    def prikazi(self):
        if(self.dduzina + self.lduzina == 0):
            print("Lista je prazna!")
        else:
            privremeni = self.pocetak
            brojac = 0

            while(privremeni != None):
                print(str(brojac) + ": " + str(privremeni), end="")

                if (privremeni == self.pocetak):
                    print( " <- početak",end="")
                if(privremeni == self.tekuci):
                    print( " <- tekući",end="")
                if(privremeni == self.kraj):
                    print( " <- kraj",end="")
                print("")

                privremeni = privremeni.sljedeci
                brojac += 1

class prosirenaPyJPLista(pyJPListe.JPlista):

    def sumaElemenata(self):
        if(self.dduzina + self.lduzina == 0):
            print("Lista je prazna!")
            return
        sum = 0
        temp = self.pocetak
        while temp is not None:
            sum += int(temp.element)
            temp = temp.sljedeci
        print(f"Suma svih elemenata u listi je: {sum}")

    def dajMaksimum(self):
        if(self.dduzina+self.lduzina == 0):
            print("Lista je prazna!")
            return
        maks = self.pocetak.element
        temp = self.pocetak
        while temp is not None:
            if(int(maks) < int(temp.element)):
                maks = temp.element
            temp = temp.sljedeci
        print(f"Najveći element u listi je: {maks}")

    def polovinaKorijena(self):
        if(self.dduzina + self.lduzina == 0):
            print("Lista je prazna!")
            return
        sum = 0
        temp = self.pocetak
        while temp is not None:
            sum += int(temp.element)
            temp = temp.sljedeci
        rezultat = math.sqrt(sum)/2
        print(f"Polovina korijena sume elemenata liste je: {rezultat}")

print("     ** TESTNI PROGRAM ZA pyJPListe **")
print("-------------------Menu--------------------")
print("1. Idi na prethodni")
print("2. Idi na sljedeći")
print("3. Idi na početak")
print("4. Idi na kraj")
print("5. Idi na poziciju")
print("6. Dodavanje elementa na kraj liste")
print("7. Umetanje elementa na tekuću poziciju")
print("8. Izbacivanje tekućeg elementa")
print("9. Ispis vrijednost tekućeg elementa")
print("10. Prikaži sadržaj liste")
print("11. Suma elemenata liste")
print("12. Maksimalni element u listi")
print("13. Polovina korijena sume elemenata liste")
print("14. Testna funkcija")
print("99. Izlaz")
unos_izbora = input("------------Izaberite opciju?-------------\n")
izbor = int(unos_izbora)

Lista = zadatak1.prosirenaPyJPLista()

def menu(izbor):
    match izbor:
        case 1:
            Lista.idiNaPrethodni()
        case 2:
            Lista.idiNaSljedeci()
        case 3:
            Lista.idiNaPocetak()
        case 4:
            Lista.idiNaKraj()
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
    unos_izbora = input("------------Izaberite opciju?-------------\n")
    izbor = int(unos_izbora)