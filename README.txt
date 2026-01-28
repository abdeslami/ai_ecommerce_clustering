============================================================
🚀 PROJET : AUDIENCE ARCHITECT AI
GUIDE D'INSTALLATION ET DE LANCEMENT
============================================================

Ce projet est une application d'analyse de données utilisant l'Intelligence Artificielle (K-Means Clustering).
Voici les étapes pour lancer l'application sur votre ordinateur.

------------------------------------------------------------
ÉTAPE 1 : VÉRIFIER QUE PYTHON EST INSTALLÉ
------------------------------------------------------------
1. Ouvrez votre Terminal (Mac) ou Invite de Commande (Windows).
2. Tapez la commande suivante et appuyez sur Entrée :
   python --version

>> Si vous voyez une version (ex: Python 3.9), c'est bon.
>> Si rien ne s'affiche, installez Python depuis python.org.

------------------------------------------------------------
ÉTAPE 2 : INSTALLER LES LIBRAIRIES NÉCESSAIRES
------------------------------------------------------------
L'application a besoin de plusieurs outils (Streamlit, IA, PDF, Graphiques).
Copiez et collez cette ligne de commande entière pour tout installer d'un coup :

   pip install streamlit pandas numpy matplotlib seaborn scikit-learn fpdf

(Note : Sur certains Mac, si "pip" ne marche pas, essayez "pip3").

------------------------------------------------------------
ÉTAPE 3 : LANCER L'APPLICATION
------------------------------------------------------------
1. Dans votre terminal, naviguez jusqu'au dossier où se trouve le fichier "app_audience.py".
   
   ASTUCE : Tapez "cd ", faites un Espace, puis glissez-déposez le dossier dans le terminal.
   Exemple : 
   cd C:\Users\VotreNom\Downloads\Projet

2. Une fois dans le bon dossier, lancez l'application :

   streamlit run app_audience.py

------------------------------------------------------------
ÉTAPE 4 : UTILISATION
------------------------------------------------------------
1. Une page web va s'ouvrir automatiquement.
2. Glissez le fichier CSV des données clients dans la zone prévue.
3. L'IA va analyser les données, créer les groupes et générer le rapport.
4. Allez dans l'onglet "RAPPORT EXPERT" pour télécharger le PDF final.

------------------------------------------------------------
DÉPANNAGE (CAS D'ERREUR)
------------------------------------------------------------
* Si le terminal dit "streamlit n'est pas reconnu" :
  Réinstallez avec : python -m pip install streamlit

* Si l'écran reste blanc au lancement :
  Rafraîchissez la page web avec CTRL + F5 (ou CMD + R sur Mac).

* Si vous avez une erreur "ModuleNotFoundError" :
  Vérifiez que vous avez bien fait l'ÉTAPE 2.

============================================================
Fin du guide.
============================================================