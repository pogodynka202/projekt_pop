from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

pracownicy = []
stacje = []


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


def aktualizuj_dropdown_stacji():
    menu = dropdown_stacje["menu"]
    menu.delete(0, "end")
    for s in stacje:
        menu.add_command(label=s.nazwa, command=lambda value=s.nazwa: wybrana_stacja.set(value))
    if stacje:
        wybrana_stacja.set(stacje[0].nazwa)
    else:
        wybrana_stacja.set("")


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


root = Tk()
root.geometry("1400x800")
root.title("System zarządzania stacjami i pracownikami")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)
ramka_stacje = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=3)
ramka_mapa.grid(row=2, column=0, columnspan=3)
ramka_stacje.grid(row=0, column=2)

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

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1400, height=500, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=2)

root.mainloop()
