import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter

#chemin des images
output_path= 'C:/Users/augus/Downloads/HP.png'
output_path_= 'C:/Users/augus/Downloads/SP.png'

# Chargement des fichiers CSV
def select_file():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    file_path = filedialog.askopenfilename(title="Sélectionnez un fichier")
    return file_path
fichier_path= select_file()
df= pd.read_excel(fichier_path, sheet_name=None, skiprows=2)
#print (df['HP_Crush_150daN_01'])
#print (df)
def get_sheets(df, name_sheet):
    """
    Sélectionne les feuilles dont le nom commence par name_sheet.
    
    :param df: Dictionnaire avec les DataFrames de chaque feuille Excel.
    :return: Dictionnaire avec uniquement les feuilles commençant par 'HP'.
    """
    hp_sheets = {nom: df for nom, df in df.items() if nom.startswith(name_sheet)}
    
    if not hp_sheets:
        print(f" Aucune feuille commençant par [{name_sheet}] trouvée.")
    else:
        print(f" Feuilles sélectionnées : {list(hp_sheets.keys())}")
    
    return hp_sheets

def courbe(hp_dfs, save, title):
    """
    Crée un DataFrame contenant uniquement les colonnes 'min' et 'dB' pour chaque feuille.

    :param hp_dfs: Dictionnaire des DataFrames des feuilles sélectionnées.
    :return: Dictionnaire de DataFrames avec les colonnes 'min' et 'dB'.
    """
    df_dict = {}  # Stocker les DataFrames filtrés
    
    fig, ax1 = plt.subplots(figsize=(12,6))
    ax2 = ax1.twinx()

    for nom_feuille, df in hp_dfs.items():
        # Nettoyage des noms de colonnes
        #print (df)
        #df.columns = df.columns.astype(str).str.strip().str.lower()
        print( 'les colonnes sont : ', df.columns.values)

        
        # Vérifier si les colonnes 'min' et 'dB' existent
        if "min" in df.columns and "dB" in df.columns:
            df_filtered = df[["min", "dB"]].dropna()  # Supprime les valeurs NaN
            df_dict[nom_feuille] = df_filtered  # Stocke le DataFrame filtré
            print(f" DataFrame créé pour : {nom_feuille}")
            
            ax1.plot(df_filtered["min"].to_numpy(), df_filtered["dB"].to_numpy(), label=nom_feuille)

        else:
            print(f" Colonnes 'min' et 'dB' manquantes dans : {nom_feuille}")

        if "min" in df.columns and "daN" in df.columns:
            df_filtered_ = df[["min", "daN"]].dropna()  # Supprime les valeurs NaN
            df_dict[nom_feuille] = df_filtered_  # Stocke le DataFrame filtré
            print(f" DataFrame créé pour : {nom_feuille}")
            
            ax2.plot(df_filtered_["min"].to_numpy(), df_filtered_["daN"].to_numpy(), label=nom_feuille)

        else:
            print(f" Colonnes 'min' et 'daN' manquantes dans : {nom_feuille}")

    plt.legend()        
    ax1.set_xlabel("Temps (min)")
    ax1.set_ylabel("Pertes (dB)")
    ax2.set_ylabel('Force en daN')

    plt.title(f"Comparaison de pertes optique")
    
    plt.grid(True)
    plt.get_current_fig_manager().set_window_title(title)
    plt.savefig(save, dpi=300)
    plt.show()

    return df_dict

sheet_SP= get_sheets(df,'SP')
courbe(sheet_SP, output_path_ , 'courbe sur porteur')
sheet_HP= get_sheets(df,'HP', )
courbe(sheet_HP, output_path, 'courbe hors porteur')

