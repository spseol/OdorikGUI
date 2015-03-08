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
        pridat_button = tk.Button(frame_na_buttony, text="přidat")
        pridat_button.grid(row=0, column=2, sticky=tk.E+tk.W+tk.N+tk.S)
        odebrat_button = tk.Button(frame_na_buttony, text="odebrat")
        odebrat_button.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S)
        callback_button = tk.Button(frame_na_buttony, text="Objednat callback", command=lambda: callback(cislo_entry, jmeno_entry,)) 
        callback_button.grid(row=0, column=4, sticky=tk.E+tk.W+tk.N+tk.S)
        prihl_okno.mainloop()
        

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
