from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

pracownicy = []
stacje = []
klienci = []


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


def aktualizuj_dropdown_stacji():
    menu = dropdown_stacje["menu"]
    menu.delete(0, "end")
    for s in stacje:
        menu.add_command(label=s.nazwa, command=lambda value=s.nazwa: wybrana_stacja.set(value))
    if stacje:
        wybrana_stacja.set(stacje[0].nazwa)
    else:
        wybrana_stacja.set("")

    menu_klient = dropdown_stacje_klienta["menu"]
    menu_klient.delete(0, "end")
    for s in stacje:
        menu_klient.add_command(label=s.nazwa, command=lambda value=s.nazwa: wybrana_stacja_klienta.set(value))
    if stacje:
        wybrana_stacja_klienta.set(stacje[0].nazwa)
    else:
        wybrana_stacja_klienta.set("")

    menu_mapa_klienci = dropdown_stacja_mapy_klienci["menu"]
    menu_mapa_klienci.delete(0, "end")
    for s in stacje:
        menu_mapa_klienci.add_command(label=s.nazwa, command=lambda value=s.nazwa: wybrana_stacja_mapy_klienci.set(value))
    if stacje:
        wybrana_stacja_mapy_klienci.set(stacje[0].nazwa)
    else:
        wybrana_stacja_mapy_klienci.set("")

    menu_mapa_pracownicy = dropdown_stacja_mapy_pracownicy["menu"]
    menu_mapa_pracownicy.delete(0, "end")
    for s in stacje:
        menu_mapa_pracownicy.add_command(label=s.nazwa, command=lambda value=s.nazwa: wybrana_stacja_mapy_pracownicy.set(value))
    if stacje:
        wybrana_stacja_mapy_pracownicy.set(stacje[0].nazwa)
    else:
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
    wybrana_stacja.set("")
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
    for s in stacje:
        s.marker = map_widget.set_marker(s.wspolrzedne[0], s.wspolrzedne[1], text=s.nazwa)
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
    wybrana_stacja.set("")
    entry_name.focus()


def pokaz_wszystkich_pracownikow():
    map_widget.delete_all_marker()
    for s in stacje:
            s.marker = map_widget.set_marker(s.wspolrzedne[0], s.wspolrzedne[1], text=s.nazwa)
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


def dodaj_klienta():
    imie = entry_klient_imie.get()
    firma = entry_klient_firma.get()
    nazwa_stacji = wybrana_stacja_klienta.get()
    stacja_obiekt = next((s for s in stacje if s.nazwa == nazwa_stacji), None)
    if stacja_obiekt:
        klienci.append(Klient(imie, firma, stacja_obiekt))
    entry_klient_imie.delete(0, END)
    entry_klient_firma.delete(0, END)
    wybrana_stacja_klienta.set("")
    entry_klient_imie.focus()
    pokaz_klientow()


def pokaz_klientow():
    listbox_klienci.delete(0, END)
    for idx, k in enumerate(klienci):
        listbox_klienci.insert(idx, f"{idx + 1}. {k.firma} - {k.imie}")

def pokaz_klientow_dla_stacji():
    nazwa_stacji = wybrana_stacja_mapy_klienci.get()
    map_widget.delete_all_marker()
    for s in stacje:
        s.marker = map_widget.set_marker(s.wspolrzedne[0], s.wspolrzedne[1], text=s.nazwa)
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
    wybrana_stacja_klienta.set("")
    entry_klient_imie.focus()

def pokaz_wszystkich_klientow():
    map_widget.delete_all_marker()
    for s in stacje:
        s.marker = map_widget.set_marker(s.wspolrzedne[0], s.wspolrzedne[1], text=s.nazwa)
    for k in klienci:
        k.marker = map_widget.set_marker(k.wspolrzedne[0], k.wspolrzedne[1], text=f"{k.firma} ({k.imie})")


root = Tk()
root.geometry("1400x900")
root.title("System zarządzania stacjami, pracownikami i klientami")

# Ramki
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)
ramka_stacje = Frame(root)
ramka_klient = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_stacje.grid(row=0, column=2)
ramka_klient.grid(row=1, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=3)
ramka_mapa.grid(row=2, column=0, columnspan=3)

Label(ramka_mapa, text="Pokaż klientów dla wybranej stacji:").grid(row=1, column=0, sticky=W)
wybrana_stacja_mapy_klienci = StringVar()
dropdown_stacja_mapy_klienci = OptionMenu(ramka_mapa, wybrana_stacja_mapy_klienci, "")
dropdown_stacja_mapy_klienci.grid(row=1, column=1, sticky=W)
button_pokaz_klientow_dla_stacji = Button(ramka_mapa, text="Pokaż klientów dla stacji", command=pokaz_klientow_dla_stacji)
button_pokaz_klientow_dla_stacji.grid(row=1, column=2, sticky=W)

Label(ramka_mapa, text="Pokaż pracowników dla wybranej stacji:").grid(row=2, column=0, sticky=W)
wybrana_stacja_mapy_pracownicy = StringVar()
dropdown_stacja_mapy_pracownicy = OptionMenu(ramka_mapa, wybrana_stacja_mapy_pracownicy, "")
dropdown_stacja_mapy_pracownicy.grid(row=2, column=1, sticky=W)
button_pokaz_pracownikow_dla_stacji = Button(ramka_mapa, text="Pokaż pracowników dla stacji", command=pokaz_pracownikow_dla_stacji)
button_pokaz_pracownikow_dla_stacji.grid(row=2, column=2, sticky=W)

button_pokaz_wszystkich_klientow = Button(ramka_mapa, text="Pokaż wszystkich klientów", command=pokaz_wszystkich_klientow)
button_pokaz_wszystkich_klientow.grid(row=3, column=0, columnspan=2, sticky=W)

button_pokaz_wszystkich_pracownikow = Button(ramka_mapa, text="Pokaż wszystkich pracowników", command=pokaz_wszystkich_pracownikow)
button_pokaz_wszystkich_pracownikow.grid(row=4, column=0, columnspan=2, sticky=W)

# Pracownicy
Label(ramka_lista_obiektow, text="Lista pracowników").grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50, height=15)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=pokaz_szczegoly).grid(row=2, column=0)
Button(ramka_lista_obiektow, text="Usuń", command=usun_pracownika).grid(row=2, column=1)
Button(ramka_lista_obiektow, text="Edytuj", command=edytuj_pracownika).grid(row=2, column=2)

Label(ramka_formularz, text="Formularz pracownika").grid(row=0, column=0, columnspan=2)
Label(ramka_formularz, text="Imię:").grid(row=1, column=0, sticky=W)
Label(ramka_formularz, text="Nazwisko:").grid(row=2, column=0, sticky=W)
Label(ramka_formularz, text="Posty:").grid(row=3, column=0, sticky=W)
Label(ramka_formularz, text="Stacja:").grid(row=4, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_surname = Entry(ramka_formularz)
entry_surname.grid(row=2, column=1)
entry_posts = Entry(ramka_formularz)
entry_posts.grid(row=3, column=1)

wybrana_stacja = StringVar()
dropdown_stacje = OptionMenu(ramka_formularz, wybrana_stacja, "")
dropdown_stacje.grid(row=4, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj pracownika", command=dodaj_pracownika)
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

Label(ramka_szczegoly_obiektow, text="Szczegóły:").grid(row=0, column=0)
Label(ramka_szczegoly_obiektow, text="Imię:").grid(row=1, column=0)
label_name_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_name_szczegoly_obiektow_wartosc.grid(row=1, column=1)
Label(ramka_szczegoly_obiektow, text="Nazwisko:").grid(row=1, column=2)
label_surname_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_surname_szczegoly_obiektow_wartosc.grid(row=1, column=3)
Label(ramka_szczegoly_obiektow, text="Posty:").grid(row=1, column=4)
label_posts_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text="...")
label_posts_szczegoly_obiektow_wartosc.grid(row=1, column=5)
Label(ramka_szczegoly_obiektow, text="Stacja:").grid(row=1, column=6)
label_stacja_szczegoly = Label(ramka_szczegoly_obiektow, text="...")
label_stacja_szczegoly.grid(row=1, column=7)

# Stacje
Label(ramka_stacje, text="Lista stacji").grid(row=0, column=0, columnspan=3)
listbox_stacje = Listbox(ramka_stacje, width=50, height=15)
listbox_stacje.grid(row=1, column=0, columnspan=3)
Button(ramka_stacje, text="Szczegóły", command=pokaz_szczegoly_stacji).grid(row=2, column=0)
Button(ramka_stacje, text="Usuń", command=usun_stacje).grid(row=2, column=1)
Button(ramka_stacje, text="Edytuj", command=edytuj_stacje).grid(row=2, column=2)

Label(ramka_stacje, text="Dodaj nową stację").grid(row=3, column=0, columnspan=2)
entry_nazwa_stacji = Entry(ramka_stacje)
entry_nazwa_stacji.grid(row=4, column=0, columnspan=2)
button_dodaj_stacje = Button(ramka_stacje, text="Dodaj stację", command=dodaj_stacje)
button_dodaj_stacje.grid(row=5, column=0, columnspan=2)

# Klienci
Label(ramka_klient, text="Lista klientów").grid(row=0, column=0, columnspan=3)
listbox_klienci = Listbox(ramka_klient, width=50, height=10)
listbox_klienci.grid(row=1, column=0, columnspan=3)
Button(ramka_klient, text="Usuń", command=usun_klienta).grid(row=2, column=0)
Button(ramka_klient, text="Edytuj", command=edytuj_klienta).grid(row=2, column=1)

Label(ramka_klient, text="Dodaj klienta").grid(row=3, column=0, columnspan=2)
Label(ramka_klient, text="Imię:").grid(row=4, column=0)
entry_klient_imie = Entry(ramka_klient)
entry_klient_imie.grid(row=4, column=1)
Label(ramka_klient, text="Firma:").grid(row=5, column=0)
entry_klient_firma = Entry(ramka_klient)
entry_klient_firma.grid(row=5, column=1)

Label(ramka_klient, text="Stacja:").grid(row=6, column=0)
wybrana_stacja_klienta = StringVar()
dropdown_stacje_klienta = OptionMenu(ramka_klient, wybrana_stacja_klienta, "")
dropdown_stacje_klienta.grid(row=6, column=1)

button_dodaj_klienta = Button(ramka_klient, text="Dodaj klienta", command=dodaj_klienta)
button_dodaj_klienta.grid(row=7, column=0, columnspan=2)

# Mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1400, height=500, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=2)

root.mainloop()
