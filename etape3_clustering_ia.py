# -*- coding: utf-8 -*-
"""
MODULE: CLUSTERING IA (K-MEANS & PCA)
DESCRIPTION: Détermination du nombre optimal de groupes et segmentation.
AUTEUR: Équipe Projet Data & Communication
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import time

# =============================================================================
# FONCTIONS UTILITAIRES (POUR LE STYLE)
# =============================================================================
def print_header(titre):
    print("\n" + "="*60)
    print(f"🧠 {titre.upper()}")
    print("="*60)
    time.sleep(1)

# =============================================================================
# 1. CHARGEMENT DES DONNÉES PRÉPARÉES
# =============================================================================
print_header("Phase 1 : Chargement des données mathématiques")

# On charge le fichier de l'étape 2 (celui avec que des chiffres)
fichier_source = 'data_ready_for_ai.csv'
try:
    X = pd.read_csv(fichier_source)
    print(f"✅ Données chargées : {X.shape[0]} clients prêts à être segmentés.")
except FileNotFoundError:
    print("❌ ERREUR : Lancez d'abord l'étape 2 pour créer 'data_ready_for_ai.csv'.")
    exit()

# =============================================================================
# 2. MÉTHODE DU COUDE (ELBOW METHOD)
# =============================================================================
print_header("Phase 2 : Recherche du nombre idéal de groupes")

print("⚙️  L'IA teste différentes configurations (de 1 à 10 clusters)...")
inertia = []
range_values = range(1, 11)

for i in range_values:
    # random_state=42 assure que le résultat est le même à chaque démo
    kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)
    print(f"   > Test avec {i} groupes terminé.")

# Affichage du graphique
plt.figure(figsize=(10, 6))
plt.plot(range_values, inertia, 'bD-', markersize=8)
plt.title('Méthode du Coude (Elbow Method)')
plt.xlabel('Nombre de Clusters (k)')
plt.ylabel('Inertie (Désordre interne)')
plt.grid(True)
plt.show()

print("\n📈 ANALYSE : Regardez le graphique qui vient de s'ouvrir.")
print("   Cherchez le point de cassure (le coude). C'est le compromis idéal.")

# =============================================================================
# 3. INTERACTION HUMAINE (L'EXPERT DÉCIDE)
# =============================================================================
print_header("Phase 3 : Décision Stratégique")

# C'est ici que vous montrez au jury que l'humain garde le contrôle
k_input = input(">> D'après le graphique, combien de Personas voulez-vous créer ? (ex: 3 ou 4) : ")
try:
    k = int(k_input)
except ValueError:
    k = 4 # Valeur par défaut si erreur de frappe
    print("⚠️ Entrée invalide. Par défaut, nous partons sur 4 groupes.")

print(f"\n🚀 Lancement de la segmentation finale avec {k} Groupes...")

# =============================================================================
# 4. CLUSTERING FINAL
# =============================================================================
kmeans_final = KMeans(n_clusters=k, random_state=42, n_init=10)
clusters = kmeans_final.fit_predict(X)

print("✅ Segmentation terminée. Chaque client a reçu son étiquette.")

# =============================================================================
# 5. VISUALISATION 2D (PCA) - INDISPENSABLE CAR TROP DE VARIABLES
# =============================================================================
print_header("Phase 4 : Visualisation (Projection PCA)")

print("ℹ️  Nous avons beaucoup de variables (Villes, Appareils, etc.).")
print("⚙️  Compression en 2 dimensions pour pouvoir dessiner la carte...")

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', alpha=0.6, s=15)
plt.title(f"Carte des {k} Personas (Projection ACP)")
plt.xlabel("Axe Principal 1 (Variance Max)")
plt.ylabel("Axe Principal 2")
plt.colorbar(scatter, label='Numéro du Groupe')
plt.show()

print("👁️  La carte des personas s'est affichée.")

# =============================================================================
# 6. SAUVEGARDE ET FUSION
# =============================================================================
print_header("Phase 5 : Fusion et Export")
# On recharge le fichier ORIGINAL (celui avec les noms des villes en texte)
# pour que le fichier final soit lisible par des humains.
df_original = pd.read_csv('dataset_ecommerce_personnas.csv')

# On ajoute la colonne magique "Cluster"
df_original['Cluster'] = clusters

# Sauvegarde
nom_fichier_final = 'etape3_resultats_clustering.csv'
df_original.to_csv(nom_fichier_final, index=False)

print(f"💾 Fichier final généré : '{nom_fichier_final}'")
print("-" * 60)
print("✅ ÉTAPE 3 TERMINÉE.")
print("   Vous avez maintenant un fichier contenant vos clients et leur groupe.")
print("   PROCHAINE ÉTAPE : Analyser qui sont ces groupes (Interprétation Marketing).")
print("-" * 60)