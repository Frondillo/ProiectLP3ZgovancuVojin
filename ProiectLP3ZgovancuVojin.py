# Importarea bibliotecilor necesare
import tkinter as tk
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Datele statice despre câștigătorii, locul al doilea și al treilea loc al Cupei Mondiale de Fotbal pentru diferite ediții
data = {
    "Year": [2022, 2018, 2014, 2010, 2006, 2002, 1998, 1994, 1990, 1986, 1982, 1978, 1974, 1970, 1966, 1962, 1958, 1954, 1950, 1938, 1934, 1930],
    "Champion": ["Argentina", "France", "Germany", "Spain", "Italy", "Brazil", "France", "Brazil", "West Germany",
                 "Argentina", "Italy", "Argentina", "West Germany", "Brazil", "England", "Brazil", "Brazil",
                 "West Germany", "Uruguay", "Italy", "Italy", "Uruguay"],
    "Runner Up": ["France", "Croatia", "Argentina", "Netherlands", "France", "Germany", "Brazil", "Italy", "Argentina",
                  "West Germany", "West Germany", "Netherlands", "Netherlands", "Italy", "West Germany",
                  "Czechoslovakia", "Sweden", "Hungary", "Brazil", "Hungary", "Czechoslovakia", "Argentina"],
    "Third Place": ["Croatia", "Belgium", "Netherlands", "Germany", "Germany", "Turkey", "Croatia", "Sweden", "Italy",
                    "France", "Poland", "Brazil", "Poland", "West Germany", "Portugal", "Chile", "France", "Austria",
                    "Sweden", "Brazil", "Germany", "United States"]
}

# Funcția pentru afișarea informațiilor principale despre proiect
def display_info():
    info = """Procesarea statisticilor din lumea fotbalului
Universitatea Politehnica Timișoara
Facultatea de Electronică, Telecomunicații și Tehnologii Informaționale
Limbaje de Programare 3
Profesori coordonatori: Conf. Dr. Ing. Mocofan Muguras /// Sl. Dr. Ing. Orhei Ciprian
Studenți: Zgovancu Antonio-Emilian /// Vojin David-Arijan"""
    info_window = tk.Toplevel(root)
    info_window.title("Detalii principale proiect")
    info_frame = tk.Frame(info_window)
    info_frame.pack(fill="both", expand=True)
    info_label = tk.Label(info_frame, text=info)
    info_label.pack()

# Funcția pentru afișarea datelor statice despre Cupele Mondiale de Fotbal
def display_data():
    df = pd.DataFrame(data)
    df_window = tk.Toplevel(root)
    df_window.title("Football World Cup Statistics 1930-2022")
    df_frame = tk.Frame(df_window)
    df_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(df_frame)
    scrollbar.pack(side="right", fill="y")
    text = tk.Text(df_frame, yscrollcommand=scrollbar.set)
    text.pack(fill="both", expand=True)
    scrollbar.config(command=text.yview)
    text.insert("end", df.to_string(index=False))
    text.configure(state="disabled")

# Funcția pentru extragerea istoricului Cupei Mondiale de pe un site web
def get_world_cup_history():
    url = 'https://www.foxsports.com/soccer/2022-fifa-world-cup/history'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extrage secțiunile istoricului Cupei Mondiale
        history_sections = soup.find_all('<div', class_='table-wrapper-container carousel-wrapper history-table-wrapper full-width-table')
        world_cup_history = []  # Creează o listă nouă pentru a stoca istoricul Cupei Mondiale
        for section in history_sections:
            year = section.find('YEAR', class_='sticky-header data-table').text.strip()
            champion = section.find_all('CHAMPION', class_='sticky-header data-table').text.strip()
            runner_up = section.find_all('RUNNER UP', class_='sticky-header data-table').text.strip()
            third_place = section.find_all('THIRD PLACE', class_='sticky-header data-table').text.strip()
            world_cup_history.append(
                 {'Year': year, 'Champion': champion, 'Runner Up': runner_up, 'Third Place': third_place})
        return world_cup_history
    except Exception as e:
        print("An error occurred:", e)
        return None

# Funcția pentru afișarea istoricului Cupei Mondiale de Fotbal preluat de pe un site web
def display_world_cup_history():
    world_cup_data = get_world_cup_history()
    if world_cup_data is not None:
        df = pd.DataFrame(world_cup_data)
        df_window = tk.Toplevel(root)
        df_window.title("Football World Cup History")
        df_frame = tk.Frame(df_window)
        df_frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(df_frame)
        scrollbar.pack(side="right", fill="y")
        text = tk.Text(df_frame, yscrollcommand=scrollbar.set)
        text.pack(fill="both", expand=True)
        scrollbar.config(command=text.yview)
        text.insert("end", df.to_string(index=False))
        text.configure(state="disabled")
    else:
        error_label = tk.Label(root, text="Eroare: Datele din site nu au putut fi afișate.")
        error_label.pack()

# Crearea ferestrei principale a aplicației
root = tk.Tk()
root.title("Football World Cup Statistics")

# Adăugarea butoanelor pentru interacțiunea cu utilizatorul
info_button = tk.Button(root, text="Afiseaza informatiile principale", command=display_info)
info_button.pack(pady=10)

display_data_button = tk.Button(root, text="Istoria Cupei Mondiale de Fotbal 1930-2022 #1", command=display_data)
display_data_button.pack(pady=10)

display_button = tk.Button(root, text="Istoria Cupei Mondiale de Fotbal 1930-2022 #2 - Eroare", command=display_world_cup_history)
display_button.pack(pady=10)

# Inițierea buclei principale a interfeței grafice
root.mainloop()
