# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:04:50 2015
@author: Tom
"""
import requests
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
    global prihl_jmeno
    prihl_jmeno = prihl_jmeno_entry.get()
    global heslo
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
        global zkratky_jmena
        zkratky_jmena = []
        for i in kontakty:
            if len(str(i[0])) == 1:
                zapsat = "%s    %s"%(i[0],i[1])
                zkratky_jmena.append(zapsat)
            elif len(str(i[0])) == 2:
                zapsat = "%s   %s"%(i[0],i[1])
                zkratky_jmena.append(zapsat)
            else:
                zapsat = "%s  %s"%(i[0],i[1])
                zkratky_jmena.append(zapsat)
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
        pred_posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-2]
        pred_pred_posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-3]
        posl_hovor_cena = "%.2f"%(posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-1][2])
        posl_hovor_datum = "%s %s.%s.%s"%(posl_hovor[0][11:19], posl_hovor[0][8:10], posl_hovor[0][5:7], posl_hovor[0][:4])
        posl_hovor_cislo = posl_hovor[1][(len(posl_hovor[1])-9):] 
        pred_posl_hovor_cena = "%.2f"%(posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-2][2])
        pred_posl_hovor_datum = "%s %s.%s.%s"%(pred_posl_hovor[0][11:19], pred_posl_hovor[0][8:10], pred_posl_hovor[0][5:7], pred_posl_hovor[0][:4])
        pred_posl_hovor_cislo = pred_posl_hovor[1][(len(pred_posl_hovor[1])-9):]
        pred_pred_posl_hovor_cena = "%.2f"%(posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-3][2])
        pred_pred_posl_hovor_datum = "%s %s.%s.%s"%(pred_pred_posl_hovor[0][11:19], pred_pred_posl_hovor[0][8:10], pred_pred_posl_hovor[0][5:7], pred_pred_posl_hovor[0][:4])
        pred_pred_posl_hovor_cislo = pred_pred_posl_hovor[1][(len(posl_hovor[1])-9):]
        uplne_hl_okno.destroy()
        kontakty_okno = tk.Tk()
        prihl_okno = tk.Frame(kontakty_okno, bg="#32CD32")
        prihl_okno.grid()
        kontakty_okno.title("Kontakty")
############################################################################### horní informace
        info_frame = tk.Frame(prihl_okno, bg="#32CD32")       
        kredit_label = tk.Label(info_frame, text="Váš kredit je: "+kredit+"Kč", bg="#32CD32", font="Arial_black 10 bold")   ##vypisuje kredit
        kredit_label.grid(sticky=tk.W)
        moje_cislo_ulozit_button = tk.Button(info_frame, text="Nastavit moje číslo", activebackground="#99FF99", command= nastavit_moje_cislo, bg="#409940", font="Arial_black 8 bold")
        moje_cislo_ulozit_button.grid(column=2, row=0, sticky=tk.E, pady=2)
        posledni_hovor_frame = tk.LabelFrame(info_frame, text="Poslední Hovory", bg="#32CD32", font="Arial_black 8 bold")
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
        pred_posl_hov_datum1 = tk.Label(posledni_hovor_frame, text=pred_posl_hovor_datum, width=20, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_datum1.grid(row=4)
        pred_posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text=pred_posl_hovor_cislo, width=20, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_cislo1.grid(row=4, column=1)
        pred_posl_hov_cena1 = tk.Label(posledni_hovor_frame, text=str(pred_posl_hovor_cena)+"Kč", width=20, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_cena1.grid(row=4, column=2)
        pred_pred_posl_hov_datum1 = tk.Label(posledni_hovor_frame, text=pred_pred_posl_hovor_datum, width=20, bg="#32CD32", font="Arial_black 8 bold")
        pred_pred_posl_hov_datum1.grid(row=5)
        pred_pred_posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text=pred_pred_posl_hovor_cislo, width=20, bg="#32CD32", font="Arial_black 8 bold")
        pred_pred_posl_hov_cislo1.grid(row=5, column=1)
        pred_posl_hov_cena1 = tk.Label(posledni_hovor_frame, text=str(pred_pred_posl_hovor_cena)+"Kč", width=20, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_cena1.grid(row=5, column=2)
        posledni_hovor_frame.grid(pady=1, columnspan=3)
        info_frame.grid(row=1, columnspan=3)
###########################################################################      
        callback_frame = tk.LabelFrame(prihl_okno, text="Callback", bg="#32CD32", font="Arial_black 8 bold")
        global zkratka_jmeno_promenna
        zkratka_jmeno_promenna = tk.StringVar(callback_frame)
        zkratka_jmeno_promenna.set(zkratky_jmena[0])
        zkratka_optmenu = tk.OptionMenu(callback_frame, zkratka_jmeno_promenna, *zkratky_jmena, command= dopln_cislo)
        zkratka_optmenu.config(bg="#409940", activebackground="#99FF99", font="Arial_black 10 bold", highlightbackground="#99FF99")                                    
        zkratka_optmenu.grid(row=0, sticky=tk.E+tk.W+tk.N+tk.S, padx= 10, pady=10)
        global cislo_label
        cislo_label = tk.Label(callback_frame, bg="#99FF99", relief="groove", text=kontakty[0][2], width=60, font="Arial_black 10 bold")
        cislo_label.grid(row=1, sticky=tk.E+tk.W+tk.N+tk.S, padx= 10, pady=10)
        callback_podframe = tk.Frame(callback_frame, bg="#32CD32")
        callback_podframe.grid(row=2, sticky=tk.E+tk.W+tk.N+tk.S)
        callback_button = tk.Button(callback_podframe, text="Objednat callback", font="Arial_black 10 bold", activebackground="#99FF99", command=lambda: objednat_callback(cislo_label, udaje), bg="#409940", width=25)
        callback_button.grid(row=0, column=0, padx=20, pady=5)
        spozdeny_callback_button = tk.Button(callback_podframe, text="Objednat zpožděný callback", font="Arial_black 10 bold", activebackground="#99FF99", command=lambda:callback(cislo_label), bg="#409940", width=25)
        spozdeny_callback_button.grid(row=0, column=1, sticky=tk.E, padx=20, pady=5)
        callback_frame.grid(row=2, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S, padx= 10, pady=5)
########################################################################### 
        pridat_button = tk.Button(prihl_okno, text="Přidat kontakt", font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940", command=pridat_kontakt)
        pridat_button.grid(row=4, column=2, padx=20, pady=10)
        odebrat_button = tk.Button(prihl_okno, text="Odebrat kontakt", command=odebrat, font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940")
        odebrat_button.grid(row=4, column=0)
        global seznam_hodnot
        seznam_hodnot = []
        for i in range(1+len(kontakty)/10):
            hodnota = "Strana"+str(i+1)+"/"+str(1+len(kontakty)/10)
            seznam_hodnot.append(hodnota)
        global hodnoty
        hodnoty = tk.StringVar()
        hodnoty.set(seznam_hodnot[0]) 
        strankovac = tk.OptionMenu(prihl_okno, hodnoty, *seznam_hodnot, command=kontakty_funkce)
        strankovac.config(bg="#409940", activebackground="#99FF99", font="Arial_black 8 bold", highlightbackground="#99FF99")        
        strankovac.grid(row=4, column=1, pady=15)
           
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


def nastavit_moje_cislo():
    try:
        moje_cislo_soubor = open("moje_cislo.txt", "r")        
        moje_ulozene_cislo = moje_cislo_soubor.readline()
        moje_cislo_soubor.close()
    except:
        moje_ulozene_cislo = ""
    
    nastavit_cislo_okno = tk.Tk()
    nastavit_cislo_okno.title(u"Nastavení čísla")
    nastavit_cislo = tk.Frame(nastavit_cislo_okno, bg="#32CD32")
    nastavit_cislo_entry = tk.Entry(nastavit_cislo, justify="center", bg="#99FF99", relief="groove")
    nastavit_cislo_entry.grid(row=0, padx=10, pady=10)
    nastavit_cislo_entry.insert(tk.END, moje_ulozene_cislo)
    nastavit_cislo_button = tk.Button(nastavit_cislo, text=u"Nastavit moje číslo", font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940", command=lambda: ulozit_cislo(nastavit_cislo_entry, nastavit_cislo_okno))
    nastavit_cislo_button.grid(row=1, padx=10, pady=10)
    nastavit_cislo.grid()
    nastavit_cislo_okno.mainloop()


def ulozit_cislo(nastavit_cislo_entry, nastavit_cislo_okno):
    cislo = nastavit_cislo_entry.get()
    moje_cislo_soubor = open("moje_cislo.txt", "w")
    moje_cislo_soubor.write(cislo)
    moje_cislo_soubor.close() 
    nastavit_cislo_okno.destroy()


def pridat_kontakt():
    global pridat_kontakt_okno
    pridat_kontakt_okno = tk.Tk()
    pridat_kontakt_frame = tk.Frame(pridat_kontakt_okno, bg="#32CD32")
    pridat_kontakt_label = tk.Label(pridat_kontakt_frame, bg="#32CD32", text=u"Přidat kontakt", font="Arial_black 15 bold")
    pridat_kontakt_label.grid(row=0, columnspan=3)
    zkratka_label = tk.Label(pridat_kontakt_frame, text="Zkratka", bg="#32CD32", font="Arial_black 10 bold")
    zkratka_label.grid(row=1, column=0)
    pridat_cislo_label = tk.Label(pridat_kontakt_frame, text=u"Číslo", bg="#32CD32", font="Arial_black 10 bold")
    pridat_cislo_label.grid(row=1, column=2)
    jmeno_label = tk.Label(pridat_kontakt_frame, text=u"Jméno", bg="#32CD32", font="Arial_black 10 bold")
    jmeno_label.grid(row=1, column=1)
    zkratka_entry = tk.Entry(pridat_kontakt_frame, bg="#99FF99")
    zkratka_entry.grid(row=2, column=0)
    cislo_entry= tk.Entry(pridat_kontakt_frame, bg="#99FF99")
    cislo_entry.grid(row=2, column=2)
    jmeno_entry = tk.Entry(pridat_kontakt_frame, bg="#99FF99")
    jmeno_entry.grid(row=2, column=1)
    pridat_kontakt_button = tk.Button(pridat_kontakt_frame, text="Přidat kontakt", activebackground="#99FF99", bg="#409940", font="Arial_black 8 bold", command=lambda: pridat(zkratka_entry, cislo_entry, jmeno_entry))
    pridat_kontakt_button.grid(row=3, columnspan=3)
    pridat_kontakt_frame.grid(row=0, column=0)  
    pridat_kontakt_okno.mainloop()
    


def dopln_cislo(blbost):
    kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje)   ##získání kontaktů
    kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
    kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)
    global zkratky_jmena
    global zkratka_jmeno_promenna
    global cislo_label
    pozice = -1
    for i in zkratky_jmena:
        pozice = pozice+1
        if i ==zkratka_jmeno_promenna.get():
            cislo_label["text"] = str(kontakty[pozice][2])

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


def odebrat():
    odebrat_okno = tk.Tk()
    odebrat_frame = tk.Frame(odebrat_okno, bg="#32CD32")
    odebrat_frame.grid()
    odebrat_label = tk.Label(odebrat_frame, bg="#32CD32", text="Zadejte zkratku", font="Arial_black 10 bold")
    odebrat_label.grid(row=0, column=0, padx=10, pady=2)
    odebrat_entry = tk.Entry(odebrat_frame, justify="center", bg="#99FF99", relief="groove")
    odebrat_entry.grid(row=1, column=0, padx=10, pady=0)
    odebrat_button = tk.Button(odebrat_frame, activebackground="#99FF99", text="Odebrat kontakt", font="Arial_black 8 bold", bg="#409940", command=lambda: odebrat_funkce(odebrat_entry.get()))
    odebrat_button.grid(row=2, column=0, padx=10, pady=10)
    odebrat_okno.mainloop()



def odebrat_funkce(zkratka):
    print prihl_jmeno,heslo
    global udaje
    print udaje
    smazat = requests.delete(url='https://www.odorik.cz/api/v1/speed_dials/'+zkratka+'.json', params=udaje)
    print smazat.text
    if smazat.text == "{}":
        tkm.showinfo(u"Úspěch", "kontakt byl úspěšně smazán")

    
        



def pridat(zkratka_entry, cislo_entry, jmeno_entry):
    global udaje
    global pridat_kontakt_okno
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
        pridat_kontakt_okno.destroy()


def callback(cislo_label):                 ##vyvolá okno po kliknutí na tlačítko callback
    callback_hlavni_okno = tk.Tk()
    callback_okno = tk.Frame(callback_hlavni_okno, bg="#32CD32")
    callback_okno.grid()
    callback_hlavni_okno.title("Callback")
    komu_volat = cislo_label["text"]   
    callback_datum_frame = tk.LabelFrame(callback_okno, text="Objednat callback na určené datum", bg="#32CD32", font="Arial_black 8 bold")
    callback_datum_frame.grid(padx=10, pady=5)
    datum_callback_label = tk.Label(callback_datum_frame, text="Datum", bg="#32CD32", font="Arial_black 10 bold")
    datum_callback_label.grid(row=0, column=0)
    datum_cas_callback_label = tk.Label(callback_datum_frame, text=u"Čas", bg="#32CD32", font="Arial_black 10 bold")
    datum_cas_callback_label.grid(row=0, column=1)
    global datum_callback_entry
    datum_callback_entry = tk.Entry(callback_datum_frame, justify="center", bg="#99FF99", relief="groove")
    datum_callback_entry.grid(row=1, column=0)
    datum_callback_entry.insert(tk.END, "YYYY-MM-DD")
    global datum_cas_callback_entry
    datum_cas_callback_entry = tk.Entry(callback_datum_frame, justify="center", bg="#99FF99", relief="groove")
    datum_cas_callback_entry.grid(row=1, column=1)
    datum_cas_callback_entry.insert(tk.END, "HH:MM:SS")
    datum_callback_button = tk.Button(callback_datum_frame, activebackground="#99FF99", text="Objednat dle data", font="Arial_black 8 bold", bg="#409940", command=lambda: callback_datum(cislo_label, udaje, datum_callback_entry, datum_cas_callback_entry, callback_hlavni_okno), width=25)
    datum_callback_button.grid(row=2, columnspan=2, padx=5, pady=10)
    callback_cas_frame = tk.LabelFrame(callback_okno, text="Objednat callback na určený čas", bg="#32CD32", font="Arial_black 8 bold")
    callback_cas_frame.grid(row=1, pady=10)
    minuty_callback_label = tk.Label(callback_cas_frame, text=u"Zpoždění (minuty)", bg="#32CD32", font="Arial_black 10 bold")
    minuty_callback_label.grid(row=0, column=0, columnspan=2)
    global minuty_callback_entry
    minuty_callback_entry = tk.Entry(callback_cas_frame, width=10, justify="center", bg="#99FF99", relief="groove")
    minuty_callback_entry.grid(row=1, column=0, columnspan=2)
    minuty_callback_entry.insert(tk.END, "1")
    minuty_callback_button = tk.Button(callback_cas_frame, activebackground="#99FF99", text="Objednat dle zpoždění", font="Arial_black 8 bold", bg="#409940", command=lambda: callback_cas(cislo_label, udaje, callback_hlavni_okno, minuty_callback_entry), width=25)
    minuty_callback_button.grid(row=2, column=0, columnspan=2, pady=5)
    callback_hlavni_okno.mainloop()


def callback_cas(cislo_label, udaje, callback_hlavni_okno, minuty_callback_entry):
    try:
        moje_cislo_soubor = open("moje_cislo.txt", "r")
        moje_cislo = moje_cislo_soubor.readline()
        moje_cislo_soubor.close()
    except:
        tkm.showwarning("CHYBA", u"Nemáte nastavené vaše číslo")
        callback_hlavni_okno.destroy()
    volane_cislo = cislo_label["text"]
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
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
    elif odpoved == "error invalid_delay_format":
        tkm.showwarning("CHYBA", u"Byl zadán špatný formát spoždění")


def callback_datum( cislo_label, udaje, datum_callback_entry, datum_cas_callback_entry, callback_hlavni_okno):
    try:
        moje_cislo_soubor = open("moje_cislo.txt", "r")
        moje_cislo = moje_cislo_soubor.readline()
        moje_cislo_soubor.close()
    except:
        tkm.showwarning("CHYBA", u"Nemáte nastavené vaše číslo")
        callback_hlavni_okno.destroy()
    volane_cislo = cislo_label["text"]
    datum = datum_callback_entry.get()+"T"+datum_cas_callback_entry.get()+"+02:00"
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo, 'delayed': datum})
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
        tkm.showwarning("CHYBA", u"Datum nebo čas zadáno ve špatném formátu")
        callback_hlavni_okno.destroy()
    elif odpoved == "error delayed_into_past":
        tkm.showwarning("CHYBA", u"Zadaný moment již proběhl")
        callback_hlavni_okno.destroy()



def objednat_callback(cislo_label,udaje):  ##objedná callback
    try:
        moje_cislo_soubor = open("moje_cislo.txt", "r")        
        moje_cislo = moje_cislo_soubor.readline()
        moje_cislo_soubor.close()
    except:
        tkm.showwarning("CHYBA",u"Nemáte nastavené vaše číslo")
    volane_cislo = cislo_label["text"]
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo})
    vsechny_udaje = udaje+"&"+cisla
    objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
    odpoved =  objednat_callback.read()
    if odpoved == "callback_ordered":
        tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
    elif odpoved == "error callback_failed":
        tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
    elif odpoved[:22] == "error missing_argument":
        tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")


#############################################################################


def ulozit_udaje():             # uloží údaje
    if ulozit_udaje_promenna.get() == 1: 
        ul_jmeno = prihl_jmeno_entry.get()
        ul_heslo = heslo_entry.get()
        #ul_udaje = ul_jmeno+ul_heslo
        jmeno_a_heslo = open("jmeno_heslo.txt", "w")
        jmeno_a_heslo.write(ul_jmeno)
        jmeno_a_heslo.write(ul_heslo)
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