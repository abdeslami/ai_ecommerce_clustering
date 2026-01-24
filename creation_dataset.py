# =============================================================================
# 1. IMPORTATION DES OUTILS (BIBLIOTHÈQUES)
# =============================================================================
# Pandas : C'est le "Excel" de Python. Il permet de créer et manipuler des tableaux.
import pandas as pd

# Numpy : C'est la calculatrice scientifique. Elle gère les maths et les grands nombres très vite.
import numpy as np

# Random : C'est le générateur de hasard (comme lancer des dés).
import random

# =============================================================================
# 2. CONFIGURATION DU GÉNÉRATEUR
# =============================================================================
# On définit la taille de notre fichier. 500 000 clients, c'est du "Big Data" pour un étudiant.
NB_CLIENTS = 500000 

# La "Graine" (Seed) est une astuce magique.
# En fixant ce nombre à 42, on oblige l'ordinateur à générer le "même hasard" à chaque fois.
# Cela permet à toute ton équipe d'avoir exactement le même fichier final.
SEED = 42 
np.random.seed(SEED)
random.seed(SEED)

print(f"🚀 Démarrage de la génération de {NB_CLIENTS} profils clients...")

# =============================================================================
# 3. CRÉATION DES DONNÉES DÉMOGRAPHIQUES (QUI SONT-ILS ?)
# =============================================================================

# On crée une liste d'IDs de 1 à 500 000 (User_00001, etc.)
ids = range(1, NB_CLIENTS + 1)

# Âge : On demande des nombres entiers aléatoires entre 18 et 75 ans.
ages = np.random.randint(18, 75, NB_CLIENTS)

# Genre : On choisit entre Homme et Femme avec des probabilités (48% H, 52% F).
genres = np.random.choice(['H', 'F'], NB_CLIENTS, p=[0.48, 0.52])

# Villes : On définit une liste de villes marocaines.
villes_liste = ['Casablanca', 'Rabat', 'Marrakech', 'Tanger', 'Agadir', 'Fès', 'Oujda', 'Autre']
# On définit le poids de chaque ville (Casa est plus grande que Oujda).
probs_villes = [0.35, 0.20, 0.10, 0.10, 0.05, 0.10, 0.05, 0.05]
# L'ordinateur distribue les clients dans les villes selon ces poids.
villes = np.random.choice(villes_liste, NB_CLIENTS, p=probs_villes)

# Appareil utilisé : Le Mobile est majoritaire (60%) dans l'e-commerce aujourd'hui.
devices = np.random.choice(['Mobile', 'Desktop', 'Tablette'], NB_CLIENTS, p=[0.60, 0.35, 0.05])


# =============================================================================
# 4. CRÉATION DES DONNÉES FINANCIÈRES (LEUR VALEUR)
# =============================================================================

# Ancienneté : Depuis combien de mois sont-ils clients ? (Entre 1 et 4 ans)
anciennete = np.random.randint(1, 49, NB_CLIENTS)

# Fréquence d'achat : Combien de fois achètent-ils par an ?
# On utilise une "Loi de Poisson" (maths) qui imite les événements naturels.
# Moyenne = 3 achats/an.
base_freq = np.random.poisson(lam=3, size=NB_CLIENTS)

# Petite astuce logique : Si le client est ancien (>24 mois), on lui ajoute un petit bonus de fidélité.
bonus_anciennete = np.where(anciennete > 24, 1, 0)
frequence = base_freq + bonus_anciennete
# On s'assure que personne n'a 0 achat (sinon ce n'est pas un client).
frequence = np.maximum(frequence, 1) 

# Panier Moyen : Combien dépensent-ils par commande ? (Entre 100 et 2000 Dhs)
panier_moyen = np.round(np.random.uniform(100, 2000, NB_CLIENTS), 2)

# Montant Total (Lifetime Value) : C'est le calcul : Fréquence x Panier.
montant_total = np.round(frequence * panier_moyen, 2)

# Diversité : Achètent-ils toujours la même chose ou plein de catégories différentes ?
# On limite la diversité par la fréquence (on ne peut pas acheter 10 catégories en 2 achats).
raw_div = np.random.randint(1, 11, NB_CLIENTS)
diversite = np.minimum(raw_div, frequence)


# =============================================================================
# 5. COMPORTEMENT DIGITAL & COMMUNICATION (L'ASPECT MARKETING)
# =============================================================================

# Temps de visite : On simule la réalité.
# Si c'est un Mobile -> On met environ 2 minutes (120 sec).
# Si c'est un Ordi -> On met environ 5 minutes (300 sec).
temps_visite = np.where(
    devices == 'Mobile',
    np.random.normal(120, 40, NB_CLIENTS), # Rapide
    np.random.normal(300, 100, NB_CLIENTS) # Lent/Explorateur
)
# On s'assure qu'il n'y a pas de temps négatif.
temps_visite = np.abs(np.round(temps_visite).astype(int))

# Newsletter : Qui ouvre nos emails ?
# On utilise une distribution Beta pour avoir des taux réalistes (souvent bas).
base_news = np.random.beta(2, 5, NB_CLIENTS)
# Les plus de 40 ans lisent un peu plus leurs emails (+10% de chance).
bonus_age = np.where(ages > 40, 0.1, 0.0)
taux_news = np.clip(base_news + bonus_age, 0, 1) # On borne entre 0% et 100%.


# =============================================================================
# 6. SATISFACTION (ASPECT QUALITÉ)
# =============================================================================

# Note Client : Moyenne générale de 4.2/5 (les gens sont plutôt gentils).
notes = np.round(np.random.normal(4.2, 0.8, NB_CLIENTS), 1)
# On bloque les notes entre 1 et 5 étoiles.
notes = np.clip(notes, 1, 5)

# Taux de retour : Pourcentage d'articles renvoyés (entre 0% et 30%).
taux_retour = np.round(np.random.beta(1, 10, NB_CLIENTS), 2)


# =============================================================================
# 7. ASSEMBLAGE ET SAUVEGARDE DU FICHIER
# =============================================================================
print("💾 Assemblage des données dans un tableau Excel géant (DataFrame)...")

# On regroupe toutes nos listes dans un seul tableau structuré
df = pd.DataFrame({
    'ClientID': ids,
    
    # --- Bloc Démographique ---
    'Age': ages,
    'Genre': genres,
    'Ville': villes,
    'Device': devices,
    
    # --- Bloc Financier ---
    'Anciennete_Mois': anciennete,
    'Frequence_Achat_Annuel': frequence,
    'Montant_Total_Dhs': montant_total,
    'Panier_Moyen_Dhs': panier_moyen,
    'Diversite_Categories': diversite,
    'Taux_Utilisation_Promo': np.round(np.random.uniform(0, 0.8, NB_CLIENTS), 2),
    
    # --- Bloc Marketing ---
    'Temps_Visite_Sec': temps_visite,
    'Pages_Vues_Par_Visite': np.random.randint(1, 15, NB_CLIENTS),
    'Taux_Abandon_Panier': np.round(np.random.uniform(0.1, 0.9, NB_CLIENTS), 2),
    'Taux_Ouverture_News': np.round(taux_news, 2),
    'Canal_Acquisition': np.random.choice(['Google', 'Facebook', 'Email', 'Direct', 'Influenceur'], NB_CLIENTS),
    
    # --- Bloc Satisfaction ---
    'Note_Client': notes,
    # Probabilité de réclamation : 80% de chance d'avoir 0 réclamation.
    'Reclamations_SAV': np.random.choice([0, 1, 2, 3], NB_CLIENTS, p=[0.8, 0.15, 0.04, 0.01]),
    'Taux_Retour_Produit': taux_retour
})

# Exportation vers un fichier CSV (lisible par Excel)
nom_fichier = 'dataset_ecommerce_personnas.csv'
print(f"📝 Écriture du fichier '{nom_fichier}' sur le disque dur...")

# index=False signifie qu'on ne veut pas ajouter une colonne de numérotation de ligne inutile
df.to_csv(nom_fichier, index=False)

print("-" * 50)
print(f"✅ SUCCÈS TOTAL ! Fichier généré avec {NB_CLIENTS} clients fictifs.")
print(f"📂 Tu peux maintenant ouvrir '{nom_fichier}' pour voir tes données.")
print("-" * 50)