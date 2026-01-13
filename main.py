import streamlit as st
import pandas as pd
import numpy as np
import pickle
import lzma  # pour lire le fichier compressé .xz

# =========================
# Configuration page
# =========================
st.set_page_config(
    page_title="Calculateur de poids idéal",
    page_icon="⚖️",
    layout="centered"
)

# =========================
# Chargement du modèle compressé (.xz)
# =========================
model = pickle.load(open('model.sav', 'rb'))

# =========================
# Sidebar
# =========================
st.sidebar.header("Informations")
st.sidebar.markdown("""
### Application de prédiction du poids
Cette application estime un **poids cible personnalisé**
à partir de vos caractéristiques.

**Auteur :** Parfait Tanoh N'goran
""")

# =========================
# Titre
# =========================
st.title("⚖️ Calculateur de poids idéal")

# =========================
# Inputs utilisateur
# =========================
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Âge", min_value=10, max_value=80, value=30)
    taille = st.number_input("Taille (cm)", min_value=140, max_value=210, value=170)

with col2:
    sexe = st.selectbox("Sexe", ["Femme", "Homme"])
    niveau_activite = st.selectbox(
        "Niveau d'activité",
        ["Sédentaire", "Modéré", "Actif"]
    )

# Encodage des variables
sexe_enc = 0 if sexe == "Femme" else 1
niveau_enc = {"Sédentaire": 0, "Modéré": 1, "Actif": 2}[niveau_activite]

poids_actuel = st.number_input(
    "Poids actuel (kg)", min_value=30.0, max_value=200.0, value=70.0
)

# =========================
# Bouton prédiction
# =========================
if st.button("Calculer mon poids idéal"):

    # DataFrame d'entrée pour le modèle
    df_input = pd.DataFrame([{
        "age": age,
        "taille": taille,
        "sexe": sexe_enc,
        "niveau_activite": niveau_enc
    }])

    # Prédiction ML
    poids_cible = model.predict(df_input)[0]

    # IMC pour poids min et max
    poids_min = 18.5 * (taille / 100) ** 2
    poids_max = 24.9 * (taille / 100) ** 2

    delta = poids_actuel - poids_cible

    # Recommandations personnalisées
    if delta > 3:
        reco = "Perte de poids"
        color = "#E74C3C"
        sport = "Cardio 4–5x/semaine + renforcement"
        alim = "Réduire sucres, augmenter protéines et fibres"
    elif delta < -3:
        reco = "Prise de masse"
        color = "#3498DB"
        sport = "Musculation 4–5x/semaine"
        alim = "Augmenter calories saines et protéines"
    else:
        reco = "Poids stable"
        color = "#2ECC71"
        sport = "Activité régulière modérée"
        alim = "Alimentation équilibrée"

    # =========================
    # Affichage résultat
    # =========================
    st.markdown(f"""
<div style='
    border:2px solid {color};
    border-radius:15px;
    padding:25px;
    background-color:#f0f8ff;
    box-shadow: 3px 3px 15px rgba(0,0,0,0.1);
    margin-bottom:20px;
    color: #000000;  
    font-weight:500;
'>
    <h2 style='color:{color}; text-align:center;'>Résultat</h2>
    <p><b>Poids idéal (IMC 18.5-24.9) :</b> {poids_min:.1f} kg – {poids_max:.1f} kg</p>
    <p><b>Poids cible personnalisé (ML) :</b> {poids_cible:.1f} kg</p>
    <p><b>Recommandation :</b> <span style='color:{color}; font-weight:bold;'>{reco}</span></p>
    <p><b>Plan alimentation :</b> {alim}</p>
    <p><b>Plan sport :</b> {sport}</p>
    <div style='background-color:#ddd; border-radius:10px; margin-top:15px;'>
        <div style='width:{min(abs(delta)*10,100)}%; 
                    background-color:{color}; 
                    padding:8px; 
                    color:white; 
                    text-align:center; 
                    border-radius:10px; font-weight:bold;'>
            Écart de poids : {delta:.1f} kg
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
