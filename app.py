# =============================================================================
# TABLEAU DE BORD — CENTRALE TRIGÉNÉRATION ADWYA
# Outil de suivi des performances énergétiques
# Projet de Fin d'Études (PFE) 2026
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# =============================================================================
# 0. CONFIGURATION PAGE
# =============================================================================
st.set_page_config(
    page_title="Trigénération ADWYA — PFE Ranim ZAMMEL 2026",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 1. CSS / STYLE GLOBAL
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #070e1a;
    color: #c2d4e8;
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
}
[data-testid="stSidebar"] {
    background-color: #0b1422;
    border-right: 1px solid #162030;
}
h1, h2, h3, h4 {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    letter-spacing: 1px;
    color: #d8ecff;
}
.kpi-card {
    background: linear-gradient(145deg, #0d1b2e 0%, #132438 100%);
    border: 1px solid #1b3352;
    border-radius: 10px;
    padding: 16px 18px 12px;
    position: relative;
    overflow: hidden;
    margin-bottom: 10px;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00b4d8, #0077b6);
}
.kpi-card.warn::before  { background: linear-gradient(90deg, #f7971e, #ffd200); }
.kpi-card.alert::before { background: linear-gradient(90deg, #e63946, #ff6b6b); }
.kpi-label { font-size: 11px; color: #4d7fa8; text-transform: uppercase;
             letter-spacing: 2px; margin-bottom: 6px; }
.kpi-value { font-family: 'Share Tech Mono', monospace; font-size: 30px;
             color: #e8f4ff; line-height: 1; }
.kpi-unit  { font-size: 14px; color: #4d7fa8; }
.kpi-delta { font-size: 12px; margin-top: 5px; }
.delta-pos { color: #2dc653; }
.delta-neg { color: #e63946; }
.delta-neu { color: #778da9; }
.sec-hdr {
    border-left: 4px solid #0077b6;
    padding-left: 12px;
    margin: 26px 0 14px;
    font-size: 18px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px;
    color: #90c2e7;
}
.arow-red  { background:rgba(230,57,70,0.09); border-left:3px solid #e63946;
             padding:8px 12px; margin-bottom:5px; border-radius:5px;
             font-size:13px; line-height:1.6; }
.arow-yel  { background:rgba(255,210,0,0.07); border-left:3px solid #ffd200;
             padding:8px 12px; margin-bottom:5px; border-radius:5px;
             font-size:13px; line-height:1.6; }
.tag-ok    { background:#1a3d2b; color:#2dc653; border-radius:4px;
             padding:2px 8px; font-size:11px; font-weight:600; }
.tag-warn  { background:#3a2c10; color:#ffd200; border-radius:4px;
             padding:2px 8px; font-size:11px; font-weight:600; }
.tag-alert { background:#3d1015; color:#ff6b6b; border-radius:4px;
             padding:2px 8px; font-size:11px; font-weight:600; }
.rbox {
    background: #0b1929; border: 1px solid #1b3352;
    border-radius: 10px; padding: 22px 26px;
    font-size: 14px; line-height: 1.9; margin-bottom: 16px;
}
.rbox h4 {
    color: #90c2e7; font-size: 15px;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin: 18px 0 8px;
    border-bottom: 1px solid #1b3352; padding-bottom: 4px;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: #0b1422; padding: 8px;
    border-radius: 10px; margin-bottom: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: #101e30; color: #4d7fa8;
    border-radius: 7px; font-family: 'Rajdhani', sans-serif;
    font-weight: 600; letter-spacing: 1px;
    font-size: 13px; padding: 6px 14px;
}
.stTabs [aria-selected="true"] {
    background: #0077b6 !important; color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. EN-TÊTE
# =============================================================================
st.markdown("""
<div style="display:flex;align-items:center;gap:18px;padding:6px 0 10px;">
  <div style="font-size:48px;line-height:1;">&#9889;</div>
  <div>
    <div style="font-size:24px;font-weight:700;letter-spacing:2px;color:#e8f4ff;
                font-family:'Rajdhani',sans-serif;line-height:1.1;">
      TABLEAU DE BORD &mdash; CENTRALE TRIG&Eacute;N&Eacute;RATION ADWYA
    </div>
    <div style="font-size:12px;color:#3a6a90;letter-spacing:3px;
                font-family:'Share Tech Mono',monospace;margin-top:4px;">
      SUIVI DES PERFORMANCES &Eacute;NERG&Eacute;TIQUES &nbsp;&middot;&nbsp; PFE RANIM ZAMMEL 2026
    </div>
  </div>
</div>
<hr style="border-color:#162030;margin-bottom:20px;">
""", unsafe_allow_html=True)

# =============================================================================
# 3. SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Paramètres système")
    PCI           = st.number_input("PCI gaz naturel (kWh/Nm³)", value=10.55, step=0.01)
    prix_kwh_steg = st.number_input("Prix kWh STEG achat (DT)", value=0.291, step=0.001)
    prix_gaz_nm3  = st.number_input("Prix gaz naturel (DT/Nm³)", value=0.575, step=0.001)
    taux_pertes   = st.number_input("Pertes canalisations (%)", value=3.0, step=0.5,
                                    min_value=0.0, max_value=20.0) / 100.0

    st.markdown("---")
    st.markdown("### 📐 Valeurs nominales")
    eta_e_nom    = st.number_input("η_e nominal",        value=0.42,  step=0.01)
    eta_th_nom   = st.number_input("η_th nominal",       value=0.30,  step=0.01)
    eta_frig_nom = st.number_input("η_frig nominal",     value=0.235, step=0.005)
    eta_glob_nom = st.number_input("η_global nominal",   value=0.765, step=0.005)
    cop_nom      = st.number_input("COP nominal absorption", value=0.78, step=0.01)

    st.markdown("---")
    st.markdown("### 🚨 Seuils d'alerte")
    seuil_eta_glob = st.number_input("Seuil η_global", value=0.60, step=0.01)
    seuil_eta_e    = st.number_input("Seuil η_e",      value=0.35, step=0.01)
    seuil_eta_th   = st.number_input("Seuil η_th",     value=0.25, step=0.01)
    seuil_cop      = st.number_input("Seuil COP",      value=0.65, step=0.01)

    st.markdown("---")
    st.markdown("### 📂 Import données")
    uploaded_file = st.file_uploader("Fichier Excel (.xlsx)", type=["xlsx"],
        help="Colonnes requises : mois, h_service, prod_nette, gaz, froid, chaleur, COP")

# =============================================================================
# 4. DONNÉES
# =============================================================================
COLONNES = ["mois", "h_service", "prod_nette", "gaz", "froid", "chaleur", "COP"]

#  mois        h_serv  prod_nette    gaz       froid    chaleur    COP
DATA_DEFAUT = [
    ("Juin 2024",  710,  771_962,  192_530,  438_844,  510_983,  0.399),
    ("Juil 2024",  576,  652_926,  154_636,  318_003,  384_522,  0.573),
    ("Août 2024",  437,  483_421,  114_942,   23_456,  221_970,  0.118),
    ("Sept 2024",  669,  735_425,  179_737,  212_682,  371_949,  0.746),
    ("Oct  2024",  742,  820_477,  197_633,  320_251,  495_215,  0.778),
    ("Nov  2024",  687,  768_932,  186_451,  176_946,  432_366,  0.554),
    ("Déc  2024",  739,  831_777,  198_821,  151_977,  490_387,  0.512),
    ("Jan  2025",  731,  849_815,  196_592,        0,  170_709,  None ),
    ("Fév  2025",  656,  747_997,  176_950,  112_379,  325_380,  0.539),
    ("Mars 2025",  724,  731_787,  176_210,  169_547,  418_558,  0.551),
    ("Avr  2025",  698,  858_198,  209_513,  204_424,  483_362,  0.567),
    ("Mai  2025",  731,  812_044,  199_061,  217_045,  488_017,  0.607),
]

# Causes opérationnelles connues (pour alertes et rapport)
CAUSES_COP = {
    "Jan  2025": (
        "Panne confirmée de la machine à absorption (janvier 2025) : "
        "COP = 0, froid récupéré = 0 kWh. "
        "Cause probable : défaillance mécanique circuit LiBr ou pompe de solution. "
        "Action : inspection complète et remise en service prioritaire."
    ),
    "Août 2024": (
        "COP anormalement bas (0.118) en période estivale. "
        "Causes probables : température eau de tour élevée (>35°C), "
        "encrassement du condenseur côté eau, déséquilibre concentration LiBr. "
        "Action : nettoyage condenseur, contrôle tour de refroidissement, "
        "analyse solution LiBr."
    ),
}

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file)
        manquantes = [c for c in COLONNES if c not in df_raw.columns]
        if manquantes:
            st.error(f"❌ Colonnes manquantes : {manquantes}. Données par défaut utilisées.")
            df_raw = pd.DataFrame(DATA_DEFAUT, columns=COLONNES)
        else:
            df_raw = df_raw[COLONNES].copy()
            st.sidebar.success(f"✅ {len(df_raw)} mois chargés")
    except Exception as e:
        st.error(f"Erreur lecture fichier : {e}")
        df_raw = pd.DataFrame(DATA_DEFAUT, columns=COLONNES)
else:
    df_raw = pd.DataFrame(DATA_DEFAUT, columns=COLONNES)

df_raw["cause_cop"] = df_raw["mois"].map(CAUSES_COP).fillna("")

# Conversions numériques sécurisées
for col in ["prod_nette", "gaz", "froid", "chaleur", "h_service"]:
    df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce").fillna(0)
df_raw["COP"] = pd.to_numeric(df_raw["COP"], errors="coerce")   # garde NaN volontairement

# =============================================================================
# 5. CALCULS KPI
# =============================================================================
# Puissance calorifique gaz (kWh_PCI)
df_raw["P_gaz"] = df_raw["gaz"] * PCI

# Rendements (protection contre division par zéro)
safe = df_raw["P_gaz"].replace(0, np.nan)
df_raw["eta_e"]    = df_raw["prod_nette"] / safe
df_raw["eta_th"]   = df_raw["chaleur"]    / safe
df_raw["eta_frig"] = df_raw["froid"]      / safe
df_raw["eta_glob"] = df_raw["eta_e"] + df_raw["eta_th"] + df_raw["eta_frig"]
for col in ["eta_e","eta_th","eta_frig","eta_glob"]:
    df_raw[col] = df_raw[col].fillna(0)

# Pertes
df_raw["pertes_reseau"] = df_raw["P_gaz"] * taux_pertes
df_raw["pertes_sys"] = (
    df_raw["P_gaz"] - df_raw["prod_nette"]
    - df_raw["chaleur"] - df_raw["froid"]
    - df_raw["pertes_reseau"]
).clip(lower=0)

# Économies financières
df_raw["cout_gaz_dt"]    = df_raw["gaz"] * prix_gaz_nm3
df_raw["val_elec_dt"]    = df_raw["prod_nette"] * prix_kwh_steg
# Valeur chaleur = équivalent gaz économisé sur chaudière (η_chaud = 90%)
df_raw["val_chaleur_dt"] = df_raw["chaleur"] / (0.90 * PCI) * prix_gaz_nm3
# Valeur froid = équivalent élec économisé sur GEG (COP_GEG = 3.1)
df_raw["val_froid_dt"]   = df_raw["froid"] / 3.1 * prix_kwh_steg
# Gain global net = valeurs produites − coût gaz
df_raw["gain_global_dt"] = (
    df_raw["val_elec_dt"] + df_raw["val_chaleur_dt"]
    + df_raw["val_froid_dt"] - df_raw["cout_gaz_dt"]
)

# Efficacité horaire
safe_h = df_raw["h_service"].replace(0, np.nan)
df_raw["elec_h"]    = (df_raw["prod_nette"] / safe_h).fillna(0)
df_raw["chaleur_h"] = (df_raw["chaleur"]    / safe_h).fillna(0)
df_raw["froid_h"]   = (df_raw["froid"]      / safe_h).fillna(0)

# =============================================================================
# 6. FILTRE MOIS
# =============================================================================
with st.sidebar:
    mois_select = st.multiselect(
        "🗓️ Sélection des mois",
        df_raw["mois"].tolist(),
        default=df_raw["mois"].tolist()
    )

df = df_raw[df_raw["mois"].isin(mois_select)].reset_index(drop=True)

if df.empty:
    st.warning("⚠️ Aucun mois sélectionné.")
    st.stop()

# =============================================================================
# 7. AGRÉGATS PÉRIODE
# =============================================================================
eta_glob_moy = df["eta_glob"].mean()
eta_e_moy    = df["eta_e"].mean()
eta_th_moy   = df["eta_th"].mean()
eta_frig_moy = df["eta_frig"].mean()

cop_valide   = df["COP"].dropna()
cop_moy      = float(cop_valide.mean()) if len(cop_valide) > 0 else np.nan

total_elec      = df["prod_nette"].sum()
total_chaleur   = df["chaleur"].sum()
total_froid     = df["froid"].sum()
total_gaz_nm3   = df["gaz"].sum()
total_pgaz      = df["P_gaz"].sum()
total_cout_gaz  = df["cout_gaz_dt"].sum()
total_val_elec  = df["val_elec_dt"].sum()
total_val_chaud = df["val_chaleur_dt"].sum()
total_val_froid = df["val_froid_dt"].sum()
total_gain      = df["gain_global_dt"].sum()

nb_mois   = len(df)
best_m    = df.loc[df["eta_glob"].idxmax(), "mois"]
worst_m   = df.loc[df["eta_glob"].idxmin(), "mois"]
periode_t = f"{df['mois'].iloc[0]} → {df['mois'].iloc[-1]}"

# =============================================================================
# 8. DÉTECTION ALERTES
# =============================================================================
def detecter_alertes(dataframe: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in dataframe.iterrows():
        mois = r["mois"]
        cause_cop = r.get("cause_cop", "")

        # η_e
        if r["eta_e"] > 0 and r["eta_e"] < seuil_eta_e:
            rows.append({
                "Mois": mois, "KPI": "η_e",
                "Valeur": f"{r['eta_e']:.1%}", "Seuil": f"{seuil_eta_e:.0%}",
                "Nominal": f"{eta_e_nom:.0%}",
                "Écart nominal": f"{r['eta_e']-eta_e_nom:+.1%}",
                "Statut": "🔴 ALERTE",
                "Cause": "Rendement électrique sous seuil",
                "Action": "Diagnostic moteur : bougies allumage, filtres air, qualité gaz, refroidissement."
            })

        # η_th
        if r["eta_th"] > 0 and r["eta_th"] < seuil_eta_th:
            niv = "🔴 ALERTE" if r["eta_th"] < 0.15 else "🟡 SURVEILLANCE"
            rows.append({
                "Mois": mois, "KPI": "η_th",
                "Valeur": f"{r['eta_th']:.1%}", "Seuil": f"{seuil_eta_th:.0%}",
                "Nominal": f"{eta_th_nom:.0%}",
                "Écart nominal": f"{r['eta_th']-eta_th_nom:+.1%}",
                "Statut": niv,
                "Cause": "Récupération thermique insuffisante",
                "Action": "Inspecter échangeurs (encrassement), vérifier débits et V3V."
            })

        # COP
        cop = r["COP"]
        if pd.isna(cop) or cop == 0:
            rows.append({
                "Mois": mois, "KPI": "COP absorption",
                "Valeur": "0 (ARRÊT)", "Seuil": f"{seuil_cop:.2f}",
                "Nominal": f"{cop_nom:.2f}", "Écart nominal": "N/A",
                "Statut": "🔴 ALERTE",
                "Cause": cause_cop if cause_cop else "Machine absorption hors service.",
                "Action": "Intervention prioritaire : niveau LiBr, étanchéité, T générateur, débit eau de tour."
            })
        elif cop < seuil_cop:
            rows.append({
                "Mois": mois, "KPI": "COP absorption",
                "Valeur": f"{cop:.3f}", "Seuil": f"{seuil_cop:.2f}",
                "Nominal": f"{cop_nom:.2f}",
                "Écart nominal": f"{cop-cop_nom:+.3f}",
                "Statut": "🔴 ALERTE",
                "Cause": cause_cop if cause_cop else "COP inférieur au seuil.",
                "Action": "Nettoyage condenseur, analyse LiBr, contrôle T° eau de tour."
            })

        # η_global
        if r["eta_glob"] > 0 and r["eta_glob"] < seuil_eta_glob:
            rows.append({
                "Mois": mois, "KPI": "η_global",
                "Valeur": f"{r['eta_glob']:.1%}", "Seuil": f"{seuil_eta_glob:.0%}",
                "Nominal": f"{eta_glob_nom:.1%}",
                "Écart nominal": f"{r['eta_glob']-eta_glob_nom:+.1%}",
                "Statut": "🔴 ALERTE",
                "Cause": "Performance globale critique",
                "Action": "Audit complet : moteur + échangeurs + absorption."
            })

    cols = ["Mois","KPI","Valeur","Seuil","Nominal","Écart nominal","Statut","Cause","Action"]
    return pd.DataFrame(rows, columns=cols)

# =============================================================================
# 9. HELPER KPI CARD
# =============================================================================
def kpi_html(label, val_str, unit, seuil, nominal, val_brut):
    delta = (val_brut - nominal) / nominal * 100 if nominal != 0 else 0
    cls   = "alert" if val_brut < seuil else ("warn" if val_brut < nominal else "")
    dcls  = "delta-pos" if delta >= 0 else "delta-neg"
    sign  = "▲" if delta >= 0 else "▼"
    nom_fmt = f"{nominal*100:.1f}%" if unit == "%" else f"{nominal:.2f}"
    return f"""<div class="kpi-card {cls}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{val_str} <span class="kpi-unit">{unit}</span></div>
      <div class="kpi-delta {dcls}">{sign} {abs(delta):.1f}% vs nominal ({nom_fmt})</div>
    </div>"""

def perf_tag(val, seuil, nom):
    if val >= nom:   return '<span class="tag-ok">&#10004; NOMINAL</span>'
    elif val >= seuil: return '<span class="tag-warn">&#9888; DEGRADE</span>'
    else:              return '<span class="tag-alert">&#10006; CRITIQUE</span>'

# =============================================================================
# 10. ONGLETS
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  KPI & Rendements",
    "🔀  Flux Énergétique",
    "🚨  Alertes",
    "💰  Analyse Économique",
    "📋  Rapport & Export",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — KPI & RENDEMENTS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:

    # KPI CARDS
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi_html("η GLOBAL",    f"{eta_glob_moy*100:.1f}", "%",
                                  seuil_eta_glob, eta_glob_nom, eta_glob_moy), unsafe_allow_html=True)
    with c2: st.markdown(kpi_html("η ELECTRIQUE",f"{eta_e_moy*100:.1f}", "%",
                                  seuil_eta_e, eta_e_nom, eta_e_moy), unsafe_allow_html=True)
    with c3: st.markdown(kpi_html("η THERMIQUE", f"{eta_th_moy*100:.1f}", "%",
                                  seuil_eta_th, eta_th_nom, eta_th_moy), unsafe_allow_html=True)
    with c4:
        cop_s = f"{cop_moy:.3f}" if not np.isnan(cop_moy) else "N/A"
        cop_b = cop_moy if not np.isnan(cop_moy) else 0.0
        st.markdown(kpi_html("COP ABSORPTION", cop_s, "", seuil_cop, cop_nom, cop_b), unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-label">Énergie utile totale</div>
          <div class="kpi-value">{(total_elec+total_chaleur+total_froid)/1e6:.2f}
            <span class="kpi-unit">GWh</span></div>
          <div class="kpi-delta delta-neu">sur {nb_mois} mois</div>
        </div>""", unsafe_allow_html=True)

    # COURBE η_global
    st.markdown('<div class="sec-hdr">Évolution du rendement global</div>', unsafe_allow_html=True)
    mc = ["#e63946" if v < seuil_eta_glob else ("#ffd200" if v < eta_glob_nom else "#2dc653")
          for v in df["eta_glob"]]
    fg = go.Figure()
    fg.add_hrect(y0=0, y1=seuil_eta_glob*100, fillcolor="rgba(230,57,70,0.05)", line_width=0)
    fg.add_hrect(y0=seuil_eta_glob*100, y1=eta_glob_nom*100,
                 fillcolor="rgba(255,210,0,0.03)", line_width=0)
    fg.add_trace(go.Scatter(x=df["mois"], y=df["eta_glob"]*100,
                            mode="lines+markers", line=dict(color="#0077b6",width=2.5),
                            marker=dict(size=11,color=mc,line=dict(color="#0077b6",width=1.5)),
                            hovertemplate="<b>%{x}</b><br>η_global = %{y:.2f}%<extra></extra>"))
    fg.add_hline(y=eta_glob_nom*100, line_dash="dash", line_color="#ffd200",
                 annotation_text=f"Nominal {eta_glob_nom*100:.1f}%",
                 annotation_font_color="#ffd200", annotation_position="right")
    fg.add_hline(y=seuil_eta_glob*100, line_dash="dot", line_color="#e63946",
                 annotation_text=f"Alerte {seuil_eta_glob*100:.0f}%",
                 annotation_font_color="#e63946", annotation_position="right")
    fg.update_layout(template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                     yaxis_title="η_global (%)", xaxis_title="",
                     height=320, margin=dict(l=50,r=110,t=20,b=40), showlegend=False)
    st.plotly_chart(fg, use_container_width=True)

    # RENDEMENTS PARTIELS + COP
    st.markdown('<div class="sec-hdr">Rendements partiels & COP mensuel</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        f2 = go.Figure()
        for c_, n_, col_ in [("eta_e", eta_e_nom, "#00b4d8"),
                              ("eta_th", eta_th_nom, "#f7971e"),
                              ("eta_frig", eta_frig_nom, "#a0e878")]:
            f2.add_trace(go.Scatter(x=df["mois"], y=df[c_]*100,
                                    mode="lines+markers",
                                    name=c_.replace("eta_","η_"),
                                    line=dict(color=col_,width=2),
                                    hovertemplate=f"<b>%{{x}}</b><br>{c_} = %{{y:.2f}}%<extra></extra>"))
            f2.add_hline(y=n_*100, line_dash="dash", line_color=col_, opacity=0.5,
                         annotation_text=f"nom {n_*100:.0f}%",
                         annotation_font_color=col_, annotation_font_size=10,
                         annotation_position="right")
        f2.update_layout(title="Rendements partiels (%)", template="plotly_dark",
                         paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                         height=300, margin=dict(l=50,r=80,t=40,b=40),
                         legend=dict(bgcolor="#0b1929",font_size=12))
        st.plotly_chart(f2, use_container_width=True)

    with cb:
        cop_col = []
        for v in df["COP"]:
            if pd.isna(v) or v == 0: cop_col.append("#e63946")
            elif v < seuil_cop:      cop_col.append("#e63946")
            elif v < cop_nom:        cop_col.append("#ffd200")
            else:                    cop_col.append("#2dc653")
        f3 = go.Figure()
        f3.add_trace(go.Bar(x=df["mois"], y=df["COP"].fillna(0),
                            marker_color=cop_col, name="COP mesuré",
                            hovertemplate="<b>%{x}</b><br>COP = %{y:.3f}<extra></extra>"))
        f3.add_hline(y=cop_nom, line_dash="dash", line_color="#ffd200",
                     annotation_text=f"Nominal {cop_nom:.2f}",
                     annotation_font_color="#ffd200", annotation_position="right")
        f3.add_hline(y=seuil_cop, line_dash="dot", line_color="#e63946",
                     annotation_text=f"Seuil {seuil_cop:.2f}",
                     annotation_font_color="#e63946", annotation_position="right")
        # Annotation arrêt janvier
        for i, row in df.iterrows():
            if (pd.isna(row["COP"]) or row["COP"] == 0) and row["cause_cop"]:
                f3.add_annotation(x=row["mois"], y=0.05, text="ARRET",
                                  showarrow=False, font=dict(color="#e63946",size=10),
                                  bgcolor="rgba(230,57,70,0.12)", borderpad=3)
        f3.update_layout(title="COP machine à absorption", template="plotly_dark",
                         paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                         height=300, margin=dict(l=50,r=80,t=40,b=40), showlegend=False)
        st.plotly_chart(f3, use_container_width=True)

    # RADAR dernier mois
    st.markdown('<div class="sec-hdr">Profil du dernier mois vs nominal</div>', unsafe_allow_html=True)
    last = df.iloc[-1]
    cop_l = float(last["COP"]) if pd.notna(last["COP"]) else 0.0
    cats = ["η_e","η_th","η_frig","COP","η_global"]
    vact = [last["eta_e"], last["eta_th"], last["eta_frig"], cop_l, last["eta_glob"]]
    vnom = [eta_e_nom, eta_th_nom, eta_frig_nom, cop_nom, eta_glob_nom]
    fr = go.Figure()
    fr.add_trace(go.Scatterpolar(r=vact, theta=cats, fill="toself",
                                 name=last["mois"], line_color="#0077b6",
                                 fillcolor="rgba(0,119,182,0.2)"))
    fr.add_trace(go.Scatterpolar(r=vnom, theta=cats, fill="toself",
                                 name="Nominal", line_color="#ffd200",
                                 line_dash="dash", fillcolor="rgba(255,210,0,0.08)"))
    rmax = max(max(vact), max(vnom)) * 1.15
    fr.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,rmax],
                                  gridcolor="#1b3352", tickfont_color="#4d7fa8"),
                   angularaxis=dict(gridcolor="#1b3352"), bgcolor="#0b1929"),
        paper_bgcolor="#070e1a",
        legend=dict(bgcolor="#0b1929",font_size=12),
        height=330, margin=dict(l=50,r=50,t=30,b=30)
    )
    st.plotly_chart(fr, use_container_width=True)

    # TABLEAU SYNTHÈSE
    st.markdown('<div class="sec-hdr">Tableau de synthèse mensuel</div>', unsafe_allow_html=True)
    td = df[["mois","h_service","gaz","prod_nette","chaleur","froid",
             "COP","eta_e","eta_th","eta_frig","eta_glob","cause_cop"]].copy()
    td.columns = ["Mois","H service (h)","Gaz (Nm³)","Élec nette (kWh)",
                  "Chaleur (kWh)","Froid (kWh)","COP",
                  "η_e","η_th","η_frig","η_global","Remarque"]
    for c_ in ["η_e","η_th","η_frig","η_global"]:
        td[c_] = td[c_].map(lambda x: f"{x:.2%}")
    td["COP"] = td["COP"].apply(lambda x: f"{float(x):.3f}" if pd.notna(x) and float(x)>0 else "ARRÊT")
    st.dataframe(td, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — FLUX ÉNERGÉTIQUE
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-hdr">Bilan des flux énergétiques cumulés</div>', unsafe_allow_html=True)

    vg  = total_pgaz
    ve  = total_elec
    vth = total_chaleur
    vfr = total_froid
    vlr = vg * taux_pertes
    vls = max(0, vg - ve - vth - vfr - vlr)

    # Sankey : 0=Gaz 1=Moteur 2=Élec 3=Chaleur 4=Froid 5=Pertes_réseau 6=Pertes_sys
    fsk = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=24, thickness=22,
            line=dict(color="#1b3352", width=1),
            label=["Gaz Naturel (PCI)","Moteur à Gaz",
                   "Électricité nette","Chaleur récupérée",
                   "Froid (absorption)","Pertes réseau","Pertes système"],
            color=["#0077b6","#023e8a","#00b4d8","#f7971e",
                   "#a0e878","#e63946","#cc2936"]
        ),
        link=dict(
            source=[0,1,1,1,1,1],
            target=[1,2,3,4,5,6],
            value=[vg,ve,vth,vfr,vlr,vls],
            color=["rgba(0,119,182,0.35)","rgba(0,180,216,0.35)",
                   "rgba(247,151,30,0.35)","rgba(160,232,120,0.35)",
                   "rgba(230,57,70,0.2)","rgba(204,41,54,0.15)"]
        )
    ))
    fsk.update_layout(template="plotly_dark", paper_bgcolor="#070e1a",
                      height=430, margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(fsk, use_container_width=True)

    st.markdown('<div class="sec-hdr">Tableau bilan par flux</div>', unsafe_allow_html=True)
    bilan = pd.DataFrame({
        "Flux": ["Gaz naturel (P_gaz PCI)", "▸ Électricité nette",
                 "▸ Chaleur récupérée", "▸ Froid (absorption)",
                 "▸ Pertes réseau", "▸ Pertes système"],
        "Énergie (kWh)": [round(x) for x in [vg,ve,vth,vfr,vlr,vls]],
        "Énergie (MWh)": [f"{x/1000:.1f}" for x in [vg,ve,vth,vfr,vlr,vls]],
        "% du gaz PCI":  [f"{x/vg*100:.1f}%" if vg>0 else "—"
                          for x in [vg,ve,vth,vfr,vlr,vls]],
    })
    st.dataframe(bilan, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-hdr">Répartition & décomposition mensuelle</div>', unsafe_allow_html=True)
    cd1, cd2 = st.columns(2)
    with cd1:
        fp = px.pie(
            names=["Électricité","Chaleur","Froid","Pertes"],
            values=[ve, vth, vfr, vlr+vls],
            color_discrete_sequence=["#00b4d8","#f7971e","#a0e878","#e63946"],
            hole=0.55
        )
        fp.update_traces(textposition="outside", textinfo="label+percent",
                         hovertemplate="<b>%{label}</b><br>%{value:,.0f} kWh<extra></extra>")
        fp.update_layout(template="plotly_dark", paper_bgcolor="#070e1a",
                         height=300, margin=dict(l=20,r=20,t=20,b=20), showlegend=False)
        st.plotly_chart(fp, use_container_width=True)
    with cd2:
        fst = go.Figure()
        fst.add_trace(go.Bar(x=df["mois"],y=df["prod_nette"]/1000,name="Élec",   marker_color="#00b4d8"))
        fst.add_trace(go.Bar(x=df["mois"],y=df["chaleur"]/1000,   name="Chaleur",marker_color="#f7971e"))
        fst.add_trace(go.Bar(x=df["mois"],y=df["froid"]/1000,     name="Froid",  marker_color="#a0e878"))
        fst.add_trace(go.Bar(x=df["mois"],y=df["pertes_sys"]/1000,name="Pertes", marker_color="#e63946",opacity=0.6))
        fst.update_layout(barmode="stack", title="Décomposition mensuelle (MWh)",
                          template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                          height=300, margin=dict(l=50,r=20,t=40,b=40),
                          legend=dict(bgcolor="#0b1929"))
        st.plotly_chart(fst, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — ALERTES
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-hdr">Système d\'alertes intelligentes</div>', unsafe_allow_html=True)

    df_al = detecter_alertes(df)
    nb_r  = (df_al["Statut"] == "🔴 ALERTE").sum()
    nb_y  = (df_al["Statut"] == "🟡 SURVEILLANCE").sum()

    if df_al.empty:
        st.success("✅ Aucune alerte sur la période sélectionnée.")
    else:
        cc1, cc2, cc3 = st.columns(3)
        cc1.error(f"🔴  {nb_r} alertes critiques")
        cc2.warning(f"🟡  {nb_y} surveillances")
        cc3.info(f"📋  {len(df_al)} événements total")
        st.markdown("<br>", unsafe_allow_html=True)
        for _, row in df_al.iterrows():
            cls = "arow-red" if "ALERTE" in row["Statut"] else "arow-yel"
            st.markdown(f"""
            <div class="{cls}">
              <strong>{row['Mois']}</strong> &nbsp;|&nbsp; {row['Statut']}
              &nbsp;|&nbsp; <strong>{row['KPI']}</strong> = {row['Valeur']}
              &nbsp;(seuil : {row['Seuil']}, nominal : {row['Nominal']}, écart : {row['Écart nominal']})
              <br><span style="color:#90c2e7;font-size:12px;">
                &#128204; <em>Cause :</em> {row['Cause']}
              </span><br>
              <span style="color:#778da9;font-size:12px;">
                &#128295; <em>Action :</em> {row['Action']}
              </span>
            </div>""", unsafe_allow_html=True)

    if not df_al.empty:
        st.markdown('<div class="sec-hdr">Timeline alertes</div>', unsafe_allow_html=True)
        cnt = df_al.groupby("Mois").size().reset_index(name="Nb alertes")
        fat = px.bar(cnt, x="Mois", y="Nb alertes", color="Nb alertes", text="Nb alertes",
                     color_continuous_scale=[[0,"#ffd200"],[0.5,"#f7971e"],[1,"#e63946"]])
        fat.update_traces(textposition="outside")
        fat.update_layout(template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                          height=260, showlegend=False, margin=dict(l=40,r=20,t=20,b=40))
        st.plotly_chart(fat, use_container_width=True)
        st.markdown('<div class="sec-hdr">Tableau des alertes</div>', unsafe_allow_html=True)
        st.dataframe(df_al, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ANALYSE ÉCONOMIQUE
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-hdr">Bilan économique de la période</div>', unsafe_allow_html=True)

    ec1, ec2, ec3, ec4 = st.columns(4)
    ec1.markdown(f"""<div class="kpi-card alert">
      <div class="kpi-label">Coût gaz total</div>
      <div class="kpi-value">{total_cout_gaz:,.0f} <span class="kpi-unit">DT</span></div>
      <div class="kpi-delta delta-neu">{total_gaz_nm3:,.0f} Nm³</div>
    </div>""", unsafe_allow_html=True)
    ec2.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Valeur élec produite</div>
      <div class="kpi-value">{total_val_elec:,.0f} <span class="kpi-unit">DT</span></div>
      <div class="kpi-delta delta-neu">{total_elec/1000:.0f} MWh × {prix_kwh_steg:.3f} DT/kWh</div>
    </div>""", unsafe_allow_html=True)
    ec3.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Valeur chaleur + froid</div>
      <div class="kpi-value">{total_val_chaud+total_val_froid:,.0f} <span class="kpi-unit">DT</span></div>
      <div class="kpi-delta delta-neu">Énergie évitée chaudières + GEG</div>
    </div>""", unsafe_allow_html=True)
    cls_g = "" if total_gain >= 0 else "alert"
    ec4.markdown(f"""<div class="kpi-card {cls_g}">
      <div class="kpi-label">Gain global net</div>
      <div class="kpi-value">{total_gain:+,.0f} <span class="kpi-unit">DT</span></div>
      <div class="kpi-delta {'delta-pos' if total_gain>=0 else 'delta-neg'}">
        Élec + Chaleur + Froid − Gaz
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;margin:4px 0 18px;padding:8px 12px;
                background:#0b1929;border-radius:6px;border:1px solid #162030;">
      <strong>Méthode de valorisation :</strong>
      Valeur électricité = production nette × tarif STEG régime uniforme (achat).
      Valeur chaleur = équivalent coût gaz économisé sur chaudières (η_chaud = 90%).
      Valeur froid = équivalent électricité économisée sur GEG (COP_GEG = 3.1).
      Gain net = somme des valeurs − coût du gaz consommé (hors O&amp;M et amortissement).
    </div>""", unsafe_allow_html=True)

    # Graphique mensuel
    st.markdown('<div class="sec-hdr">Évolution mensuelle des flux financiers</div>', unsafe_allow_html=True)
    fe = go.Figure()
    fe.add_trace(go.Bar(x=df["mois"],y=df["cout_gaz_dt"],
                        name="Coût gaz (DT)",marker_color="#e63946",opacity=0.85))
    fe.add_trace(go.Bar(x=df["mois"],y=df["val_elec_dt"],
                        name="Valeur élec (DT)",marker_color="#00b4d8",opacity=0.85))
    fe.add_trace(go.Bar(x=df["mois"],y=df["val_chaleur_dt"]+df["val_froid_dt"],
                        name="Valeur ch+fr (DT)",marker_color="#f7971e",opacity=0.85))
    fe.add_trace(go.Scatter(x=df["mois"],y=df["gain_global_dt"],
                            mode="lines+markers",name="Gain global (DT)",
                            line=dict(color="#2dc653",width=2.5),marker=dict(size=9)))
    fe.add_hline(y=0, line_color="#555", line_dash="dot")
    fe.update_layout(barmode="group", template="plotly_dark",
                     paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                     height=340, margin=dict(l=50,r=20,t=20,b=40),
                     legend=dict(bgcolor="#0b1929",font_size=12))
    st.plotly_chart(fe, use_container_width=True)

    # Heatmap KPI
    st.markdown('<div class="sec-hdr">Carte thermique des indicateurs de performance</div>',
                unsafe_allow_html=True)
    hd = df[["mois","eta_e","eta_th","eta_frig","eta_glob","COP"]].set_index("mois")
    hd.columns = ["η_e","η_th","η_frig","η_global","COP"]
    fh = px.imshow(hd.T.astype(float), color_continuous_scale="RdYlGn",
                   aspect="auto", zmin=0, zmax=1, text_auto=".2f",
                   labels=dict(x="Mois",y="Indicateur",color="Valeur"))
    fh.update_layout(template="plotly_dark", paper_bgcolor="#070e1a",
                     height=280, margin=dict(l=80,r=20,t=20,b=40))
    st.plotly_chart(fh, use_container_width=True)

    # Efficacité horaire
    st.markdown('<div class="sec-hdr">Production horaire (kWh/h de service)</div>',
                unsafe_allow_html=True)
    fhr = go.Figure()
    fhr.add_trace(go.Scatter(x=df["mois"],y=df["elec_h"],mode="lines+markers",
                             name="Élec (kWh/h)",line_color="#00b4d8"))
    fhr.add_trace(go.Scatter(x=df["mois"],y=df["chaleur_h"],mode="lines+markers",
                             name="Chaleur (kWh/h)",line_color="#f7971e"))
    fhr.add_trace(go.Scatter(x=df["mois"],y=df["froid_h"],mode="lines+markers",
                             name="Froid (kWh/h)",line_color="#a0e878"))
    fhr.add_hline(y=1200, line_dash="dash", line_color="#00b4d8",
                  annotation_text="P_nom élec 1200 kW",
                  annotation_font_color="#00b4d8", annotation_font_size=10,
                  annotation_position="right")
    fhr.update_layout(template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                      height=300, margin=dict(l=50,r=110,t=20,b=40),
                      legend=dict(bgcolor="#0b1929"))
    st.plotly_chart(fhr, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — RAPPORT TECHNIQUE & EXPORT
# ─────────────────────────────────────────────────────────────────────────────
with tab5:

    tg  = perf_tag(eta_glob_moy, seuil_eta_glob, eta_glob_nom)
    te  = perf_tag(eta_e_moy,    seuil_eta_e,    eta_e_nom)
    tth = perf_tag(eta_th_moy,   seuil_eta_th,   eta_th_nom)
    tc  = perf_tag(cop_moy if not np.isnan(cop_moy) else 0, seuil_cop, cop_nom)

    df_al5   = detecter_alertes(df)
    nb_al    = len(df_al5)
    nb_ok    = nb_mois - df_al5["Mois"].nunique()
    jan_flag = any(df["mois"].str.strip().str.lower().str.startswith("jan"))

    # Estimation froid perdu en janvier
    jan_rows = df[df["mois"].str.strip().str.lower().str.startswith("jan")]
    froid_perdu_jan = 0
    if not jan_rows.empty:
        chaleur_jan = jan_rows["chaleur"].values[0]
        froid_perdu_jan = chaleur_jan * cop_nom

    # ── A. SYNTHÈSE GÉNÉRALE ────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">A — Synthèse générale</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rbox">
      <p>
        <strong>Centrale :</strong> Trigénération ADWYA &mdash; Moteur CAT/CG 170-12,
        P_élec = 1 200 kW &middot; Récupération thermique = 1 270 kW &middot;
        Absorption THERMAX TAC L5 E1 = 802 kW_frig<br>
        <strong>Période :</strong> {periode_t} ({nb_mois} mois analysés)
      </p>
      <h4>Performance énergétique globale</h4>
      <p>
        η_global moyen : <strong>{eta_glob_moy*100:.1f}%</strong> {tg}
        &nbsp;&mdash;&nbsp; Nominal : {eta_glob_nom*100:.1f}%
        &nbsp;&mdash;&nbsp; Écart : {(eta_glob_moy-eta_glob_nom)*100:+.1f} pts<br>
        η_électrique moyen : <strong>{eta_e_moy*100:.1f}%</strong> {te}
        &nbsp;&mdash;&nbsp; Nominal : {eta_e_nom*100:.0f}%<br>
        η_thermique moyen : <strong>{eta_th_moy*100:.1f}%</strong> {tth}
        &nbsp;&mdash;&nbsp; Nominal : {eta_th_nom*100:.0f}%<br>
        η_frigorifique moyen : <strong>{eta_frig_moy*100:.1f}%</strong>
        &nbsp;&mdash;&nbsp; Nominal : {eta_frig_nom*100:.1f}%<br>
        COP absorption moyen : <strong>{f"{cop_moy:.3f}" if not np.isnan(cop_moy) else "N/A"}</strong>
        {tc} &nbsp;&mdash;&nbsp; Nominal : {cop_nom:.2f}
      </p>
      <h4>Énergie produite et récupérée</h4>
      <p>
        Électricité nette : <strong>{total_elec/1e6:.3f} GWh</strong><br>
        Chaleur récupérée : <strong>{total_chaleur/1e6:.3f} GWh</strong><br>
        Froid récupéré : <strong>{total_froid/1e6:.3f} GWh</strong><br>
        Énergie utile totale : <strong>{(total_elec+total_chaleur+total_froid)/1e6:.3f} GWh</strong><br>
        Gaz consommé : <strong>{total_gaz_nm3:,.0f} Nm³</strong>
        ({total_pgaz/1e6:.3f} GWh_PCI)
      </p>
      <h4>Mois remarquables</h4>
      <p>
        Meilleur mois (η_global) : <strong>{best_m}</strong>
        = {df.loc[df['eta_glob'].idxmax(),'eta_glob']*100:.1f}%<br>
        Mois le plus dégradé : <strong>{worst_m}</strong>
        = {df.loc[df['eta_glob'].idxmin(),'eta_glob']*100:.1f}%
        {f'<br><span class="tag-alert">Janvier 2025 : machine absorption hors service.</span> Froid perdu estimé : {froid_perdu_jan/1000:.0f} MWh.' if jan_flag else ""}
      </p>
      <h4>Bilan économique estimé</h4>
      <p>
        Coût gaz : <strong>{total_cout_gaz:,.0f} DT</strong><br>
        Valeur électricité produite : <strong>{total_val_elec:,.0f} DT</strong><br>
        Valeur chaleur évitée : <strong>{total_val_chaud:,.0f} DT</strong><br>
        Valeur froid évité : <strong>{total_val_froid:,.0f} DT</strong><br>
        <strong>Gain global net : {total_gain:+,.0f} DT</strong>
        {'<span class="tag-ok">POSITIF</span>' if total_gain>=0 else '<span class="tag-alert">NEGATIF</span>'}
      </p>
      <h4>Alertes</h4>
      <p>
        {nb_al} événements détectés ({nb_ok} mois sans alerte sur {nb_mois}).
        {'<span class="tag-alert">Interventions requises.</span>' if nb_al>0
         else '<span class="tag-ok">Aucune alerte.</span>'}
      </p>
    </div>""", unsafe_allow_html=True)

    # ── B. OBSERVATIONS & DIAGNOSTIC ────────────────────────────────────
    st.markdown('<div class="sec-hdr">B — Observations & diagnostic technique</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rbox">
      <h4>1. Rendement électrique (η_e)</h4>
      <p>
        Le η_e moyen de <strong>{eta_e_moy*100:.1f}%</strong>
        {'est proche du nominal' if abs(eta_e_moy-eta_e_nom)<0.03
         else 'est inférieur au nominal de '+str(round((eta_e_nom-eta_e_moy)*100,1))+' pts'}
        ({eta_e_nom*100:.0f}%). La variabilité mensuelle
        ({df['eta_e'].min()*100:.1f}% – {df['eta_e'].max()*100:.1f}%)
        reflète la qualité de la combustion et l'état mécanique du moteur.
        Un entretien périodique (bougies, filtres, injections gaz) permet de se rapprocher
        du nominal. L'analyse des gaz d'échappement (CO, NOx, O₂) est recommandée.
      </p>
      <h4>2. Récupération thermique (η_th)</h4>
      <p>
        Le η_th moyen de <strong>{eta_th_moy*100:.1f}%</strong>
        (plage : {df['eta_th'].min()*100:.1f}% – {df['eta_th'].max()*100:.1f}%)
        indique une récupération thermique fonctionnelle mais variable.
        Les fluctuations s'expliquent par l'état des vannes 3 voies (V3V) dont
        la majorité est by-passée ou défaillante selon l'audit ADWYA 2025.
        L'encrassement des échangeurs à plaques (côté eau chaude moteur) et
        la non-récupération pour la zone Béta sont des axes d'amélioration identifiés.
      </p>
      <h4>3. Machine à absorption — COP et disponibilité</h4>
      <p>
        <strong>Disponibilité :</strong> la machine a été hors service en janvier 2025
        (COP = 0, froid = 0 kWh), représentant une perte estimée de
        <strong>{froid_perdu_jan/1000:.0f} MWh</strong> de froid non produit sur ce mois.<br>
        <strong>COP moyen opérationnel :</strong>
        {f"{cop_moy:.3f}" if not np.isnan(cop_moy) else "N/A"} vs nominal {cop_nom:.2f}.
        Le COP d'août 2024 (0.118) est anormalement bas : la température élevée
        de l'eau de tour en été (>35°C) dégrade fortement les performances de l'absorption.
        La pompe eau de tour a un débit réel de ~150 m³/h vs 230 m³/h nominal
        (sous-dimensionnement confirmé par l'audit).<br>
        <strong>Recommandation clé :</strong> redimensionner la pompe eau de tour
        et maintenir T_tour &lt; 32°C en été pour garantir COP &gt; 0.65.
      </p>
      <h4>4. Disponibilité horaire</h4>
      <p>
        Les heures de service varient de {df['h_service'].min()}h à {df['h_service'].max()}h/mois
        (référence : 730h pour un fonctionnement continu 3×8).
        Les mois &lt; 600h signalent des arrêts non planifiés ou des maintenances
        à optimiser (planification préventive recommandée pendant les congés annuels).
      </p>
      <h4>5. Pertes système</h4>
      <p>
        Les pertes estimées représentent
        <strong>{df['pertes_sys'].sum()/total_pgaz*100:.1f}%</strong> du gaz PCI,
        valeur normale pour ce type d'installation (15–25%).
        Une valeur excessive pourrait indiquer des fuites sur les canalisations
        d'eau chaude non calorifugées (identifiées dans l'audit, notamment en zone Béta).
      </p>
    </div>""", unsafe_allow_html=True)

    # ── C. CONCLUSIONS ───────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">C — Conclusions</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rbox">
      <p>La centrale trigénération ADWYA constitue un investissement stratégique
      qui a permis une réduction significative de la dépendance au réseau STEG
      et une meilleure valorisation du gaz naturel. Sur la période {periode_t} :</p>
      <ol style="line-height:2.2;">
        <li>Le η_global moyen de <strong>{eta_glob_moy*100:.1f}%</strong>
          {'atteint le niveau nominal' if eta_glob_moy>=eta_glob_nom
           else 'reste inférieur de '+str(round((eta_glob_nom-eta_glob_moy)*100,1))+' pts au nominal'},
          principalement pénalisé par les défaillances de la machine à absorption.</li>
        <li>La <strong>machine à absorption est le maillon critique</strong> :
          sa panne en janvier 2025 et ses performances dégradées en été (COP ~0.118 en août)
          représentent la principale source de pertes d'efficacité de la centrale.</li>
        <li>La récupération thermique est satisfaisante (η_th ~ {eta_th_moy*100:.1f}%)
          mais sous-exploitée en zone Béta (aucune récupération prévue).</li>
        <li>Le bilan économique est <strong>{'positif' if total_gain>=0 else 'négatif'}
          ({total_gain:+,.0f} DT)</strong> sur la période, confirmant la rentabilité
          de l'installation malgré les incidents.</li>
        <li>Des actions correctives ciblées (plan D ci-dessous) permettraient d'atteindre
          η_global > {eta_glob_nom*100:.0f}% et d'améliorer le gain annuel de 15 à 30%.</li>
      </ol>
    </div>""", unsafe_allow_html=True)

    # ── D. PLAN D'ACTIONS ────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">D — Plan d\'actions & recommandations</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="rbox">
      <h4>&#128295; Actions immédiates — Priorité critique</h4>
      <ol style="line-height:2.2;">
        <li>
          <strong>Fiabilisation machine à absorption</strong><br>
          Contrat de maintenance préventive trimestrielle :
          contrôle niveau/concentration LiBr, test étanchéité, vérification
          T° générateur (80–100°C) / absorbeur / condenseur,
          nettoyage tubes eau de tour. Objectif : disponibilité &gt; 95%, COP &gt; 0.70.
        </li>
        <li>
          <strong>Redimensionnement pompe eau de tour</strong><br>
          Débit réel mesuré ≈ 150 m³/h vs 230 m³/h nominal.
          Remplacer la pompe ou installer une pompe booster en série.
          Installer des manomètres amont/aval pour suivi en temps réel.
          Impact estimé : +20% sur COP absorption.
        </li>
        <li>
          <strong>Réhabilitation des vannes 3 voies (V3V)</strong><br>
          Remplacer les V3V by-passées sur les CTA des zones Alpha et Béta.
          Activer la régulation automatique. Impact : réduction consommation GEG
          et amélioration qualité conditionnement d'air.
        </li>
      </ol>
      <h4>&#128200; Améliorations court terme (1–6 mois)</h4>
      <ol style="line-height:2.2;" start="4">
        <li>
          <strong>Comptabilité énergétique complète</strong><br>
          Connecter au monitoring : compteurs vapeur, GN par chaudière,
          débitmètres eau glacée et un calorimètre dédié absorbeur
          (mesure COP en temps réel). Économie estimée : 62 830 DT/an. TRB : 2.3–4.6 ans.
        </li>
        <li>
          <strong>Optimisation consigne eau glacée</strong><br>
          Augmenter la consigne de 6°C à 7–8°C en hiver (gain ~3%/°C sur GEG).
          Automatiser la variation saisonnière.
        </li>
        <li>
          <strong>Réduction pression air comprimé</strong><br>
          Passer de 7.5 bar à 7.0 bar après réhabilitation réseau Béta.
          Gain : ~5% consommation air comprimé ≈ 36 990 kWh/an.
        </li>
        <li>
          <strong>Révision puissance souscrite STEG</strong><br>
          Réduire de 1 300 kVA à 1 000 kVA.
          Économie redevance : ~14 200 DT/an. Sans investissement.
        </li>
        <li>
          <strong>Réhabilitation batteries de condensateurs</strong><br>
          TR1 hors service, TR2 et TR3 dégradées. Ajouter 400 kVAr.
          Objectif cos φ = 1 sans solliciter l'alternateur.
          Économie : ~89 464 DT/an. TRB : 0.2 an.
        </li>
      </ol>
      <h4>&#128640; Améliorations moyen terme (6–18 mois)</h4>
      <ol style="line-height:2.2;" start="9">
        <li>
          <strong>Extension récupération vers zone Béta</strong><br>
          Installer un 4ème échangeur à plaques + 2 pompes secondaires.
          Éliminer la dépendance à la chaudière eau chaude Béta pendant
          le fonctionnement de la trigénération.
        </li>
        <li>
          <strong>Remplacement CTA vétustes — Zone Alpha</strong><br>
          Regrouper 6 CTA en 3 nouvelles unités : double flux, roue libre,
          free-cooling, variateurs de vitesse. Économie : 87 305 DT/an. TRB : 5.5–6.9 ans.
        </li>
        <li>
          <strong>ISO 50001 — Système de management de l'énergie</strong><br>
          Formaliser IPE, procédures, revues de direction énergie.
          Gain comportemental estimé : ~2% consommation globale.
          TRB : 0.9–2.9 ans.
        </li>
      </ol>
      <h4>&#128202; Tableau récapitulatif des gains potentiels</h4>
      <table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:8px;">
        <tr style="background:#0d2a40;color:#90c2e7;text-align:left;">
          <th style="padding:8px 10px;">Action</th>
          <th style="padding:8px 10px;">Priorité</th>
          <th style="padding:8px 10px;">Économie estimée</th>
          <th style="padding:8px 10px;">Investissement</th>
          <th style="padding:8px 10px;">TRB</th>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Fiabilisation absorption + pompe tour</td>
          <td style="padding:7px 10px;color:#e63946;font-weight:600;">CRITIQUE</td>
          <td style="padding:7px 10px;">&gt;200 MWh froid/an récupéré</td>
          <td style="padding:7px 10px;">Maintenance</td>
          <td style="padding:7px 10px;">&lt; 1 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Batteries condensateurs</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">URGENT</td>
          <td style="padding:7px 10px;">89 464 DT/an</td>
          <td style="padding:7px 10px;">23 000 DT</td>
          <td style="padding:7px 10px;">0.2 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Comptabilité énergétique étendue</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">62 830 DT/an</td>
          <td style="padding:7px 10px;">290 000 DT</td>
          <td style="padding:7px 10px;">2.3–4.6 ans</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Optimisation eau glacée + GEG</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">51 429 DT/an</td>
          <td style="padding:7px 10px;">230 000 DT</td>
          <td style="padding:7px 10px;">3.3–4.5 ans</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Puissance souscrite (Pss 1000 kVA)</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">14 200 DT/an</td>
          <td style="padding:7px 10px;">0 DT</td>
          <td style="padding:7px 10px;">Immédiat</td>
        </tr>
        <tr style="background:#0b1929;">
          <td style="padding:7px 10px;">Remplacement CTA Zone Alpha</td>
          <td style="padding:7px 10px;color:#90c2e7;font-weight:600;">MOYEN TERME</td>
          <td style="padding:7px 10px;">87 305 DT/an</td>
          <td style="padding:7px 10px;">600 000 DT</td>
          <td style="padding:7px 10px;">5.5–6.9 ans</td>
        </tr>
      </table>
    </div>""", unsafe_allow_html=True)

    # ── E. EXPORT ────────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">E — Export des données</div>', unsafe_allow_html=True)

    df_exp = df[["mois","h_service","gaz","prod_nette","chaleur","froid","COP",
                 "eta_e","eta_th","eta_frig","eta_glob",
                 "cout_gaz_dt","val_elec_dt","val_chaleur_dt",
                 "val_froid_dt","gain_global_dt","cause_cop"]].copy()
    df_exp.columns = [
        "Mois","H service (h)","Gaz (Nm³)","Élec nette (kWh)",
        "Chaleur (kWh)","Froid (kWh)","COP",
        "η_e","η_th","η_frig","η_global",
        "Coût gaz (DT)","Valeur élec (DT)","Valeur chaleur (DT)",
        "Valeur froid (DT)","Gain global (DT)","Remarque"
    ]

    ce1, ce2 = st.columns(2)
    with ce1:
        csv_b = df_exp.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button("📥 Télécharger CSV", csv_b,
                           "kpi_trigeneration_adwya.csv", mime="text/csv")
    with ce2:
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_exp.to_excel(w, sheet_name="KPI Mensuels", index=False)
            bilan.to_excel(w, sheet_name="Bilan Flux", index=False)
            if not df_al5.empty:
                df_al5.to_excel(w, sheet_name="Alertes", index=False)
            eco = df[["mois","cout_gaz_dt","val_elec_dt","val_chaleur_dt",
                       "val_froid_dt","gain_global_dt"]].copy()
            eco.columns = ["Mois","Coût gaz (DT)","Valeur élec (DT)",
                           "Valeur chaleur (DT)","Valeur froid (DT)","Gain global (DT)"]
            eco.to_excel(w, sheet_name="Analyse Économique", index=False)
        buf.seek(0)
        st.download_button("📊 Télécharger Excel (multi-onglets)", buf.read(),
                           "rapport_trigeneration_adwya.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("""
    <div style="font-size:11px;color:#2a4a6a;margin-top:28px;text-align:center;
                padding:10px;border-top:1px solid #162030;">
      Outil de suivi des performances &eacute;nerg&eacute;tiques &mdash;
      Centrale Trig&eacute;n&eacute;ration ADWYA &nbsp;&middot;&nbsp;
      PFE RANIM ZAMMEL 2026 &nbsp;&middot;&nbsp; 
    </div>""", unsafe_allow_html=True)

