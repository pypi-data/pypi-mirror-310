import math


class Cvor:
    # Klasa Čvor - osnovni gradivni element za sve strukture podataka
    # Iniciranje prošireno sa parametrom sljedeci
    def __init__(self, element=None, sljedeci = None):
        self.element = element
        self.sljedeci = sljedeci
    
    def __str__(self):
        return str(self.element)

class JPStek():
    # Klasa kojom definiramo strukturu JP Steka, pomoću strukture Čvor
    # Kapacitet :: "NEOGRANIČEN"   

    # Iniciranje steka
    def __init__(self):
        self.vrh = None
        self.velicina = 0 # Već imamo metodu duzina, pa je nemoguće da nam varijabla ima isti naziv (duzina = velicina)
  
    # Ispistuje da li je stek PRAZAN (true - prazan)
    def jeLiPrazan(self):
        return self.vrh == None    

    # Vraća trenutnu dužinu(velicinu) steka tj. broj elemenata koji se nalazi u steku
    def duzina(self):
        return self.velicina

    # Dodavanje elemenata u stek
    def dodajNaStek(self,x):
        novicvor = Cvor(x, self.vrh) # Kreiranje novog cvora, sljedeći pamti podatka o čvoru koji sadrži vrijednost koja se nalazi "ispod" novog čvora
        self.vrh = novicvor          # Svaki novokreirani čvor je vrh
        self.velicina += 1
        print("Element vrijednosti " + str(x) + " je dodan na stek.")

    # Uklanjanje elemenata sa stek (LIFO)
    def ukloniSaSteka(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan! Nema elemenata za uklanjanje.")
        else:            
            x = self.vrh.element                # Pamtimo vrijednost koju brisemo kako bi istu ispisali
            privremeni = self.vrh.sljedeci      # Pamtimo "sljedeći"  
            del self.vrh                        # Brišemo element na vrhu
            self.vrh = privremeni               # Novi vrh je sljedeći koji smo zapamtili
            self.velicina -= 1                  # Veličinu/Dužinu steka moramo smanjiti za 1
            print("Element vrijednosti " + str(x) + " je skinut na stek.")
    
    # U potpunosti briše stek
    def brisi(self):
        while(not (self.jeLiPrazan())):
            self.ukloniSaSteka()
        print("Stek u potpunosti obrisan!")

    # Ispis elementa na vrhu steka
    def elementNaVrhu(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan! Nema elemenata za ispis.")
        else:
            print("Element na vrhu steka: " + str(self.vrh))
   
    # Ispis sadržaja steka
    def prikazi(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan! Nema elemenata za ispis.")
        else:
            privremeni = self.vrh

            print("Sadržaj steka:\n")
            while(privremeni != None):
                print(str(privremeni.element))
                privremeni = privremeni.sljedeci

# UNZE PTF ASP 2021/2022 :: M.S. :: 01.12.2021

class prosireniPyJPStek(JPStek, Cvor):

    def sumaElemenata(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan!")
            return
        sum = 0
        temp = self.vrh
        while temp is not None:
            sum += int(temp.element)
            temp = temp.sljedeci
        print(f"Suma svih elemenata u steku je: {sum}")

    def dajMaksimum(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan!")
            return
        maks = self.vrh
        temp = self.vrh
        while temp is not None:
            if(int(maks.element) < int(temp.element)):
                maks = temp
            temp = temp.sljedeci
        print(f"Najveći element u listi je: {maks.element}")

    def polovinaKorijena(self):
        if(self.jeLiPrazan()):
            print("Stek je prazan!")
            return
        sum = 0
        temp = self.vrh
        while temp is not None:
            sum += int(temp.element)
            temp = temp.sljedeci
        rezultat = math.sqrt(sum)/2
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

# Iniciranje JP Steka
Stek = prosireniPyJPStek()

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
            if(Stek.jeLiPrazan()):
                print("Stek je prazan!")
            else:
                print("Stek NIJE prazan!")
        case 6:
            print("Kapacitet JPSteka je \"neograničen!\"")
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