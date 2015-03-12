# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:04:50 2015

@author: Tom
"""
import json
import urllib
import Tkinter as tk
import tkMessageBox as tkm
##############################################################################
##############################################################################


def vypsat(kontakty):                   ##získá kontakty ve formátu json
     return kontakty["shortcut"], kontakty["name"], kontakty["number"]



def prihlasit():
    prihl_jmeno = prihl_jmeno_entry.get()
    heslo = heslo_entry.get()
    global udaje
    udaje = urllib.urlencode({"user": prihl_jmeno, "password": heslo})            ## přihlašovací údaje jako parametr
    kredit_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/balance?"+udaje)  ## získání kreditu
    kredit = kredit_mezikrok.read()         ## kredit jako řetězec   
    if prihl_jmeno_entry.get() == "" or heslo_entry.get() == "":  ## nevyplněné údaje
        tkm.showwarning("CHYBA", u"Jeden, nebo oba údaje zůstaly nevyplněny")
    elif kredit == "error authentication_failed":     ## špatně zadané údaje
        tkm.showwarning("CHYBA", u"Zadal/a jste špatné přihlašovací údaje")
    else:                                           ## dobře zadané údaje
        kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje)   ##získání kontaktů
        kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
        global kontakty
        kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)          ##kontakty jako 3-členné ntice v seznamu
        hl_okno.destroy()                       
        prihl_okno = tk.Tk()
############################################################################### horní informace
        kredit_label = tk.Label(prihl_okno, text="Váš kredit je: "+kredit+"Kč")   ##vypisuje kredit
        kredit_label.grid(columnspan=3)
########################################################################### vstupy       
        zkratka_label = tk.Label(prihl_okno, text="Zkratka")                    ##záhlaví callbacku
        zkratka_label.grid(row=1)
        jmeno_label = tk.Label(prihl_okno, text=u"Jméno")
        jmeno_label.grid(row=1, column=1)
        cislo_label = tk.Label(prihl_okno, text=u"Číslo")
        cislo_label.grid(row=1, column=2)
        zkratka_entry = tk.Entry(prihl_okno)                                    
        zkratka_entry.grid(row=2)
        jmeno_entry = tk.Entry(prihl_okno)
        jmeno_entry.grid(row=2, column=1)
        cislo_entry = tk.Entry(prihl_okno)
        cislo_entry.grid(row=2, column=2)
########################################################################### tlačítka pod vstupy
        frame_na_buttony = tk.Frame(prihl_okno)
        frame_na_buttony.grid(row=3, sticky=tk.E+tk.W+tk.N+tk.S, columnspan=3) 
        doplnit_button = tk.Button(frame_na_buttony, text="Doplnit", command=lambda: doplnit(zkratka_entry, cislo_entry, jmeno_entry, kontakty))                  ## tlacitka pod vstupy
        doplnit_button.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        smazat_button = tk.Button(frame_na_buttony, text="Smazat", command=lambda: smazat(zkratka_entry, cislo_entry, jmeno_entry))
        smazat_button.grid(column=1, row=0, sticky=tk.E+tk.W+tk.N+tk.S)
        pridat_button = tk.Button(frame_na_buttony, text="přidat", command=lambda: pridat(zkratka_entry, cislo_entry, jmeno_entry))
        pridat_button.grid(row=0, column=2, sticky=tk.E+tk.W+tk.N+tk.S)
        odebrat_button = tk.Button(frame_na_buttony, text="odebrat", command=lambda: odebrat(kontakty))
        odebrat_button.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S)
        callback_button = tk.Button(frame_na_buttony, text="Objednat callback", command=lambda: callback(cislo_entry, jmeno_entry,))
        callback_button.grid(row=0, column=4, sticky=tk.E+tk.W+tk.N+tk.S)
        global seznam_hodnot
        seznam_hodnot = []
        for i in range(1+len(kontakty)/10):
            hodnota = "Strana"+str(i+1)+"/"+str(1+len(kontakty)/10)
            seznam_hodnot.append(hodnota)
        global hodnoty
        hodnoty = tk.StringVar()
        hodnoty.set(seznam_hodnot[0]) 
        strankovac = tk.OptionMenu(prihl_okno, hodnoty, *seznam_hodnot, command=kontakty_funkce)     
        strankovac.grid(row=4, column=0, columnspan=3)
           
        if len(kontakty)==0:
            kontakt = tk.Label(prihl_okno, text=u"Nemáte žádný uložený kontakt")
            kontakt.grid(row=5, column=0, columnspan=3)
        else:
            global kontakt1_zkratka
            global kontakt1_jmeno
            global kontakt1_cislo
            global kontakt2_zkratka
            global kontakt2_jmeno
            global kontakt2_cislo
            global kontakt3_zkratka
            global kontakt3_jmeno
            global kontakt3_cislo
            global kontakt4_zkratka
            global kontakt4_jmeno
            global kontakt4_cislo
            global kontakt5_zkratka
            global kontakt5_jmeno
            global kontakt5_cislo
            global kontakt6_zkratka
            global kontakt6_jmeno
            global kontakt6_cislo
            global kontakt7_zkratka
            global kontakt7_jmeno
            global kontakt7_cislo
            global kontakt8_zkratka
            global kontakt8_jmeno
            global kontakt8_cislo
            global kontakt9_zkratka
            global kontakt9_jmeno
            global kontakt9_cislo
            global kontakt10_zkratka
            global kontakt10_jmeno
            global kontakt10_cislo
            kontakt1_zkratka = tk.Label(prihl_okno, text=kontakty[0][0])
            kontakt1_zkratka.grid(row=5, column=0)
            kontakt1_jmeno = tk.Label(prihl_okno, text=kontakty[0][1])
            kontakt1_jmeno.grid(row=5, column=1)
            kontakt1_cislo = tk.Label(prihl_okno, text=kontakty[0][2])
            kontakt1_cislo.grid(row=5, column=2)
            kontakt2_zkratka = tk.Label(prihl_okno, text=kontakty[1][0])
            kontakt2_zkratka.grid(row=6, column=0)
            kontakt2_jmeno = tk.Label(prihl_okno, text=kontakty[1][1])
            kontakt2_jmeno.grid(row=6, column=1)
            kontakt2_cislo = tk.Label(prihl_okno, text=kontakty[1][2])
            kontakt2_cislo.grid(row=6, column=2)
            kontakt3_zkratka = tk.Label(prihl_okno, text=kontakty[2][0])
            kontakt3_zkratka.grid(row=7, column=0)
            kontakt3_jmeno = tk.Label(prihl_okno, text=kontakty[2][1])
            kontakt3_jmeno.grid(row=7, column=1)
            kontakt3_cislo = tk.Label(prihl_okno, text=kontakty[2][2])
            kontakt3_cislo.grid(row=7, column=2)
            kontakt4_zkratka = tk.Label(prihl_okno, text=kontakty[3][0])
            kontakt4_zkratka.grid(row=8, column=0)
            kontakt4_jmeno = tk.Label(prihl_okno, text=kontakty[3][1])
            kontakt4_jmeno.grid(row=8, column=1)
            kontakt4_cislo = tk.Label(prihl_okno, text=kontakty[3][2])
            kontakt4_cislo.grid(row=8, column=2)
            kontakt5_zkratka = tk.Label(prihl_okno, text=kontakty[4][0])
            kontakt5_zkratka.grid(row=9, column=0)
            kontakt5_jmeno = tk.Label(prihl_okno, text=kontakty[4][1])
            kontakt5_jmeno.grid(row=9, column=1)
            kontakt5_cislo = tk.Label(prihl_okno, text=kontakty[4][2])
            kontakt5_cislo.grid(row=9, column=2)
            kontakt6_zkratka = tk.Label(prihl_okno, text=kontakty[5][0])
            kontakt6_zkratka.grid(row=10, column=0)
            kontakt6_jmeno = tk.Label(prihl_okno, text=kontakty[5][1])
            kontakt6_jmeno.grid(row=10, column=1)
            kontakt6_cislo = tk.Label(prihl_okno, text=kontakty[5][2])
            kontakt6_cislo.grid(row=10, column=2)
            kontakt7_zkratka = tk.Label(prihl_okno, text=kontakty[6][0])
            kontakt7_zkratka.grid(row=11, column=0)
            kontakt7_jmeno = tk.Label(prihl_okno, text=kontakty[6][1])
            kontakt7_jmeno.grid(row=11, column=1)
            kontakt7_cislo = tk.Label(prihl_okno, text=kontakty[6][2])
            kontakt7_cislo.grid(row=11, column=2)
            kontakt8_zkratka = tk.Label(prihl_okno, text=kontakty[7][0])
            kontakt8_zkratka.grid(row=12, column=0)
            kontakt8_jmeno = tk.Label(prihl_okno, text=kontakty[7][1])
            kontakt8_jmeno.grid(row=12, column=1)
            kontakt8_cislo = tk.Label(prihl_okno, text=kontakty[7][2])
            kontakt8_cislo.grid(row=12, column=2)
            kontakt9_zkratka = tk.Label(prihl_okno, text=kontakty[8][0])
            kontakt9_zkratka.grid(row=13, column=0)
            kontakt9_jmeno = tk.Label(prihl_okno, text=kontakty[8][1])
            kontakt9_jmeno.grid(row=13, column=1)
            kontakt9_cislo = tk.Label(prihl_okno, text=kontakty[8][2])
            kontakt9_cislo.grid(row=13, column=2)
            kontakt10_zkratka = tk.Label(prihl_okno, text=kontakty[9][0])
            kontakt10_zkratka.grid(row=14, column=0)
            kontakt10_jmeno = tk.Label(prihl_okno, text=kontakty[9][1])
            kontakt10_jmeno.grid(row=14, column=1)
            kontakt10_cislo = tk.Label(prihl_okno, text=kontakty[9][2])
            kontakt10_cislo.grid(row=14, column=2)
            prihl_okno.mainloop()
aktualni_hodnota = hodnoty.get()           


def kontakty_funkce(aktualni_hodnota):
    global seznam_hodnot
    global kontakty
    global hodnoty
    global kontakt1_zkratka
    global kontakt1_jmeno
    global kontakt1_cislo
    global kontakt2_zkratka
    global kontakt2_jmeno
    global kontakt2_cislo
    global kontakt3_zkratka
    global kontakt3_jmeno
    global kontakt3_cislo
    global kontakt4_zkratka
    global kontakt4_jmeno
    global kontakt4_cislo
    global kontakt5_zkratka
    global kontakt5_jmeno
    global kontakt5_cislo
    global kontakt6_zkratka
    global kontakt6_jmeno
    global kontakt6_cislo
    global kontakt7_zkratka
    global kontakt7_jmeno
    global kontakt7_cislo
    global kontakt8_zkratka
    global kontakt8_jmeno
    global kontakt8_cislo
    global kontakt9_zkratka
    global kontakt9_jmeno
    global kontakt9_cislo
    global kontakt10_zkratka
    global kontakt10_jmeno
    global kontakt10_cislo
    strana = -1
    for i in seznam_hodnot:
        strana = strana+1
        if i == hodnoty.get():
            pozice = strana * 10
            kontakt1_zkratka["text"] = kontakty[pozice][0]
            kontakt1_jmeno["text"] = kontakty[pozice][1]
            kontakt1_cislo["text"] = kontakty[pozice][2]
            kontakt2_zkratka["text"] = kontakty[pozice+1][0]
            kontakt2_jmeno["text"] = kontakty[pozice+1][1]
            kontakt2_cislo["text"] = kontakty[pozice+1][2]
            kontakt3_zkratka["text"] = kontakty[pozice+2][0]
            kontakt3_jmeno["text"] = kontakty[pozice+2][1]
            kontakt3_cislo["text"] = kontakty[pozice+2][2]
            kontakt4_zkratka["text"] = kontakty[pozice+3][0]
            kontakt4_jmeno["text"] = kontakty[pozice+3][1]
            kontakt4_cislo["text"] = kontakty[pozice+3][2]
            kontakt5_zkratka["text"] = kontakty[pozice+4][0]
            kontakt5_jmeno["text"] = kontakty[pozice+4][1]
            kontakt5_cislo["text"] = kontakty[pozice+4][2]
            kontakt6_zkratka["text"] = kontakty[pozice+5][0]
            kontakt6_jmeno["text"] = kontakty[pozice+5][1]
            kontakt6_cislo["text"] = kontakty[pozice+5][2]
            kontakt7_zkratka["text"] = kontakty[pozice+6][0]
            kontakt7_jmeno["text"] = kontakty[pozice+6][1]
            kontakt7_cislo["text"] = kontakty[pozice+6][2]
            kontakt8_zkratka["text"] = kontakty[pozice+7][0]
            kontakt8_jmeno["text"] = kontakty[pozice+7][1]
            kontakt8_cislo["text"] = kontakty[pozice+7][2]
            kontakt9_zkratka["text"] = kontakty[pozice+8][0]
            kontakt9_jmeno["text"] = kontakty[pozice+8][1]
            kontakt9_cislo["text"] = kontakty[pozice+8][2]
            kontakt10_zkratka["text"] = kontakty[pozice+9][0]
            kontakt10_jmeno["text"] = kontakty[pozice+9][1]
            kontakt10_cislo["text"] = kontakty[pozice+9][2]



def odebrat(kontakty):
    pass
        



def pridat(zkratka_entry, cislo_entry, jmeno_entry):
    zkratka = zkratka_entry.get()
    cislo = cislo_entry.get()
    jmeno = jmeno_entry.get()
    dalsi_udaje = urllib.urlencode({'shortcut': zkratka, 'name': jmeno, 'number': cislo})
    celkove_udaje = udaje+"&"+dalsi_udaje
    pridani = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json"+celkove_udaje)
    print pridani
    print pridani.read()
    print dalsi_udaje


def doplnit(zkratka_entry, cislo_entry, jmeno_entry, kontakty):  ## doplní ostatní údaje do entry v hlavičce
    jmeno = jmeno_entry.get()
    cislo = cislo_entry.get()
    zkratka = zkratka_entry.get()
    if len(zkratka) > 0:            ## pokud je vyplněna zkratka doplní jmeno a cislo
        for i in kontakty:
            if str(i[0]) == zkratka:
                jmeno_entry.delete(0, tk.END)
                jmeno_entry.insert(tk.INSERT, i[1])
                cislo_entry.delete(0, tk.END)
                cislo_entry.insert(tk.INSERT, i[2])
    elif len(jmeno) > 0:            ##doplnene jmeno .. doplni zkratku a cislo
        for i in kontakty:
            if str(i[1]) == jmeno:
                zkratka_entry.delete(0, tk.END)
                zkratka_entry.insert(tk.INSERT, i[0])
                cislo_entry.delete(0, tk.END)
                cislo_entry.insert(tk.INSERT, i[2])
    elif len(cislo) > 0:            ## napodobe ale je vyplnene cislo
        for i in kontakty:
            if str(i[2]) == cislo:
                zkratka_entry.delete(0, tk.END)
                zkratka_entry.insert(tk.INSERT, i[0])
                jmeno_entry.delete(0, tk.END)
                jmeno_entry.insert(tk.INSERT, i[1])
    elif len(jmeno) > 0:
         for i in kontakty:
            if str(i[3]) == jmeno:
                zkratka_entry.delete(0, tk.END)
                zkratka_entry.insert(tk.INSERT, i[0])
                jmeno_entry.delete(0, tk.END)
                jmeno_entry.insert(tk.INSERT, i[1])
    else:
        print "CHYBAasad"


def smazat(zkratka_entry, jmeno_entry, cislo_entry):        ##po kliknutí na tlačítko smazat
    zkratka_entry.delete(0, tk.END)
    jmeno_entry.delete(0, tk.END)
    cislo_entry.delete(0, tk.END)


def callback(cislo_entry, jmeno_entry,):                 ##vyvolá okno po kliknutí na tlačítko callback
    callback_okno = tk.Tk()
    callback_okno.title("Callback")
    if len(jmeno_entry.get())>0:
        komu_volat = cislo_entry.get()+" ("+str(jmeno_entry.get())+")"
    else:
        komu_volat = cislo_entry.get()
    callback_label = tk.Label(callback_okno, text="Volání na:  "+komu_volat)
    callback_label.grid(columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
    moje_cislo_label = tk.Label(callback_okno, text="Moje číslo:")
    moje_cislo_label.grid(row=1, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
    moje_cislo_entry = tk.Entry(callback_okno)
    moje_cislo_entry.grid(row=2, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
    cislo_ulozit_button = tk.Button(callback_okno, text="Uložit", command=lambda: ulozit_moje_cislo(moje_cislo_entry))
    cislo_ulozit_button.grid(row=3, sticky=tk.E+tk.W+tk.N+tk.S)
    cislo_vyplnit_button = tk.Button(callback_okno, text="Vyplnit", command=lambda: vyplnit_moje_cislo(moje_cislo_entry))
    cislo_vyplnit_button.grid(row=3, column=1, sticky=tk.E+tk.W+tk.N+tk.S)
    objednat_callback_button = tk.Button(callback_okno, text="Objednat callback", command=lambda: objednat_callback(moje_cislo_entry, cislo_entry, udaje))
    objednat_callback_button.grid(row=4, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
    spozdeny_callback_label = tk.Label(callback_okno, text="Obejdnat spoždený callback" )
    spozdeny_callback_label.grid(row=5, sticky=tk.E+tk.W+tk.N+tk.S, columnspan=2)
    datum_callback_label = tk.Label(callback_okno, text="Datum (YYYY-MM-DD)")
    datum_callback_label.grid(row=6)
    datum_cas_callback_label = tk.Label(callback_okno, text=u"Čas (HH:MM:SS)")
    datum_cas_callback_label.grid(row=6, column=1)
    datum_callback_entry = tk.Entry(callback_okno)
    datum_callback_entry.grid(row=7)
    datum_cas_callback_entry = tk.Entry(callback_okno)
    datum_cas_callback_entry.grid(row=7, column=1)
    datum_callback_button = tk.Button(callback_okno, text="Objednat dle data", command=lambda: callback_datum(moje_cislo_entry, cislo_entry, udaje, datum_callback_entry, datum_cas_callback_entry))
    datum_callback_button.grid(row=8, columnspan=2)
    minuty_callback_label = tk.Label(callback_okno, text=u"Spoždění (minuty)")
    minuty_callback_label.grid(row=9, columnspan=2)
    minuty_callback_entry = tk.Entry(callback_okno)
    minuty_callback_entry.grid(row=10, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
    minuty_callback_button = tk.Button(callback_okno,text="Objednat dle spoždění", command= lambda: callback_cas(moje_cislo_entry, cislo_entry, udaje, minuty_callback_entry))
    minuty_callback_button.grid(row=11, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
    callback_okno.mainloop()


def ulozit_moje_cislo(moje_cislo_entry):
    cislo_soubor = open("cislo.txt", "w")
    cislo_soubor.write(moje_cislo_entry.get())
    cislo_soubor.close()
    
    
def vyplnit_moje_cislo(moje_cislo_entry):
    cislo_soubor = open("cislo.txt", "r")
    cislo = cislo_soubor.readline()
    moje_cislo_entry.delete(0, tk.END)
    moje_cislo_entry.insert(tk.END, cislo)


def callback_cas(moje_cislo_entry, cislo_entry, udaje, minuty_callback_entry):
    moje_cislo = moje_cislo_entry.get()
    volane_cislo = cislo_entry.get()
    minuty = minuty_callback_entry.get()
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo, 'delayed': minuty})
    vsechny_udaje = udaje+"&"+cisla
    objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
    odpoved = objednat_callback.read()
    if odpoved == "successfully_enqueued":
        tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
    elif odpoved == "error callback_failed":
        tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
    elif odpoved == "error invalid_delay_format":
        tkm.showwarning("CHYBA", u"Byl zadán špatný formát spoždění")


def callback_datum(moje_cislo_entry, cislo_entry, udaje, datum_callback_entry, datum_cas_callback_entry):
    moje_cislo = moje_cislo_entry.get()
    volane_cislo = cislo_entry.get()
    datum = datum_callback_entry.get()+"T"+datum_cas_callback_entry.get()+"+01:00"
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo, 'delayed': datum})
    vsechny_udaje = udaje+"&"+cisla
    objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
    odpoved =  objednat_callback.read()
    print odpoved
    if odpoved == "successfully_enqueued":
        tkm.showinfo("Callback" ,u"Callback byl úspěšně objednán")
    elif odpoved == "error callback_failed":
        tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
    elif odpoved == "error invalid_delay_format":
        tkm.showwarning("CHYBA", u"Datum nebo čas zadáno ve špatném formátu")
    elif odpoved == "error delayed_into_past":
        tkm.showwarning("CHYBA", u"Zadaný moment již proběhl")



def objednat_callback(moje_cislo_entry, cislo_entry, udaje):  ##objedná callback
    moje_cislo = moje_cislo_entry.get()
    volane_cislo = cislo_entry.get()
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo})
    vsechny_udaje = udaje+"&"+cisla
    objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
    odpoved =  objednat_callback.read()
    print odpoved
    if odpoved == "callback_ordered":
        tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
    elif odpoved == "error callback_failed":
        tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
    

#############################################################################


def ulozit_udaje():             # uloží údaje
    jmeno = prihl_jmeno_entry.get()
    heslo = heslo_entry.get()
    jmeno_soubor = open("jmeno.txt", "w")
    heslo_soubor = open("heslo.txt", "w")
    jmeno_soubor.write(jmeno)
    heslo_soubor.write(heslo)
    jmeno_soubor.close()
    heslo_soubor.close()


def vyplnit_udaje():
    jmeno_soubor = open("jmeno.txt", "r")
    heslo_soubor = open("heslo.txt", "r")
    jmeno = jmeno_soubor.readline()
    heslo = heslo_soubor.readline()
    prihl_jmeno_entry.delete(0, tk.END)
    heslo_entry.delete(0, tk.END)
    prihl_jmeno_entry.insert(tk.END, jmeno)
    heslo_entry.insert(tk.END, heslo)

##############################################################################
##############################################################################

hl_okno = tk.Tk()                   ##Úvodní přihlašovací okno
hl_okno.title("Odorik.cz")

prihl_jmeno_label = tk.Label(hl_okno, text="Jméno")
prihl_jmeno_label.grid()

prihl_jmeno_entry = tk.Entry(hl_okno, justify="center")
prihl_jmeno_entry.grid(row=1)

heslo_label = tk.Label(hl_okno, text="Heslo")
heslo_label.grid(row=2)

heslo_entry = tk.Entry(hl_okno, justify="center")
heslo_entry.grid(row=3)

prihlaseni_button = tk.Button(hl_okno, text="Přihlásit", command=prihlasit, width=10)
prihlaseni_button.grid(row=4)

ulozeni_udaju_button = tk.Button(hl_okno, text="Uložit údaje", command=ulozit_udaje, width=10)
ulozeni_udaju_button.grid(row=5)

vyplneni_udaju_button = tk.Button(hl_okno, text="Vyplnit údaje", command=vyplnit_udaje, width=10)
vyplneni_udaju_button.grid(row=6)

hl_okno.mainloop()
