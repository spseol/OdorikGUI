# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:04:50 2015
@author: Tom
"""
import json
import urllib
import Tkinter as tk
import tkMessageBox as tkm
import httplib
import datetime
##############################################################################
##############################################################################
def erory(odpoved):
    return odpoved["errors"]


def uspech(odpoved):
    return odpoved["name"]

def vypsat(kontakty):                   ##získá kontakty ve formátu json
     return kontakty["shortcut"], kontakty["name"], kontakty["number"]


def datum_cislo_cena(posl_hovor):
    return posl_hovor["date"], posl_hovor["destination_number"], posl_hovor["price"]


def prihlasit():
    ulozit_udaje()
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
        dnes = datetime.datetime.now()
        mesic = "%d" % dnes.month
        mesic = int(mesic)
        if mesic == 1:
            prmesic = 12
        else:
            prmesic = mesic-1
        if prmesic <10:
            prmesic = "0"+str(prmesic)
        dnes = str(dnes)
        do = dnes[:10]+"T"+dnes[11:19]+"Z"
        od = do[:5]+str(prmesic)+do[7:]
        posl_hovor_url = "https://www.odorik.cz/api/v1/calls.json?"+"user="+prihl_jmeno+"&password="+heslo+"&from="+od+"&to="+do+"&direction=out"
        zjistit_posl_hovor = urllib.urlopen(posl_hovor_url)
        posl_hovor_mezikrok = zjistit_posl_hovor.read()
        posl_hovor_mezikrok2=json.loads(posl_hovor_mezikrok,object_hook=datum_cislo_cena)
        posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-1]
        posl_hovor_cena = "%.2f"%(posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-1][2])
        posl_hovor_datum = "%s %s.%s.%s"%(posl_hovor[0][11:19], posl_hovor[0][8:10], posl_hovor[0][5:7], posl_hovor[0][:4])
        posl_hovor_cislo = posl_hovor[1][(len(posl_hovor[1])-9):]        
        uplne_hl_okno.destroy()
        kontakty_okno = tk.Tk()
        prihl_okno = tk.Frame(kontakty_okno, bg="#32CD32")
        prihl_okno.grid()
        kontakty_okno.title("Kontakty")
############################################################################### horní informace
        info_frame = tk.Frame(prihl_okno, bg="#32CD32")        
        kredit_label = tk.Label(info_frame, text="Váš kredit je: "+kredit+"Kč", bg="#32CD32", font="Arial_black 10 bold")   ##vypisuje kredit
        kredit_label.grid(columnspan=3, sticky=tk.W)
        posledni_hovor_frame = tk.Frame(info_frame, bg="#32CD32",bd=1)
        posledni_hovor_label = tk.Label(posledni_hovor_frame, text="Poslední hovor:", bg="#32CD32", font="Arial_black 15 bold")
        posledni_hovor_label.grid(row=1, columnspan=3)
        posl_hov_datum = tk.Label(posledni_hovor_frame, text="Datum", width=20, bg="#32CD32", font="Arial_black 10 bold")
        posl_hov_datum.grid(row=2)
        posl_hov_cislo = tk.Label(posledni_hovor_frame, text="Číslo", width=20, bg="#32CD32", font="Arial_black 10 bold")
        posl_hov_cislo.grid(row=2, column=1)
        posl_hov_cena = tk.Label(posledni_hovor_frame, text="Cena", width=20, bg="#32CD32", font="Arial_black 10 bold")
        posl_hov_cena.grid(row=2, column=2)
        posl_hov_datum1 = tk.Label(posledni_hovor_frame, text=posl_hovor_datum, width=20, bg="#32CD32", font="Arial_black 8 bold")
        posl_hov_datum1.grid(row=3)
        posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text=posl_hovor_cislo, width=20, bg="#32CD32", font="Arial_black 8 bold")
        posl_hov_cislo1.grid(row=3, column=1)
        posl_hov_cena1 = tk.Label(posledni_hovor_frame, text=str(posl_hovor_cena)+"Kč", width=20, bg="#32CD32", font="Arial_black 8 bold")
        posl_hov_cena1.grid(row=3, column=2)
        posledni_hovor_frame.grid(pady=20)
        info_frame.grid( columnspan=3)
########################################################################### vstupy       
        zkratka_label = tk.Label(prihl_okno, text="Zkratka", bg="#32CD32", font="Arial_black 10 bold")                    ##záhlaví callbacku
        zkratka_label.grid(row=1, column=0)
        jmeno_label = tk.Label(prihl_okno, text=u"Jméno", bg="#32CD32", font="Arial_black 10 bold")
        jmeno_label.grid(row=1, column=1)
        cislo_label = tk.Label(prihl_okno, text=u"Číslo", bg="#32CD32", font="Arial_black 10 bold")
        cislo_label.grid(row=1, column=2)
        zkratka_entry = tk.Entry(prihl_okno, bg="#99FF99", relief="groove", justify="center")                                    
        zkratka_entry.grid(row=2)
        jmeno_entry = tk.Entry(prihl_okno, bg="#99FF99", relief="groove", justify="center")
        jmeno_entry.grid(row=2, column=1)
        cislo_entry = tk.Entry(prihl_okno, bg="#99FF99", relief="groove", justify="center")
        cislo_entry.grid(row=2, column=2)
########################################################################### tlačítka pod vstupy
        frame_na_buttony = tk.Frame(prihl_okno, bg="#32CD32")
        frame_na_buttony.grid(row=3, padx=10, columnspan=3) 
        doplnit_button = tk.Button(frame_na_buttony, text="Doplnit pole", font="Arial_black 8 bold", activebackground="#99FF99", command=lambda: doplnit(zkratka_entry, cislo_entry, jmeno_entry), bg="#409940")                  ## tlacitka pod vstupy
        doplnit_button.grid(row=0, column=0, pady=10)
        smazat_button = tk.Button(frame_na_buttony, text="Smazat pole", font="Arial_black 8 bold", activebackground="#99FF99", command=lambda: smazat(zkratka_entry, cislo_entry, jmeno_entry), bg="#409940")
        smazat_button.grid(column=1, row=0, pady=10, padx= 20)
        pridat_button = tk.Button(frame_na_buttony, text="Přidat kontakt", font="Arial_black 8 bold", activebackground="#99FF99", command=lambda: pridat(zkratka_entry, cislo_entry, jmeno_entry), bg="#409940")
        pridat_button.grid(row=0, column=2, padx=20, sticky=tk.E)
        odebrat_button = tk.Button(frame_na_buttony, text="Odebrat kontakt", font="Arial_black 8 bold", activebackground="#99FF99", command=lambda: odebrat(zkratka_entry), bg="#409940")
        odebrat_button.grid(row=0, column=3, sticky=tk.E)
        callback_button = tk.Button(frame_na_buttony, text="Objednat callback", font="Arial_black 8 bold", activebackground="#99FF99", command=lambda: callback(cislo_entry, jmeno_entry,), bg="#409940")
        callback_button.grid(row=1, column=0, columnspan=4, padx=40, sticky=tk.E+tk.W+tk.N+tk.S)
        global seznam_hodnot
        seznam_hodnot = []
        for i in range(1+len(kontakty)/10):
            hodnota = "Strana"+str(i+1)+"/"+str(1+len(kontakty)/10)
            seznam_hodnot.append(hodnota)
        global hodnoty
        hodnoty = tk.StringVar()
        hodnoty.set(seznam_hodnot[0]) 
        strankovac = tk.OptionMenu(prihl_okno, hodnoty, *seznam_hodnot, command=kontakty_funkce)
        strankovac["background"] = "#409940"
        strankovac["activebackground"] = "#99FF99"
        strankovac["font"] = "Arial_black 8 bold"
        strankovac["highlightbackground"] = "#99FF99"

        
        strankovac.grid(row=4, column=0, columnspan=3, pady=15)
           
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
            kontakt1_zkratka = tk.Label(prihl_okno, text=kontakty[0][0], bg="#99FF99", font="Arial_black 8 bold")
            kontakt1_zkratka.grid(row=5, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt1_jmeno = tk.Label(prihl_okno, text=kontakty[0][1], bg="#99FF99", font="Arial_black 8 bold")
            kontakt1_jmeno.grid(row=5, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt1_cislo = tk.Label(prihl_okno, text=kontakty[0][2][-9:], bg="#99FF99", font="Arial_black 8 bold")
            kontakt1_cislo.grid(row=5, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt2_zkratka = tk.Label(prihl_okno, text=kontakty[1][0], bg="#32CD32", font="Arial_black 8 bold")
            kontakt2_zkratka.grid(row=6, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt2_jmeno = tk.Label(prihl_okno, text=kontakty[1][1], bg="#32CD32", font="Arial_black 8 bold")
            kontakt2_jmeno.grid(row=6, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt2_cislo = tk.Label(prihl_okno, text=kontakty[1][2][-9:], bg="#32CD32", font="Arial_black 8 bold")
            kontakt2_cislo.grid(row=6, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt3_zkratka = tk.Label(prihl_okno, text=kontakty[2][0], bg="#99FF99", font="Arial_black 8 bold")
            kontakt3_zkratka.grid(row=7, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt3_jmeno = tk.Label(prihl_okno, text=kontakty[2][1], bg="#99FF99", font="Arial_black 8 bold")
            kontakt3_jmeno.grid(row=7, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt3_cislo = tk.Label(prihl_okno, text=kontakty[2][2][-9:], bg="#99FF99", font="Arial_black 8 bold")
            kontakt3_cislo.grid(row=7, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt4_zkratka = tk.Label(prihl_okno, text=kontakty[3][0], bg="#32CD32", font="Arial_black 8 bold")
            kontakt4_zkratka.grid(row=8, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt4_jmeno = tk.Label(prihl_okno, text=kontakty[3][1], bg="#32CD32", font="Arial_black 8 bold")
            kontakt4_jmeno.grid(row=8, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt4_cislo = tk.Label(prihl_okno, text=kontakty[3][2][-9:], bg="#32CD32", font="Arial_black 8 bold")
            kontakt4_cislo.grid(row=8, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt5_zkratka = tk.Label(prihl_okno, text=kontakty[4][0], bg="#99FF99", font="Arial_black 8 bold")
            kontakt5_zkratka.grid(row=9, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt5_jmeno = tk.Label(prihl_okno, text=kontakty[4][1], bg="#99FF99", font="Arial_black 8 bold")
            kontakt5_jmeno.grid(row=9, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt5_cislo = tk.Label(prihl_okno, text=kontakty[4][2][-9:], bg="#99FF99", font="Arial_black 8 bold")
            kontakt5_cislo.grid(row=9, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt6_zkratka = tk.Label(prihl_okno, text=kontakty[5][0], bg="#32CD32", font="Arial_black 8 bold")
            kontakt6_zkratka.grid(row=10, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt6_jmeno = tk.Label(prihl_okno, text=kontakty[5][1], bg="#32CD32", font="Arial_black 8 bold")
            kontakt6_jmeno.grid(row=10, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt6_cislo = tk.Label(prihl_okno, text=kontakty[5][2][-9:], bg="#32CD32", font="Arial_black 8 bold")
            kontakt6_cislo.grid(row=10, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt7_zkratka = tk.Label(prihl_okno, text=kontakty[6][0], bg="#99FF99", font="Arial_black 8 bold")
            kontakt7_zkratka.grid(row=11, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt7_jmeno = tk.Label(prihl_okno, text=kontakty[6][1], bg="#99FF99", font="Arial_black 8 bold")
            kontakt7_jmeno.grid(row=11, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt7_cislo = tk.Label(prihl_okno, text=kontakty[6][2][-9:], bg="#99FF99", font="Arial_black 8 bold")
            kontakt7_cislo.grid(row=11, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt8_zkratka = tk.Label(prihl_okno, text=kontakty[7][0], bg="#32CD32", font="Arial_black 8 bold")
            kontakt8_zkratka.grid(row=12, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt8_jmeno = tk.Label(prihl_okno, text=kontakty[7][1], bg="#32CD32", font="Arial_black 8 bold")
            kontakt8_jmeno.grid(row=12, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt8_cislo = tk.Label(prihl_okno, text=kontakty[7][2][-9:], bg="#32CD32", font="Arial_black 8 bold")
            kontakt8_cislo.grid(row=12, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt9_zkratka = tk.Label(prihl_okno, text=kontakty[8][0], bg="#99FF99", font="Arial_black 8 bold")
            kontakt9_zkratka.grid(row=13, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt9_jmeno = tk.Label(prihl_okno, text=kontakty[8][1], bg="#99FF99", font="Arial_black 8 bold")
            kontakt9_jmeno.grid(row=13, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt9_cislo = tk.Label(prihl_okno, text=kontakty[8][2][-9:], bg="#99FF99", font="Arial_black 8 bold")
            kontakt9_cislo.grid(row=13, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt10_zkratka = tk.Label(prihl_okno, text=kontakty[9][0], bg="#32CD32", font="Arial_black 8 bold")
            kontakt10_zkratka.grid(row=14, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt10_jmeno = tk.Label(prihl_okno, text=kontakty[9][1], bg="#32CD32", font="Arial_black 8 bold")
            kontakt10_jmeno.grid(row=14, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakt10_cislo = tk.Label(prihl_okno, text=kontakty[9][2][-9:], bg="#32CD32", font="Arial_black 8 bold")
            kontakt10_cislo.grid(row=14, column=2, sticky=tk.E+tk.N+tk.W+tk.S)
            kontakty_okno.mainloop()
            global aktualni_hodnota
            aktualni_hodnota = hodnoty.get()           


def kontakty_funkce(aktualni_hodnota):
    global aktualni_honota
    global seznam_hodnot
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
    kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje)   ##získání kontaktů
    kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
    kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)
    strana = -1
    for i in seznam_hodnot:
        strana = strana+1
        if i == hodnoty.get():
            if len(seznam_hodnot)-strana != 1:
                pozice = strana*10
                kontakt1_zkratka["text"] = kontakty[pozice][0]
                kontakt1_jmeno["text"] = kontakty[pozice][1]
                kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                kontakt5_zkratka["text"] = kontakty[pozice+4][0]
                kontakt5_jmeno["text"] = kontakty[pozice+4][1]
                kontakt5_cislo["text"] = kontakty[pozice+4][2][-9:]
                kontakt6_zkratka["text"] = kontakty[pozice+5][0]
                kontakt6_jmeno["text"] = kontakty[pozice+5][1]
                kontakt6_cislo["text"] = kontakty[pozice+5][2][-9:]
                kontakt7_zkratka["text"] = kontakty[pozice+6][0]
                kontakt7_jmeno["text"] = kontakty[pozice+6][1]
                kontakt7_cislo["text"] = kontakty[pozice+6][2][-9:]
                kontakt8_zkratka["text"] = kontakty[pozice+7][0]
                kontakt8_jmeno["text"] = kontakty[pozice+7][1]
                kontakt8_cislo["text"] = kontakty[pozice+7][2][-9:]
                kontakt9_zkratka["text"] = kontakty[pozice+8][0]
                kontakt9_jmeno["text"] = kontakty[pozice+8][1]
                kontakt9_cislo["text"] = kontakty[pozice+8][2][-9:]
                kontakt10_zkratka["text"] = kontakty[pozice+9][0]
                kontakt10_jmeno["text"] = kontakty[pozice+9][1]
                kontakt10_cislo["text"] = kontakty[pozice+9][2][-9:]
            else:
                posledni_strana = len(kontakty)%10
                pozice = strana*10
                if posledni_strana == 1:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = ""
                    kontakt2_jmeno["text"] = ""
                    kontakt2_cislo["text"] = ""
                    kontakt3_zkratka["text"] = ""
                    kontakt3_jmeno["text"] = ""
                    kontakt3_cislo["text"] = ""
                    kontakt4_zkratka["text"] = ""
                    kontakt4_jmeno["text"] = ""
                    kontakt4_cislo["text"] = ""
                    kontakt5_zkratka["text"] = ""
                    kontakt5_jmeno["text"] = ""
                    kontakt5_cislo["text"] = ""
                    kontakt6_zkratka["text"] = ""
                    kontakt6_jmeno["text"] = ""
                    kontakt6_cislo["text"] = ""
                    kontakt7_zkratka["text"] = ""
                    kontakt7_jmeno["text"] = ""
                    kontakt7_cislo["text"] = ""
                    kontakt8_zkratka["text"] = ""
                    kontakt8_jmeno["text"] = ""
                    kontakt8_cislo["text"] = ""
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana == 2:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = ""
                    kontakt3_jmeno["text"] = ""
                    kontakt3_cislo["text"] = ""
                    kontakt4_zkratka["text"] = ""
                    kontakt4_jmeno["text"] = ""
                    kontakt4_cislo["text"] = ""
                    kontakt5_zkratka["text"] = ""
                    kontakt5_jmeno["text"] = ""
                    kontakt5_cislo["text"] = ""
                    kontakt6_zkratka["text"] = ""
                    kontakt6_jmeno["text"] = ""
                    kontakt6_cislo["text"] = ""
                    kontakt7_zkratka["text"] = ""
                    kontakt7_jmeno["text"] = ""
                    kontakt7_cislo["text"] = ""
                    kontakt8_zkratka["text"] = ""
                    kontakt8_jmeno["text"] = ""
                    kontakt8_cislo["text"] = ""
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana == 3:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = ""
                    kontakt4_jmeno["text"] = ""
                    kontakt4_cislo["text"] = ""
                    kontakt5_zkratka["text"] = ""
                    kontakt5_jmeno["text"] = ""
                    kontakt5_cislo["text"] = ""
                    kontakt6_zkratka["text"] = ""
                    kontakt6_jmeno["text"] = ""
                    kontakt6_cislo["text"] = ""
                    kontakt7_zkratka["text"] = ""
                    kontakt7_jmeno["text"] = ""
                    kontakt7_cislo["text"] = ""
                    kontakt8_zkratka["text"] = ""
                    kontakt8_jmeno["text"] = ""
                    kontakt8_cislo["text"] = ""
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana == 4:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                    kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                    kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                    kontakt5_zkratka["text"] = ""
                    kontakt5_jmeno["text"] = ""
                    kontakt5_cislo["text"] = ""
                    kontakt6_zkratka["text"] = ""
                    kontakt6_jmeno["text"] = ""
                    kontakt6_cislo["text"] = ""
                    kontakt7_zkratka["text"] = ""
                    kontakt7_jmeno["text"] = ""
                    kontakt7_cislo["text"] = ""
                    kontakt8_zkratka["text"] = ""
                    kontakt8_jmeno["text"] = ""
                    kontakt8_cislo["text"] = ""
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana == 5:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                    kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                    kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                    kontakt5_zkratka["text"] = kontakty[pozice+4][0]
                    kontakt5_jmeno["text"] = kontakty[pozice+4][1]
                    kontakt5_cislo["text"] = kontakty[pozice+4][2][-9:]
                    kontakt6_zkratka["text"] = ""
                    kontakt6_jmeno["text"] = ""
                    kontakt6_cislo["text"] = ""
                    kontakt7_zkratka["text"] = ""
                    kontakt7_jmeno["text"] = ""
                    kontakt7_cislo["text"] = ""
                    kontakt8_zkratka["text"] = ""
                    kontakt8_jmeno["text"] = ""
                    kontakt8_cislo["text"] = ""
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana == 6:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                    kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                    kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                    kontakt5_zkratka["text"] = kontakty[pozice+4][0]
                    kontakt5_jmeno["text"] = kontakty[pozice+4][1]
                    kontakt5_cislo["text"] = kontakty[pozice+4][2][-9:]
                    kontakt6_zkratka["text"] = kontakty[pozice+5][0]
                    kontakt6_jmeno["text"] = kontakty[pozice+5][1]
                    kontakt6_cislo["text"] = kontakty[pozice+5][2][-9:]
                    kontakt7_zkratka["text"] = ""
                    kontakt7_jmeno["text"] = ""
                    kontakt7_cislo["text"] = ""
                    kontakt8_zkratka["text"] = ""
                    kontakt8_jmeno["text"] = ""
                    kontakt8_cislo["text"] = ""
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana ==7:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                    kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                    kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                    kontakt5_zkratka["text"] = kontakty[pozice+4][0]
                    kontakt5_jmeno["text"] = kontakty[pozice+4][1]
                    kontakt5_cislo["text"] = kontakty[pozice+4][2][-9:]
                    kontakt6_zkratka["text"] = kontakty[pozice+5][0]
                    kontakt6_jmeno["text"] = kontakty[pozice+5][1]
                    kontakt6_cislo["text"] = kontakty[pozice+5][2][-9:]
                    kontakt7_zkratka["text"] = kontakty[pozice+6][0]
                    kontakt7_jmeno["text"] = kontakty[pozice+6][1]
                    kontakt7_cislo["text"] = kontakty[pozice+6][2][-9:]
                    kontakt8_zkratka["text"] = ""
                    kontakt8_jmeno["text"] = ""
                    kontakt8_cislo["text"] = ""
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana == 8:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                    kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                    kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                    kontakt5_zkratka["text"] = kontakty[pozice+4][0]
                    kontakt5_jmeno["text"] = kontakty[pozice+4][1]
                    kontakt5_cislo["text"] = kontakty[pozice+4][2][-9:]
                    kontakt6_zkratka["text"] = kontakty[pozice+5][0]
                    kontakt6_jmeno["text"] = kontakty[pozice+5][1]
                    kontakt6_cislo["text"] = kontakty[pozice+5][2][-9:]
                    kontakt7_zkratka["text"] = kontakty[pozice+6][0]
                    kontakt7_jmeno["text"] = kontakty[pozice+6][1]
                    kontakt7_cislo["text"] = kontakty[pozice+6][2][-9:]
                    kontakt8_zkratka["text"] = kontakty[pozice+7][0]
                    kontakt8_jmeno["text"] = kontakty[pozice+7][1]
                    kontakt8_cislo["text"] = kontakty[pozice+7][2][-9:]
                    kontakt9_zkratka["text"] = ""
                    kontakt9_jmeno["text"] = ""
                    kontakt9_cislo["text"] = ""
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                elif posledni_strana == 9:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                    kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                    kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                    kontakt5_zkratka["text"] = kontakty[pozice+4][0]
                    kontakt5_jmeno["text"] = kontakty[pozice+4][1]
                    kontakt5_cislo["text"] = kontakty[pozice+4][2][-9:]
                    kontakt6_zkratka["text"] = kontakty[pozice+5][0]
                    kontakt6_jmeno["text"] = kontakty[pozice+5][1]
                    kontakt6_cislo["text"] = kontakty[pozice+5][2][-9:]
                    kontakt7_zkratka["text"] = kontakty[pozice+6][0]
                    kontakt7_jmeno["text"] = kontakty[pozice+6][1]
                    kontakt7_cislo["text"] = kontakty[pozice+6][2][-9:]
                    kontakt8_zkratka["text"] = kontakty[pozice+7][0]
                    kontakt8_jmeno["text"] = kontakty[pozice+7][1]
                    kontakt8_cislo["text"] = kontakty[pozice+7][2][-9:]
                    kontakt9_zkratka["text"] = kontakty[pozice+8][0]
                    kontakt9_jmeno["text"] = kontakty[pozice+8][1]
                    kontakt9_cislo["text"] = kontakty[pozice+8][2][-9:]
                    kontakt10_zkratka["text"] = ""
                    kontakt10_jmeno["text"] = ""
                    kontakt10_cislo["text"] = ""
                else:
                    kontakt1_zkratka["text"] = kontakty[pozice][0]
                    kontakt1_jmeno["text"] = kontakty[pozice][1]
                    kontakt1_cislo["text"] = kontakty[pozice][2][-9:]
                    kontakt2_zkratka["text"] = kontakty[pozice+1][0]
                    kontakt2_jmeno["text"] = kontakty[pozice+1][1]
                    kontakt2_cislo["text"] = kontakty[pozice+1][2][-9:]
                    kontakt3_zkratka["text"] = kontakty[pozice+2][0]
                    kontakt3_jmeno["text"] = kontakty[pozice+2][1]
                    kontakt3_cislo["text"] = kontakty[pozice+2][2][-9:]
                    kontakt4_zkratka["text"] = kontakty[pozice+3][0]
                    kontakt4_jmeno["text"] = kontakty[pozice+3][1]
                    kontakt4_cislo["text"] = kontakty[pozice+3][2][-9:]
                    kontakt5_zkratka["text"] = kontakty[pozice+4][0]
                    kontakt5_jmeno["text"] = kontakty[pozice+4][1]
                    kontakt5_cislo["text"] = kontakty[pozice+4][2][-9:]
                    kontakt6_zkratka["text"] = kontakty[pozice+5][0]
                    kontakt6_jmeno["text"] = kontakty[pozice+5][1]
                    kontakt6_cislo["text"] = kontakty[pozice+5][2][-9:]
                    kontakt7_zkratka["text"] = kontakty[pozice+6][0]
                    kontakt7_jmeno["text"] = kontakty[pozice+6][1]
                    kontakt7_cislo["text"] = kontakty[pozice+6][2][-9:]
                    kontakt8_zkratka["text"] = kontakty[pozice+7][0]
                    kontakt8_jmeno["text"] = kontakty[pozice+7][1]
                    kontakt8_cislo["text"] = kontakty[pozice+7][2][-9:]
                    kontakt9_zkratka["text"] = kontakty[pozice+8][0]
                    kontakt9_jmeno["text"] = kontakty[pozice+8][1]
                    kontakt9_cislo["text"] = kontakty[pozice+8][2][-9:]
                    kontakt10_zkratka["text"] = kontakty[pozice+9][0]
                    kontakt10_jmeno["text"] = kontakty[pozice+9][1]
                    kontakt10_cislo["text"] = kontakty[pozice+9][2][-9:]

                



def odebrat(zkratka_entry):
    global udaje
    zkratka = zkratka_entry.get()
    prihl=httplib.HTTPSConnection("www.odorik.cz")
    prihl.request('DELETE', "/api/v1/speed_dials/"+zkratka+".json", udaje)
    odp = prihl.getresponse()
    odpoved = odp.read()
    print odpoved
    prihl.close()
    
        



def pridat(zkratka_entry, cislo_entry, jmeno_entry):
    global udaje
    zkratka = zkratka_entry.get()
    cislo = cislo_entry.get()
    jmeno = jmeno_entry.get()
    prihl=httplib.HTTPSConnection("www.odorik.cz")
    dalsi_udaje = urllib.urlencode({'shortcut': zkratka, 'name': jmeno, 'number': cislo})
    celkove_udaje = udaje+"&"+dalsi_udaje
    prihl.request('POST', "/api/v1/speed_dials.json" , celkove_udaje)
    odp = prihl.getresponse()
    odpoved_mezikrok = odp.read()
    prihl.close()
    if odpoved_mezikrok[2] =="e":
        odpoved = json.loads(odpoved_mezikrok, object_hook=erory)
        for i in odpoved:
            if i == "invalid_shortcut":
                tkm.showerror("CHYBA", u"Neplatná zkratka")
            elif i == "invalid_number":
                tkm.showerror("CHYBA", u"Neplatné číslo")
            elif i == "name_too_long":
                tkm.showerror("CHYBA", u"Příliš dlouhé jméno")
            elif i == "shortcut_already_used":
                tkm.showerror("CHYBA", u"Zkratka je již obsazená")
            elif i == "speed_dials_full":
                tkm.showerror("CHYBA", u"Vaše rychlé kontakty jsou již plné")
            elif i== "unauthorized":
                tkm.showerror("CHYBA", u"Požadavek nelze vykonat")
    else:
        odpoved = json.loads(odpoved_mezikrok, object_hook=uspech)
        tkm.showinfo(u"Přidáno", u"Kontakt byl úspěšně přidán")
    print odpoved
    
       
        
            
            

    


def doplnit(zkratka_entry, cislo_entry, jmeno_entry):  ## doplní ostatní údaje do entry v hlavičce
    kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje)   ##získání kontaktů
    kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
    kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)
    jmeno = jmeno_entry.get()
    cislo = cislo_entry.get()
    zkratka = zkratka_entry.get()
    if len(zkratka) > 0:            ## pokud je vyplněna zkratka doplní jmeno a cislo
        for i in kontakty:
            if str(i[0]) == zkratka:
                jmeno_entry.delete(0, tk.END)
                jmeno_entry.insert(tk.INSERT, i[1])
                cislo_entry.delete(0, tk.END)
                cislo_entry.insert(tk.INSERT, i[2][-9:])
    elif len(jmeno) > 0:            ##doplnene jmeno .. doplni zkratku a cislo
        for i in kontakty:
            if str(i[1]) == jmeno:
                zkratka_entry.delete(0, tk.END)
                zkratka_entry.insert(tk.INSERT, i[0])
                cislo_entry.delete(0, tk.END)
                cislo_entry.insert(tk.INSERT, i[2][-9:])
    elif len(cislo) > 0:            ## napodobe ale je vyplnene cislo
        for i in kontakty:
            if str(i[2][-9:]) == cislo:
                zkratka_entry.delete(0, tk.END)
                zkratka_entry.insert(tk.INSERT, i[0])
                jmeno_entry.delete(0, tk.END)
                jmeno_entry.insert(tk.INSERT, i[1])

        

def smazat(zkratka_entry, jmeno_entry, cislo_entry):        ##po kliknutí na tlačítko smazat
    zkratka_entry.delete(0, tk.END)
    jmeno_entry.delete(0, tk.END)
    cislo_entry.delete(0, tk.END)


def callback(cislo_entry, jmeno_entry,):                 ##vyvolá okno po kliknutí na tlačítko callback
    callback_hlavni_okno = tk.Tk()
    callback_okno = tk.Frame(callback_hlavni_okno, bg="#32CD32")
    callback_okno.grid()
    
    callback_hlavni_okno.title("Callback")
    if len(jmeno_entry.get())>0:
        komu_volat = cislo_entry.get()+" ("+str(jmeno_entry.get())+")"
    else:
        komu_volat = cislo_entry.get()
    callback_label = tk.Label(callback_okno, text="Volání na:  "+komu_volat, bg="#32CD32", font="Arial_black 15 bold")
    callback_label.grid(columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S, padx=5, pady=5)
    moje_cislo_label = tk.Label(callback_okno, text="Moje číslo", bg="#32CD32", font="Arial_black 10 bold")
    moje_cislo_label.grid(row=1, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
    moje_cislo_entry = tk.Entry(callback_okno, width=35, justify="center", bg="#99FF99", relief="groove")
    moje_cislo_entry.grid(row=2, columnspan=2)
    """
    cislo_ulozit_button = tk.Button(callback_okno, text="Uložit", activebackground="#99FF99", command=lambda: ulozit_moje_cislo(moje_cislo_entry), bg="#409940", font="Arial_black 8 bold")
    cislo_ulozit_button.grid(row=3, sticky=tk.E+tk.W+tk.N+tk.S, padx=5, pady=10)
    cislo_vyplnit_button = tk.Button(callback_okno, text="Vyplnit", activebackground="#99FF99", font="Arial_black 8 bold", command=lambda: vyplnit_moje_cislo(moje_cislo_entry), bg="#409940")
    cislo_vyplnit_button.grid(row=3, column=1, sticky=tk.E+tk.W+tk.N+tk.S, padx=5, pady=10)
    """
    objednat_callback_button = tk.Button(callback_okno, width=25, activebackground="#99FF99", text="Objednat callback", font="Arial_black 8 bold", command=lambda: objednat_callback(moje_cislo_entry, cislo_entry, udaje, callback_hlavni_okno), bg="#409940")
    objednat_callback_button.grid(row=4, columnspan=2, pady=10)
    spozdeny_callback_label = tk.Label(callback_okno, text="Objednat spoždený callback", bg="#32CD32", font="Arial_black 15 bold" )
    spozdeny_callback_label.grid(row=5, sticky=tk.E+tk.W+tk.N+tk.S, columnspan=2, padx=5, pady=10)
    datum_callback_label = tk.Label(callback_okno, text="Datum", bg="#32CD32", font="Arial_black 10 bold")
    datum_callback_label.grid(row=6)
    datum_cas_callback_label = tk.Label(callback_okno, text=u"Čas", bg="#32CD32", font="Arial_black 10 bold")
    datum_cas_callback_label.grid(row=6, column=1)
    datum_callback_entry = tk.Entry(callback_okno, justify="center", bg="#99FF99", relief="groove")
    datum_callback_entry.grid(row=7)
    datum_callback_entry.insert(tk.END, "YYYY-MM-DD")
    datum_cas_callback_entry = tk.Entry(callback_okno, justify="center", bg="#99FF99", relief="groove")
    datum_cas_callback_entry.grid(row=7, column=1)
    datum_cas_callback_entry.insert(tk.END, "HH:MM:SS")
    datum_callback_button = tk.Button(callback_okno, activebackground="#99FF99", text="Objednat dle data", font="Arial_black 8 bold", bg="#409940", command=lambda: callback_datum(moje_cislo_entry, cislo_entry, udaje, datum_callback_entry, datum_cas_callback_entry, callback_hlavni_okno), width=25)
    datum_callback_button.grid(row=8, columnspan=2, padx=5, pady=10)
    minuty_callback_label = tk.Label(callback_okno, text=u"Spoždění (minuty)", bg="#32CD32", font="Arial_black 10 bold")
    minuty_callback_label.grid(row=9, columnspan=2)
    minuty_callback_entry = tk.Entry(callback_okno, width=10, justify="center", bg="#99FF99", relief="groove")
    minuty_callback_entry.grid(row=10, columnspan=2)
    minuty_callback_entry.insert(tk.END, "1")
    minuty_callback_button = tk.Button(callback_okno, activebackground="#99FF99", text="Objednat dle spoždění", font="Arial_black 8 bold", bg="#409940", command= lambda: callback_cas(moje_cislo_entry, cislo_entry, udaje, minuty_callback_entry, callback_hlavni_okno), width=25)
    minuty_callback_button.grid(row=11, columnspan=2, padx=5, pady=10)
    callback_hlavni_okno.mainloop()


def ulozit_moje_cislo(moje_cislo_entry):
    cislo_soubor = open("cislo.txt", "w")
    cislo_soubor.write(moje_cislo_entry.get())
    cislo_soubor.close()
    
    
def vyplnit_moje_cislo(moje_cislo_entry):
    cislo_soubor = open("cislo.txt", "r")
    cislo = cislo_soubor.readline()
    moje_cislo_entry.delete(0, tk.END)
    moje_cislo_entry.insert(tk.END, cislo)


def callback_cas(moje_cislo_entry, cislo_entry, udaje, minuty_callback_entry,callback_hlavni_okno):
    moje_cislo = moje_cislo_entry.get()
    volane_cislo = cislo_entry.get()
    minuty = minuty_callback_entry.get()
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo, 'delayed': minuty})
    vsechny_udaje = udaje+"&"+cisla
    objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
    odpoved = objednat_callback.read()
    if odpoved == "successfully_enqueued":
        tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
        callback_hlavni_okno.destroy()
    elif odpoved == "error callback_failed":
        tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
        callback_hlavni_okno.destroy()
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
        callback_hlavni_okno.destroy()
    elif odpoved == "error invalid_delay_format":
        callback_hlavni_okno.destroy()
        tkm.showwarning("CHYBA", u"Byl zadán špatný formát spoždění")


def callback_datum(moje_cislo_entry, cislo_entry, udaje, datum_callback_entry, datum_cas_callback_entry,callback_hlavni_okno):
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
        callback_hlavni_okno.destroy()
    elif odpoved == "error callback_failed":
        tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
        callback_hlavni_okno.destroy()
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
        callback_hlavni_okno.destroy()
    elif odpoved == "error invalid_delay_format":
        tkm.showwarning("CHYBA", u"Datum nebo čas zadáno ve špatném formátu")
        callback_hlavni_okno.destroy()
    elif odpoved == "error delayed_into_past":
        tkm.showwarning("CHYBA", u"Zadaný moment již proběhl")
        callback_hlavni_okno.destroy()



def objednat_callback(moje_cislo_entry, cislo_entry, udaje,callback_hlavni_okno):  ##objedná callback
    moje_cislo = moje_cislo_entry.get()
    volane_cislo = cislo_entry.get()
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo})
    vsechny_udaje = udaje+"&"+cisla
    objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
    odpoved =  objednat_callback.read()
    if odpoved == "callback_ordered":
        tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
        callback_hlavni_okno.destroy()
    elif odpoved == "error callback_failed":
        tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
        callback_hlavni_okno.destroy()
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
        callback_hlavni_okno.destroy()
    

#############################################################################


def ulozit_udaje():             # uloží údaje
    if ulozit_udaje_promenna.get() == 1: 
        ul_jmeno = prihl_jmeno_entry.get()
        ul_heslo = heslo_entry.get()
        ul_udaje = ul_jmeno+ul_heslo
        jmeno_a_heslo = open("jmeno_heslo.txt", "w")
        jmeno_a_heslo.write(ul_udaje)
        jmeno_a_heslo.close()
    if ulozit_udaje_promenna.get() == 0:
        jmeno_a_heslo = open("jmeno_heslo.txt", "w")
        jmeno_a_heslo.writelines("")
        jmeno_a_heslo.close()


##############################################################################
##############################################################################




uplne_hl_okno = tk.Tk()                   ##Úvodní přihlašovací okno
uplne_hl_okno.title("Odorik.cz")

hl_okno = tk.Frame(uplne_hl_okno, bg="#32CD32", padx=10, pady=10)
hl_okno.grid()

prihl_nadpis_label = tk.Label(hl_okno, text="Příhlášení", font="Arial_black 15 bold", bg="#32CD32")
prihl_nadpis_label.grid()

jmeno_frame = tk.Frame(hl_okno, bg="#32CD32", pady=10)
jmeno_frame.grid(row=1)
prihl_jmeno_label = tk.Label(jmeno_frame, text="Jméno", bg="#32CD32", font="Arial_black 10 bold")
prihl_jmeno_label.grid()

prihl_jmeno_entry = tk.Entry(jmeno_frame, justify="center", bg="#99FF99")
prihl_jmeno_entry.grid(row=1)

heslo_label = tk.Label(hl_okno, text="Heslo", bg="#32CD32", font="Arial_black 10 bold")
heslo_label.grid(row=2)

heslo_entry = tk.Entry(hl_okno, justify="center", bg="#99FF99", show="*")
heslo_entry.grid(row=3)

ulozit_udaje_promenna = tk.IntVar()
ulozit_udaje_check = tk.Checkbutton(hl_okno, text="Uložit údaje", variable=ulozit_udaje_promenna)
ulozit_udaje_check["bg"] = "#32CD32"
ulozit_udaje_check["font"] = "Arial_black 8 bold"
ulozit_udaje_check.grid(row=4, pady=2)

prihlaseni_button = tk.Button(hl_okno, text="Přihlásit", bg="#409940", command=prihlasit, font="Arial_black 8 bold", activebackground="#99FF99")
prihlaseni_button.grid(row=5, pady=10, sticky=tk.NSEW)


try:
    jmeno_a_heslo = open("jmeno_heslo.txt", "r")
    citac = 0        
    for i in jmeno_a_heslo.readlines():
        citac = citac+1
        if citac == 1:
            if i != "":
               ulozit_udaje_promenna.set(1) 
            prihl_jmeno_entry.insert(tk.END, i)
        elif citac == 2:
            heslo_entry.insert(tk.END, i)
    jmeno_a_heslo.close()

except:
    pass


uplne_hl_okno.mainloop()