import pandas as pd
from geopy.geocoders import ArcGIS
from geopy.extra.rate_limiter import RateLimiter
import re

def clean_address(text):
    if not isinstance(text, str): return ""
    # Usuwanie zbędnych znaków nowej linii i spacji
    text = text.replace('\n', ' ')
    # Usuwanie typowych fraz blokujących wyszukiwanie
    text = re.sub(r'(?i)ul\.|ulica|adres:|schronisko|górskie|pttk|s\.c\.', '', text)
    # Standaryzacja kodu pocztowego
    text = re.sub(r'(\d{2})\s?-\s?(\d{3})', r'\1-\2', text)
    return ' '.join(text.split()).strip()

def run_conversion():
    input_file = 'Schroniska adresy.xlsx'
    output_file = 'Schroniska_gotowe.xlsx'
    
    # 1. Wczytanie danych
    df = pd.read_excel(input_file)
    
    # 2. Pominięcie pustych lokalizacji
    initial_count = len(df)
    df = df.dropna(subset=['Lokalizacja'])
    print(f"Pominięto {initial_count - len(df)} wierszy z pustą lokalizacją.")
    
    # 3. Konfiguracja geokodera
    geolocator = ArcGIS(timeout=10)
    # ArcGIS nie wymaga tak dużych przerw jak OSM, ustawiamy minimalny delay
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)

    print(f"Przetwarzanie {len(df)} rekordów...")

    lats = []
    lons = []

    for index, row in df.iterrows():
        raw_address = str(row['Lokalizacja'])
        name = str(row['Nazwa schroniska'])
        
        # Przygotowanie zapytania: Nazwa + Oczyszczony Adres (zwiększa celność)
        query = f"{name}, {clean_address(raw_address)}"
        
        try:
            location = geocode(query)
            if location:
                print(f"[{index+1}] SUKCES: {name}")
                lats.append(location.latitude)
                lons.append(location.longitude)
            else:
                # Fallback: sama lokalizacja bez nazwy
                location = geocode(clean_address(raw_address))
                if location:
                    lats.append(location.latitude)
                    lons.append(location.longitude)
                    print(f"[{index+1}] SUKCES (fallback): {name}")
                else:
                    print(f"[{index+1}] BŁĄD: {name}")
                    lats.append(None)
                    lons.append(None)
        except Exception as e:
            print(f"Błąd sieci przy {name}: {e}")
            lats.append(None)
            lons.append(None)

    # 4. Zapisanie wyników
    df['lat'] = lats
    df['lon'] = lons
    df.to_excel(output_file, index=False)
    print(f"\nGotowe! Wynik zapisano w: {output_file}")

if __name__ == "__main__":
    run_conversion()