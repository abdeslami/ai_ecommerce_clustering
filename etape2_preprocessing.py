# -*- coding: utf-8 -*-
"""
MODULE: PRÉPARATION DES DONNÉES (PREPROCESSING)
DESCRIPTION: Ce script nettoie, transforme et standardise 100% des données pour l'IA.
AUTEUR: Équipe Projet Data & Communication
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import time # Juste pour créer un petit effet d'attente "pro"

# =============================================================================
# FONCTION POUR L'AFFICHAGE "STYLISE" (POUR LA DÉMO)
# =============================================================================
def print_header(titre):
    print("\n" + "="*60)
    print(f"🚀 {titre.upper()}")
    print("="*60)
    time.sleep(1) # Petite pause pour laisser le prof lire

# =============================================================================
# 1. CHARGEMENT DES DONNÉES
# =============================================================================
print_header("Phase 1 : Chargement du Big Data")

nom_fichier = 'dataset_ecommerce_personnas.csv'
print(f"📂 Lecture du fichier source : '{nom_fichier}'...")

try:
    df = pd.read_csv(nom_fichier)
    print(f"✅ SUCCÈS : Base de données chargée.")
    print(f"📊 Volume : {df.shape[0]} clients analysés | {df.shape[1]} attributs détectés.")
except FileNotFoundError:
    print("❌ ERREUR CRITIQUE : Le fichier est introuvable.")
    exit()

# =============================================================================
# 2. NETTOYAGE ET SÉLECTION
# =============================================================================
print_header("Phase 2 : Nettoyage & Sélection")

# On enlève l'ID Client car l'IA n'a pas besoin de connaître le nom/numéro
# pour grouper les comportements. C'est une donnée "administrative".
if 'ClientID' in df.columns:
    df_clean = df.drop('ClientID', axis=1)
    print("🗑️  Suppression de la colonne 'ClientID' (Non pertinente pour le clustering).")
else:
    df_clean = df.copy()

print("✅ Colonnes conservées pour l'analyse intégrale :")
print(list(df_clean.columns))

# =============================================================================
# 3. ENCODAGE : TRADUCTION DU TEXTE EN CHIFFRES (CRUCIAL)
# =============================================================================
print_header("Phase 3 : Encodage (Text -> Math)")

print("ℹ️  L'algorithme K-Means ne comprend pas 'Casablanca' ou 'Mobile'.")
print("⚙️  Transformation des variables textuelles en vecteurs binaires (0/1)...")

# Cette fonction magique transforme tout le texte en chiffres.
# Exemple : La colonne "Ville" devient "Ville_Casablanca", "Ville_Rabat", etc.
df_encoded = pd.get_dummies(df_clean, drop_first=True)

print(f"⚡ Transformation terminée !")
print(f"📈 Nous sommes passés de {df_clean.shape[1]} colonnes simples à {df_encoded.shape[1]} colonnes mathématiques.")

# =============================================================================
# 4. STANDARDISATION : MISE À L'ÉCHELLE
# =============================================================================
print_header("Phase 4 : Standardisation (Normalisation)")

print("⚖️  Harmonisation des échelles (Âge vs Salaire vs Temps)...")
# Sans ça, le salaire (ex: 5000) écraserait l'âge (ex: 30) dans le calcul.

scaler = StandardScaler()
data_scaled = scaler.fit_transform(df_encoded)

# On remet le résultat dans un beau tableau avec les noms de colonnes
df_final = pd.DataFrame(data_scaled, columns=df_encoded.columns)

print("✅ Données standardisées avec succès.")
print("   (Moyenne = 0, Écart-type = 1 pour toutes les variables)")

# =============================================================================
# 5. VISUALISATION AVANCÉE (MATRICE DE CORRÉLATION)
# =============================================================================
print_header("Phase 5 : Analyse des Corrélations")

print("🎨 Génération de la Heatmap pour visualiser les liens cachés...")

plt.figure(figsize=(12, 10)) # On fait un graphique plus grand car il y a beaucoup de variables
# On calcule les liens mathématiques
correlation = df_final.corr()
# On dessine
sns.heatmap(correlation, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Matrice de Corrélation Globale (Toutes variables incluses)")
plt.tight_layout()
plt.show()

print("👁️  Le graphique s'est ouvert dans une nouvelle fenêtre.")

# =============================================================================
# 6. SAUVEGARDE POUR L'ÉTAPE SUIVANTE
# =============================================================================
print_header("Phase 6 : Exportation")

# On sauvegarde ce fichier "prêt pour l'IA"
fichier_export = "data_ready_for_ai.csv"
print(f"💾 Sauvegarde des données traitées dans '{fichier_export}'...")
df_final.to_csv(fichier_export, index=False)

print("-" * 60)
print("✅ PRÊT POUR LE CLUSTERING.")
print("   Vous pouvez maintenant lancer l'algorithme K-Means.")
print("-" * 60)