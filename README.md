# Symulacja Wybuchu Bomby Grzybowej 3D

## Opis Projektu

Projekt jest interaktywną symulacją 3D wybuchu bomby, stworzoną w języku Python przy użyciu bibliotek Pygame, PyOpenGL oraz Pygame GUI. Aplikacja renderuje trójwymiarową scenę, w której użytkownik może obserwować opadanie bomby, eksplozję, formowanie się krateru, fali uderzeniowej oraz chmury grzybowej. Kluczowym elementem jest panel kontrolny, który pozwala na modyfikację parametrów symulacji w czasie rzeczywistym.

## Funkcjonalności
A
*   **Scena 3D:** Renderowanie środowiska i obiektów w 3D przy użyciu OpenGL.
*   **Interaktywny Panel GUI:** Panel po prawej stronie ekranu pozwala na dynamiczną zmianę parametrów symulacji, takich jak:
    *   Ogólna skala eksplozji.
    *   Parametry chmury (rozrzut, opór powietrza).
    *   Parametry piasku (prędkość, grawitacja).
    *   Wizualna skala modelu bomby.
*   **System Cząstek:** Symulacja chmury dymu oraz piasku wyrzucanego podczas eksplozji.
*   **Dynamiczne Efekty:**
    *   **Krater:** Po eksplozji na ziemi pojawia się krater, którego rozmiar zależy od skali wybuchu.
    *   **Fala uderzeniowa:** Wizualny efekt rozchodzącej się fali uderzeniowej.
*   **Model 3D Bomby:** Wczytywanie i wyświetlanie prostego modelu bomby z pliku `bomb.obj`.
*   **Zapis i Odczyt Ustawień:** Możliwość zapisania bieżących ustawień do pliku `settings.json`, które są automatycznie wczytywane przy ponownym uruchomieniu aplikacji.
*   **Sterowanie Kamerą:** Pełna kontrola nad kamerą (obrót za pomocą myszy i klawiszy strzałek, zoom za pomocą kółka myszy).

---

## Instalacja i Wymagania

1.  Upewnij się, że masz zainstalowanego **Pythona w wersji 3.x**.
2.  Zainstaluj wymagane biblioteki za pomocą menedżera pakietów pip, wykonując w terminalu poniższe polecenie:

```bash
pip install pygame pygame_gui PyOpenGL PyOpenGL_accelerate
```

## Uruchomienie

Aby uruchomić symulację, przejdź do głównego katalogu projektu w terminalu i wykonaj polecenie:

```bash
python mushroom_explosion.py
```

---

## Sterowanie

*   **Obrót kamery:**
    *   Przeciąganie myszą z wciśniętym lewym przyciskiem (gdy kursor jest nad sceną 3D).
    *   Klawisze strzałek (Góra, Dół, Lewo, Prawo).
*   **Zoom kamery:** Kółko myszy (gdy kursor jest nad sceną 3D).
*   **Interakcja z Panelem GUI:** Klikanie i przeciąganie suwaków w panelu po prawej stronie, aby zmienić parametry.
*   **Przyciski w GUI:**
    *   **"Resetuj Symulację"**: Przywraca symulację do stanu początkowego.
    *   **"Zapisz Ustawienia"**: Zapisuje aktualne wartości suwaków do pliku `settings.json`.

**Uwaga:** Sterowanie kamerą jest zablokowane, gdy kursor myszy znajduje się nad panelem GUI.

---

## Struktura Projektu

```
.
├── mushroom_explosion.py   # Główny plik aplikacji, pętla gry, obsługa GUI
├── config.py               # Plik konfiguracyjny (stałe, domyślne wartości)
├── settings.json           # Plik z zapisanymi ustawieniami (tworzony automatycznie)
├── bomb.obj                # Model 3D bomby
├── entities/               # Moduły definiujące obiekty w symulacji
│   ├── bomb.py             # Logika bomby (spadanie, eksplozja, model)
│   ├── particle.py         # Logika cząstek chmury
│   ├── sand_particle.py    # Logika cząstek piasku
│   └── shockwave.py        # Logika fali uderzeniowej
└── graphics/               # Moduły graficzne
    └── drawing.py          # Funkcje rysujące (podłoże, krater, tło)
```

## Autorzy

*   Kacper Lange
*   Jakub Linda
*   Jakub Maciejewski
