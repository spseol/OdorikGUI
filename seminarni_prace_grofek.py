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
                zapsat = "%s      %s" % (i[0], i[1])
                zkratky_jmena.append(zapsat)
            elif len(str(i[0])) == 2:
                zapsat = "%s    %s" % (i[0], i[1])
                zkratky_jmena.append(zapsat)
            else:
                zapsat = "%s  %s" % (i[0], i[1])
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
        posl_hov_datum = tk.Label(posledni_hovor_frame, text="Datum", width=21, bg="#32CD32", font="Arial_black 10 bold")
        posl_hov_datum.grid(row=2)
        posl_hov_cislo = tk.Label(posledni_hovor_frame, text="Číslo", width=21, bg="#32CD32", font="Arial_black 10 bold")
        posl_hov_cislo.grid(row=2, column=1)
        posl_hov_cena = tk.Label(posledni_hovor_frame, text="Cena", width=21, bg="#32CD32", font="Arial_black 10 bold")
        posl_hov_cena.grid(row=2, column=2)
        posl_hov_datum1 = tk.Label(posledni_hovor_frame, text=posl_hovor_datum, width=21, bg="#32CD32", font="Arial_black 8 bold")
        posl_hov_datum1.grid(row=3)
        posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text=posl_hovor_cislo, width=21, bg="#32CD32", font="Arial_black 8 bold")
        posl_hov_cislo1.grid(row=3, column=1)
        posl_hov_cena1 = tk.Label(posledni_hovor_frame, text=str(posl_hovor_cena)+"Kč", width=21, bg="#32CD32", font="Arial_black 8 bold")
        posl_hov_cena1.grid(row=3, column=2)
        pred_posl_hov_datum1 = tk.Label(posledni_hovor_frame, text=pred_posl_hovor_datum, width=21, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_datum1.grid(row=4)
        pred_posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text=pred_posl_hovor_cislo, width=21, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_cislo1.grid(row=4, column=1)
        pred_posl_hov_cena1 = tk.Label(posledni_hovor_frame, text=str(pred_posl_hovor_cena)+"Kč", width=21, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_cena1.grid(row=4, column=2)
        pred_pred_posl_hov_datum1 = tk.Label(posledni_hovor_frame, text=pred_pred_posl_hovor_datum, width=21, bg="#32CD32", font="Arial_black 8 bold")
        pred_pred_posl_hov_datum1.grid(row=5)
        pred_pred_posl_hov_cislo1 = tk.Label(posledni_hovor_frame, text=pred_pred_posl_hovor_cislo, width=21, bg="#32CD32", font="Arial_black 8 bold")
        pred_pred_posl_hov_cislo1.grid(row=5, column=1)
        pred_posl_hov_cena1 = tk.Label(posledni_hovor_frame, text=str(pred_pred_posl_hovor_cena)+"Kč", width=21, bg="#32CD32", font="Arial_black 8 bold")
        pred_posl_hov_cena1.grid(row=5, column=2)
        posledni_hovor_frame.grid(pady=1, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
        info_frame.grid(row=1, columnspan=3, padx=10)
###########################################################################      
        callback_frame = tk.LabelFrame(prihl_okno, text="Callback", bg="#32CD32", font="Arial_black 8 bold")
        global zkratka_jmeno_promenna
        zkratka_jmeno_promenna = tk.StringVar(callback_frame)
        zkratka_jmeno_promenna.set(zkratky_jmena[0])
        zkratka_optmenu = tk.OptionMenu(callback_frame, zkratka_jmeno_promenna, *zkratky_jmena, command= dopln_cislo)
        zkratka_optmenu.config(bg="#409940", activebackground="#99FF99", font="Arial_black 10 bold", highlightbackground="#99FF99")                                    
        zkratka_optmenu.grid(row=0, sticky=tk.E+tk.W+tk.N+tk.S, padx= 10, pady=10)
        global cislo_label
        cislo_label = tk.Label(callback_frame, bg="#99FF99", relief="groove", text=kontakty[0][2], width=65, font="Arial_black 10 bold")
        cislo_label.grid(row=1, sticky=tk.E+tk.W+tk.N+tk.S, padx= 10, pady=10)
        callback_podframe = tk.Frame(callback_frame, bg="#32CD32")
        callback_podframe.grid(row=2, sticky=tk.E+tk.W+tk.N+tk.S)
        callback_button = tk.Button(callback_podframe, text="Objednat callback", font="Arial_black 10 bold", activebackground="#99FF99", command=lambda: objednat_callback(cislo_label, udaje), bg="#409940", width=25)
        callback_button.grid(row=0, column=0, padx=28, pady=5, sticky=tk.W)
        spozdeny_callback_button = tk.Button(callback_podframe, text="Objednat zpožděný callback", font="Arial_black 10 bold", activebackground="#99FF99", command=lambda:callback(cislo_label), bg="#409940", width=25)
        spozdeny_callback_button.grid(row=0, column=1, sticky=tk.E, padx=28, pady=5)
        callback_frame.grid(row=2, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S, padx= 10, pady=5)
########################################################################### 
        kontakty_frame = tk.LabelFrame(prihl_okno, text="Kontakty", bg="#32CD32", font="Arial_black 8 bold")
        listboxy_frame = tk.Frame(kontakty_frame, bg="#32CD32")
        listboxy_frame.grid(row=0, column=0, padx=5)
        scrollbar = tk.Scrollbar(listboxy_frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(listboxy_frame, yscrollcommand=scrollbar.set, width=50, bg="#99FF99", font="Arial_black 8 bold", bd=0)
        listbox2 = tk.Listbox(listboxy_frame, yscrollcommand=scrollbar.set, width=35, bg="#99FF99", font="Arial_black 8 bold", bd=0) 
        scrollbar.grid(row=0, column=2, sticky=tk.S+tk.N)
        listbox2.grid(row=0, column=1)
        listbox.grid(row=0, column=0)
        scrollbar.config(command=listbox.yview)
        scrollbar.config(command=listbox2.yview)
        for i in kontakty:
            listbox2.insert(tk.END, i[2])
        for i in zkratky_jmena:
            listbox.insert(tk.END, i)
        kontakty_frame.grid(row=3, columnspan=3, padx=10, pady=10, sticky=tk.E+tk.W+tk.N+tk.S)
        kontakty_buttony_frame = tk.Frame(kontakty_frame, bg="#32CD32")
        pridat_button = tk.Button(kontakty_buttony_frame, text="Přidat kontakt", font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940", command=pridat_kontakt)
        pridat_button.grid(row=0, column=0, padx=20, pady=10)
        odebrat_button = tk.Button(kontakty_buttony_frame, text="Odebrat kontakt", command=odebrat, font="Arial_black 8 bold", activebackground="#99FF99", bg="#409940")
        odebrat_button.grid(row=0, column=1,pady=10 , padx=20)
        kontakty_buttony_frame.grid(row=1, columnspan=3)


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