from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

pracownicy = []
stacje = []
klienci = []

def focus_next_entry(event, next_entry):
    next_entry.focus()
    return "break"

# --------- KLASY ---------
class Stacja:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=nazwa)

    def pobierz_wspolrzedne(self):
        url = f"https://pl.wikipedia.org/wiki/{self.nazwa}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [lat, lon]

class Pracownik:
    def __init__(self, imie, nazwisko, posty, stacja_obiekt):
        self.imie = imie
        self.nazwisko = nazwisko
        self.posty = posty
        self.stacja = stacja_obiekt.nazwa
        self.wspolrzedne = stacja_obiekt.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=imie + " " + nazwisko)

class Klient:
    def __init__(self, imie, firma, stacja_obiekt):
        self.imie = imie
        self.firma = firma
        self.stacja = stacja_obiekt.nazwa
        self.wspolrzedne = stacja_obiekt.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{firma} ({imie})")

# --------- FUNKCJE ---------
def aktualizuj_dropdown_stacji():
    dropdown_stacje['values'] = [s.nazwa for s in stacje]
    dropdown_stacje_klienta['values'] = [s.nazwa for s in stacje]
    dropdown_stacja_mapy_klienci['values'] = [s.nazwa for s in stacje]
    dropdown_stacja_mapy_pracownicy['values'] = [s.nazwa for s in stacje]
    if stacje:
        wybrana_stacja.set(stacje[0].nazwa)
        wybrana_stacja_klienta.set(stacje[0].nazwa)
        wybrana_stacja_mapy_klienci.set(stacje[0].nazwa)
        wybrana_stacja_mapy_pracownicy.set(stacje[0].nazwa)
    else:
        wybrana_stacja.set("")
        wybrana_stacja_klienta.set("")
        wybrana_stacja_mapy_klienci.set("")
        wybrana_stacja_mapy_pracownicy.set("")


def dodaj_pracownika():
    imie = entry_name.get()
    nazwisko = entry_surname.get()
    posty = entry_posts.get()
    nazwa_stacji = wybrana_stacja.get()
    stacja_obiekt = next((s for s in stacje if s.nazwa == nazwa_stacji), None)
    if stacja_obiekt:
        pracownicy.append(Pracownik(imie, nazwisko, posty, stacja_obiekt))
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_posts.delete(0, END)
    wybrana_stacja.set(stacje[0].nazwa if stacje else "")
    entry_name.focus()
    pokaz_pracownikow()

def pokaz_pracownikow():
    listbox_lista_obiektow.delete(0, END)
    for idx, p in enumerate(pracownicy):
        listbox_lista_obiektow.insert(idx, f"{idx + 1}. {p.imie} {p.nazwisko}")

def usun_pracownika():
    i = listbox_lista_obiektow.index(ACTIVE)
    pracownicy[i].marker.delete()
    pracownicy.pop(i)
    pokaz_pracownikow()

def pokaz_pracownikow_dla_stacji():
    nazwa_stacji = wybrana_stacja_mapy_pracownicy.get()
    map_widget.delete_all_marker()
    for p in pracownicy:
        if p.stacja == nazwa_stacji:
            p.marker = map_widget.set_marker(p.wspolrzedne[0], p.wspolrzedne[1], text=f"{p.imie} {p.nazwisko}")


def pokaz_szczegoly():
    i = listbox_lista_obiektow.index(ACTIVE)
    p = pracownicy[i]
    label_name_szczegoly_obiektow_wartosc.config(text=p.imie)
    label_surname_szczegoly_obiektow_wartosc.config(text=p.nazwisko)
    label_posts_szczegoly_obiektow_wartosc.config(text=p.posty)
    label_stacja_szczegoly.config(text=p.stacja)
    map_widget.set_position(p.wspolrzedne[0], p.wspolrzedne[1])
    map_widget.set_zoom(14)

def edytuj_pracownika():
    i = listbox_lista_obiektow.index(ACTIVE)
    p = pracownicy[i]
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_posts.delete(0, END)
    entry_name.insert(0, p.imie)
    entry_surname.insert(0, p.nazwisko)
    entry_posts.insert(0, p.posty)
    wybrana_stacja.set(p.stacja)
    button_dodaj_obiekt.config(text="Zapisz", command=lambda: zapisz_edycje(i))

def zapisz_edycje(i):
    imie = entry_name.get()
    nazwisko = entry_surname.get()
    posty = entry_posts.get()
    nazwa_stacji = wybrana_stacja.get()
    stacja_obiekt = next((s for s in stacje if s.nazwa == nazwa_stacji), None)
    if stacja_obiekt:
        pracownicy[i].marker.delete()
        pracownicy[i] = Pracownik(imie, nazwisko, posty, stacja_obiekt)
    pokaz_pracownikow()
    button_dodaj_obiekt.config(text="Dodaj pracownika", command=dodaj_pracownika)
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_posts.delete(0, END)
    wybrana_stacja.set(stacje[0].nazwa if stacje else "")
    entry_name.focus()

def pokaz_wszystkich_pracownikow():
    map_widget.delete_all_marker()
    for p in pracownicy:
        p.marker = map_widget.set_marker(p.wspolrzedne[0], p.wspolrzedne[1], text=f"{p.imie} {p.nazwisko}")


def dodaj_stacje():
    nazwa = entry_nazwa_stacji.get()
    if nazwa:
        stacje.append(Stacja(nazwa))
        entry_nazwa_stacji.delete(0, END)
        pokaz_stacje()
        aktualizuj_dropdown_stacji()

def pokaz_stacje():
    listbox_stacje.delete(0, END)
    for idx, s in enumerate(stacje):
        listbox_stacje.insert(idx, f"{idx + 1}. {s.nazwa}")

def usun_stacje():
    i = listbox_stacje.index(ACTIVE)
    stacje[i].marker.delete()
    stacje.pop(i)
    pokaz_stacje()
    aktualizuj_dropdown_stacji()

def edytuj_stacje():
    i = listbox_stacje.index(ACTIVE)
    entry_nazwa_stacji.delete(0, END)
    entry_nazwa_stacji.insert(0, stacje[i].nazwa)
    button_dodaj_stacje.config(text="Zapisz", command=lambda: zapisz_edycje_stacji(i))

def zapisz_edycje_stacji(i):
    nowa_nazwa = entry_nazwa_stacji.get()
    stacje[i].marker.delete()
    stacje[i] = Stacja(nowa_nazwa)
    pokaz_stacje()
    aktualizuj_dropdown_stacji()
    button_dodaj_stacje.config(text="Dodaj stację", command=dodaj_stacje)
    entry_nazwa_stacji.delete(0, END)

def pokaz_szczegoly_stacji():
    i = listbox_stacje.index(ACTIVE)
    s = stacje[i]
    map_widget.set_position(s.wspolrzedne[0], s.wspolrzedne[1])
    map_widget.set_zoom(10)

def pokaz_wszystkie_stacje():
    map_widget.delete_all_marker()
    for s in stacje:
        s.marker = map_widget.set_marker(s.wspolrzedne[0], s.wspolrzedne[1], text=s.nazwa)


def dodaj_klienta():
    imie = entry_klient_imie.get()
    firma = entry_klient_firma.get()
    nazwa_stacji = wybrana_stacja_klienta.get()
    stacja_obiekt = next((s for s in stacje if s.nazwa == nazwa_stacji), None)
    if stacja_obiekt:
        klienci.append(Klient(imie, firma, stacja_obiekt))
    entry_klient_imie.delete(0, END)
    entry_klient_firma.delete(0, END)
    wybrana_stacja_klienta.set(stacje[0].nazwa if stacje else "")
    entry_klient_imie.focus()
    pokaz_klientow()

def pokaz_klientow():
    listbox_klienci.delete(0, END)
    for idx, k in enumerate(klienci):
        listbox_klienci.insert(idx, f"{idx + 1}. {k.firma} - {k.imie}")

def pokaz_klientow_dla_stacji():
    nazwa_stacji = wybrana_stacja_mapy_klienci.get()
    map_widget.delete_all_marker()
    for k in klienci:
        if k.stacja == nazwa_stacji:
            k.marker = map_widget.set_marker(k.wspolrzedne[0], k.wspolrzedne[1], text=f"{k.firma} ({k.imie})")



def usun_klienta():
    i = listbox_klienci.index(ACTIVE)
    klienci[i].marker.delete()
    klienci.pop(i)
    pokaz_klientow()

def edytuj_klienta():
    i = listbox_klienci.index(ACTIVE)
    k = klienci[i]
    entry_klient_imie.delete(0, END)
    entry_klient_firma.delete(0, END)
    entry_klient_imie.insert(0, k.imie)
    entry_klient_firma.insert(0, k.firma)
    wybrana_stacja_klienta.set(k.stacja)
    button_dodaj_klienta.config(text="Zapisz", command=lambda: zapisz_edycje_klienta(i))

def zapisz_edycje_klienta(i):
    imie = entry_klient_imie.get()
    firma = entry_klient_firma.get()
    nazwa_stacji = wybrana_stacja_klienta.get()
    stacja_obiekt = next((s for s in stacje if s.nazwa == nazwa_stacji), None)
    if stacja_obiekt:
        klienci[i].marker.delete()
        klienci[i] = Klient(imie, firma, stacja_obiekt)
    pokaz_klientow()
    button_dodaj_klienta.config(text="Dodaj klienta", command=dodaj_klienta)
    entry_klient_imie.delete(0, END)
    entry_klient_firma.delete(0, END)
    wybrana_stacja_klienta.set(stacje[0].nazwa if stacje else "")
    entry_klient_imie.focus()

def pokaz_wszystkich_klientow():
    map_widget.delete_all_marker()
    for k in klienci:
        k.marker = map_widget.set_marker(k.wspolrzedne[0], k.wspolrzedne[1], text=f"{k.firma} ({k.imie})")

# --------- GUI ---------
root = Tk()
root.geometry("800x1000")
root.title("System zarządzania stacjami, pracownikami i klientami")

ramka_gora = Frame(root)
ramka_gora.grid(row=0, column=0, columnspan=3, sticky="ew")
ramka_lewa = Frame(ramka_gora)
ramka_srodek = Frame(ramka_gora)
ramka_prawa = Frame(ramka_gora)
ramka_mapa = Frame(root)

ramka_lewa.grid(row=0, column=0, sticky="n", padx=12, pady=8)
ramka_srodek.grid(row=0, column=1, sticky="n", padx=12, pady=8)
ramka_prawa.grid(row=0, column=2, sticky="n", padx=12, pady=8)
ramka_mapa.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# --- Pracownicy ---

ttk.Label(ramka_lewa, text="Lista pracowników", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow = Listbox(ramka_lewa, width=38, height=12)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3, pady=(0, 8))

ttk.Button(ramka_lewa, text="Edytuj", command=edytuj_pracownika).grid(row=2, column=0, sticky="ew")
ttk.Button(ramka_lewa, text="Usuń", command=usun_pracownika).grid(row=2, column=1, sticky="ew")

ttk.Label(ramka_lewa, text="Formularz pracownika", font=("Arial", 11, "bold")).grid(row=3, column=0, columnspan=3, pady=(8, 0))
ttk.Label(ramka_lewa, text="Imię:").grid(row=4, column=0, sticky="e")
entry_name = ttk.Entry(ramka_lewa)
entry_name.grid(row=4, column=1, columnspan=2, sticky="ew")
ttk.Label(ramka_lewa, text="Nazwisko:").grid(row=5, column=0, sticky="e")
entry_surname = ttk.Entry(ramka_lewa)
entry_surname.grid(row=5, column=1, columnspan=2, sticky="ew")
ttk.Label(ramka_lewa, text="Posty:").grid(row=6, column=0, sticky="e")
entry_posts = ttk.Entry(ramka_lewa)
entry_posts.grid(row=6, column=1, columnspan=2, sticky="ew")
ttk.Label(ramka_lewa, text="Stacja:").grid(row=7, column=0, sticky="e")
wybrana_stacja = StringVar()
dropdown_stacje = ttk.Combobox(ramka_lewa, textvariable=wybrana_stacja, state="readonly", width=18)
dropdown_stacje.grid(row=7, column=1, columnspan=2, sticky="ew")

button_dodaj_obiekt = ttk.Button(ramka_lewa, text="Dodaj pracownika", command=dodaj_pracownika)
button_dodaj_obiekt.grid(row=8, column=0, columnspan=3, pady=(7, 0), sticky="ew")

label_szczegoly_header = ttk.Label(ramka_lewa, text="Szczegóły pracownika", font=("Arial", 11, "bold"))
label_szczegoly_header.grid(row=9, column=0, columnspan=3, pady=(10, 0))

label_name_szczegoly_obiektow = ttk.Label(ramka_lewa, text="Imię:")
label_name_szczegoly_obiektow.grid(row=10, column=0, sticky="e")
label_name_szczegoly_obiektow_wartosc = ttk.Label(ramka_lewa, text="")
label_name_szczegoly_obiektow_wartosc.grid(row=10, column=1, columnspan=2, sticky="w")

label_surname_szczegoly_obiektow = ttk.Label(ramka_lewa, text="Nazwisko:")
label_surname_szczegoly_obiektow.grid(row=11, column=0, sticky="e")
label_surname_szczegoly_obiektow_wartosc = ttk.Label(ramka_lewa, text="")
label_surname_szczegoly_obiektow_wartosc.grid(row=11, column=1, columnspan=2, sticky="w")

label_posts_szczegoly_obiektow = ttk.Label(ramka_lewa, text="Posty:")
label_posts_szczegoly_obiektow.grid(row=12, column=0, sticky="e")
label_posts_szczegoly_obiektow_wartosc = ttk.Label(ramka_lewa, text="")
label_posts_szczegoly_obiektow_wartosc.grid(row=12, column=1, columnspan=2, sticky="w")

label_stacja_szczegoly_label = ttk.Label(ramka_lewa, text="Stacja:")
label_stacja_szczegoly_label.grid(row=13, column=0, sticky="e")
label_stacja_szczegoly = ttk.Label(ramka_lewa, text="")
label_stacja_szczegoly.grid(row=13, column=1, columnspan=2, sticky="w")

# --- Stacje ---
ttk.Label(ramka_srodek, text="Lista stacji", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=3)
listbox_stacje = Listbox(ramka_srodek, width=38, height=12)
listbox_stacje.grid(row=1, column=0, columnspan=3, pady=(0, 8))

ttk.Button(ramka_srodek, text="Edytuj", command=edytuj_stacje).grid(row=2, column=0, sticky="ew")
ttk.Button(ramka_srodek, text="Usuń", command=usun_stacje).grid(row=2, column=1, sticky="ew")

ttk.Label(ramka_srodek, text="Dodaj nową stację", font=("Arial", 11, "bold")).grid(row=3, column=0, columnspan=3, pady=(8, 0))
entry_nazwa_stacji = ttk.Entry(ramka_srodek)
entry_nazwa_stacji.grid(row=4, column=0, columnspan=2, sticky="ew")
button_dodaj_stacje = ttk.Button(ramka_srodek, text="Dodaj stację", command=dodaj_stacje)
button_dodaj_stacje.grid(row=4, column=2, sticky="ew")

# --- Klienci ---
ttk.Label(ramka_prawa, text="Lista klientów", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=3)
listbox_klienci = Listbox(ramka_prawa, width=38, height=12)
listbox_klienci.grid(row=1, column=0, columnspan=3, pady=(0, 8))

ttk.Button(ramka_prawa, text="Edytuj", command=edytuj_klienta).grid(row=2, column=0, sticky="ew")
ttk.Button(ramka_prawa, text="Usuń", command=usun_klienta).grid(row=2, column=1, sticky="ew")

ttk.Label(ramka_prawa, text="Dodaj klienta", font=("Arial", 11, "bold")).grid(row=3, column=0, columnspan=3, pady=(8, 0))
ttk.Label(ramka_prawa, text="Imię:").grid(row=4, column=0, sticky="e")
entry_klient_imie = ttk.Entry(ramka_prawa)
entry_klient_imie.grid(row=4, column=1, columnspan=2, sticky="ew")
ttk.Label(ramka_prawa, text="Firma:").grid(row=5, column=0, sticky="e")
entry_klient_firma = ttk.Entry(ramka_prawa)
entry_klient_firma.grid(row=5, column=1, columnspan=2, sticky="ew")
ttk.Label(ramka_prawa, text="Stacja:").grid(row=6, column=0, sticky="e")
wybrana_stacja_klienta = StringVar()
dropdown_stacje_klienta = ttk.Combobox(ramka_prawa, textvariable=wybrana_stacja_klienta, state="readonly", width=18)
dropdown_stacje_klienta.grid(row=6, column=1, columnspan=2, sticky="ew")
button_dodaj_klienta = ttk.Button(ramka_prawa, text="Dodaj klienta", command=dodaj_klienta)
button_dodaj_klienta.grid(row=7, column=0, columnspan=3, pady=(7, 0), sticky="ew")

# --- Mapa ---
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=800, height=420, corner_radius=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

# --- Filtry pod mapą ---
ramka_filtry_mapy = Frame(root)
ramka_filtry_mapy.grid(row=3, column=0, columnspan=3, pady=(5, 10), sticky="ew")

ttk.Label(ramka_filtry_mapy, text="Pokaż klientów dla stacji:").grid(row=0, column=0, sticky="w")
wybrana_stacja_mapy_klienci = StringVar()
dropdown_stacja_mapy_klienci = ttk.Combobox(ramka_filtry_mapy, textvariable=wybrana_stacja_mapy_klienci, state="readonly", width=14)
dropdown_stacja_mapy_klienci.grid(row=0, column=1, sticky="w")
ttk.Button(ramka_filtry_mapy, text="Pokaż klientów", command=pokaz_klientow_dla_stacji).grid(row=0, column=2, sticky="w", padx=5)

ttk.Label(ramka_filtry_mapy, text="Pokaż pracowników dla stacji:").grid(row=1, column=0, sticky="w")
wybrana_stacja_mapy_pracownicy = StringVar()
dropdown_stacja_mapy_pracownicy = ttk.Combobox(ramka_filtry_mapy, textvariable=wybrana_stacja_mapy_pracownicy, state="readonly", width=14)
dropdown_stacja_mapy_pracownicy.grid(row=1, column=1, sticky="w")
ttk.Button(ramka_filtry_mapy, text="Pokaż pracowników", command=pokaz_pracownikow_dla_stacji).grid(row=1, column=2, sticky="w", padx=5)

ttk.Button(ramka_filtry_mapy, text="Wszyscy klienci", command=pokaz_wszystkich_klientow).grid(
    row=2, column=0, pady=(6, 0), sticky="w", padx=(0, 10)
)
ttk.Button(ramka_filtry_mapy, text="Wszyscy pracownicy", command=pokaz_wszystkich_pracownikow).grid(
    row=2, column=1, pady=(6, 0), sticky="w", padx=(0, 10)
)
ttk.Button(ramka_filtry_mapy, text="Wszystkie stacje", command=pokaz_wszystkie_stacje).grid(
    row=2, column=2, pady=(6, 0), sticky="w"
)


aktualizuj_dropdown_stacji()
root.mainloop()