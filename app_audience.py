# -*- coding: utf-8 -*-

# ==============================================================================
# 1. LA BOÎTE À OUTILS (IMPORTATION DES LIBRAIRIES)
# ==============================================================================
# Imaginez que vous ouvrez une caisse à outils. Ici, on sort les outils dont on a besoin.
import streamlit as st          # L'outil pour construire le Site Web (boutons, titres...)
import pandas as pd             # L'outil pour manipuler les tableaux (comme un Excel surpuissant)
import numpy as np              # L'outil pour faire des calculs mathématiques rapides
import matplotlib.pyplot as plt # L'outil pour dessiner des graphiques de base
import seaborn as sns           # L'outil pour rendre les graphiques plus jolis et colorés
from sklearn.preprocessing import StandardScaler # L'outil pour mettre tous les chiffres à la même échelle (0 à 1)
from sklearn.cluster import KMeans # L'Intelligence Artificielle (Le cerveau qui va créer les groupes)
from math import pi             # Le nombre Pi (3.14...) nécessaire pour dessiner des cercles
import time                     # L'outil pour gérer le temps (pauses, animations)
from fpdf import FPDF           # L'outil spécial pour créer des fichiers PDF
import tempfile                 # L'outil pour créer des fichiers temporaires (qui s'effacent après)

# ==============================================================================
# 2. CONFIGURATION DE LA PAGE WEB
# ==============================================================================
# On dit à l'application de s'ouvrir en grand (mode 'wide') et on met un titre dans l'onglet du navigateur
st.set_page_config(page_title="Audience Architect", page_icon="🎯", layout="wide")

# ==============================================================================
# 3. LE DESIGN (LE MAQUILLAGE CSS)
# ==============================================================================
# Ici, c'est du code CSS. C'est ce qui rend l'application belle (couleurs, polices, ombres).
# On ne touche pas à la logique ici, juste à l'apparence.
st.markdown("""
    <style>
    /* On importe une jolie police d'écriture (Roboto) depuis Google */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;500;700;900&display=swap');
    
    /* On applique cette police à tout le site */
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }
    
    /* Couleur de fond gris très clair pour faire propre */
    .stApp { background-color: #f8f9fa; }
    
    /* Style du Grand Titre (Bleu foncé, très gros) */
    h1 { color: #0D47A1 !important; font-weight: 900 !important; font-size: 3rem !important; margin-top: -18px; }
    
    /* Style du Sous-titre (Gris bleuté) */
    .subtitle { color: #546E7A; font-size: 1.3rem; margin-top: -10px; font-weight: 300; }
    
    /* Style des Cartes KPI (Les rectangles blancs avec les chiffres) */
    .metric-card { 
        background-color: white; 
        border-radius: 8px; /* Coins arrondis */
        padding: 20px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); /* Petite ombre */
        border-left: 5px solid #1565C0; /* Barre bleue à gauche */
        text-align: center; 
    }
    
    /* Style des gros chiffres */
    .metric-value { font-size: 28px; font-weight: bold; color: #0D47A1; }
    
    /* Style du petit texte sous les chiffres */
    .metric-label { font-size: 12px; color: #78909C; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Style de la console noire (l'animation style Hacker) */
    .console-box { 
        background-color: #263238; 
        color: #80CBC4; /* Texte vert */
        font-family: 'Courier New', monospace; /* Police robot */
        padding: 15px; 
        border-radius: 5px; 
        font-size: 12px; 
        margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True) # On valide l'injection du design

# ==============================================================================
# 4. LE ROBOT PDF (CLASSE SPÉCIALE)
# ==============================================================================
# On crée un "Modèle de PDF" personnalisé qui sait écrire des en-têtes et des pieds de page tout seul.
class ExpertPDF(FPDF):
    def header(self):
        # Cette fonction s'exécute automatiquement en haut de chaque page
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150) # Gris clair
        self.cell(0, 10, 'AUDIENCE ARCHITECT - RAPPORT DE SEGMENTATION STRATEGIQUE', 0, 0, 'R') # Texte aligné à droite
        self.ln(15) # Saut de ligne

    def footer(self):
        # Cette fonction s'exécute automatiquement en bas de chaque page
        self.set_y(-15) # On se place à 15mm du bas
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150)
        self.cell(0, 10, f'Page {self.page_no()} | AUDIENCE ARCHITECT', 0, 0, 'C') # Numéro de page centré

    def chapter_title(self, title):
        # Une fonction pour faire de jolis titres de chapitres bleus
        self.set_font('Arial', 'B', 16)
        self.set_text_color(13, 71, 161) # Bleu Consulting
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(13, 71, 161) # Couleur de la ligne
        self.line(10, self.get_y(), 200, self.get_y()) # On trace une ligne sous le titre
        self.ln(10)

    def chapter_body(self, body):
        # Une fonction pour écrire les paragraphes de texte
        self.set_font('Arial', '', 11)
        self.set_text_color(50) # Gris foncé
        self.multi_cell(0, 6, body) # multi_cell permet au texte d'aller à la ligne tout seul
        self.ln()

# ==============================================================================
# 5. LES FONCTIONS INTELLIGENTES (LES MINI-PROGRAMMES)
# ==============================================================================

def create_radar_chart(df_clean, optimal_k):
    """
    Cette fonction dessine le graphique en toile d'araignée.
    Elle compare l'Âge, la Fidélité, le Panier et la Promo.
    """
    # On choisit les colonnes à dessiner (PAS de revenu ici)
    categories = ['Age', 'Score_Fidelite', 'Panier_Moyen', 'Sensibilite_Promo']
    categories_labels = ['Age', 'Fidélité', 'Panier', 'Promo']
    
    # On calcule la moyenne de chaque groupe
    radar_df = df_clean.groupby('Cluster')[categories].mean()
    
    # On normalise (on met tout entre 0 et 1) pour que le dessin soit équilibré
    scaler = StandardScaler()
    radar_scaled = pd.DataFrame(scaler.fit_transform(radar_df), columns=categories)
    
    # Calculs mathématiques complexes pour faire le cercle (Angles)
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1] # On ferme la boucle du cercle
    
    # Création du dessin
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    colors = ['#1E88E5', '#43A047', '#FDD835', '#E53935', '#8E24AA'] # Palette de couleurs pro
    
    # On dessine chaque groupe un par un
    for i in range(optimal_k):
        values = radar_scaled.iloc[i].values.flatten().tolist()
        values += values[:1] # On ferme la ligne
        # On trace le trait
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=f"Groupe {i+1}", color=colors[i % len(colors)])
        # On colorie l'intérieur (transparence alpha=0.1)
        ax.fill(angles, values, color=colors[i % len(colors)], alpha=0.1)
    
    # On ajoute les étiquettes (Age, Promo...) autour du cercle
    plt.xticks(angles[:-1], categories_labels, color='grey', size=9)
    ax.set_rlabel_position(0)
    # On enlève les chiffres moches sur les axes
    plt.yticks([-1, 0, 1, 2], ["-", "Moy", "+", "++"], color="grey", size=7)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=8)
    return fig

def create_bubble_chart(df_clean):
    """
    Cette fonction crée le graphique à Bulles (Cartographie).
    Axe X = Fidélité, Axe Y = Panier Moyen.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Si le fichier est trop gros (+1000 lignes), on prend un échantillon pour que ça reste lisible
    sample_df = df_clean.sample(min(1000, len(df_clean)))
    
    # On utilise Seaborn pour dessiner
    sns.scatterplot(
        data=sample_df, 
        x='Score_Fidelite', 
        y='Panier_Moyen', 
        hue='Cluster',  # La couleur dépend du groupe
        size='Age',     # La taille de la bulle dépend de l'âge
        sizes=(20, 200),
        palette='viridis', 
        alpha=0.7,      # Transparence des bulles
        ax=ax
    )
    plt.title("Cartographie : Fidelite vs Panier Moyen (Taille = Age)")
    plt.grid(True, alpha=0.3) # On ajoute une grille légère
    return fig

def create_elbow_chart(k_range, inertie, optimal_k):
    """
    Cette fonction dessine la courbe du Coude pour montrer comment l'IA a choisi le nombre de groupes.
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.plot(k_range, inertie, color='#1565C0', marker='o', linestyle='--')
    # On dessine un gros point rouge sur le choix de l'IA
    plt.plot(optimal_k, inertie[optimal_k-1], 'o', color='#D32F2F', markersize=12, label='Point Optimal (Coude)')
    plt.xlabel('Nombre de Groupes')
    plt.ylabel('Inertie (Variance)')
    plt.title(f'Detection Algorithmique : {optimal_k} Groupes')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return fig

def trouver_nombre_ideal(df_scaled):
    """
    C'est ici que la magie opère ! 
    L'algorithme teste de 1 à 9 groupes et calcule l'erreur (inertie) à chaque fois.
    Ensuite, il utilise la géométrie pour trouver la "cassure" de la courbe (le coude).
    """
    inertie = []
    k_range = range(1, 10)
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10) # On initialise l'IA
        km.fit(df_scaled) # On l'entraîne
        inertie.append(km.inertia_) # On mesure l'erreur
    
    # Calcul géométrique de la distance point-droite pour trouver le coude parfait
    p1 = np.array([1, inertie[0]])
    p2 = np.array([len(inertie), inertie[-1]])
    distances = []
    for i in range(len(inertie)):
        p0 = np.array([i+1, inertie[i]])
        dist = np.abs(np.cross(p2-p1, p1-p0)) / np.linalg.norm(p2-p1)
        distances.append(dist)
    
    # On retourne le nombre de groupes qui a la plus grande distance (le coude)
    return distances.index(max(distances)) + 1, inertie, k_range

def generer_description(stats, global_stats):
    """
    Cette fonction donne un nom intelligent au groupe sans parler de revenu.
    Elle compare les stats du groupe avec la moyenne globale.
    """
    tags = []
    
    # Règle 1 : Âge
    if stats['Age'] < global_stats['Age'] - 5: tags.append("GEN Z")
    elif stats['Age'] > global_stats['Age'] + 5: tags.append("SENIOR")
    
    # Règle 2 : Panier Moyen 
    if stats['Panier_Moyen'] > global_stats['Panier_Moyen'] * 1.2: tags.append("HIGH SPENDER") # Dépense beaucoup
    elif stats['Panier_Moyen'] < global_stats['Panier_Moyen'] * 0.8: tags.append("PETIT PANIER") # Dépense peu
    
    # Règle 3 : Comportement
    if stats['Sensibilite_Promo'] > 0.5: tags.append("CHASSEUR PROMO")
    if stats['Score_Fidelite'] > 70: tags.append("FAN")
    if stats['Score_Fidelite'] < 40: tags.append("VOLATILE") # Infidèle
    
    # Si on ne trouve rien de spécial, on l'appelle "Standard"
    return " / ".join(tags) if tags else "CLIENT STANDARD"

def generer_pdf_expert(df_clean, optimal_k, profils, stats_globales, fig_elbow, fig_bubble, fig_radar):
    """
    Cette fonction fabrique le fichier PDF complet page par page.
    """
    pdf = ExpertPDF()
    
    # --- PAGE DE GARDE ---
    pdf.add_page()
    pdf.ln(60) # On descend
    pdf.set_font('Arial', 'B', 26)
    pdf.set_text_color(13, 71, 161)
    pdf.cell(0, 20, "AUDIT DE BASE CLIENTS", 0, 1, 'C') # Titre centré
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(100)
    pdf.cell(0, 10, "Analyse de Clustering & Recommandations Strategiques", 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Date du rapport : {time.strftime('%d/%m/%Y')}", 0, 1, 'C')
    pdf.ln(50)
    
    # --- PAGE 1 : MÉTHODOLOGIE ---
    pdf.add_page()
    pdf.chapter_title("1. Methodologie & Detection des Groupes")
    pdf.chapter_body(f"Nous avons utilise l'algorithme K-Means pour segmenter votre base. La methode du 'Coude' ci-dessous a permis de determiner scientifiquement le nombre ideal de segments.")
    pdf.chapter_body(f"RESULTAT : L'analyse detecte {optimal_k} groupes homogenes distincts.")
    
    # On colle l'image de la courbe Elbow
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_elbow:
        fig_elbow.savefig(tmp_elbow.name, format="png", bbox_inches='tight', dpi=100)
        pdf.image(tmp_elbow.name, x=30, y=90, w=150)
    pdf.ln(100)
    
    # --- PAGE 2 : CARTOGRAPHIE ---
    pdf.add_page()
    pdf.chapter_title("2. Cartographie des Clients (Mapping)")
    pdf.chapter_body("Le graphique ci-dessous positionne chaque client selon la Fidelite (Axe X) et le Panier Moyen (Axe Y). La couleur represente le groupe.")
    
    # On colle l'image des Bulles
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_bubble:
        fig_bubble.savefig(tmp_bubble.name, format="png", bbox_inches='tight', dpi=100)
        pdf.image(tmp_bubble.name, x=20, y=60, w=170)
    pdf.ln(110)
    
    # --- PAGE 3 : DÉTAILS ---
    pdf.add_page()
    pdf.chapter_title("3. Fiches Detailles & Plans d'Action")
    
    # On boucle sur chaque groupe pour écrire ses détails
    for i in range(optimal_k):
        p = profils.iloc[i]
        nom = generer_description(p, stats_globales)
        pop = len(df_clean[df_clean['Cluster']==i])
        part = int(pop/len(df_clean)*100)
        
        # Fond gris clair pour le titre du groupe
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f" GROUPE {i+1} : {nom.upper()}", 0, 1, 'L', 1)
        
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 7, f"   - Poids : {part}% de la base ({pop} clients)", 0, 1)
        # On affiche le Panier au lieu du Revenu
        pdf.cell(0, 7, f"   - Profil : {int(p['Age'])} ans | Panier : {int(p['Panier_Moyen'])} Dhs", 0, 1)
        pdf.cell(0, 7, f"   - Fidelite : {int(p['Score_Fidelite'])}/100", 0, 1)
        
        # Logique de recommandation automatique
        if p['Score_Fidelite'] < 40: action = "URGENCE : Plan de retention + Coupon reactivation."
        elif p['Score_Fidelite'] > 70: action = "OFFENSIF : Programme VIP + Ventes Privees."
        elif p['Sensibilite_Promo'] > 0.5: action = "TACTIQUE : Envoi SMS Promo Flash (-20%)."
        else: action = "MAINTIEN : Newsletter Contenu & Branding."
        
        # On écrit l'action en rouge foncé
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(183, 28, 28) 
        pdf.cell(0, 8, f"   -> STRATEGIE : {action}", 0, 1)
        pdf.set_text_color(0) # On remet le texte en noir
        pdf.ln(4)

    return pdf.output(dest='S').encode('latin-1')

# ==============================================================================
# 6. LE CHEF D'ORCHESTRE (PROGRAMME PRINCIPAL)
# ==============================================================================

# Affichage du Logo et du Titre
c_h1, c_h2 = st.columns([0.5, 5])
with c_h1: st.image("https://cdn-icons-png.flaticon.com/512/2814/2814666.png", width=90)
with c_h2: 
    st.markdown("<h1>AUDIENCE ARCHITECT</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Plateforme de Segmentation Stratégique Automatisée</p>', unsafe_allow_html=True)
st.markdown("---")

# Zone de dépôt de fichier
uploaded_file = st.file_uploader("📂 Importez votre fichier CSV", type=["csv"])

# SI UN FICHIER EST DÉPOSÉ
if uploaded_file is not None:
    
    # GESTION DE MÉMOIRE (SESSION STATE)
    # C'est l'astuce pour que l'app ne recommence pas à zéro quand on clique sur un bouton
    if 'data_analyzed' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
        
        # === 1. ANIMATION DE DÉMARRAGE (Une seule fois) ===
        status = st.empty()
        bar = st.progress(0)
        
        status.markdown('<div class="console-box">> SYSTEM: Initialisation Core IA...</div>', unsafe_allow_html=True)
        bar.progress(10)
        time.sleep(3.5)
        
        df = pd.read_csv(uploaded_file)
        
        # NETTOYAGE
        df_clean = df.fillna(df.mean())
        status.markdown('<div class="console-box">> [ETL] Nettoyage de {len(df)} lignes...<br>> Imputation des valeurs manquantes....</div>', unsafe_allow_html=True)
        # PRÉPARATION DES DONNÉES POUR L'IA
        # On utilise Age, Fidelite, Panier, Promo (On exclut le revenu pour le calcul)
        features_cols = ['Age', 'Score_Fidelite', 'Panier_Moyen', 'Sensibilite_Promo']
        bar.progress(10)
        time.sleep(2.5)
        # Vérification de sécurité : si les colonnes existent, on les prend, sinon on prend tout
        if set(features_cols).issubset(df_clean.columns):
            X = df_clean[features_cols]
        else:
            X = df_clean.select_dtypes(include=[np.number])

        # Normalisation
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(X)
        
        status.markdown('<div class="console-box">> [AI] Recherche du nombre optimal de groupes...<br>> Exécution algorithme K-Means (Elbow Method)..</div>', unsafe_allow_html=True)
        bar.progress(60)
        time.sleep(1)
        
        # CALCUL DES GROUPES
        optimal_k, inertie, k_range = trouver_nombre_ideal(df_scaled)
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        df_clean['Cluster'] = kmeans.fit_predict(df_scaled)
        
        status.markdown(f'<div class="console-box">> SUCCESS: {optimal_k} Segments détectés.</div>', unsafe_allow_html=True)
        bar.progress(100)
        time.sleep(2.5)
        status.empty() # On efface les messages
        bar.empty()
        
        # ON SAUVEGARDE TOUT DANS LA MÉMOIRE
        st.session_state.df_clean = df_clean
        st.session_state.optimal_k = optimal_k
        st.session_state.inertie = inertie
        st.session_state.k_range = k_range
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.data_analyzed = True

    # === 2. AFFICHAGE DES RÉSULTATS (Immédiat) ===
    # On récupère les données de la mémoire
    df_clean = st.session_state.df_clean
    optimal_k = st.session_state.optimal_k
    inertie = st.session_state.inertie
    k_range = st.session_state.k_range

    st.success(f"✅ Analyse Terminée : {optimal_k} Groupes Stratégiques Identifiés.")
    
    # --- LES CHIFFRES CLÉS (KPI) ---
    k1, k2, k3 = st.columns(3) 
    with k1: st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(df_clean):,}</div><div class="metric-label">Base Clients</div></div>""", unsafe_allow_html=True)
    with k2: st.markdown(f"""<div class="metric-card"><div class="metric-value">{optimal_k}</div><div class="metric-label">Segments Clés</div></div>""", unsafe_allow_html=True)
    with k3: st.markdown(f"""<div class="metric-card"><div class="metric-value">{int(df_clean['Panier_Moyen'].mean())} Dhs</div><div class="metric-label">Panier Moyen Global</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # CRÉATION DES GRAPHIQUES (Pour l'écran et le PDF)
    # 1. Camembert
    fig_pie, ax = plt.subplots(figsize=(5,5))
    colors = ['#1E88E5', '#43A047', '#FDD835', '#E53935', '#8E24AA']
    plt.pie(df_clean['Cluster'].value_counts(), labels=[f"Grp {i+1}" for i in range(optimal_k)], autopct='%1.1f%%', colors=colors, wedgeprops={'edgecolor':'white'})
    
    # 2. Autres graphiques
    fig_radar = create_radar_chart(df_clean, optimal_k)
    fig_bubble = create_bubble_chart(df_clean)
    fig_elbow = create_elbow_chart(k_range, inertie, optimal_k)

    # --- LES ONGLETS ---
    tab1, tab2, tab3, tab4 = st.tabs(["VUE STRATÉGIQUE", "PERSONAS", "CARTOGRAPHIE", "RAPPORT EXPERT"])
    
    # Onglet 1 : Vue d'ensemble
    with tab1:
        c1, c2 = st.columns(2)
        with c1: 
            st.subheader("Poids des Segments")
            st.pyplot(fig_pie)
        with c2: 
            st.subheader("Justification IA (Coude)")
            st.pyplot(fig_elbow)
            st.caption(f"L'algorithme a détecté une cassure optimale à {optimal_k} groupes.")

    # Onglet 2 : Détails des groupes
    with tab2:
        profils = df_clean.groupby('Cluster').mean()
        stats_globales = df_clean.mean()
        for i in range(optimal_k):
            p = profils.iloc[i]
            nom = generer_description(p, stats_globales)
            with st.expander(f"👤 GROUPE {i+1} : {nom}", expanded=True):
                c_info, c_act, c_dl = st.columns([1, 2, 0.5])
                with c_info:
                    st.write(f"**Pop:** {len(df_clean[df_clean['Cluster']==i])}")
                    st.write(f"**Panier:** {int(p['Panier_Moyen'])} Dhs") # Pas de revenu
                    st.write(f"**Fidélité:** {int(p['Score_Fidelite'])}/100")
                with c_act:
                    # Logique de recommandation
                    if p['Score_Fidelite'] < 40: st.error("🚨 ACTION : Campagne Rétention")
                    elif p['Score_Fidelite'] > 70: st.success("💎 ACTION : Club VIP")
                    elif p['Sensibilite_Promo'] > 0.5: st.warning("🏷️ ACTION : Promo Flash")
                    else: st.info("📧 ACTION : Newsletter")
                with c_dl:
                    # Bouton pour télécharger juste ce groupe
                    df_grp = df_clean[df_clean['Cluster']==i]
                    st.download_button("📥 CSV", df_grp.to_csv(index=False).encode('utf-8'), f"groupe_{i+1}.csv", "text/csv", key=f"dl_{i}")

    # Onglet 3 : Carte des bulles
    with tab3:
        st.subheader("Cartographie Clients (Fidélité vs Panier)")
        st.pyplot(fig_bubble)
        st.info("💡 Les grosses bulles représentent les clients plus âgés. Les couleurs différencient les groupes.")

    # Onglet 4 : Téléchargements
    with tab4:
        st.header("Centre de Téléchargement")
        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            st.info("📊 Données Segmentées")
            # Le CSV complet contient la colonne Cluster
            st.download_button("📥 Télécharger CSV Complet", df_clean.to_csv(index=False).encode('utf-8'), "audience_analysee.csv", "text/csv")
        with c_ex2:
            st.success("📄 Rapport Consulting PDF")
            # Génération du PDF Expert
            pdf_bytes = generer_pdf_expert(df_clean, optimal_k, profils, stats_globales, fig_elbow, fig_bubble, fig_radar)
            st.download_button("📥 Télécharger le Rapport PDF", pdf_bytes, "Rapport_Segmentation_Expert.pdf", "application/pdf")

else:
    # Si aucun fichier n'est chargé, on affiche un message d'attente
    st.info("👋 En attente de données...")