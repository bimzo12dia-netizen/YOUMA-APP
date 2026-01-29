import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="YOUMA - Facturation", layout="wide")

st.title("🚀 YOUMA - Système de Facturation")

# --- BASE DE DONNÉES ---
if 'clients' not in st.session_state:
    st.session_state.clients = ["Passager", "Entreprise Alpha", "Jean Dupont"]

produits = {
    "Photocopie Noir et Blanc": 25,
    "Photocopie Couleur": 100,
    "Impression Noir et Blanc": 50,
    "Impression Couleur": 200,
    "Tirage Photo": 500,
    "Reliure": 1000,
    "Plastification": 500,
    "Conception de Logo": 15000
}

# --- BARRE LATÉRALE (NAVIGATION) ---
menu = st.sidebar.selectbox("Menu", ["Nouvelle Facture", "Gestion Clients", "Historique"])

if menu == "Nouvelle Facture":
    st.header("📄 Créer une facture")
    
    col1, col2 = st.columns(2)
    with col1:
        client = st.selectbox("Sélectionner le Client", st.session_state.clients)
        date = st.date_input("Date", datetime.now())
    with col2:
        n_facture = st.text_input("N° de Facture", "FAC-2024-001")

    st.subheader("Articles")
    
    # Système de sélection dynamique
    if 'items' not in st.session_state:
        st.session_state.items = []

    selected_prod = st.selectbox("Ajouter un produit", list(produits.keys()))
    qty = st.number_input("Quantité", min_value=1, value=1)
    
    if st.button("Ajouter à la facture"):
        st.session_state.items.append({
            "Produit": selected_prod,
            "Quantité": qty,
            "Prix Unitaire": produits[selected_prod],
            "Total": qty * produits[selected_prod]
        })

    # Affichage du tableau de facture
    if st.session_state.items:
        df_facture = pd.DataFrame(st.session_state.items)
        st.table(df_facture)
        
        total_general = df_facture["Total"].sum()
        st.metric("TOTAL À PAYER", f"{total_general} FCFA")

        if st.button("Enregistrer et Imprimer"):
            st.success(f"Facture {n_facture} pour {client} enregistrée !")
            # Ici on pourrait ajouter la génération de PDF
            st.session_state.items = [] # Réinitialisation

elif menu == "Gestion Clients":
    st.header("👥 Base de données Clients")
    nouveau_client = st.text_input("Nom du nouveau client")
    if st.button("Ajouter le client"):
        st.session_state.clients.append(nouveau_client)
        st.success("Client ajouté !")
    
    st.write("Liste des clients :", st.session_state.clients)
