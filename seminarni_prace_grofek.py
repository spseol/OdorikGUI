# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:04:50 2015
@author: Tomáš Grofek
License: GNU/GPL
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


def vypsat(kontakty):                   # získá kontakty ve formátu json
    return kontakty["shortcut"], kontakty["name"], kontakty["number"]


def datum_cislo_cena(posl_hovor):
    return (posl_hovor["date"], posl_hovor["destination_number"],
            posl_hovor["price"])


def datum_hovoru_2hod(datum):               # Při letním čase, stačí přejmenovat funkci(2hod na 1hod a v druhé funkci naopak)
    datum1 = datetime.datetime(int(datum[:4]), int(datum[5:7]),
                               int(datum[8:10]), int(datum[11:13]),
                               int(datum[14:16]), int(datum[17:19]))
    dve_hodiny = datetime.timedelta(hours=2)
    pred_dvema_hodinama = datum1+dve_hodiny
    pred_dvema_hodinama = "%s.%s.%s  %s" % (str(pred_dvema_hodinama)[8:10], str(pred_dvema_hodinama)[5:7], str(pred_dvema_hodinama)[:4], str(pred_dvema_hodinama)[11:19])
    return pred_dvema_hodinama
    

def datum_hovoru_1hod(datum):               # Při zimním čase
    datum1 = datetime.datetime(int(datum[:4]), int(datum[5:7]), int(datum[8:10]), int(datum[11:13]), int(datum[14:16]), int(datum[17:19]))
    hodina = datetime.timedelta(hours=1)
    pred_dvema_hodinama = datum1+hodina
    pred_dvema_hodinama = "%s.%s.%s  %s" % (str(pred_dvema_hodinama)[8:10], str(pred_dvema_hodinama)[5:7], str(pred_dvema_hodinama)[:4], str(pred_dvema_hodinama)[11:19])
    return pred_dvema_hodinama


def aktualizovat_kredit(udaje, kontakty_okno, kredit_label):
    try:
        kredit_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/balance?"+udaje)  # získání kreditu
    except:
        pass
    else:
        kredit = kredit_mezikrok.read()         # kredit jako řetězec
        if kredit != "error authentication_failed":     # špatně zadané údaje
           kredit_label["text"] = "Váš kredit je: "+kredit+" Kč"
    kontakty_okno.after(10000, lambda: aktualizovat_kredit(udaje, kontakty_okno, kredit_label))


def aktualizovat_posledni_hovory(prihl_jmeno, heslo, posl_hov_datum1, posl_hov_cislo1, posl_hov_cena1, pred_posl_hov_datum1, pred_posl_hov_cislo1, pred_posl_hov_cena1, pred_pred_posl_hov_datum1, pred_pred_posl_hov_cislo1, pred_pred_posl_hov_cena1, kontakty_okno):
    try:
        dnes = datetime.datetime.today()
        do = "%sT%sZ" % (str(dnes)[:10], str(dnes)[11:19])
        ctyri_tydny = datetime.timedelta(weeks=4)
        pred_ctyrmi_tydny = "%s" % (dnes-ctyri_tydny)
        od = "%sT%sZ" % (pred_ctyrmi_tydny[:10], pred_ctyrmi_tydny[11:19])
        posl_hovor_url = "https://www.odorik.cz/api/v1/calls.json?"+"user="+prihl_jmeno+"&password="+heslo+"&from="+od+"&to="+do+"&direction=out"
        zjistit_posl_hovor = urllib.urlopen(posl_hovor_url)
    except:
        pass
    else:
        posl_hovor_mezikrok = zjistit_posl_hovor.read()
        posl_hovor_mezikrok2 = json.loads(posl_hovor_mezikrok, object_hook=datum_cislo_cena)
        try:
            posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-1]
            posl_hovor_cena = "%.2f Kč" % (posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-1][2])
            posl_hovor_datum = datum_hovoru_2hod(posl_hovor[0])
            posl_hovor_cislo = posl_hovor[1][(len(posl_hovor[1])-9):]
            posl_hov_datum1["text"] = posl_hovor_datum
            posl_hov_cislo1["text"] = posl_hovor_cislo
            posl_hov_cena1["text"] = posl_hovor_cena
        except:
            pass
        try:
            pred_posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-2]
            pred_posl_hovor_cena = "%.2f Kč" % (posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-2][2])
            pred_posl_hovor_datum = datum_hovoru_2hod(pred_posl_hovor[0])
            pred_posl_hovor_cislo = pred_posl_hovor[1][(len(pred_posl_hovor[1])-9):]
            pred_posl_hov_datum1["text"] = pred_posl_hovor_datum
            pred_posl_hov_cislo1["text"] = pred_posl_hovor_cislo
            pred_posl_hov_cena1["text"] = pred_posl_hovor_cena
        except:
            pass
        try:
            pred_pred_posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-3]
            pred_pred_posl_hovor_cena = "%.2f Kč" % (posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-3][2])
            pred_pred_posl_hovor_datum = datum_hovoru_2hod(pred_pred_posl_hovor[0])
            pred_pred_posl_hovor_cislo = pred_pred_posl_hovor[1][(len(posl_hovor[1])-9):]
            pred_pred_posl_hov_datum1["text"] = pred_pred_posl_hovor_datum
            pred_pred_posl_hov_cislo1["text"] = pred_pred_posl_hovor_cislo
            pred_pred_posl_hov_cena1["text"] = pred_pred_posl_hovor_cena
        except:
            pass
    kontakty_okno.after(10000, lambda: aktualizovat_posledni_hovory(prihl_jmeno, heslo, posl_hov_datum1, posl_hov_cislo1, posl_hov_cena1, pred_posl_hov_datum1, pred_posl_hov_cislo1, pred_posl_hov_cena1, pred_pred_posl_hov_datum1, pred_pred_posl_hov_cislo1, pred_pred_posl_hov_cena1, kontakty_okno))


def aktualizovat_kontakty(udaje, listbox, kontakty_okno, zkratky_jmena_cisla):
    try:
        kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje)
    except:
        pass
    else:
        kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
        kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)          # kontakty jako 3-členné ntice v seznamu
        zkratky_jmena_cisla2 = []
        for i in kontakty:
            if len(str(i[0])) == 1:
                zapsat = "  %s    %s" % (i[0], i[1])
            elif len(str(i[0])) == 2:
                zapsat = "  %s   %s" % (i[0], i[1])
            else:
                zapsat = "  %s  %s" % (i[0], i[1])
            if len(zapsat) > 58:
                zapsat = zapsat[:55]+"...  "
            for y in range(60-len(zapsat)):
                zapsat = zapsat+" "
            citac_hvezdicka = -1
            pozicovac_hvezdicka = 0
            pozicovac_dvojtecka = 0
            citac_dvojtecka = -1
            for pismeno in str(i[2]):
                if pismeno == ":":
                    pozicovac_dvojtecka = 1
                elif pismeno == "*":
                    pozicovac_hvezdicka = 1
                if pozicovac_hvezdicka == 1:
                    citac_hvezdicka = citac_hvezdicka + 1
                if pozicovac_dvojtecka == 1:
                    citac_dvojtecka = citac_dvojtecka+1
            if citac_dvojtecka > 0:
                upravene_cislo = i[2][(citac_dvojtecka*-1):]
            elif citac_hvezdicka > 0:
                upr_cis = i[2][(len(i)-citac_hvezdicka):]
                if len(upr_cis) == 9:
                    upravene_cislo = "    %s %s %s" % (upr_cis[-9:-6], upr_cis[-6:-3], upr_cis[:-3])
                else:
                    upravene_cislo = "%s %s %s %s" % (i[2][-12:-9], i[2][-9:-6], i[2][-6:-3], i[2][-3:])
            else:
                if len(i[2]) == 9:
                    upravene_cislo = "    %s %s %s" % (i[2][-9:-6], i[2][-6:-3], i[2][-3:])
                else:
                    upravene_cislo = "%s %s %s %s" % (i[2][-12:-9], i[2][-9:-6], i[2][-6:-3], i[2][-3:])
            if len(str(upravene_cislo)) > 20:
                zapsat = zapsat+upravene_cislo[:20]+"..."
            else:
                zapsat = zapsat+str(upravene_cislo)
            zkratky_jmena_cisla2.append(zapsat)
        if zkratky_jmena_cisla != zkratky_jmena_cisla2:
            listbox.delete(0, tk.END)
            for i in zkratky_jmena_cisla:
                listbox.insert(tk.END, i)
    kontakty_okno.after(10000, lambda:aktualizovat_kontakty(udaje, listbox, kontakty_okno, zkratky_jmena_cisla))


def aktualizovat_kontakty_bez_opakovani(udaje, listbox):
    try:
        kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje)
    except:
        pass
    else:
        kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
        kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)          # kontakty jako 3-členné ntice v seznamu
        zkratky_jmena_cisla = []
        for i in kontakty:
            if len(str(i[0])) == 1:
                zapsat = "  %s    %s" % (i[0], i[1])
            elif len(str(i[0])) == 2:
                zapsat = "  %s   %s" % (i[0], i[1])
            else:
                zapsat = "  %s  %s" % (i[0], i[1])
            if len(zapsat) > 58:
                zapsat = zapsat[:55]+"...  "
            for y in range(60-len(zapsat)):
                zapsat = zapsat+" "
            citac_hvezdicka = -1
            pozicovac_hvezdicka = 0
            pozicovac_dvojtecka = 0
            citac_dvojtecka = -1
            for pismeno in str(i[2]):
                if pismeno == ":":
                    pozicovac_dvojtecka = 1
                elif pismeno == "*":
                    pozicovac_hvezdicka = 1
                if pozicovac_hvezdicka == 1:
                    citac_hvezdicka = citac_hvezdicka + 1
                if pozicovac_dvojtecka == 1:
                    citac_dvojtecka = citac_dvojtecka+1
            if citac_dvojtecka > 0:
                upravene_cislo = i[2][(citac_dvojtecka*-1):]
            elif citac_hvezdicka > 0:
                upr_cis = i[2][(len(i)-citac_hvezdicka):]
                if len(upr_cis) == 9:
                    upravene_cislo = "    %s %s %s" % (upr_cis[-9:-6], upr_cis[-6:-3], upr_cis[:-3])
                else:
                    upravene_cislo = "%s %s %s %s" % (i[2][-12:-9], i[2][-9:-6], i[2][-6:-3], i[2][-3:])
            else:
                if len(i[2]) == 9:
                    upravene_cislo = "    %s %s %s" % (i[2][-9:-6], i[2][-6:-3], i[2][-3:])
                else:
                    upravene_cislo = "%s %s %s %s" % (i[2][-12:-9], i[2][-9:-6], i[2][-6:-3], i[2][-3:])
            if len(str(upravene_cislo)) > 20:
                zapsat = zapsat+upravene_cislo[:20]+"..."
            else:
                zapsat = zapsat+str(upravene_cislo)
            zkratky_jmena_cisla.append(zapsat)
        listbox.delete(0, tk.END)
        for i in zkratky_jmena_cisla:
            listbox.insert(tk.END, i)


def prihlasit():
    ulozit_udaje()
    global prihl_jmeno
    prihl_jmeno = prihl_jmeno_entry.get()
    global heslo
    heslo = heslo_entry.get()
    global udaje
    if prihl_jmeno_entry.get() == "" or heslo_entry.get() == "":  # nevyplněné údaje
        tkm.showwarning("CHYBA", u"Jeden, nebo oba údaje zůstaly nevyplněny")
    udaje = urllib.urlencode({"user": prihl_jmeno, "password": heslo})            # přihlašovací údaje jako parametr
    try:
        kredit_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/balance?"+udaje)  # získání kreditu
        kontakty_mezikrok = urllib.urlopen("https://www.odorik.cz/api/v1/speed_dials.json?"+udaje)   # získání kontaktů
        dnes = datetime.datetime.today()
        do = "%sT%sZ" % (str(dnes)[:10], str(dnes)[11:19])
        ctyri_tydny = datetime.timedelta(weeks=4)
        pred_ctyrmi_tydny = "%s"%(dnes-ctyri_tydny)
        od = "%sT%sZ" % (pred_ctyrmi_tydny[:10], pred_ctyrmi_tydny[11:19])
        posl_hovor_url = "https://www.odorik.cz/api/v1/calls.json?"+"user="+prihl_jmeno+"&password="+heslo+"&from="+od+"&to="+do+"&direction=out"
        zjistit_posl_hovor = urllib.urlopen(posl_hovor_url)
    except:
        tkm.showwarning("CHYBA", u"Nelze se připojit k síti")
    else:
        kredit = kredit_mezikrok.read()         ## kredit jako řetězec   
        if kredit == "error authentication_failed":     ## špatně zadané údaje
            tkm.showwarning("CHYBA", u"Zadal/a jste špatné přihlašovací údaje")
        else:                                           ## dobře zadané údaje
            global kontakty
            kontakty_dalsi_mezikrok = kontakty_mezikrok.read()
            kontakty = json.loads(kontakty_dalsi_mezikrok, object_hook=vypsat)          # kontakty jako 3-členné ntice v seznamu
            zkratky_jmena_cisla = []
            for i in kontakty:
                if len(str(i[0])) == 1:
                    zapsat = "  %s    %s" % (i[0], i[1])
                elif len(str(i[0])) == 2:
                    zapsat = "  %s   %s" % (i[0], i[1])
                else:
                    zapsat = "  %s  %s" % (i[0], i[1])
                if len(zapsat) > 58:
                    zapsat = zapsat[:55]+"...  "
                for y in range(60-len(zapsat)):
                    zapsat = zapsat+" "
                citac_hvezdicka = -1
                pozicovac_hvezdicka = 0
                pozicovac_dvojtecka = 0
                citac_dvojtecka = -1
                for pismeno in str(i[2]):
                    if pismeno == ":":
                        pozicovac_dvojtecka = 1
                    elif pismeno == "*":
                        pozicovac_hvezdicka = 1
                    if pozicovac_hvezdicka == 1:
                        citac_hvezdicka = citac_hvezdicka + 1
                    if pozicovac_dvojtecka == 1:
                        citac_dvojtecka = citac_dvojtecka+1 
                if citac_dvojtecka > 0:
                    upravene_cislo = i[2][(citac_dvojtecka*-1):]
                
                elif citac_hvezdicka > 0:
                    upr_cis = i[2][(len(i)-citac_hvezdicka):]
                    if len(upr_cis) == 9:    
                        upravene_cislo = "    %s %s %s" % (upr_cis[-9:-6], upr_cis[-6:-3], upr_cis[:-3])
                    else:upravene_cislo = "%s %s %s %s"%(i[2][-12:-9], i[2][-9:-6], i[2][-6:-3], i[2][-3:])
                else:
                    if len(i[2]) == 9:
                        upravene_cislo = "    %s %s %s"%(i[2][-9:-6], i[2][-6:-3], i[2][-3:])
                    else:
                        upravene_cislo = "%s %s %s %s"%(i[2][-12:-9], i[2][-9:-6], i[2][-6:-3], i[2][-3:])
                if len(str(upravene_cislo)) > 20:
                    zapsat = zapsat+upravene_cislo[:20]+"..."
                else:
                    zapsat = zapsat+str(upravene_cislo)
                zkratky_jmena_cisla.append(zapsat)
            posl_hovor_mezikrok = zjistit_posl_hovor.read()
            posl_hovor_mezikrok2 = json.loads(posl_hovor_mezikrok, object_hook=datum_cislo_cena)
            try:
                moje_cislo_soubor = open("moje_cislo.txt", "r")
                moje_ulozene_cislo = moje_cislo_soubor.readline()
                moje_cislo_soubor.close()
            except:
                moje_ulozene_cislo = ""
            uplne_hl_okno.destroy()
            kontakty_okno = tk.Tk()
            prihl_okno = tk.Frame(kontakty_okno, bg="#32CD32")
            prihl_okno.grid()
            kontakty_okno.title("Kontakty")
    # ############################################################################## horní informace
            info_frame = tk.Frame(prihl_okno, bg="#32CD32")
            kredit_label = tk.Label(info_frame, text="Váš kredit je: "+kredit+" Kč", bg="#32CD32", font="Arial_black 10 bold")   ##vypisuje kredit
            kredit_label.grid(sticky=tk.W, column=0, row=0)
            kontakty_okno.after(10000, lambda: aktualizovat_kredit(udaje, kontakty_okno, kredit_label))
            moje_cislo_label = tk.Label(info_frame, text=moje_ulozene_cislo, bg="#32CD32", font="Arial_black 8 bold")
            moje_cislo_label.grid(column=1,row=0, sticky=tk.E,columnspan=2)
            moje_cislo_ulozit_button = tk.Button(info_frame, text="Nastavit čislo pro callback", activebackground="#99FF99", command=lambda: nastavit_moje_cislo(moje_cislo_label), bg="#409940", font="Arial_black 8 bold")
            moje_cislo_ulozit_button.grid(column=3, row=0, sticky=tk.E, pady=2)
            posledni_hovor_frame = tk.LabelFrame(info_frame, text="Poslední hovory", bg="#32CD32", font="Arial_black 8 bold")
            posl_hov_datum = tk.Label(posledni_hovor_frame, text="Datum  Čas", width=21, bg="#32CD32", font="Arial_black 10 bold")
            posl_hov_datum.grid(row=2)
            posl_hov_cislo = tk.Label(posledni_hovor_frame, text="Číslo", width=21, bg="#32CD32", font="Arial_black 10 bold")
            posl_hov_cislo.grid(row=2, column=1)
            posl_hov_cena = tk.Label(posledni_hovor_frame, text="Cena", width=21, bg="#32CD32", font="Arial_black 10 bold")
            posl_hov_cena.grid(row=2, column=2)
            posl_hov_datum1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            posl_hov_datum1.grid(row=3)
            posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            posl_hov_cislo1.grid(row=3, column=1)
            posl_hov_cena1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            posl_hov_cena1.grid(row=3, column=2)
            pred_posl_hov_datum1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            pred_posl_hov_datum1.grid(row=4)
            pred_posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            pred_posl_hov_cislo1.grid(row=4, column=1)
            pred_posl_hov_cena1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            pred_posl_hov_cena1.grid(row=4, column=2)
            pred_pred_posl_hov_datum1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            pred_pred_posl_hov_datum1.grid(row=5)
            pred_pred_posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            pred_pred_posl_hov_cislo1.grid(row=5, column=1)
            pred_pred_posl_hov_cena1 = tk.Label(posledni_hovor_frame, text="", width=21, bg="#32CD32", font="Arial_black 8 bold")
            pred_pred_posl_hov_cena1.grid(row=5, column=2)
            posledni_hovor_frame.grid(pady=1, columnspan=4, sticky=tk.E+tk.W+tk.N+tk.S)
            info_frame.grid(row=1, columnspan=3, padx=10)
            try:
                posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-1]
                posl_hovor_cena = "%.2f Kč" % (posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-1][2])
                posl_hovor_datum = datum_hovoru_2hod(posl_hovor[0])
                posl_hovor_cislo = posl_hovor[1][(len(posl_hovor[1])-9):]
                posl_hov_datum1["text"] = posl_hovor_datum
                posl_hov_cislo1["text"] = posl_hovor_cislo
                posl_hov_cena1["text"] = posl_hovor_cena
            except:
                pass
            try:
                pred_posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-2]
                pred_posl_hovor_cena = "%.2f Kč" % (posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-2][2])
                pred_posl_hovor_datum = datum_hovoru_2hod(pred_posl_hovor[0])
                pred_posl_hovor_cislo = pred_posl_hovor[1][(len(pred_posl_hovor[1])-9):]
                pred_posl_hov_datum1["text"] = pred_posl_hovor_datum
                pred_posl_hov_cislo1["text"] = pred_posl_hovor_cislo
                pred_posl_hov_cena1["text"] = pred_posl_hovor_cena
            except:
                pass
            try:
                pred_pred_posl_hovor = posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-3]
                pred_pred_posl_hovor_cena = "%.2f Kč" % (posl_hovor_mezikrok2[len(posl_hovor_mezikrok2)-3][2])
                pred_pred_posl_hovor_datum = datum_hovoru_2hod(pred_pred_posl_hovor[0])
                pred_pred_posl_hovor_cislo = pred_pred_posl_hovor[1][(len(posl_hovor[1])-9):]
                pred_pred_posl_hov_datum1["text"] = pred_pred_posl_hovor_datum
                pred_pred_posl_hov_cislo1["text"] = pred_pred_posl_hovor_cislo
                pred_pred_posl_hov_cena1["text"] = pred_pred_posl_hovor_cena
            except:
                pass
            kontakty_okno.after(10000, lambda: aktualizovat_posledni_hovory(prihl_jmeno, heslo, posl_hov_datum1, posl_hov_cislo1, posl_hov_cena1, pred_posl_hov_datum1, pred_posl_hov_cislo1, pred_posl_hov_cena1, pred_pred_posl_hov_datum1, pred_pred_posl_hov_cislo1, pred_pred_posl_hov_cena1, kontakty_okno))
    # ##########################################################################
            kontakty_frame = tk.LabelFrame(prihl_okno, text="Kontakty", bg="#32CD32", font="Arial_black 8 bold")
            callback_podframe = tk.Frame(kontakty_frame, bg="#32CD32")
            callback_podframe.grid(row=0, sticky=tk.E+tk.W+tk.N+tk.S, column=0)
            callback_button = tk.Button(callback_podframe, text="Objednat callback nyní", font="Arial_black 8 bold", activebackground="#99FF99", command=lambda: objednat_callback(listbox, udaje, kontakty), bg="#409940", width=25)
            callback_button.grid(row=0, column=0, padx=40, pady=10, sticky=tk.W)
            spozdeny_callback_button = tk.Button(callback_podframe, text="Objednat zpožděný callback", font="Arial_black 8 bold", activebackground="#99FF99", command=lambda: callback(listbox, kontakty), bg="#409940", width=25)
            spozdeny_callback_button.grid(row=0, column=1, sticky=tk.E, padx=40, pady=10)
            listbox_frame = tk.Frame(kontakty_frame, bg="#32CD32")
            listbox_frame.grid(row=1, column=0, padx=7)
            scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
            listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, width=85, bg="#99FF99", font="Courier 8 bold", bd=0)
            scrollbar.config(command=listbox.yview)
            listbox.grid(row=0, column=0)
            for i in zkratky_jmena_cisla:
                listbox.insert(tk.END, i)
            scrollbar.grid(row=0, column=1, sticky=tk.S+tk.N)
            kontakty_okno.after(10000, lambda:aktualizovat_kontakty(udaje, listbox, kontakty_okno, zkratky_jmena_cisla))
            kontakty_frame.grid(row=3, columnspan=3, padx=10, pady=10, sticky=tk.E+tk.W+tk.N+tk.S)
            kontakty_buttony_frame = tk.Frame(kontakty_frame, bg="#32CD32")
            pridat_button = tk.Button(kontakty_buttony_frame, text="Přidat kontakt", font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940", command=lambda: pridat_kontakt(udaje, listbox))
            pridat_button.grid(row=0, column=0, padx=20, pady=10)
            odebrat_button = tk.Button(kontakty_buttony_frame, text="Odebrat kontakt", command=lambda: odebrat(listbox, udaje, kontakty), font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940")
            odebrat_button.grid(row=0, column=2, pady=10, padx=20)
            upravit_button = tk.Button(kontakty_buttony_frame, text="Upravit kontakt", font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940", command=lambda: upravit_kontakt(listbox, udaje, kontakty))
            upravit_button.grid(row=0, column=1, pady=10, padx=20)
            kontakty_buttony_frame.grid(row=2, columnspan=3)


def upravit_kontakt(listbox, udaje, kontakty):
    try:  
        zvoleny_kontakt = map(int, listbox.curselection())
        kontakt = kontakty[zvoleny_kontakt[0]]
        upravit_kontakt_okno = tk.Tk()
        upravit_kontakt_frame = tk.Frame(upravit_kontakt_okno, bg="#32CD32")
        upravit_kontakt_label = tk.Label(upravit_kontakt_frame, bg="#32CD32", text=u"Upravit kontakt", font="Arial_black 15 bold")
        upravit_kontakt_label.grid(row=0, columnspan=3)
        zkratka_label = tk.Label(upravit_kontakt_frame, text="Zkratka", bg="#32CD32", font="Arial_black 10 bold")
        zkratka_label.grid(row=1, column=0)
        upravit_cislo_label = tk.Label(upravit_kontakt_frame, text=u"Číslo", bg="#32CD32", font="Arial_black 10 bold")
        upravit_cislo_label.grid(row=1, column=2)
        jmeno_label = tk.Label(upravit_kontakt_frame, text=u"Jméno", bg="#32CD32", font="Arial_black 10 bold")
        jmeno_label.grid(row=1, column=1)
        zkratka_entry = tk.Entry(upravit_kontakt_frame, bg="#99FF99")
        zkratka_entry.grid(row=2, column=0)
        zkratka_entry.insert(tk.END, kontakt[0])
        cislo_entry = tk.Entry(upravit_kontakt_frame, bg="#99FF99")
        cislo_entry.grid(row=2, column=2)
        cislo_entry.insert(tk.END, kontakt[2])
        jmeno_entry = tk.Entry(upravit_kontakt_frame, bg="#99FF99")
        jmeno_entry.grid(row=2, column=1)
        jmeno_entry.insert(tk.END, kontakt[1])
        upravit_kontakt_button = tk.Button(upravit_kontakt_frame, text="Upravit kontakt", activebackground="#99FF99", bg="#409940", font="Arial_black 8 bold", command=lambda: upravit(kontakt, zkratka_entry, cislo_entry, jmeno_entry, udaje, upravit_kontakt_okno, listbox))
        upravit_kontakt_button.grid(row=3, columnspan=3)
        upravit_kontakt_frame.grid(row=0, column=0)
        upravit_kontakt_okno.mainloop()
    except:
        tkm.showwarning("CHYBA", u"Nezvolil jste žádný kontakt")


def upravit(kontakt, zkratka_entry, cislo_entry, jmeno_entry, udaje, upravit_kontakt_okno, listbox):
    zkratka = str(kontakt[0])
    nova_zkratka = zkratka_entry.get()
    nove_jmeno = jmeno_entry.get()
    nove_cislo = cislo_entry.get()
    nove_udaje = urllib.urlencode({"shortcut": nova_zkratka, "number": nove_cislo, "name": nove_jmeno})
    celkove_udaje = udaje+"&"+nove_udaje
    try:
        upravit = requests.put(url='https://www.odorik.cz/api/v1/speed_dials/'+zkratka+'.json', params=celkove_udaje)
        odpoved_mezikrok = upravit.text
    except:
        tkm.showwarning("CHYBA", u"Nelze se připojit k síti")
    else:
        if odpoved_mezikrok[2] == "e":
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
                elif i == "unauthorized":
                    tkm.showerror("CHYBA", u"Požadavek nelze vykonat")
        else:
            aktualizovat_kontakty_bez_opakovani(udaje, listbox)
            tkm.showinfo(u"Upraveno", u"Kontakt byl úspěšně upraven")
            upravit_kontakt_okno.destroy()


def pridat_kontakt(udaje, listbox):
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
    cislo_entry = tk.Entry(pridat_kontakt_frame, bg="#99FF99")
    cislo_entry.grid(row=2, column=2)
    jmeno_entry = tk.Entry(pridat_kontakt_frame, bg="#99FF99")
    jmeno_entry.grid(row=2, column=1)
    pridat_kontakt_button = tk.Button(pridat_kontakt_frame, text="Přidat kontakt", activebackground="#99FF99", bg="#409940", font="Arial_black 8 bold", command=lambda: pridat(zkratka_entry, cislo_entry, jmeno_entry, pridat_kontakt_okno, udaje, listbox))
    pridat_kontakt_button.grid(row=3, columnspan=3)
    pridat_kontakt_frame.grid(row=0, column=0)
    pridat_kontakt_okno.mainloop()


def pridat(zkratka_entry, cislo_entry, jmeno_entry, pridat_kontakt_okno, udaje, listbox):
    zkratka = zkratka_entry.get()
    cislo = cislo_entry.get()
    jmeno = jmeno_entry.get()
    prihl=httplib.HTTPSConnection("www.odorik.cz")
    dalsi_udaje = urllib.urlencode({'shortcut': zkratka, 'name': jmeno, 'number': cislo})
    celkove_udaje = udaje+"&"+dalsi_udaje
    try:
        prihl.request('POST', "/api/v1/speed_dials.json" , celkove_udaje)
        odp = prihl.getresponse()
        odpoved_mezikrok = odp.read()
        prihl.close()
    except:
        tkm.showwarning("CHYBA", u"Nelze se připojit k síti")
    else:
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
            aktualizovat_kontakty_bez_opakovani(udaje, listbox)
            tkm.showinfo(u"Přidáno", u"Kontakt byl úspěšně přidán")
            pridat_kontakt_okno.destroy()


def odebrat(listbox, udaje, kontakty):
    try:  
        zvoleny_kontakt = map(int, listbox.curselection())
        zkratka = str(kontakty[zvoleny_kontakt[0]][0])
        print zkratka
        if tkm.askokcancel("Smazat", "Jste si jisti?"):
            try:
                smazat = requests.delete(url='https://www.odorik.cz/api/v1/speed_dials/'+zkratka+'.json', params=udaje)
            except:
                tkm.showwarning("CHYBA", u"Nelze se připojit k síti")
            else:
                if smazat.text == "{}":
                    aktualizovat_kontakty_bez_opakovani(udaje, listbox)
                    tkm.showinfo(u"Úspěch", "Kontakt byl úspěšně smazán")
                else:
                    tkm.showwarning("Chyba", "Kontakt se nepovedlo smazat")
    except:
        tkm.showwarning("CHYBA", u"Nezvolil jste žádný kontakt")


def nastavit_moje_cislo(moje_cislo_label):
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
    nastavit_cislo_button = tk.Button(nastavit_cislo, text=u"Nastavit moje číslo", font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940", command=lambda: ulozit_cislo(nastavit_cislo_entry, nastavit_cislo_okno, moje_cislo_label))
    nastavit_cislo_button.grid(row=1, padx=10, pady=10)
    nastavit_cislo.grid()
    nastavit_cislo_okno.mainloop()


def ulozit_cislo(nastavit_cislo_entry, nastavit_cislo_okno, moje_cislo_label):
    cislo = nastavit_cislo_entry.get()
    moje_cislo_soubor = open("moje_cislo.txt", "w")
    moje_cislo_soubor.write(cislo)
    moje_cislo_soubor.close() 
    nastavit_cislo_okno.destroy()
    moje_cislo_label["text"] = cislo


def callback(listbox, kontakty):                 ##vyvolá okno po kliknutí na tlačítko callback
    try:
        moje_cislo_soubor = open("moje_cislo.txt", "r")
        moje_cislo = moje_cislo_soubor.readline()
        moje_cislo_soubor.close()
    except:
        tkm.showwarning("CHYBA", u"Nemáte nastavené vaše číslo")
    else:
        try:  
            zvoleny_kontakt = map(int, listbox.curselection())
            komu_volat = kontakty[zvoleny_kontakt[0]][2]
        except:
            tkm.showwarning("CHYBA", u"Nezvolil jste příjemce")
        else:
            callback_hlavni_okno = tk.Tk()
            callback_okno = tk.Frame(callback_hlavni_okno, bg="#32CD32")
            callback_okno.grid()
            callback_hlavni_okno.title("Callback")  
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
            datum_callback_button = tk.Button(callback_datum_frame, activebackground="#99FF99", text="Objednat dle data", font="Arial_black 8 bold", bg="#409940", command=lambda: callback_datum(listbox, udaje, datum_callback_entry, datum_cas_callback_entry, callback_hlavni_okno, kontakty, komu_volat), width=25)
            datum_callback_button.grid(row=2, columnspan=2, padx=5, pady=10)
            callback_cas_frame = tk.LabelFrame(callback_okno, text="Objednat callback na určený čas", bg="#32CD32", font="Arial_black 8 bold")
            callback_cas_frame.grid(row=1, pady=10)
            minuty_callback_label = tk.Label(callback_cas_frame, text=u"Zpoždění (minuty)", bg="#32CD32", font="Arial_black 10 bold")
            minuty_callback_label.grid(row=0, column=0, columnspan=2)
            global minuty_callback_entry
            minuty_callback_entry = tk.Entry(callback_cas_frame, width=10, justify="center", bg="#99FF99", relief="groove")
            minuty_callback_entry.grid(row=1, column=0, columnspan=2)
            minuty_callback_entry.insert(tk.END, "1")
            minuty_callback_button = tk.Button(callback_cas_frame, activebackground="#99FF99", text="Objednat dle zpoždění", font="Arial_black 8 bold", bg="#409940", command=lambda: callback_cas(listbox, udaje, callback_hlavni_okno, minuty_callback_entry, kontakty, komu_volat), width=25)
            minuty_callback_button.grid(row=2, column=0, columnspan=2, pady=5)
            callback_hlavni_okno.mainloop()
        


def callback_cas(listbox, udaje, callback_hlavni_okno, minuty_callback_entry, kontakty, volane_cislo):
    moje_cislo_soubor = open("moje_cislo.txt", "r")
    moje_cislo = moje_cislo_soubor.readline()
    moje_cislo_soubor.close()
    minuty = minuty_callback_entry.get()
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo, 'delayed': minuty})
    vsechny_udaje = udaje+"&"+cisla
    try:
        objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
        odpoved = objednat_callback.read()
    except:
        tkm.showwarning("CHYBA", u"Nelze se připojit k síti")
    else:
        if odpoved == "successfully_enqueued":
            tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
            callback_hlavni_okno.destroy()
        elif odpoved == "error callback_failed":
            tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
        elif odpoved[:22] == "error missing_argument":
            tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
        elif odpoved == "error invalid_delay_format":
            tkm.showwarning("CHYBA", u"Byl zadán špatný formát spoždění")



def callback_datum(listbox, udaje, datum_callback_entry, datum_cas_callback_entry, callback_hlavni_okno, kontakty, volane_cislo):
    moje_cislo_soubor = open("moje_cislo.txt", "r")
    moje_cislo = moje_cislo_soubor.readline()
    moje_cislo_soubor.close()
    datum = datum_callback_entry.get()+"T"+datum_cas_callback_entry.get()+"+02:00"
    cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo, 'delayed': datum})
    vsechny_udaje = udaje+"&"+cisla
    try:
        objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
        odpoved = objednat_callback.read()
    except:
        tkm.showwarning("CHYBA", u"Nelze se připojit k síti")
    else:
        if odpoved == "successfully_enqueued":
            tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
            callback_hlavni_okno.destroy()
        elif odpoved == "error callback_failed":
            tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
        elif odpoved[:22] == "error missing_argument":
            tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")
        elif odpoved == "error invalid_delay_format":
            tkm.showwarning("CHYBA", u"Datum nebo čas zadáno ve špatném formátu")
        elif odpoved == "error delayed_into_past":
            tkm.showwarning("CHYBA", u"Zadaný moment již proběhl")


def objednat_callback(listbox,udaje, kontakty):  ##objedná callback
    try:
        moje_cislo_soubor = open("moje_cislo.txt", "r")        
        moje_cislo = moje_cislo_soubor.readline()
        moje_cislo_soubor.close()
    except:
        tkm.showwarning("CHYBA", u"Nemáte nastavené vaše číslo")
    try:
        zvoleny_kontakt = map(int, listbox.curselection())
        volane_cislo = kontakty[zvoleny_kontakt[0]][2]
    except:
        tkm.showwarning("CHYBA", u"Nezvolil jste příjemce")
    else:
        cisla = urllib.urlencode({'caller': moje_cislo, 'recipient': volane_cislo})
        vsechny_udaje = udaje+"&"+cisla
        try:
            objednat_callback = urllib.urlopen("https://www.odorik.cz/api/v1/callback", vsechny_udaje)
            odpoved = objednat_callback.read()
        except:
            tkm.showwarning("CHYBA", u"Nelze se připojit k síti")
        else:
            if odpoved == "callback_ordered":
                tkm.showinfo("Callback", u"Callback byl úspěšně objednán")
            elif odpoved == "error callback_failed":
                tkm.showwarning("Callback", u"Požadavek se nepodařilo odeslat na Odorik.cz")
            elif odpoved[:22] == "error missing_argument":
                tkm.showwarning("CHYBA", u"Chybí jeden nebo více argumentů")



# ############################################################################

def ulozit_udaje():             # uloží údaje
    if ulozit_udaje_promenna.get() == 1:
        ul_jmeno = prihl_jmeno_entry.get().strip()
        ul_heslo = heslo_entry.get().strip()
        jmeno_a_heslo = open("jmeno_heslo.txt", "w")
        ul_udaje = ul_jmeno+'\n'+ul_heslo
        print ul_udaje
        jmeno_a_heslo.write(ul_udaje)
        jmeno_a_heslo.close()
    if ulozit_udaje_promenna.get() == 0:
        jmeno_a_heslo = open("jmeno_heslo.txt", "w")
        jmeno_a_heslo.close()


# #############################################################################
# #############################################################################


uplne_hl_okno = tk.Tk()                   # Úvodní přihlašovací okno
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
    flogin = open("jmeno_heslo.txt", "r")
    radky = flogin.readlines()
    flogin.close()
    prihl_jmeno_entry.insert(tk.END, radky[0].strip())
    ulozit_udaje_promenna.set(1)
    heslo_entry.insert(tk.END, radky[1].strip())
except:
    pass


uplne_hl_okno.mainloop()
