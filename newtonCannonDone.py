import tkinter as tk
from PIL import Image, ImageTk
import math
import sympy as sp
# Inicjalizacja pocisku
def inicjalizacja():
    canvas.delete('pocisk')
    x = 0
    y = promien_ziemi + wysokosc_wyrzutni
    vx = wybor_predkosci.get() * math.cos(math.radians(wybor_katu.get()))
    vy = wybor_predkosci.get() * math.sin(math.radians(wybor_katu.get()))
    wyznaczanie_trasy(x, y, vx, vy)

def wyznaczanie_trasy(x, y, vx, vy):
    r = math.sqrt(x ** 2 + y ** 2)
    if r > promien_ziemi: # Warunek sprawdzający, czy pocisk dotknął Ziemię
        # Obliczenie przyspieszenia Ziemskiego (g)
        ag = stala_grawitacji * masa_ziemi / (r ** 2) #przysp grawitacyjne
        # Oblicz przyspieszenie w danej osi
        ax = - ag * x / r #czyli -ag*cos
        ay = - ag * y / r #czyli -ag*sin
        # Oblicz prędkość
        vx += sp.integrate(ax, (t, 0, dt))
        vy += sp.integrate(ay, (t, 0, dt))
        lastx = x
        # Oblicz współrzędne
        x += sp.integrate(vx, (t, 0, dt))
        y += sp.integrate(vy, (t, 0, dt))
        rysowanie_trasy(x, y)
        
        if not ((lastx < 0) and (x > 0)): # Warunek sprawdzający, czy pocisk wrócił do miejsca początkowego (przeszedł przez x=0)
            if not(x > 2 * promien_ziemi): # Warunek sprawdzający, czy pocisk wyleciał poza okno
                canvas.after(1000 // 120, wyznaczanie_trasy, x, y, vx, vy)
            else:
                print("Pocisk wyleciał")
        else:
            print("pocisk wrócił")

# Funkcja rysująca okręgi reprezentujące trajektorię na canvasie
def rysowanie_trasy(x, y):
    pixel_x = szerokosc / 2 + x / liczba_metrow_w_pikselu
    pixel_y = wysokosc / 2 - y / liczba_metrow_w_pikselu
    canvas.create_oval(pixel_x-2, pixel_y-2, pixel_x+2, pixel_y+2, fill="black", tags="pocisk", width=0.1)


# Tworzenie okna
root = tk.Tk()
root.title("Newton's Cannon")

szerokosc = 500
wysokosc = 500
canvas = tk.Canvas(root, width=szerokosc, height=wysokosc, bg="lightpink")
canvas.pack()


def resizable_callback():
    root.resizable(False, False)

# ustawienie wygladu Gui oraz pozycja przycikow

# Wczytanie obrazka
try:
    image_path = "ZiemiaRys.png"
except:
    print("Nie udało się wczytać obrazka")


resizable_callback()
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

wybor_predkosci = tk.Scale(root, from_=3000, to=10000, resolution=100, orient=tk.HORIZONTAL, length=300, label="Podaj prędkość pocisku")
wybor_predkosci.set(3000)
wybor_predkosci.pack()

wybor_katu = tk.Scale(root, from_=0, to=90, resolution=1, orient=tk.HORIZONTAL, label="Podaj kąt lotu pocisku")
wybor_katu.set(0)
wybor_katu.pack()

przycisk_start = tk.Button(root, text="Start", command=inicjalizacja)
przycisk_start.pack()

przycisk_czysc = tk.Button(root, text="Koniec", command=lambda: canvas.delete("pocisk"))
przycisk_czysc.pack()

# stale rzeczywiste dla ziemi
stala_grawitacji = 6.67e-11
masa_ziemi = 5.972e24
promien_ziemi = 6378000
promien_ziemi = 6378000
liczba_metrow_w_pikselu = promien_ziemi * 2 / (0.7 * szerokosc)
wysokosc_wyrzutni = promien_ziemi * 0.165
dt = 10
t = sp.symbols('t')
root.mainloop()
