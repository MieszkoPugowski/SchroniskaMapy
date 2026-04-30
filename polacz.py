import pandas as pd

def polacz_pliki_excel():
    # 1. Nazwy plików
    file_bazowy = 'schroniska.xlsx'
    file_z_wspolrzednymi = 'Schroniska_gotowe.xlsx'
    output_file = 'schroniska.xlsx'

    try:
        # 2. Wczytanie plików
        print("Wczytywanie plików...")
        df_bazowy = pd.read_excel(file_bazowy)
        df_gotowe = pd.read_excel(file_z_wspolrzednymi)

        # 3. Łączenie plików
        # Wybieramy tylko klucze oraz kolumny lat/lon z pliku wynikowego konwertera
        print("Łączenie danych...")
        df_wynikowy = pd.merge(
            df_bazowy, 
            df_gotowe[['Nazwa schroniska', 'Lokalizacja', 'lat', 'lon']], 
            on=['Nazwa schroniska', 'Lokalizacja'], 
            how='left'
        )

        # 4. Zapisanie do pliku 'schroniska.xlsx' (którego używa Twój kod HTML)
        df_wynikowy.to_excel(output_file, index=False)
        
        print("-" * 30)
        print(f"SUKCES!")
        print(f"Połączono dane i zapisano do: {output_file}")
        print(f"Liczba rekordów: {len(df_wynikowy)}")
        print("-" * 30)

    except FileNotFoundError as e:
        print(f"BŁĄD: Nie znaleziono pliku. Upewnij się, że pliki znajdują się w tym samym folderze co skrypt.")
    except KeyError as e:
        print(f"BŁĄD: Nie znaleziono kolumny: {e}. Sprawdź czy nazwy nagłówków w Excelu są poprawne.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    polacz_pliki_excel()