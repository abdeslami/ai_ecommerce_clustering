# -*- coding: utf-8 -*-
"""
=============================================================================
PROJET  : AUDIENCE ARCHITECT (MASTER COMMUNICATION & DATA)
DESC    : Ce script simule le comportement de 500 000 clients uniques.
          Il n'utilise pas de groupes pré-faits, mais des règles sociologiques
          (ex: "Le revenu augmente avec l'âge") pour créer une data organique.
=============================================================================
"""

# --- 1. IMPORTATION DES LIBRAIRIES ---
import pandas as pd  # Outil de gestion de tableaux (Excel pour Python)
import numpy as np   # Outil mathématique (Génération de hasard)
import time          # Pour gérer les temps d'affichage

# Fonction pour l'esthétique de la console
def print_header(titre):
    print("\n" + "═"*70)
    print(f"🏗️  {titre.center(64)}")
    print("═"*70)
    time.sleep(0.8) # Pause pour l'effet visuel

# --- DÉMARRAGE ---
print("\n")
print("╔════════════════════════════════════════════════════════════════════╗")
print("║                     AUDIENCE ARCHITECT ™                           ║")
print("║         Génération de Population Virtuelle Réaliste                ║")
print("╚════════════════════════════════════════════════════════════════════╝")
time.sleep(1)

# =============================================================================
# PHASE 1 : INITIALISATION
# =============================================================================
print_header("PHASE 1 : CONFIGURATION DU MOTEUR")

# Nombre de clients à simuler (Big Data)
NB_CLIENTS = 50000
print(f"[CONFIG] Volume cible : {NB_CLIENTS:,} profils uniques.".replace(',', ' '))

# Fixer la graine aléatoire (Seed)
# Cela permet d'avoir toujours le même résultat à chaque lancement (Reproductibilité scientifique)
np.random.seed(42)
print("[CONFIG] Stabilisation du générateur aléatoire (Seed=42)... [OK]")

# Création du tableau vide
df = pd.DataFrame()
print("[INIT] Création du conteneur de données (DataFrame)...     [OK]")

# =============================================================================
# PHASE 2 : GÉNÉRATION DES ATTRIBUTS (LOGIQUE MÉTIER)
# =============================================================================
print_header("PHASE 2 : SIMULATION COMPORTEMENTALE")
print("[INFO] Lancement des algorithmes de corrélation sociologique...\n")

# --- A. DÉMOGRAPHIE (L'AGE) ---
print("   ► Génération du noyau démographique (Âge)...")
# On génère des entiers aléatoires entre 18 et 75 ans (Population active + Retraités)
df['Age'] = np.random.randint(18, 75, NB_CLIENTS)
time.sleep(0.5)

# --- B. ÉCONOMIE (LE REVENU) ---
print("   ► Calcul des revenus (Corrélation Âge/Salaire)...")
# LOGIQUE : Le revenu dépend de l'expérience, donc de l'âge.
# 1. Base : Une distribution normale (courbe en cloche) centrée sur 3000 Dhs
base_revenu = np.random.normal(3000, 1000, NB_CLIENTS)
# 2. Bonus : On ajoute 40 Dhs pour chaque année d'âge (Prime à l'ancienneté simulée)
bonus_age = df['Age'] * 40 
# 3. Total : On additionne et on prend la valeur absolue pour éviter les négatifs
df['Revenu_Mensuel_Estime'] = np.abs(base_revenu + bonus_age)

# --- C. PSYCHOLOGIE (FIDÉLITÉ) ---
print("   ► Attribution des scores de fidélité...")
# Un score pur de 0 à 100 assigné au hasard
df['Score_Fidelite'] = np.random.randint(0, 100, NB_CLIENTS)

# --- D. MARKETING (SENSIBILITÉ AUX PROMOS) ---
print("   ► Modélisation de la psychologie Prix (Promo)...")
# LOGIQUE : Plus on est riche, moins on court après les promos.
# Formule inversée : 1 moins (Revenu divisé par un facteur).
# On ajoute du "bruit" (random) car il existe des riches radins !
bruit = np.random.normal(0, 0.2, NB_CLIENTS) 
df['Sensibilite_Promo'] = 1 - (df['Revenu_Mensuel_Estime'] / 8000) + bruit
# "Clip" force les valeurs à rester entre 0 et 1 (On ne peut pas avoir 120% de sensibilité)
df['Sensibilite_Promo'] = np.clip(df['Sensibilite_Promo'], 0, 1)

# --- E. ACHAT (PANIER MOYEN) ---
print("   ► Simulation des transactions (Paniers)...")
# LOGIQUE : On dépense environ 15% de son revenu estimé par commande + variation.
df['Panier_Moyen'] = (df['Revenu_Mensuel_Estime'] * 0.15) + np.random.normal(0, 100, NB_CLIENTS)
df['Panier_Moyen'] = np.abs(df['Panier_Moyen']) # Sécurité anti-négatif

# --- F. HABITUDE (FRÉQUENCE) ---
print("   ► Calcul de la récurrence d'achat...")
# LOGIQUE : Les clients fidèles (Score élevé) achètent plus souvent.
df['Frequence_Achat_Mois'] = (df['Score_Fidelite'] / 20) + np.random.normal(0, 1, NB_CLIENTS)
df['Frequence_Achat_Mois'] = np.clip(df['Frequence_Achat_Mois'], 1, 10).astype(int)

# --- G. NAVIGATION WEB (TEMPS DE SESSION) ---
print("   ► Simulation du comportement Web (Durée visite)...")
# LOGIQUE "NP.WHERE" (C'est comme la fonction SI dans Excel) :
# SI moins de 30 ans ALORS moyenne de 3 min (zapping) SINON moyenne de 6 min.
df['Temps_Session_Sec'] = np.where(df['Age'] < 30, 
                                   np.random.normal(180, 60, NB_CLIENTS), 
                                   np.random.normal(400, 120, NB_CLIENTS))
df['Temps_Session_Sec'] = np.abs(df['Temps_Session_Sec'])

# --- H. TECHNOLOGIE (DEVICE) ---
print("   ► Assignation des terminaux (Mobile vs Desktop)...")
# LOGIQUE : Les jeunes (<40 ans) ont 80% de chance d'être sur Mobile.
proba_mobile = np.where(df['Age'] < 40, 0.8, 0.4) 
rand_vals = np.random.random(NB_CLIENTS) # On lance un dé virtuel
# Si le dé est inférieur à la proba, c'est Mobile (0.0), sinon Ordi (1.0)
df['Score_Tech_Device'] = np.where(rand_vals < proba_mobile, 0.0, 1.0)

# --- I. INDICATEURS SECONDAIRES ---
print("   ► Finalisation des KPIs (Abandon, Satisfaction, Pages)...")

# 1. Taux d'abandon (Lié au prix : plus c'est cher, plus on hésite)
df['Taux_Abandon_Panier'] = (df['Panier_Moyen'] / 2000) + np.random.normal(0, 0.1, NB_CLIENTS)
df['Taux_Abandon_Panier'] = np.clip(df['Taux_Abandon_Panier'], 0, 1)

# 2. Satisfaction (Tendance humaine à mettre souvent 3 ou 4 étoiles)
df['Note_Satisfaction'] = np.random.choice([1, 2, 3, 4, 5], NB_CLIENTS, p=[0.05, 0.1, 0.2, 0.4, 0.25])

# 3. Pages Vues (Lié au temps passé : 1 page toutes les 30 sec env.)
df['Nombre_Pages_Vues'] = (df['Temps_Session_Sec'] / 30).astype(int)

# 4. Récence (Inversement proportionnelle à la fidélité)
df['Jours_Depuis_Dernier_Achat'] = (100 - df['Score_Fidelite']) * 3 + np.random.randint(0, 20, NB_CLIENTS)

print("\n[SUCCESS] Tous les attributs ont été générés avec cohérence.")

# =============================================================================
# PHASE 3 : EXPORTATION
# =============================================================================
print_header("PHASE 3 : STOCKAGE ET EXPORT")

# Nettoyage cosmétique (Arrondi à 2 chiffres après la virgule)
df = df.round(2)

nom_fichier = 'audience_architect_data_50k.csv'
print(f"[I/O] Écriture sur le disque : '{nom_fichier}'")
print("[INFO] Veuillez patienter pendant l'enregistrement CSV...")

# Sauvegarde sans l'index (pour ne pas avoir une colonne 0,1,2,3 inutile)
df.to_csv(nom_fichier, index=False)

print("\n" + "═"*70)
print(f"✅ TERMINÉ. Fichier prêt pour l'analyse : {len(df)} lignes x {len(df.columns)} colonnes.")
print("═"*70)

# Petit aperçu pour le jury
print("\n--- APERÇU ÉCHANTILLON (5 PREMIÈRES LIGNES) ---")
print(df.head().to_string())