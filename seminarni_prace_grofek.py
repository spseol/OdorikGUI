# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:04:50 2015

@author: Tom
"""
import urllib
import Tkinter as tk
##############################################################################
##############################################################################


def vypsat(kontakty):
     return kontakty["shortcut"], kontakty["name"], kontakty["number"]


def prihlasit():
    jmeno = jmeno_entry.get()
    heslo = heslo_entry.get()
    udaje = urllib.urlencode({"user": jmeno, "password": heslo})            ## přihlašovací údaje jako parametr
    kredit_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/balance?"+udaje) ## získání kreditu
    kredit = kredit_mezikrok.read()         ## kredit jako řetězec
    kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje) ##získání kontaktů
    kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
    kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)          ##kontakty jako seznam
    if kredit == "error authentication_failed":     ##špatně zadané údaje
        chybne_prihl_okno = tk.Tk()
        chybne_prihl_okno.title("Chyba!!")
        chybne_prihl_label = tk.Label(chybne_prihl_okno, text=u"Špatně zadané  přihlašovací údaje!!")
        chybne_prihl_label.pack()
        chybne_prihl_okno.mainloop()
    else:                                           ## dobře zadané údaje
        """hl_okno.quit()"""                        ## proč nefunguje?! 
        prihl_okno = tk.Tk()
        kredit_label = tk.Label(prihl_okno, text="Váš kredit je: "+kredit+"Kč")   ##vypisuje kredit
        kredit_label.grid(columnspan=3)
        zkratka_label = tk.Label(prihl_okno, text="Zkratka")                    ##záhlaví callbacku
        zkratka_label.grid(row=1)
        jmeno_label = tk.Label(prihl_okno, text=u"Jméno")
        jmeno_label.grid(row=1, column=1)
        cislo_label = tk.Label(prihl_okno, text=u"Číslo")
        cislo_label.grid(row=1, column=2)
        zkratka_vstup = tk.Entry(prihl_okno)                                    ##vstupy 
        zkratka_vstup.grid(row=2)
        jmeno_vstup = tk.Entry(prihl_okno)
        jmeno_vstup.grid(row=2, column=1)
        cislo_vstup = tk.Entry(prihl_okno)
        cislo_vstup.grid(row=2, column=2)
        doplnit_button = tk.Button(prihl_okno, text="Doplnit")                  ## tlacitka pod vstupy
        doplnit_button.grid(row=3)
        callback_button = tk.Button(prihl_okno, text="Objednat callback")
        callback_button.grid(row=3, columnspan=2, column=2)
        prihl_okno.mainloop()


def ulozit_udaje():             # uloží údaje
    jmeno = jmeno_entry.get()
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
    jmeno_entry.delete(0, tk.END)
    heslo_entry.delete(0, tk.END)
    jmeno_entry.insert(tk.END, jmeno)
    heslo_entry.insert(tk.END, heslo)

##############################################################################
##############################################################################

hl_okno = tk.Tk()                   ##Úvodní přihlašovací okno
hl_okno.title("Odorik.cz")

jmeno_label = tk.Label(hl_okno, text="Jméno")
jmeno_label.grid()

jmeno_entry = tk.Entry(hl_okno, justify="center")
jmeno_entry.grid(row=1)

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
