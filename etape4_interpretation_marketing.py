# -*- coding: utf-8 -*-
"""
MODULE: INTERPRÉTATION MARKETING (STEP 4)
DESCRIPTION: Analyse détaillée des 3 Personas identifiés.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. CHARGEMENT
# On reprend le fichier créé par l'IA à l'étape précédente
try:
    df = pd.read_csv('etape3_resultats_clustering.csv')
    print(f"✅ Fichier chargé avec {len(df)} clients.")
except:
    print("❌ Erreur : Lancez d'abord l'étape 3 (Clustering) et choisissez 3 groupes.")
    exit()

# 2. CALCUL DES MOYENNES (PROFILING)
# On sélectionne les critères qui intéressent le Directeur Marketing
kpis = [
    'Age', 
    'Panier_Moyen_Dhs', 
    'Frequence_Achat_Annuel', 
    'Temps_Visite_Sec', 
    'Note_Client',
    'Taux_Utilisation_Promo'
]

print("⚙️  Calcul de l'ADN de vos 3 groupes...")

# Moyennes mathématiques
moyennes = df.groupby('Cluster')[kpis].mean().round(1)

# On ajoute la taille (Combien sont-ils ?)
moyennes['Nombre_Clients'] = df['Cluster'].value_counts()

# Pour les infos Texte (Ville, Device...), on prend le plus fréquent (Majorité)
infos_texte = ['Device', 'Ville', 'Canal_Acquisition']
modes = df.groupby('Cluster')[infos_texte].agg(lambda x: x.mode()[0])

# On fusionne tout
rapport = pd.concat([moyennes, modes], axis=1)

print("\n" + "="*50)
print("📊 RÉSULTATS : QUI SONT VOS 3 PERSONAS ?")
print("="*50)
print(rapport)
print("="*50)

# 3. VISUALISATION (LA PREUVE PAR L'IMAGE)
# On normalise les données pour que le graphique soit lisible
# (Sinon le salaire écrase l'âge)
df_graph = moyennes.drop('Nombre_Clients', axis=1)
df_norm = (df_graph - df_graph.mean()) / df_graph.std()

plt.figure(figsize=(12, 5))
sns.heatmap(df_norm.T, cmap='RdBu_r', annot=True, fmt=".1f", linewidths=1)
plt.title('Identité des 3 Groupes (Rouge = Fort / Bleu = Faible)')
plt.xlabel('Groupe (Cluster)')
plt.show()