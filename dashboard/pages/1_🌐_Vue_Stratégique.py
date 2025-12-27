import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Vue Stratégique", page_icon="🌐", layout="wide")

st.title("🌐 Vue Stratégique Globale")
st.markdown("**Rôle:** Vice-doyen/Doyen")
st.markdown("---")

# Métriques KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🎓 Étudiants", "13,247", "3.2%")
with col2:
    st.metric("📅 Examens", "1,856", "5.8%")
with col3:
    st.metric("🏢 Salles", "42", "78% occ.")
with col4:
    st.metric("👨‍🏫 Professeurs", "287", "92% sat.")
with col5:
    st.metric("⚠️ Conflits", "47", "-12%")

st.markdown("### 📊 Tableau de Bord des Performances")

# Graphique 1: Occupation globale
st.subheader("🏢 Occupation Globale des Amphis et Salles")
col1, col2 = st.columns(2)

with col1:
    data_occupation = {
        'Type': ['Amphis (>100)', 'Salles (20-100)', 'Salles (<20)', 'Laboratoires'],
        'Total': [15, 18, 6, 3],
        'Utilisés': [12, 15, 5, 2],
        'Taux': [80, 83, 83, 67]
    }
    df_occ = pd.DataFrame(data_occupation)
    fig1 = px.bar(df_occ, x='Type', y='Taux', color='Type',
                 title="Taux d'Occupation par Type de Salle",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Heatmap occupation
    jours = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']
    creneaux = ['8h', '10h', '14h', '16h']
    data_heatmap = [[random.randint(60, 95) for _ in creneaux] for _ in jours]
    
    fig2 = go.Figure(data=go.Heatmap(
        z=data_heatmap,
        x=creneaux,
        y=jours,
        colorscale='RdYlGn',
        zmin=0,
        zmax=100,
        text=[[f'{val}%' for val in row] for row in data_heatmap],
        texttemplate="%{text}",
        textfont={"size": 10}
    ))
    fig2.update_layout(title="Occupation Hebdomadaire - Amphi A")
    st.plotly_chart(fig2, use_container_width=True)

# Graphique 2: Taux conflits par département
st.subheader("⚠️ Taux de Conflits par Département")
data_conflits = {
    'Département': ['Info', 'Maths', 'Physique', 'Chimie', 'Bio', 'Éco', 'Droit'],
    'Examens': [320, 280, 190, 150, 210, 260, 180],
    'Conflits': [12, 8, 5, 3, 6, 9, 4],
    'Taux %': [3.8, 2.9, 2.6, 2.0, 2.9, 3.5, 2.2]
}
df_conflits = pd.DataFrame(data_conflits)

fig3 = px.scatter(df_conflits, x='Examens', y='Conflits', size='Taux %',
                 color='Département', hover_name='Département',
                 size_max=60, title="Analyse des Conflits par Département")
st.plotly_chart(fig3, use_container_width=True)

# Section KPIs académiques
st.subheader("📈 KPIs Académiques")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("⏰ Heures Profs", "12,850h", "3.2%", delta_color="normal")
    st.caption("Total heures de surveillance")
with col2:
    st.metric("🏫 Taux Salles", "78%", "1.5%", delta_color="normal")
    st.caption("Salles utilisées / disponibles")
with col3:
    st.metric("📊 Satisfaction", "92%", "2.1%", delta_color="normal")
    st.caption("Enquête satisfaction")
with col4:
    st.metric("⚡ Performance", "94%", "0.8%", delta_color="normal")
    st.caption("Taux réussite génération")

# Validation finale
st.subheader("✅ Validation Finale EDT")
col1, col2 = st.columns([2, 1])

with col1:
    st.info("**Statut de validation globale**")
    
    validation_data = {
        'Département': ['Info', 'Maths', 'Physique', 'Chimie', 'Bio', 'Éco', 'Droit'],
        'Statut': ['✓ Validé', '✓ Validé', '✓ Validé', '⏳ En cours', '❌ Rejeté', '⏳ En cours', '✓ Validé'],
        'Date': ['15/01', '15/01', '16/01', '-', '14/01', '-', '16/01']
    }
    df_validation = pd.DataFrame(validation_data)
    st.dataframe(df_validation, use_container_width=True, hide_index=True)

with col2:
    st.write("**Actions globales:**")
    if st.button("✅ Valider EDT Global", type="primary", use_container_width=True):
        st.success("Emploi du temps validé avec succès!")
        st.balloons()
    
    if st.button("📤 Exporter Rapport", use_container_width=True):
        st.info("Rapport exporté au format PDF")
    
    if st.button("🔄 Planifier Réunion", use_container_width=True):
        st.info("Réunion planifiée avec les chefs de département")
