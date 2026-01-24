# -*- coding: utf-8 -*-
"""
MODULE: SIMULATEUR DE PRÉDICTION (DÉMO JURY)
DESCRIPTION: L'IA prédit le profil d'un NOUVEAU client en temps réel.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import time

def print_header(titre):
    print("\n" + "="*60)
    print(f"🔮 {titre.upper()}")
    print("="*60)
    time.sleep(0.5)

# =============================================================================
# 1. PRÉPARATION DE L'IA (EN ARRIÈRE-PLAN)
# =============================================================================
print_header("Initialisation du Cerveau de l'IA")
print("⚙️  Entraînement du modèle sur les données existantes...")

# On recharge les données pour calibrer l'IA
try:
    # On reprend le fichier nettoyé de l'étape 2 pour avoir les mêmes colonnes
    df_source = pd.read_csv('dataset_ecommerce_personnas.csv')
    
    # On garde les mêmes colonnes clés que l'étape 4
    features = ['Age', 'Panier_Moyen_Dhs', 'Frequence_Achat_Annuel', 
                'Temps_Visite_Sec', 'Note_Client', 'Taux_Utilisation_Promo']
    
    X = df_source[features]
    
    # On calibre le "Mètre étalon" (StandardScaler)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # On entraîne le K-Means avec 3 Groupes (Votre choix validé)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    print("✅ IA Prête et Calibrée sur 3 Profils (VIP, Flâneurs, Occasionnels).")

except Exception as e:
    print(f"❌ Erreur : {e}")
    print("Assurez-vous d'avoir 'dataset_ecommerce_personnas.csv' dans le dossier.")
    exit()

# =============================================================================
# 2. DÉFINITION DES NOMS MARKETING (VOS INTERPRÉTATIONS)
# =============================================================================
# ATTENTION : Vérifiez que les numéros correspondent bien à vos résultats de l'étape 4 !
# Selon votre Heatmap précédente :
# Groupe 1 (Rouge partout) = VIP
# Groupe 2 (Rouge sur Temps) = Flâneurs
# Groupe 0 (Bleu partout) = Occasionnels
# (L'ordre peut varier, l'IA recalcule parfois, on va afficher les stats pour être sûrs)

def get_nom_profil(cluster_id):
    # Dictionnaire basé sur votre analyse précédente
    if cluster_id == 1: return "🏆 VIP (Big Spender)"
    elif cluster_id == 2: return "⏱️ FLÂNEUR (Visiteur Curieux)"
    else: return "💤 OCCASIONNEL (Zappeur)" # Cluster 0

# =============================================================================
# 3. INTERFACE DE DÉMONSTRATION
# =============================================================================
print_header("DÉMARRAGE DU SIMULATEUR")
print("Imaginez qu'un nouveau visiteur arrive sur le site...")

while True:
    print("\n--- NOUVEAU TEST (Tapez 'exit' pour quitter) ---")
    
    try:
        # Saisie des données (On fait semblant d'être le site web)
        age = input("1. Âge du client ? (ex: 25) : ")
        if age == 'exit': break
        
        panier = input("2. Panier Moyen en Dhs ? (ex: 1200) : ")
        freq = input("3. Combien d'achats par an ? (ex: 5) : ")
        temps = input("4. Temps sur le site en secondes ? (ex: 300) : ")
        note = input("5. Note laissée (1-5) ? (ex: 4) : ")
        promo = input("6. Aime les promos ? (0=Non, 1=Oui) : ")
        
        # Création du profil mathématique
        nouveau_client = pd.DataFrame([[
            int(age), float(panier), int(freq), 
            int(temps), float(note), float(promo)
        ]], columns=features)
        
        # Mise à l'échelle (IMPORTANT : On utilise le même scaler qu'avant)
        client_scaled = scaler.transform(nouveau_client)
        
        # Prédiction de l'IA
        cluster_predit = kmeans.predict(client_scaled)[0]
        nom_marketing = get_nom_profil(cluster_predit)
        
        # Résultat
        print("\n" + "-"*40)
        print(f"🤖 ANALYSE IA : Ce client appartient au GROUPE {cluster_predit}")
        print(f"🏷️  ÉTIQUETTE MARKETING : {nom_marketing}")
        print("-"*40)
        
        # Petite recommandation automatique (Bonus Communication)
        if "VIP" in nom_marketing:
            print("💡 ACTION : Lui envoyer une invitation Vente Privée.")
        elif "FLÂNEUR" in nom_marketing:
            print("💡 ACTION : Lui pousser une pub de retargeting 'Vous avez oublié ça ?'.")
        else:
            print("💡 ACTION : Lui envoyer un code promo -10% immédiat.")
            
    except ValueError:
        print("⚠️ Erreur : Entrez des chiffres uniquement !")

print("\nFin de la démo. Merci !")