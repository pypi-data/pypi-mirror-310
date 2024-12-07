class Cvor:
    # Klasa Čvor - osnovni gradivni element za sve strukture podataka
    # Iniciranje prošireno sa parametrom sljedeci
    def __init__(self, element=None, sljedeci = None):
        self.element = element
        self.sljedeci = sljedeci
    
    def __str__(self):
        return str(self.element)

class JPRed():
    # Klasa kojom definiramo strukturu JP Red, pomoću strukture Čvor
    # Kapacitet :: "NEOGRANIČEN"   

    # Iniciranje reda
    def __init__(self):
        self.pocetak = None
        self.kraj = None
        self.velicina = 0 # Već imamo metodu duzina, pa je nemoguće da nam varijabla ima isti naziv (duzina = velicina)

    # Ispistuje da li je red PRAZAN (true - prazan)
    def jeLiPrazan(self):
        return self.pocetak == None

    # Vraća trenutnu dužinu reda tj. broj elemenata koji se nalazi u redu
    def duzina(self):
        return self.velicina

    # Dodavanje elemenata u red
    def dodajURed(self,x):
        novicvor = Cvor(x)                # Kreiranje novog cvora
        
        if(self.pocetak == None):                   # Ako je red prazan
            self.pocetak = self.kraj = novicvor 
        else:
            self.kraj.sljedeci = novicvor           # Povezujemo element na kraju sa novim cvorom
            self.kraj = self.kraj.sljedeci          # Pokazivač kraj prebacujemo na novi cvor

        self.velicina += 1
        print("Element vrijednosti " + str(x) + " je dodan u red.")

    # Izbacivanje elemenata iz rada (FIFO)
    def izbaciIzReda(self):
        if(self.jeLiPrazan()):
            print("Red je prazan! Nema elemenata za izbacivanje!")
        else:
            x = self.pocetak.element                    # Pamtimo vrijednost koju brisemo kako bi istu ispisali
            privremeni = self.pocetak            

            if (self.pocetak == self.kraj):             # Samo jedan element u redu
                self.pocetak = self.kraj = None         # Prazan red
            else:
                self.pocetak = self.pocetak.sljedeci    # Pomjeramo pokazivač početak na element koji se nalazi iza u redu
            
            del privremeni                              # Brišemo element iz memorije            
            self.velicina -= 1                          # Veličinu/Dužinu reda moramo smanjiti za 1
            print("Element vrijednosti " + str(x) + " je uklonjen iz reda.")

    # U potpunosti briše red
    def brisi(self):
        while(not (self.jeLiPrazan())):
            self.izbaciIzReda()
        print("Red u potpunosti obrisan!")

    # Ispis elementa na vrpoečtku reda
    def elementNaCelu(self):
        if(self.jeLiPrazan()):
            print("Red je prazan! Nema elemenata za ispis.")
        else:
            print("Element na početku reda: " + str(self.pocetak))
   
    # Ispis sadržaja reda
    def prikazi(self):
        if(self.jeLiPrazan()):
            print("Red je prazan! Nema elemenata za ispis.")
        else:
            print("Sadržaj reda:\n")

            privremeni = self.pocetak

            while(privremeni != None):
                print(str(privremeni.element))
                privremeni = privremeni.sljedeci        

# UNZE PTF ASP 2021/2022 :: M.S. :: 01.12.2021

class prosireniPyJPRed(JPRed):

    def ariSredina(self):
        if(self.jeLiPrazan()):
            print("Red je prazan!")
            return
        sum = 0
        temp = self.pocetak
        while temp is not None:
            sum += int(temp.element)
            temp = temp.sljedeci
        ariSredina = sum / float(self.duzina())
        print(f"Aritmeticka sredina svih elemenat u strukturi je: {ariSredina}")

    def dajMinimum(self):
        if(self.jeLiPrazan()):
            print("Red je prazan!")
            return
        minimum = self.pocetak.element
        temp = self.pocetak
        while temp is not None:
            if(int(minimum) > int(temp.element)):
                minimum = int(temp.element)
            temp = temp.sljedeci
        print(f"Najmanji element u strukturi je: {minimum}")

# Ispis menija
print("      ** TESTNI PROGRAM ZA pyRed **")
print("-------------------Menu--------------------")
print("1. Dodaje element u red")
print("2. Ukloni element iz reda")
print("3. Element na početku reda")
print("4. Prikazi sadrzaj reda")
print("5. Da li je red prazan?")
print("6. Da li je red pun?")
print("7. Potpuno brisanje reda!")
print("8. Aritmeticka sredina elemenata reda")
print("9. Minimalni element reda")
print("10. Testna funkcija")
print("99. Izlaz")

unos_izbor = input("--------------Izaberite opciju?---------------\n")
izbor = int(unos_izbor)

# Iniciranje JP Reda
Red = prosireniPyJPRed()

# case petlja za definiranje opcija u meniju
def menu(izbor):
    match izbor:
        case 1:
            x = input("Unesite vrijednost elementa za dodavanje u red?\n")
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
            print("Kapacitet JPReda je \"neograničen!\"")
        case 7:
            Red.brisi()
        case 8:
            Red.ariSredina()
        case 9:
            Red.dajMinimum()
        case 10:
            testni = [8,6,9,2,3,1,5,5,9,7]
            for i in range(len(testni)):
                Red.dodajURed(testni[i])
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