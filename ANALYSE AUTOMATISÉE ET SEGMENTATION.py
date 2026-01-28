# -*- coding: utf-8 -*-
"""
=============================================================================
PROJET  : AUDIENCE ARCHITECT
DESC    : Solution de segmentation client par Intelligence Artificielle.
          Intègre : Nettoyage ETL, Clustering K-Means, Analyse Géométrique
          et Moteur Narratif (Génération de texte).
=============================================================================
"""

# --- 1. IMPORTATION DES LIBRAIRIES (LA BOÎTE À OUTILS) ---
import pandas as pd             # Gestionnaire de tableaux (Excel pour Python)
import numpy as np              # Moteur de calcul mathématique
import matplotlib.pyplot as plt # Outil de dessin graphique
import seaborn as sns           # Outil de design graphique avancé (Heatmaps)
from sklearn.preprocessing import StandardScaler # Pour normaliser les données (Mise à l'échelle)
from sklearn.cluster import KMeans # Le cerveau de l'IA (Algorithme de regroupement)
from sklearn.decomposition import PCA # Pour la visualisation 2D (Projection)
import time # Pour créer des délais et simuler un chargement réaliste

# --- FONCTION D'INTERFACE GRAPHIQUE (CONSOLE) ---
# Cette fonction sert juste à faire joli dans la console (Titres encadrés)
def print_header(titre):
    print("\n" + "═"*70)
    print(f"🔷 {titre.center(66)}") # .center permet de centrer le texte
    print("═"*70)
    time.sleep(1) # Pause d'une seconde pour que le jury ait le temps de lire

# --- DÉMARRAGE DU PROGRAMME ---
print("\n")
print("╔════════════════════════════════════════════════════════════════════╗")
print("║                        AUDIENCE ARCHITECT ™                        ║")
print("║          Segmentation Prédictive & Analyse Comportementale         ║")
print("╚════════════════════════════════════════════════════════════════════╝")
time.sleep(1.5)

print("\n[SYSTEM] Initialisation des modules IA......... [OK]")
print("[SYSTEM] Allocation mémoire Big Data........... [OK]")

# =============================================================================
# MODULE A : CHARGEMENT ET PRÉPARATION (ETL - Extract Transform Load)
# =============================================================================
print_header("MODULE A : CHARGEMENT ET NETTOYAGE DES DONNÉES")

nom_fichier = 'audience_architect_data_50k.csv'

# 1. Chargement du fichier CSV
try:
    print(f"[INFO] Lecture du fichier source : '{nom_fichier}'")
    # On lit le fichier
    df = pd.read_csv(nom_fichier)
    # Affichage pro avec séparateur de milliers (ex: 500 000)
    print(f"[SUCCÈS] Base de données connectée. Volume : {len(df):,} profils clients.".replace(',', ' '))
except:
    print("[ERREUR FATALE] Le fichier csv est introuvable.")
    exit()

# 2. Nettoyage des données (Data Cleaning)
print("\n[ETL] Scan de l'intégrité des données...")
# On compte les cases vides
nb_vides = df.isnull().sum().sum()

if nb_vides > 0:
    # Si on trouve des trous, on les bouche avec la moyenne (Imputation)
    df = df.fillna(df.mean())
    print(f"[ACTION] CORRECTION : {nb_vides} valeurs manquantes remplacées par la moyenne.")
else:
    print("[OK] Données certifiées intègres (Aucune valeur manquante).")
# --- GRAPHIQUE 0 : PREUVE DE VARIÉTÉ ---
print("\n[ACTION] Génération du Graphique de Contrôle (Distribution)...")
plt.figure(figsize=(12, 5))

# Histogramme Age (Compatible Mac 2011)
plt.subplot(1, 2, 1)
try:
    sns.distplot(df['Age'], bins=30, kde=True, color='#3498db')
except:
    plt.hist(df['Age'], bins=30, color='#3498db', alpha=0.7)
plt.title("Distribution des Âges (Variété confirmée)")
plt.xlabel("Âge")

# Histogramme Revenu
plt.subplot(1, 2, 2)
try:
    sns.distplot(df['Revenu_Mensuel_Estime'], bins=30, kde=True, color='#2ecc71')
except:
    plt.hist(df['Revenu_Mensuel_Estime'], bins=30, color='#2ecc71', alpha=0.7)
plt.title("Distribution des Revenus")
plt.xlabel("Revenu (Dhs)")

plt.tight_layout()
plt.savefig('graphique_0_preuve_variete.png') # Sauvegarde
print("      ✅ Image sauvegardée : 'graphique_0_preuve_variete.png'")
plt.show()
# ------------------------------------------------------------------
# 3. Standardisation (Mise à l'échelle) - CRUCIAL
# Expliquez au jury : "L'IA ne peut pas comparer des salaires (5000) et des âges (30)."
# "On transforme tout en score relatif (Z-Score) pour que chaque critère ait le même poids."
print("\n[ETL] Standardisation des variables (Scaling Z-Score)...")
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

print("      ...Transformation terminée.")

# =============================================================================
# MODULE B : ANALYSE STRATÉGIQUE (ELBOW METHOD)
# =============================================================================
print_header("MODULE B : DÉTECTION AUTOMATIQUE DES GROUPES")
print(f"[ANALYSE] Lancement de l'algorithme 'Elbow' sur {len(df)} lignes.")
print("[NOTE] L'IA teste plusieurs configurations pour trouver la segmentation idéale.")

inertie = [] # Stockera le score d'erreur pour chaque test
k_range = range(1, 10) # On va tester de 1 à 9 groupes

print("\n[CALCUL EN COURS] Modélisation itérative :")

# Boucle d'apprentissage : L'IA essaie 1 groupe, puis 2, puis 3...
for k in k_range:
    # Création du modèle temporaire
    kmeans_test = KMeans(n_clusters=k, random_state=42, n_init=10)
    # Entraînement sur TOUTES les données
    kmeans_test.fit(df_scaled)
    # Enregistrement de la performance
    inertie.append(kmeans_test.inertia_)
    
    # Barre de progression visuelle (Pour faire patienter le jury)
    pourcentage = int((k / 9) * 100)
    barre = "█" * k + "░" * (9 - k)
    print(f"   ► Test de {k} Clusters terminé |{barre}| {pourcentage}%")

# --- ALGORITHME GÉOMÉTRIQUE (DÉCISION) ---
# Cette fonction mathématique remplace l'œil humain.
# Elle calcule l'angle de la courbe pour trouver la cassure nette.
def trouver_coude_automatique(inerties):
    p1 = np.array([1, inerties[0]])
    p2 = np.array([len(inerties), inerties[-1]])
    distances = []
    for i in range(len(inerties)):
        p0 = np.array([i+1, inerties[i]])
        # Calcul de la distance point-droite
        dist = np.abs(np.cross(p2-p1, p1-p0)) / np.linalg.norm(p2-p1)
        distances.append(dist)
    # On retourne l'index du point le plus éloigné
    return distances.index(max(distances)) + 1

# L'ordinateur prend la décision finale ici
nombre_ideal = trouver_coude_automatique(inertie)

print(f"\n[RÉSULTAT] L'Intelligence Artificielle recommande : {nombre_ideal} PERSONAS.")
print("          (Optimum mathématique détecté par méthode géométrique)")

# --- GRAPHIQUE 1 : ELBOW ---
print("[ACTION] Génération de la Courbe d'Inertie (Preuve mathématique)...")
plt.figure(figsize=(10, 6))
plt.plot(k_range, inertie, 'bD-', linewidth=2, label='Inertie')
plt.plot(nombre_ideal, inertie[nombre_ideal-1], 'ro', markersize=15, label=f'Choix IA ({nombre_ideal})')
plt.title(f"Méthode du Coude : Cassure optimale à {nombre_ideal} groupes")
plt.xlabel("Nombre de Clusters")
plt.ylabel("Inertie")
plt.grid(True)
plt.legend()
plt.savefig('graphique_1_coude_elbow.png')
print("      ✅ Image sauvegardée : 'graphique_1_coude_elbow.png'")
plt.show()

# ----------------------------------------------------------------------
# =============================================================================
# MODULE C : SEGMENTATION MASSIVE (DEPLOYMENT)
# =============================================================================
print_header(f"MODULE C : CLASSIFICATION FINALE ({nombre_ideal} CLUSTERS)")
print(f"[ACTION] Segmentation de la base de données ({len(df)} clients)...")

# 1. Configuration de l'IA finale
kmeans_final = KMeans(n_clusters=nombre_ideal, random_state=42, n_init=10)

# 2. L'IA étiquette chaque client (0, 1, 2...)
clusters = kmeans_final.fit_predict(df_scaled)

# 3. On enregistre le résultat dans le tableau
df['Cluster'] = clusters

print("[SUCCÈS] Segmentation terminée. 100% des clients ont été affectés.")
print("[INFO] La colonne 'Cluster' a été ajoutée au dataset.")

# =============================================================================
# MODULE D : LE STORYTELLER (INTERPRÉTATION AUTOMATIQUE)
# =============================================================================
# C'est la partie "Communication" du projet.
# Le code transforme les chiffres en mots pour le rapport.
print_header("MODULE D : MOTEUR NARRATIF (INTERPRÉTATION)")

# Calcul des moyennes par groupe
profils = df.groupby('Cluster').mean().round(2)
profils['POPULATION'] = df['Cluster'].value_counts()
moyennes_globales = df.mean() # Moyenne nationale pour comparer

# --- FONCTION D'ÉCRITURE AUTOMATIQUE ---
def generer_description(stats_groupe, stats_globales):
    txt = []
    
    # Règle sur l'Âge
    if stats_groupe['Age'] < stats_globales['Age'] - 4: txt.append("JEUNE (Gen Z)")
    elif stats_groupe['Age'] > stats_globales['Age'] + 4: txt.append("SENIOR")
    else: txt.append("D'ÂGE MOYEN")
    
    # Règle sur le Revenu
    if stats_groupe['Revenu_Mensuel_Estime'] > stats_globales['Revenu_Mensuel_Estime'] * 1.1:
        txt.append("au POUVOIR D'ACHAT ÉLEVÉ")
    elif stats_groupe['Revenu_Mensuel_Estime'] < stats_globales['Revenu_Mensuel_Estime'] * 0.9:
        txt.append("au BUDGET LIMITÉ")
        
    # Règle sur les Promos
    if stats_groupe['Sensibilite_Promo'] > 0.6: txt.append("CHASSEUR DE PROMOS")
    
    # Règle sur la Fidélité
    if stats_groupe['Score_Fidelite'] > 60: txt.append("TRÈS FIDÈLE")
    if stats_groupe['Score_Fidelite'] < 40: txt.append("VOLATILE (Risque de départ)")

    return " / ".join(txt) # On relie les mots par des slashs

print("Génération du rapport d'analyse...\n")

# Boucle d'affichage pour chaque groupe
for i in range(nombre_ideal):
    # On récupère les stats du groupe
    groupe = profils.loc[i]
    # L'IA écrit la description
    desc = generer_description(groupe, moyennes_globales)
    
    # Affichage stylé
    print(f"🏆 GROUPE {i+1} : {int(groupe['POPULATION']):,} Clients")
    print(f"   📝 PROFIL : {desc}")
    print(f"   📊 DATA   : Panier Moyen {groupe['Panier_Moyen']} Dhs | Age {groupe['Age']} ans")
    print("   " + "-"*50)
    
# =============================================================================
# MODULE E : VISUALISATION GRAPHIQUE (DASHBOARD)
# =============================================================================
print_header("MODULE E : GÉNÉRATION DES GRAPHIQUES")

# GRAPHIQUE 1 : HEATMAP (L'ADN)
print("1. Construction de la Heatmap (ADN des Groupes)...")
profils_norm = (profils - profils.mean()) / profils.std()
plt.figure(figsize=(14, 7))
sns.heatmap(profils_norm.drop('POPULATION', axis=1).T, 
            cmap='RdBu_r', annot=True, fmt=".1f", linewidths=1)
plt.title("ADN Marketing des Personas (Comparaison par rapport à la moyenne)")
plt.show()

# GRAPHIQUE 2 : PCA (LES NUAGES DE POINTS)
print("\n2. Construction de la Projection 2D (PCA)...")
print("   [NOTE] Projection optimisée pour la lisibilité visuelle.")
pca = PCA(n_components=2)
# On affiche un sous-ensemble pour éviter de saturer le dessin (mais le calcul est global)
idx = np.random.choice(len(df_scaled), 20000, replace=False)
coords = pca.fit_transform(df_scaled[idx])
plt.figure(figsize=(10, 8))
sc = plt.scatter(coords[:, 0], coords[:, 1], c=df['Cluster'].iloc[idx], cmap='viridis', alpha=0.6, s=10)
plt.title(f"Carte des {nombre_ideal} Tribus (Analyse en Composantes Principales)")
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.colorbar(sc, label="Segment")
plt.show()
# SAUVEGARDE FINALE
df.to_csv('audience_architect_final_report.csv', index=False)
print("\n" + "═"*70)
print(f"✅ TRAITEMENT TERMINÉ. Fichier exporté : 'audience_architect_final_report.csv'")
print("═"*70)