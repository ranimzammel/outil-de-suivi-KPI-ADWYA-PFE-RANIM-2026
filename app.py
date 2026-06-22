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
.zone-alpha { border-left: 4px solid #00b4d8; padding-left: 12px; }
.zone-beta  { border-left: 4px solid #f7971e; padding-left: 12px; }
.zone-gamma { border-left: 4px solid #a0e878; padding-left: 12px; }
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
# Taux de pertes canalisations — valeur fixe (3 %, non exposée dans la sidebar)
taux_pertes = 0.03
# =============================================================================
# 3. SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Paramètres système")
    PCI           = st.number_input("PCI gaz naturel (kWh/Nm³)", value=10.55, step=0.01)
    prix_gaz_nm3  = st.number_input("Prix gaz naturel (DT/Nm³)", value=0.575, step=0.001)
    prix_kwh_steg = st.number_input("Prix kWh d'électricité achetée (DT)", value=0.291, step=0.001)


    st.markdown("---")
    st.markdown("### 📐 Valeurs nominales")
    eta_e_nom    = st.number_input("rendement électrique nominal",        value=0.42,  step=0.01)
    eta_th_nom   = st.number_input("rendement thermique nominal",       value=0.30,  step=0.01)
    eta_frig_nom = st.number_input("rendement frigorifique nominal",     value=0.235, step=0.005)
    eta_glob_nom = st.number_input("rendement global nominal",   value=0.765, step=0.005)
    cop_nom      = st.number_input("COP nominal absorption", value=0.78, step=0.01)

    st.markdown("---")
    st.markdown("### 📊 Seuils de dérive mensuelle")
    seuil_derive_moderee  = st.number_input("Écart modéré vs nominal (%)", value=5.0, step=1.0,
        help="Dérive ⚠️ si l'écart au nominal dépasse ce % sur un mois") / 100.0
    seuil_derive_critique = st.number_input("Écart significatif vs nominal (%)", value=15.0, step=1.0,
        help="Dérive ❌ si l'écart au nominal dépasse ce % sur un mois") / 100.0
    nb_mois_tendance = st.number_input("Mois consécutifs pour tendance", value=3, step=1, min_value=2, max_value=6,
        help="Nombre de mois consécutifs en baisse pour détecter une tendance de dégradation")

    # Valeurs compatibilité (utilisées uniquement pour les graphiques — lignes de référence)
    seuil_eta_glob = eta_glob_nom * (1 - seuil_derive_critique)
    seuil_eta_e    = eta_e_nom    * (1 - seuil_derive_critique)
    seuil_eta_th   = eta_th_nom   * (1 - seuil_derive_critique)
    seuil_cop      = cop_nom      * (1 - seuil_derive_critique)

    st.markdown("---")
    st.markdown("### 📂 Import données")
    uploaded_file = st.file_uploader("Fichier Excel (.xlsx)", type=["xlsx"],
        help="Colonnes requises : mois, h_service, prod_nette, gaz, froid, chaleur, COP")

# =============================================================================
# 4. DONNÉES — Dataset complet mai 2024 → mars 2026 (23 mois)
# Source : Suivi_trigénération.xlsx combiné avec données antérieures
# Colonnes : mois | h_service | prod_nette(kWh) | gaz(Nm³) | froid(kWh) | chaleur(kWh) | COP
# =============================================================================
COLONNES = ["mois", "h_service", "prod_nette", "gaz", "froid", "chaleur", "COP"]

#  mois           h_serv  prod_nette    gaz        froid     chaleur     COP
DATA_DEFAUT = [
    # ── Anciennes données (mai 2024 – mai 2025) ─────────────────────────────
    ("Mai  2024",  262,  797_294,  198_116,        0,  476_974,  None ),  # démarrage — pas de froid
    ("Juin 2024",  710,  771_962,  192_530,  175_145,  510_983,  0.399),
    ("Juil 2024",  576,  652_926,  154_636,  182_092,  384_522,  0.573),
    ("Août 2024",  437,  483_421,  114_942,   23_456,  221_970,  0.118),
    ("Sept 2024",  669,  735_425,  179_737,  212_682,  371_949,  0.746),
    ("Oct  2024",  742,  820_477,  197_633,  320_251,  495_215,  0.778),
    ("Nov  2024",  687,  768_932,  186_451,  176_946,  432_365,  0.554),
    ("Déc  2024",  739,  831_777,  198_821,  151_977,  490_387,  0.512),
    ("Jan  2025",  731,  849_815,  196_592,        0,  170_709,  None ),  # panne absorption
    ("Fév  2025",  656,  747_997,  176_950,  112_379,  325_380,  0.539),
    ("Mars 2025",  724,  731_787,  176_210,  169_547,  418_558,  0.551),
    ("Avr  2025",  698,  858_198,  209_513,  204_424,  483_363,  0.567),
    ("Mai  2025",  731,  812_044,  199_061,  217_045,  488_018,  0.607),
    # ── Nouvelles données (juin 2025 – mars 2026) ────────────────────────────
    ("Juin 2025",  668,  728_584,  181_636,  174_776,  431_932,  0.568),
    ("Juil 2025",  585,  621_357,  154_744,   91_827,  253_989,  0.573),
    ("Août 2025",  423,  468_868,  115_157,    4_160,   45_834,  0.506),
    ("Sept 2025",  711,  804_069,  193_717,        0,  137_424,  None ),  # abs. hors service
    ("Oct  2025",  706,  764_207,  192_125,  199_696,  417_421,  0.676),
    ("Nov  2025",  672,  742_398,  182_997,  228_292,  507_470,  0.690),
    ("Déc  2025",  678,  736_383,  182_252,  218_581,  523_373,  0.628),
    ("Jan  2026",  741,  811_989,  199_706,  178_501,  522_157,  0.554),
    ("Fév  2026",  663,  737_835,  178_295,   85_310,  278_336,  0.572),
    ("Mars 2026",  700,  803_107,  189_806,   21_305,   55_615,  0.609),
]

CAUSES_COP = {
    "Mai  2024": (
        "Premier mois de démarrage (mai 2024) : machine à absorption non encore opérationnelle. "
        "COP = 0, froid récupéré = 0 kWh. Mise en service progressive de l'unité."
    ),
    "Jan  2025": (
        "Panne confirmée de la machine à absorption (janvier 2025) : "
        "COP = 0, froid récupéré = 0 kWh. "
        "Cause probable : défaillance mécanique circuit LiBr ou pompe de solution. "
        "Action : inspection complète et remise en service prioritaire."
    ),
    "Sept 2025": (
        "Arrêt de la machine à absorption (septembre 2025) : "
        "COP = 0, froid récupéré = 0 kWh. "
        "Causes à investiguer : maintenance préventive ou défaillance technique. "
        "Action : rapport d'intervention et remise en service."
    ),
    "Août 2024": (
        "COP anormalement bas (0.118) en période estivale. "
        "Causes probables : température eau de tour élevée (>35°C), "
        "encrassement du condenseur côté eau, déséquilibre concentration LiBr. "
        "Action : nettoyage condenseur, contrôle tour de refroidissement, "
        "analyse solution LiBr."
    ),
    "Août 2025": (
        "COP bas (0.506) en période estivale — même phénomène qu'août 2024. "
        "Température eau de tour élevée en été, froid récupéré quasi nul (4 160 kWh). "
        "Action : renforcer le refroidissement tour, augmenter débit eau tour en été."
    ),
    "Mars 2026": (
        "Froid très faible (21 305 kWh) et récupération thermique réduite (55 615 kWh). "
        "Possible réduction des besoins en froid en fin d'hiver ou régulation conservative. "
        "À surveiller : vérifier consignes eau glacée et état de l'absorbeur."
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

for col in ["prod_nette", "gaz", "froid", "chaleur", "h_service"]:
    df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce").fillna(0)
df_raw["COP"] = pd.to_numeric(df_raw["COP"], errors="coerce")

# =============================================================================
# 5. CALCULS KPI
# =============================================================================
df_raw["P_gaz"] = df_raw["gaz"] * PCI

safe = df_raw["P_gaz"].replace(0, np.nan)
df_raw["eta_e"]    = df_raw["prod_nette"] / safe
df_raw["eta_th"]   = df_raw["chaleur"]    / safe
df_raw["eta_frig"] = df_raw["froid"]      / safe
df_raw["eta_glob"] = df_raw["eta_e"] + df_raw["eta_th"] + df_raw["eta_frig"]
for col in ["eta_e","eta_th","eta_frig","eta_glob"]:
    df_raw[col] = df_raw[col].fillna(0)

df_raw["pertes_reseau"] = df_raw["P_gaz"] * taux_pertes
df_raw["pertes_sys"] = (
    df_raw["P_gaz"] - df_raw["prod_nette"]
    - df_raw["chaleur"] - df_raw["froid"]
    - df_raw["pertes_reseau"]
).clip(lower=0)

df_raw["cout_gaz_dt"]    = df_raw["gaz"] * prix_gaz_nm3
df_raw["val_elec_dt"]    = df_raw["prod_nette"] * prix_kwh_steg
df_raw["val_chaleur_dt"] = df_raw["chaleur"] / (0.90 * PCI) * prix_gaz_nm3
df_raw["val_froid_dt"]   = df_raw["froid"] / 3.1 * prix_kwh_steg
df_raw["gain_global_dt"] = (
    df_raw["val_elec_dt"] + df_raw["val_chaleur_dt"]
    + df_raw["val_froid_dt"] - df_raw["cout_gaz_dt"]
)

# =============================================================================
# CALCULS CO₂ ET TEP (coefficients ANME / Tableau 1 & 2 de l'audit)
# STEG électricité  : 0.283 TEP/MWh  × 2.349 tCO₂/TEP
# Gaz naturel       : 0.9 TEP/kNm³   × 2.349 tCO₂/TEP
# Frigorie évitée   : via COP_GEG=3.1 → kWh élec évités → CO₂ évité
# Chaleur évitée    : via η_chaud=0.90 → Nm³ GN évités → CO₂ évité
# =============================================================================
FACTEUR_TEP_ELEC   = 0.283 / 1000      # TEP/kWh
FACTEUR_CO2_ELEC   = 2.349             # tCO₂/TEP
FACTEUR_TEP_GAZ    = 0.9 / 1000        # TEP/Nm³
FACTEUR_CO2_GAZ    = 2.349             # tCO₂/TEP
COP_GEG_REF        = 3.1               # COP groupe froid électrique de référence
ETA_CHAUD_REF      = 0.90              # rendement chaudière de référence

# TEP & CO₂ du gaz consommé
df_raw["tep_gaz"]      = df_raw["gaz"] * FACTEUR_TEP_GAZ
df_raw["co2_gaz"]      = df_raw["tep_gaz"] * FACTEUR_CO2_GAZ

# kWh STEG évités (= élec + froid/COP_GEG + chaleur/η_chaud/PCI → Nm³ →TEP)
df_raw["elec_steg_evite"]    = df_raw["prod_nette"]                     # kWh élec
df_raw["elec_equiv_froid"]   = df_raw["froid"] / COP_GEG_REF            # kWh élec équiv.
df_raw["nm3_equiv_chaleur"]  = df_raw["chaleur"] / (ETA_CHAUD_REF * PCI) # Nm³ GN équiv.

df_raw["tep_evite_elec"]   = df_raw["elec_steg_evite"] * FACTEUR_TEP_ELEC
df_raw["tep_evite_froid"]  = df_raw["elec_equiv_froid"] * FACTEUR_TEP_ELEC
df_raw["tep_evite_chaud"]  = df_raw["nm3_equiv_chaleur"] * FACTEUR_TEP_GAZ
df_raw["tep_evite_total"]  = (df_raw["tep_evite_elec"]
                              + df_raw["tep_evite_froid"]
                              + df_raw["tep_evite_chaud"])
df_raw["tep_net"]          = df_raw["tep_evite_total"] - df_raw["tep_gaz"]

df_raw["co2_evite_elec"]   = df_raw["tep_evite_elec"]  * FACTEUR_CO2_ELEC
df_raw["co2_evite_froid"]  = df_raw["tep_evite_froid"] * FACTEUR_CO2_ELEC
df_raw["co2_evite_chaud"]  = df_raw["tep_evite_chaud"] * FACTEUR_CO2_GAZ
df_raw["co2_evite_total"]  = (df_raw["co2_evite_elec"]
                               + df_raw["co2_evite_froid"]
                               + df_raw["co2_evite_chaud"])
df_raw["co2_net"]          = df_raw["co2_evite_total"] - df_raw["co2_gaz"]

# Score de performance 0–100 (pondéré par les 4 KPI vs nominal)
def _score_perf(row, e_nom, th_nom, frig_nom, cop_nom_):
    scores = []
    if e_nom > 0:
        scores.append(min(1.0, row["eta_e"] / e_nom) * 30)
    if th_nom > 0:
        scores.append(min(1.0, row["eta_th"] / th_nom) * 25)
    if frig_nom > 0:
        scores.append(min(1.0, row["eta_frig"] / frig_nom) * 20)
    cop_v = row["COP"]
    if pd.notna(cop_v) and cop_v > 0 and cop_nom_ > 0:
        scores.append(min(1.0, cop_v / cop_nom_) * 25)
    return sum(scores) if scores else 0.0

df_raw["score_perf"] = df_raw.apply(
    lambda r: _score_perf(r, 0.42, 0.30, 0.235, 0.78), axis=1
)

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

# Agrégats CO₂ & TEP sur la période filtrée
total_tep_gaz       = df["tep_gaz"].sum()
total_co2_gaz       = df["co2_gaz"].sum()
total_tep_evite     = df["tep_evite_total"].sum()
total_co2_evite     = df["co2_evite_total"].sum()
total_tep_net       = df["tep_net"].sum()
total_co2_net       = df["co2_net"].sum()
score_perf_moy      = df["score_perf"].mean()

# =============================================================================
# 8. DÉTECTION DÉRIVE MENSUELLE (remplace les seuils d'alerte temps-réel)
# Logique : comparaison mois M vs nominal + tendance sur N mois consécutifs
# =============================================================================
def _statut_ecart(val, nominal, seuil_mod, seuil_crit):
    """Retourne (statut, classe_css) selon l'écart relatif au nominal."""
    if nominal == 0 or val == 0:
        return "⛔ Arrêt / N.D.", "arow-red"
    ecart = (val - nominal) / nominal   # négatif = dégradation
    if ecart >= -seuil_mod:
        return "✅ Conforme", ""
    elif ecart >= -seuil_crit:
        return "⚠️ Écart modéré", "arow-yel"
    else:
        return "❌ Écart significatif", "arow-red"

def _detecter_tendance(series: pd.Series, n: int) -> bool:
    """Retourne True si les n dernières valeurs sont strictement décroissantes."""
    vals = series.dropna().tolist()
    if len(vals) < n:
        return False
    tail = vals[-n:]
    return all(tail[i] > tail[i+1] for i in range(len(tail)-1))

def detecter_derives_mensuelles(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Pour chaque mois et chaque KPI, calcule :
      - l'écart au nominal
      - le statut (Conforme / Écart modéré / Écart significatif)
      - la variation mois/mois (M vs M-1)
    """
    rows = []
    kpis = [
        ("η_e",      "eta_e",    eta_e_nom,    "Rendement électrique",
         "Vérifier filtres air moteur, qualité gaz, refroidissement moteur."),
        ("η_th",     "eta_th",   eta_th_nom,   "Récupération thermique",
         "Inspecter échangeurs à plaques (encrassement), débits circuits EC."),
        ("η_frig",   "eta_frig", eta_frig_nom, "Récupération frigorifique",
         "Contrôle absorbeur : niveau LiBr, T° eau de tour, débit pompe tour."),
        ("η_global", "eta_glob", eta_glob_nom, "Performance globale",
         "Bilan complet moteur + récupération thermique + absorbeur."),
        ("COP",      "COP",      cop_nom,      "COP machine à absorption",
         "Nettoyage condenseur, analyse solution LiBr, débit eau de tour."),
    ]
    for nom_kpi, col, nominal, label, action in kpis:
        prev_val = None
        for idx, r in dataframe.iterrows():
            val = r[col]
            mois = r["mois"]
            cause = r.get("cause_cop", "")
            # Valeur numérique
            val_num = float(val) if pd.notna(val) and val != 0 else 0.0
            # Écart nominal
            if nominal > 0 and val_num > 0:
                ecart_nom = (val_num - nominal) / nominal
            else:
                ecart_nom = None
            # Variation M vs M-1
            if prev_val is not None and prev_val > 0 and val_num > 0:
                var_mm = (val_num - prev_val) / prev_val
            else:
                var_mm = None
            # Statut
            if val_num == 0 or pd.isna(val):
                statut = "⛔ Arrêt / N.D."
                css    = "arow-red"
            else:
                statut, css = _statut_ecart(val_num, nominal,
                                            seuil_derive_moderee, seuil_derive_critique)
            rows.append({
                "Mois":        mois,
                "KPI":         nom_kpi,
                "Libellé":     label,
                "Valeur":      f"{val_num:.3f}" if "COP" in nom_kpi
                               else (f"{val_num:.1%}" if val_num > 0 else "ARRÊT"),
                "Nominal":     f"{nominal:.2f}" if "COP" in nom_kpi else f"{nominal:.1%}",
                "Écart/Nom":   f"{ecart_nom:+.1%}" if ecart_nom is not None else "N/A",
                "Var. M/M-1":  f"{var_mm:+.1%}" if var_mm is not None else "—",
                "Statut":      statut,
                "_css":        css,
                "Cause":       cause if cause else "—",
                "Action":      action,
            })
            prev_val = val_num if val_num > 0 else None

    return pd.DataFrame(rows)

def detecter_tendances(dataframe: pd.DataFrame) -> list:
    """
    Détecte les tendances de dégradation sur nb_mois_tendance mois consécutifs.
    Retourne une liste de dicts {kpi, nb_mois, message}.
    """
    nb = int(nb_mois_tendance)
    tendances = []
    kpis_tend = [
        ("η_global", "eta_glob", "Rendement global"),
        ("COP",      "COP",      "COP absorption"),
        ("η_e",      "eta_e",    "Rendement électrique"),
        ("η_th",     "eta_th",   "Récupération thermique"),
    ]
    for nom_kpi, col, label in kpis_tend:
        serie = dataframe[col].replace(0, np.nan)
        if _detecter_tendance(serie, nb):
            vals = serie.dropna().tolist()[-nb:]
            tendances.append({
                "kpi":     nom_kpi,
                "label":   label,
                "nb":      nb,
                "vals":    vals,
                "message": (f"**{label}** en baisse continue sur {nb} mois consécutifs "
                            f"({vals[0]:.3f} → {vals[-1]:.3f}). "
                            f"Tendance de dégradation à surveiller."),
            })
    return tendances

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
# 10. DONNÉES PAR ZONE (Audit ADWYA 2025 — Tableaux 43 & 44)
# =============================================================================
ZONE_DATA_ANNUEL = {
    "elec": {
        "CTA":          {"Alpha": 537_093,  "Béta": 223_581,  "Gamma": 182_777},
        "GEG (froid)":  {"Alpha": 755_955,  "Béta": 371_177,  "Gamma": 279_603},
        "Pompes EG":    {"Alpha": 105_558,  "Béta":  96_737,  "Gamma":  99_566},
        "Chaufferies":  {"Alpha":  55_600,  "Béta": 104_244,  "Gamma": 126_065},
        "Production":   {"Alpha": 428_597,  "Béta": 313_246,  "Gamma": 276_314},
    },
    "elec_objectif": {
        "CTA":          {"Alpha": 442_569,  "Béta": 184_351,  "Gamma": 150_729},
        "GEG (froid)":  {"Alpha": 623_162,  "Béta": 306_120,  "Gamma": 230_481},
        "Pompes EG":    {"Alpha":  87_080,  "Béta":  79_764,  "Gamma":  82_082},
        "Chaufferies":  {"Alpha":  45_867,  "Béta":  85_985,  "Gamma": 103_938},
        "Production":   {"Alpha": 353_549,  "Béta": 258_277,  "Gamma": 227_874},
    },
    "gaz_nm3": {
        "Chaudière vapeur":  {"Alpha":  81_325,  "Béta":       0,  "Gamma": 126_014},
        "Chaudière EC":      {"Alpha":      0,   "Béta": 277_860,  "Gamma":       0},
        "Munters":           {"Alpha":      0,   "Béta":  50_000,  "Gamma":       0},
    },
    "gaz_nm3_objectif": {
        "Chaudière vapeur":  {"Alpha":  49_445,  "Béta":       0,  "Gamma":  76_613},
        "Chaudière EC":      {"Alpha":      0,   "Béta": 168_954,  "Gamma":       0},
        "Munters":           {"Alpha":      0,   "Béta":  30_380,  "Gamma":       0},
    },
}

ZONES         = ["Alpha", "Béta", "Gamma"]
COULEURS_ZONE = {"Alpha": "#00b4d8", "Béta": "#f7971e", "Gamma": "#a0e878"}

# =============================================================================
# DONNÉES MENSUELLES RÉELLES — Froid produit & Énergie récupérée par zone
# Source : Suivi_trigénération.xlsx — Feuille Centrale (mai 2024 → mars 2026)
# =============================================================================
# Note : L'énergie récupérée par zone = EC Alpha + EC Alpha Sanitaire + EC Gamma
# La zone Béta n'a pas de récupération thermique directe depuis la trigénération.
# Le froid produit (absorbeur) est global — réparti entre les 3 zones.

MONTHLY_ZONE_DATA = [
    # (mois_label, froid_kWh, ec_chiller_kWh, ec_alpha_kWh, ec_alpha_sani_kWh, ec_gamma_kWh)
    # ── Données mai 2024 – mai 2025 ──────────────────────────────────────────
    ("Mai  2024",       0,  408_288,  41_131,  18_500,   9_055),
    ("Juin 2024",  175_145,  438_844,  47_960,  13_891,  10_287),
    ("Juil 2024",  182_092,  318_003,  38_746,  10_254,  17_520),
    ("Août 2024",   23_456,  198_850,  16_390,   6_730,       0),
    ("Sept 2024",  212_682,  285_259,  41_532,  12_849,  32_309),
    ("Oct  2024",  320_251,  411_872,  35_797,  15_546,  32_000),
    ("Nov  2024",  176_946,  319_286,  59_147,  18_582,  35_350),
    ("Déc  2024",  151_977,  296_938,  85_798,  24_782,  82_870),
    ("Jan  2025",       0,        0,  109_581,  24_154,  36_974),
    ("Fév  2025",  112_379,  208_528,  59_434,  22_631,  34_787),
    ("Mars 2025",  169_547,  307_868,  46_214,  19_274,  45_202),
    ("Avr  2025",  204_424,  360_312,  41_737,  23_544,  57_770),
    ("Mai  2025",  217_045,  357_416,  57_555,  15_609,  57_438),
    # ── Nouvelles données juin 2025 – mars 2026 ──────────────────────────────
    ("Juin 2025",  174_776,  307_540,  41_871,  10_532,  71_989),
    ("Juil 2025",   91_827,  160_289,  42_386,   8_731,  42_583),
    ("Août 2025",    4_160,    8_226,  21_743,     879,  14_986),
    ("Sept 2025",       0,        0,   85_899,  10_790,  40_735),
    ("Oct  2025",  199_696,  295_253,  73_770,  17_789,  30_609),
    ("Nov  2025",  228_292,  330_901,  70_766,  20_539,  85_264),
    ("Déc  2025",  218_581,  347_820,  79_486,  26_883,  69_184),
    ("Jan  2026",  178_501,  322_039,  84_557,  27_687,  87_875),
    ("Fév  2026",   85_310,  149_260,  52_616,  28_268,  48_192),
    ("Mars 2026",   21_305,   34_989,  14_667,       0,   5_959),
]

df_zone_monthly = pd.DataFrame(MONTHLY_ZONE_DATA, columns=[
    "mois", "froid_total_kwh", "ec_chiller_kwh",
    "ec_alpha_kwh", "ec_alpha_sani_kwh", "ec_gamma_kwh"
])
# Calculs dérivés par zone
df_zone_monthly["ec_alpha_total_kwh"]  = df_zone_monthly["ec_alpha_kwh"] + df_zone_monthly["ec_alpha_sani_kwh"]
df_zone_monthly["ec_gamma_total_kwh"]  = df_zone_monthly["ec_gamma_kwh"]
df_zone_monthly["ec_beta_total_kwh"]   = 0   # pas de récupération zone Béta
df_zone_monthly["rec_totale_kwh"]      = (df_zone_monthly["ec_alpha_total_kwh"]
                                          + df_zone_monthly["ec_gamma_total_kwh"]
                                          + df_zone_monthly["ec_chiller_kwh"])
# Froid par zone : répartition estimée absorbeur 33% / 33% / 34%
df_zone_monthly["froid_alpha_kwh"]  = (df_zone_monthly["froid_total_kwh"] * 0.333).round()
df_zone_monthly["froid_beta_kwh"]   = (df_zone_monthly["froid_total_kwh"] * 0.333).round()
df_zone_monthly["froid_gamma_kwh"]  = (df_zone_monthly["froid_total_kwh"] * 0.334).round()

# =============================================================================
# DONNÉES EAU CHAUDE & EAU GLACÉE PAR ZONE (Audit ADWYA 2025)
# =============================================================================

# ── EAU CHAUDE ──────────────────────────────────────────────────────────────
EC_ZONES = {
    # Source principale par zone (chaudière ou récupération TRI)
    "source": {
        "Alpha":  "Chaudière XR408 (348 kW) + Récup. TRI (300 kW EC + 370 kW ECS)",
        "Béta":   "Chaudière VIADRUS G700 (400 kW) — sans récupération TRI",
        "Gamma":  "Chaudière EC (291 kW) + Récup. TRI (600 kW)",
    },
    # Puissance installée chaudière EC (kW)
    "pu_chaudiere_kw": {"Alpha": 348,  "Béta": 400,  "Gamma": 291},
    # Puissance récupérable depuis TRI (kW) — 0 si pas de récupération
    "pu_recuperation_kw": {"Alpha": 670,  "Béta": 0,    "Gamma": 600},
    # Besoins réels estimés (kW)
    "besoin_reel_kw":     {"Alpha": 300,  "Béta": 350,  "Gamma": 320},
    # Température de départ circuit secondaire (°C)
    "T_depart_c":         {"Alpha": 75,   "Béta": 75,   "Gamma": 75},
    # Température de retour circuit secondaire (°C)
    "T_retour_c":         {"Alpha": 60,   "Béta": 60,   "Gamma": 60},
    # Énergie annuelle consommée par la chaudière EC (kWh/an) — audit tab 44
    "energie_chaudiere_kwh": {
        "Alpha": 55_600,   # armoire chaufferie Alpha (électricité auxiliaire)
        "Béta":  104_244,  # armoire chaufferie Béta (+ consommation gaz)
        "Gamma": 126_065,  # armoire chaufferie Gamma
    },
    # Gaz naturel dédié chaudière EC (Nm³/an)
    "gaz_chaudiere_nm3": {"Alpha": 0,       "Béta": 277_860,  "Gamma": 0},
    # Énergie thermique récupérée TRI (kWh/an — 6 mois 2024 extrapolés)
    "energie_recuperee_kwh": {
        "Alpha": 300_000,  # ~300 kW × 1 000 h service estimé
        "Béta":  0,
        "Gamma": 600_000,  # ~600 kW × 1 000 h service estimé
    },
    # Nombre de pompes installées / en service
    "pompes_installees": {"Alpha": 4, "Béta": 4, "Gamma": 3},
    "pompes_service":    {"Alpha": 3, "Béta": 2, "Gamma": 2},
    # État VEV pompes
    "vev_pompes": {"Alpha": "Oui (2 pompes récup.)", "Béta": "Non", "Gamma": "Oui (2 pompes récup.)"},
    # Ballon ECS : volume (litres) et calorifugé
    "ballon_ecs_L":       {"Alpha": 1000, "Béta": 1000, "Gamma": 1500},
    "ballon_calorifuge":  {"Alpha": "Oui", "Béta": "NON ⚠️", "Gamma": "Oui"},
    # Objectif après actions (−39,2 % sur GN, optimisation pompes)
    "gaz_objectif_nm3": {"Alpha": 0, "Béta": 168_954, "Gamma": 0},
}

# ── EAU GLACÉE ──────────────────────────────────────────────────────────────
EG_ZONES = {
    "source": {
        "Alpha": "2 GEG Carrier 30XA (391 kW + 274 kW) + Récup. TRI (absorbeur)",
        "Béta":  "2 GEG Carrier 30XB (393 kW + 393 kW) + Récup. TRI (absorbeur)",
        "Gamma": "2 GEG Carrier 30XA (503 kW + 503 kW) + Récup. TRI (absorbeur)",
    },
    # Puissance frigorifique installée GEG (kW)
    "pu_geg_kw": {"Alpha": 665,  "Béta": 786,  "Gamma": 1006},
    # Puissance frigorifique récupération TRI absorbeur (kW) — répartition 3 zones
    "pu_absorption_kw": {"Alpha": 211,  "Béta": 211,  "Gamma": 213},
    # Puissance totale disponible (kW)
    "pu_totale_kw": {"Alpha": 876,  "Béta": 997,  "Gamma": 1219},
    # Température départ eau glacée (°C)
    "T_depart_eg_c": {"Alpha": 6, "Béta": 6, "Gamma": 6},
    # Température retour eau glacée (°C)
    "T_retour_eg_c": {"Alpha": 12, "Béta": 12, "Gamma": 12},
    # EER moyen des GEG
    "EER_moyen": {"Alpha": 3.08, "Béta": 3.22, "Gamma": 3.24},
    # Consommation électrique GEG (kWh/an) — audit tableau 43
    "energie_geg_kwh": {"Alpha": 755_955, "Béta": 371_177, "Gamma": 279_603},
    # Consommation électrique pompes EG (kWh/an)
    "energie_pompes_kwh": {"Alpha": 105_558, "Béta": 96_737, "Gamma": 99_566},
    # Nombre de pompes installées / en service
    "pompes_installees": {"Alpha": 3, "Béta": 3, "Gamma": 2},
    "pompes_service":    {"Alpha": 3, "Béta": 3, "Gamma": 2},  # ⚠️ toutes en marche !
    # VEV pompes
    "vev_pompes": {"Alpha": "Non ⚠️", "Béta": "Non ⚠️", "Gamma": "Non ⚠️"},
    # État V3V régulation dans les CTA
    "v3v_etat": {
        "Alpha": "Majorité by-passées ⚠️",
        "Béta":  "Majorité by-passées ⚠️",
        "Gamma": "Quelques défaillances",
    },
    # Objectifs après actions (−17,6% élec GEG + pompes)
    "energie_geg_obj_kwh":    {"Alpha": 623_162, "Béta": 306_120, "Gamma": 230_481},
    "energie_pompes_obj_kwh": {"Alpha":  87_080, "Béta":  79_764, "Gamma":  82_082},
    # Recommandations principales
    "recommandations": {
        "Alpha": "Unifier HMT pompes, asservir selon besoin, relever T consigne EG en hiver, réhabiliter V3V",
        "Béta":  "Uniformiser pompes parallèles (HMT différentes), installer VEV, relever T consigne",
        "Gamma": "Fermer vannes GEG à l'arrêt, VEV pompes, supervision temps réel",
    },
}

COULEURS_USAGE = {
    "CTA":              "#0077b6",
    "GEG (froid)":      "#a0e878",
    "Pompes EG":        "#48cae4",
    "Chaufferies":      "#f7971e",
    "Production":       "#9b72cf",
    "Chaudière vapeur": "#e63946",
    "Chaudière EC":     "#ffd200",
    "Munters":          "#ff9f1c",
}

# Pré-calculs zone (utilisés dans tab5 et tab6)
totaux_elec     = {z: sum(ZONE_DATA_ANNUEL["elec"][u][z]     for u in ZONE_DATA_ANNUEL["elec"])     for z in ZONES}
totaux_elec_obj = {z: sum(ZONE_DATA_ANNUEL["elec_objectif"][u][z] for u in ZONE_DATA_ANNUEL["elec_objectif"]) for z in ZONES}
totaux_gaz      = {z: sum(ZONE_DATA_ANNUEL["gaz_nm3"][u][z]  for u in ZONE_DATA_ANNUEL["gaz_nm3"])  for z in ZONES}
totaux_gaz_obj  = {z: sum(ZONE_DATA_ANNUEL["gaz_nm3_objectif"][u][z] for u in ZONE_DATA_ANNUEL["gaz_nm3_objectif"]) for z in ZONES}
total_usine_elec = sum(totaux_elec.values())
total_usine_gaz  = sum(totaux_gaz.values())

PROD_ZONE = {"Alpha": 0.40, "Béta": 0.35, "Gamma": 0.25}
prod_ref  = 16_411_490

# =============================================================================
# 11. ONGLETS  (tab5 = Énergie par Zone | tab6 = Rapport & Export)
# =============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊  KPI & Rendements",
    "🔀  Flux Énergétique",
    "📉  Dérives Mensuelles",
    "💰  Analyse Économique",
    "🏭  Énergie par Zone",
    "📅  Comparaison Annuelle",
    "📋  Rapport & Export",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — KPI & RENDEMENTS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:

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

    # ── Score de santé + CO₂ + TEP ───────────────────────────────────────────
    score_cls = ("alert" if score_perf_moy < 60
                 else "warn" if score_perf_moy < 80 else "")
    score_col = ("#e63946" if score_perf_moy < 60
                 else "#ffd200" if score_perf_moy < 80 else "#2dc653")
    score_label = ("⚠️ DÉGRADÉ" if score_perf_moy < 60
                   else "🔶 PARTIEL" if score_perf_moy < 80 else "✅ BON")

    ks1, ks2, ks3, ks4 = st.columns(4)
    ks1.markdown(f"""<div class="kpi-card {score_cls}">
      <div class="kpi-label">Score de performance</div>
      <div class="kpi-value" style="color:{score_col};">{score_perf_moy:.1f}
        <span class="kpi-unit">/ 100</span></div>
      <div class="kpi-delta" style="color:{score_col};">{score_label}</div>
    </div>""", unsafe_allow_html=True)
    ks2.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">CO₂ net évité</div>
      <div class="kpi-value" style="color:#2dc653;">{total_co2_net:.1f}
        <span class="kpi-unit">tCO₂</span></div>
      <div class="kpi-delta delta-pos">Évité : {total_co2_evite:.1f} t — Émis : {total_co2_gaz:.1f} t</div>
    </div>""", unsafe_allow_html=True)
    ks3.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">TEP net économisé</div>
      <div class="kpi-value" style="color:#00b4d8;">{total_tep_net:.1f}
        <span class="kpi-unit">TEP</span></div>
      <div class="kpi-delta delta-pos">Évité : {total_tep_evite:.1f} — Consommé : {total_tep_gaz:.1f}</div>
    </div>""", unsafe_allow_html=True)
    ks4.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Disponibilité absorption</div>
      <div class="kpi-value">{df['COP'].notna().sum() / max(nb_mois,1)*100:.0f}
        <span class="kpi-unit">%</span></div>
      <div class="kpi-delta delta-neu">{df['COP'].notna().sum()}/{nb_mois} mois avec COP valide</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">Évolution du rendement global</div>', unsafe_allow_html=True)
    seuil_eg_mod  = eta_glob_nom * (1 - seuil_derive_moderee)
    seuil_eg_crit = eta_glob_nom * (1 - seuil_derive_critique)
    mc = ["#e63946" if v < seuil_eg_crit else ("#ffd200" if v < seuil_eg_mod else "#2dc653")
          for v in df["eta_glob"]]
    fg = go.Figure()
    fg.add_hrect(y0=0, y1=seuil_eg_crit*100, fillcolor="rgba(230,57,70,0.05)", line_width=0)
    fg.add_hrect(y0=seuil_eg_crit*100, y1=seuil_eg_mod*100,
                 fillcolor="rgba(255,210,0,0.03)", line_width=0)
    fg.add_trace(go.Scatter(x=df["mois"], y=df["eta_glob"]*100,
                            mode="lines+markers", line=dict(color="#0077b6",width=2.5),
                            marker=dict(size=11,color=mc,line=dict(color="#0077b6",width=1.5)),
                            hovertemplate="<b>%{x}</b><br>η_global = %{y:.2f}%<extra></extra>"))
    fg.add_hline(y=eta_glob_nom*100, line_dash="dash", line_color="#ffd200",
                 annotation_text=f"Nominal {eta_glob_nom*100:.1f}%",
                 annotation_font_color="#ffd200", annotation_position="right")
    fg.add_hline(y=seuil_eg_crit*100, line_dash="dot", line_color="#e63946",
                 annotation_text=f"Écart significatif {seuil_eg_crit*100:.0f}%",
                 annotation_font_color="#e63946", annotation_position="right")
    fg.update_layout(template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                     yaxis_title="η_global (%)", xaxis_title="",
                     height=320, margin=dict(l=50,r=110,t=20,b=40), showlegend=False)
    st.plotly_chart(fg, use_container_width=True)

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
        seuil_cop_mod  = cop_nom * (1 - seuil_derive_moderee)
        seuil_cop_crit = cop_nom * (1 - seuil_derive_critique)
        cop_col = []
        for v in df["COP"]:
            if pd.isna(v) or v == 0:        cop_col.append("#555555")
            elif v < seuil_cop_crit:         cop_col.append("#e63946")
            elif v < seuil_cop_mod:          cop_col.append("#ffd200")
            else:                            cop_col.append("#2dc653")
        f3 = go.Figure()
        f3.add_trace(go.Bar(x=df["mois"], y=df["COP"].fillna(0),
                            marker_color=cop_col, name="COP mesuré",
                            hovertemplate="<b>%{x}</b><br>COP = %{y:.3f}<extra></extra>"))
        f3.add_hline(y=cop_nom, line_dash="dash", line_color="#ffd200",
                     annotation_text=f"Nominal {cop_nom:.2f}",
                     annotation_font_color="#ffd200", annotation_position="right")
        f3.add_hline(y=seuil_cop_crit, line_dash="dot", line_color="#e63946",
                     annotation_text=f"Écart significatif {seuil_cop_crit:.2f}",
                     annotation_font_color="#e63946", annotation_position="right")
        for i, row in df.iterrows():
            if (pd.isna(row["COP"]) or row["COP"] == 0) and row["cause_cop"]:
                f3.add_annotation(x=row["mois"], y=0.05, text="ARRET",
                                  showarrow=False, font=dict(color="#e63946",size=10),
                                  bgcolor="rgba(230,57,70,0.12)", borderpad=3)
        f3.update_layout(title="COP machine à absorption", template="plotly_dark",
                         paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                         height=300, margin=dict(l=50,r=80,t=40,b=40), showlegend=False)
        st.plotly_chart(f3, use_container_width=True)

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
# TAB 3 — SUIVI DES DÉRIVES MENSUELLES
# Les données étant saisies manuellement (non SCADA), les seuils temps-réel
# n'ont pas de sens opérationnel. On analyse les dérives mois/mois vs nominal.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — DÉRIVES MENSUELLES  (refonte complète)
# ─────────────────────────────────────────────────────────────────────────────
with tab3:

    # ── Données de base ──────────────────────────────────────────────────────
    df_derive = detecter_derives_mensuelles(df)
    tendances = detecter_tendances(df)

    nb_conform = (df_derive["Statut"] == "✅ Conforme").sum()
    nb_modere  = (df_derive["Statut"] == "⚠️ Écart modéré").sum()
    nb_signif  = (df_derive["Statut"] == "❌ Écart significatif").sum()
    nb_arret   = (df_derive["Statut"] == "⛔ Arrêt / N.D.").sum()
    nb_total   = len(df_derive)
    pct_sante  = round(nb_conform / nb_total * 100) if nb_total > 0 else 0

    # Dernier mois disponible
    dernier_mois = df["mois"].iloc[-1] if len(df) > 0 else "—"
    df_last = df_derive[df_derive["Mois"] == dernier_mois]

    # ── BANDEAU TITRE ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0b1929 0%,#0d2137 100%);
                border:1px solid #1b3352;border-radius:10px;
                padding:16px 22px;margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div>
          <div style="font-size:11px;color:#4d7fa8;text-transform:uppercase;letter-spacing:1.5px;
                      margin-bottom:4px;">Diagnostic opérationnel — Suivi des dérives</div>
          <div style="font-size:20px;font-weight:700;color:#e0f0ff;">
            Analyse mensuelle des KPI vs nominaux
          </div>
          <div style="font-size:12px;color:#4d7fa8;margin-top:4px;">
            Données manuelles (relevés de comptage) · Non connecté SCADA ·
            Période : mai 2024 – mars 2026 ({len(df)} mois)
          </div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:11px;color:#4d7fa8;text-transform:uppercase;letter-spacing:1px;">
            Indice de santé global
          </div>
          <div style="font-size:42px;font-weight:900;
                      color:{'#2dc653' if pct_sante>=70 else ('#ffd200' if pct_sante>=50 else '#e63946')};">
            {pct_sante}%
          </div>
          <div style="font-size:11px;color:#778da9;">
            {nb_conform} / {nb_total} mesures conformes
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 1 — ÉTAT DU DERNIER MOIS (cartes KPI avec jauge circulaire)
    # ════════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="sec-hdr">🔍 État instantané — {dernier_mois}</div>',
                unsafe_allow_html=True)

    kpi_meta = {
        "η_global": {"nom": eta_glob_nom, "col": "eta_glob", "label": "η Global",    "icon": "⚡", "unit": "%"},
        "η_e":      {"nom": eta_e_nom,    "col": "eta_e",    "label": "η Électrique","icon": "🔌", "unit": "%"},
        "η_th":     {"nom": eta_th_nom,   "col": "eta_th",   "label": "η Thermique", "icon": "🔥", "unit": "%"},
        "η_frig":   {"nom": eta_frig_nom, "col": "eta_frig", "label": "η Frig.",     "icon": "❄️", "unit": "%"},
        "COP":      {"nom": cop_nom,      "col": "COP",      "label": "COP Absorp.", "icon": "🌡️", "unit": ""},
    }

    cols_inst = st.columns(5)
    for i, (kpi_id, meta) in enumerate(kpi_meta.items()):
        row_last = df_last[df_last["KPI"] == kpi_id]
        if row_last.empty:
            statut_last = "—"
            val_last_raw = 0.0
            ecart_last = None
        else:
            statut_last = row_last.iloc[0]["Statut"]
            val_str = row_last.iloc[0]["Valeur"]
            ecart_str = row_last.iloc[0]["Écart/Nom"]
            try:
                val_last_raw = float(val_str.replace("%","").replace("ARRÊT","0"))
                if meta["unit"] == "%":
                    val_last_raw = val_last_raw / 100 if val_last_raw > 1 else val_last_raw
            except Exception:
                val_last_raw = 0.0
            try:
                ecart_last = float(ecart_str.replace("%","").replace("+","").replace("N/A","0")) / 100
            except Exception:
                ecart_last = None

        # Couleur selon statut
        if statut_last == "✅ Conforme":
            border_col = "#2dc653"
            bg_col     = "rgba(45,198,83,0.08)"
            badge_txt  = "✅ OK"
            badge_col  = "#2dc653"
        elif statut_last == "⚠️ Écart modéré":
            border_col = "#ffd200"
            bg_col     = "rgba(255,210,0,0.08)"
            badge_txt  = "⚠ MODÉRÉ"
            badge_col  = "#ffd200"
        elif statut_last == "❌ Écart significatif":
            border_col = "#e63946"
            bg_col     = "rgba(230,57,70,0.10)"
            badge_txt  = "❌ CRITIQUE"
            badge_col  = "#e63946"
        else:
            border_col = "#445566"
            bg_col     = "rgba(30,40,60,0.4)"
            badge_txt  = "— N/D"
            badge_col  = "#556677"

        # Valeur formatée
        if meta["unit"] == "%":
            val_disp = f"{val_last_raw*100:.1f}%" if val_last_raw > 0 else "—"
            nom_disp = f"{meta['nom']*100:.1f}%"
        else:
            val_disp = f"{val_last_raw:.3f}" if val_last_raw > 0 else "—"
            nom_disp = f"{meta['nom']:.3f}"

        ecart_disp = (f"{'▲' if ecart_last>=0 else '▼'} {abs(ecart_last)*100:.1f}% / nominal"
                      if ecart_last is not None else "")
        ecart_col  = "#2dc653" if (ecart_last or 0) >= 0 else "#e63946"

        with cols_inst[i]:
            st.markdown(f"""
            <div style="background:{bg_col};border:1.5px solid {border_col};
                        border-radius:10px;padding:14px 12px;text-align:center;min-height:160px;
                        display:flex;flex-direction:column;justify-content:space-between;">
              <div style="font-size:22px;margin-bottom:4px;">{meta['icon']}</div>
              <div style="font-size:11px;color:#90c2e7;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:6px;">{meta['label']}</div>
              <div style="font-size:28px;font-weight:900;color:#e0f0ff;
                          margin-bottom:2px;">{val_disp}</div>
              <div style="font-size:11px;color:#556677;margin-bottom:6px;">
                nominal : {nom_disp}
              </div>
              <div style="font-size:11px;color:{ecart_col};margin-bottom:8px;">
                {ecart_disp}
              </div>
              <div style="background:{border_col};color:#000;font-size:10px;font-weight:700;
                          border-radius:20px;padding:3px 8px;display:inline-block;">
                {badge_txt}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 2 — RADAR DE SANTÉ + JAUGE DE SYNTHÈSE
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-hdr">📡 Profil de performance — Radar multi-KPI</div>',
                unsafe_allow_html=True)

    col_radar, col_gauge = st.columns([3, 2])

    with col_radar:
        # Radar : valeur normalisée vs nominal pour chaque KPI, sur le dernier mois
        kpi_labels_rad = ["η Global", "η Électrique", "η Thermique", "η Frig.", "COP"]
        kpi_cols_rad   = ["eta_glob", "eta_e", "eta_th", "eta_frig", "COP"]
        kpi_noms_rad   = [eta_glob_nom, eta_e_nom, eta_th_nom, eta_frig_nom, cop_nom]

        # Valeurs normalisées (% du nominal) — dernier mois et moyenne période
        def _get_norm_vals(data_slice):
            vals = []
            for col_r, nom_r in zip(kpi_cols_rad, kpi_noms_rad):
                if col_r in data_slice.columns:
                    v = data_slice[col_r].mean()
                    vals.append(round(v / nom_r * 100, 1) if (nom_r > 0 and pd.notna(v) and v > 0) else 0)
                else:
                    vals.append(0)
            return vals

        last_row = df[df["mois"] == dernier_mois] if dernier_mois in df["mois"].values else df.tail(1)
        vals_last = _get_norm_vals(last_row)
        vals_moy  = _get_norm_vals(df)

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_last + [vals_last[0]],
            theta=kpi_labels_rad + [kpi_labels_rad[0]],
            fill="toself",
            name=f"Dernier mois ({dernier_mois})",
            line=dict(color="#00b4d8", width=2),
            fillcolor="rgba(0,180,216,0.15)",
            marker=dict(size=7, color="#00b4d8"),
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_moy + [vals_moy[0]],
            theta=kpi_labels_rad + [kpi_labels_rad[0]],
            fill="toself",
            name="Moyenne période",
            line=dict(color="#9b72cf", width=1.5, dash="dot"),
            fillcolor="rgba(155,114,207,0.08)",
            marker=dict(size=5, color="#9b72cf"),
        ))
        # Cercle nominal (100%)
        fig_radar.add_trace(go.Scatterpolar(
            r=[100]*6,
            theta=kpi_labels_rad + [kpi_labels_rad[0]],
            mode="lines",
            name="Nominal (100%)",
            line=dict(color="#ffd200", width=1.5, dash="dash"),
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#0b1929",
                radialaxis=dict(
                    visible=True, range=[0, 130],
                    tickvals=[0, 25, 50, 75, 100, 125],
                    ticktext=["0%", "25%", "50%", "75%", "nominal", ""],
                    tickfont=dict(size=9, color="#4d7fa8"),
                    gridcolor="#1b3352", linecolor="#1b3352",
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color="#90c2e7"),
                    gridcolor="#1b3352", linecolor="#1b3352",
                ),
            ),
            paper_bgcolor="#070e1a",
            template="plotly_dark",
            height=340,
            margin=dict(l=60, r=60, t=40, b=40),
            legend=dict(
                bgcolor="#0b1929", font_size=11,
                orientation="h", y=-0.12, x=0.5, xanchor="center",
            ),
            showlegend=True,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_gauge:
        # Jauge indicateur de santé global
        st.markdown("""
        <div style="font-size:12px;color:#4d7fa8;text-align:center;
                    margin-bottom:8px;text-transform:uppercase;letter-spacing:1px;">
          Score de santé global (période complète)
        </div>""", unsafe_allow_html=True)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pct_sante,
            delta={"reference": 70, "valueformat": ".0f",
                   "increasing": {"color": "#2dc653"},
                   "decreasing": {"color": "#e63946"}},
            number={"suffix": "%", "font": {"size": 44, "color": "#e0f0ff"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1,
                         "tickcolor": "#4d7fa8", "tickfont": {"size": 10}},
                "bar":  {"color": "#00b4d8", "thickness": 0.3},
                "bgcolor": "#0b1929",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40],  "color": "rgba(230,57,70,0.25)"},
                    {"range": [40, 70], "color": "rgba(255,210,0,0.15)"},
                    {"range": [70, 100],"color": "rgba(45,198,83,0.15)"},
                ],
                "threshold": {
                    "line": {"color": "#ffd200", "width": 3},
                    "thickness": 0.75, "value": 70,
                },
            },
            title={"text": "Conformité KPI × mois", "font": {"size": 12, "color": "#4d7fa8"}},
        ))
        fig_gauge.update_layout(
            paper_bgcolor="#070e1a",
            font_color="#e0f0ff",
            height=280,
            margin=dict(l=30, r=30, t=30, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Répartition des statuts en donuts
        fig_donut = go.Figure(go.Pie(
            labels=["✅ Conforme", "⚠ Modéré", "❌ Significatif", "⛔ Arrêt"],
            values=[nb_conform, nb_modere, nb_signif, nb_arret],
            hole=0.6,
            marker_colors=["#2dc653", "#ffd200", "#e63946", "#445566"],
            textfont_size=11,
            hovertemplate="%{label}<br>%{value} mesures (%{percent})<extra></extra>",
        ))
        fig_donut.update_layout(
            paper_bgcolor="#070e1a",
            template="plotly_dark",
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(font_size=10, bgcolor="#0b1929",
                        orientation="h", y=-0.15, x=0.5, xanchor="center"),
            annotations=[dict(text=f"<b>{nb_total}</b><br>mesures",
                              x=0.5, y=0.5, font_size=12,
                              font_color="#90c2e7", showarrow=False)],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 3 — HEATMAP CHRONOLOGIQUE (compacte, design amélioré)
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-hdr">🗓️ Carte de conformité chronologique</div>',
                unsafe_allow_html=True)

    statut_num   = {"✅ Conforme": 1, "⚠️ Écart modéré": 0,
                    "❌ Écart significatif": -1, "⛔ Arrêt / N.D.": -2}
    statut_court = {"✅ Conforme": "✅", "⚠️ Écart modéré": "⚠",
                    "❌ Écart significatif": "❌", "⛔ Arrêt / N.D.": "—"}

    def _mois_sort_key(label):
        MOIS_K = {
            "jan":1,"fév":2,"mar":3,"avr":4,"mai":5,
            "jun":6,"juin":6,"jul":7,"juil":7,
            "aoû":8,"août":8,"sep":9,"sept":9,"oct":10,"nov":11,"déc":12
        }
        parts = label.strip().lower().split()
        mm = next((v for k, v in MOIS_K.items() if parts[0].startswith(k)), 0)
        yy = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return yy * 100 + mm

    df_pivot_raw = df_derive.pivot(index="KPI", columns="Mois", values="Statut")
    cols_sorted  = sorted(df_pivot_raw.columns.tolist(), key=_mois_sort_key)
    df_pivot_raw = df_pivot_raw[cols_sorted]

    kpi_order = ["η_global", "η_e", "η_th", "η_frig", "COP"]
    rows_sorted = [k for k in kpi_order if k in df_pivot_raw.index] + \
                  [k for k in df_pivot_raw.index if k not in kpi_order]
    df_pivot_raw = df_pivot_raw.loc[rows_sorted]

    df_pivot_num  = df_pivot_raw.map(lambda s: statut_num.get(s, 0))
    df_pivot_text = df_pivot_raw.map(lambda s: statut_court.get(s, "?"))

    def _short_label(label):
        parts = label.strip().split()
        return f"{parts[0][:3]} {parts[1][-2:]}" if len(parts) >= 2 else label[:6]

    x_labels = [_short_label(c) for c in cols_sorted]

    # Hover enrichi avec valeurs réelles
    hover_matrix = []
    for kpi_row in rows_sorted:
        row_hover = []
        for col_m in cols_sorted:
            cell_statut = df_pivot_raw.loc[kpi_row, col_m] if col_m in df_pivot_raw.columns else "—"
            cell_val = df_derive[(df_derive["KPI"]==kpi_row) & (df_derive["Mois"]==col_m)]
            if not cell_val.empty:
                v = cell_val.iloc[0]["Valeur"]
                e = cell_val.iloc[0]["Écart/Nom"]
                row_hover.append(f"{cell_statut}<br>Val: {v} | Écart: {e}")
            else:
                row_hover.append(str(cell_statut))
        hover_matrix.append(row_hover)

    fhm = go.Figure(go.Heatmap(
        z=df_pivot_num.values,
        x=x_labels,
        y=df_pivot_num.index.tolist(),
        customdata=hover_matrix,
        colorscale=[
            [0.00, "#1a1a2e"],
            [0.33, "#7b0a14"],
            [0.66, "#7a6000"],
            [1.00, "#155a2e"],
        ],
        zmin=-2, zmax=1,
        text=df_pivot_text.values,
        texttemplate="%{text}",
        textfont={"size": 15},
        showscale=False,
        hovertemplate="<b>%{y}</b> — %{x}<br>%{customdata}<extra></extra>",
    ))

    h_hm = max(220, len(rows_sorted) * 58 + 90)
    fhm.update_layout(
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        height=h_hm,
        margin=dict(l=100, r=20, t=10, b=80),
        xaxis=dict(
            tickangle=-45, tickfont_size=10,
            side="bottom",
        ),
        yaxis=dict(tickfont_size=13, autorange="reversed"),
    )
    st.plotly_chart(fhm, use_container_width=True)

    st.markdown("""
    <div style="display:flex;gap:20px;font-size:12px;margin-top:-8px;margin-bottom:16px;
                flex-wrap:wrap;">
      <span style="color:#2dc653;">■ ✅ Conforme (nominal ±{:.0f}%)</span>
      <span style="color:#ffd200;">■ ⚠ Écart modéré</span>
      <span style="color:#e63946;">■ ❌ Écart significatif (>{:.0f}%)</span>
      <span style="color:#555;">■ — Arrêt / Données manquantes</span>
    </div>""".format(seuil_derive_moderee*100, seuil_derive_critique*100),
    unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 4 — TUNNEL DE PERFORMANCE : évolution écart + zones colorées
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-hdr">📈 Tunnel de performance — Écart au nominal par KPI</div>',
                unsafe_allow_html=True)

    kpi_sel_ecart = st.multiselect(
        "KPI à afficher",
        options=["η_global", "η_e", "η_th", "η_frig", "COP"],
        default=["η_global", "η_e", "COP"],
        key="kpi_sel_tunnel"
    )

    kpi_colors = {
        "η_global": "#0077b6", "η_e": "#00b4d8",
        "η_th": "#f7971e", "η_frig": "#a0e878", "COP": "#9b72cf"
    }

    fig_tunnel = go.Figure()

    # Zones de fond
    x_range_paper = [0, 1]
    for y0, y1, col_bg in [
        (-1.0, -seuil_derive_critique, "rgba(230,57,70,0.07)"),
        (-seuil_derive_critique, -seuil_derive_moderee, "rgba(255,210,0,0.06)"),
        (-seuil_derive_moderee, seuil_derive_moderee, "rgba(45,198,83,0.05)"),
        (seuil_derive_moderee, 0.5, "rgba(45,198,83,0.03)"),
    ]:
        fig_tunnel.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, x1=1, y0=y0, y1=y1,
            fillcolor=col_bg, line_width=0,
        )

    for kpi_name in kpi_sel_ecart:
        col_data = df_derive[df_derive["KPI"] == kpi_name].copy()
        if col_data.empty:
            continue
        ecarts = col_data["Écart/Nom"].replace("N/A", np.nan)
        ecarts_num = pd.to_numeric(
            ecarts.str.replace("%","").str.replace("+",""), errors="coerce"
        ) / 100

        fig_tunnel.add_trace(go.Scatter(
            x=col_data["Mois"].tolist(),
            y=ecarts_num.tolist(),
            mode="lines+markers",
            name=kpi_name,
            line=dict(color=kpi_colors.get(kpi_name, "#ccc"), width=2.5),
            marker=dict(size=7, symbol="circle",
                        color=kpi_colors.get(kpi_name, "#ccc")),
            hovertemplate=(f"<b>{kpi_name}</b><br>%{{x}}<br>"
                           f"Écart : %{{y:.1%}}<extra></extra>"),
        ))

    # Lignes de seuil
    for y_val, color, dash, label in [
        (0,                      "#ffffff", "dash",  "Nominal"),
        (-seuil_derive_moderee,  "#ffd200", "dot",   f"⚠ −{seuil_derive_moderee*100:.0f}%"),
        (-seuil_derive_critique, "#e63946", "dot",   f"❌ −{seuil_derive_critique*100:.0f}%"),
    ]:
        fig_tunnel.add_shape(
            type="line", xref="paper", yref="y",
            x0=0, x1=1, y0=y_val, y1=y_val,
            line=dict(color=color, dash=dash, width=1.2),
        )
        fig_tunnel.add_annotation(
            x=1.01, xref="paper", y=y_val, yref="y",
            text=label, showarrow=False,
            font=dict(color=color, size=10), xanchor="left",
        )

    fig_tunnel.update_layout(
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis=dict(title="Écart au nominal", tickformat=".0%", zeroline=False),
        height=360,
        margin=dict(l=70, r=160, t=20, b=70),
        legend=dict(bgcolor="#0b1929", font_size=12,
                    orientation="h", y=-0.25, x=0, xanchor="left"),
        xaxis=dict(tickangle=-45, tickfont_size=10),
    )
    st.plotly_chart(fig_tunnel, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 5 — ALERTES DE TENDANCE + TABLEAU FILTRABLE
    # ════════════════════════════════════════════════════════════════════════
    col_tend, col_table = st.columns([1, 2])

    with col_tend:
        st.markdown('<div class="sec-hdr">📉 Tendances de dégradation</div>',
                    unsafe_allow_html=True)
        if tendances:
            for t in tendances:
                vals_str = " → ".join([f"{v:.3f}" for v in t["vals"]])
                st.markdown(f"""
                <div class="arow-yel" style="margin-bottom:10px;">
                  <div style="font-size:13px;font-weight:700;color:#ffd200;margin-bottom:4px;">
                    📉 {t['label']}
                  </div>
                  <div style="font-size:11px;color:#aaa;margin-bottom:4px;">
                    {int(t['nb'])} mois consécutifs en baisse
                  </div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                               color:#ffd200;">{vals_str}</div>
                  <div style="font-size:11px;color:#778da9;margin-top:4px;">
                    🔧 Planifier une inspection si la tendance persiste.
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:rgba(45,198,83,0.08);border:1px solid #2dc653;
                        border-radius:8px;padding:16px;text-align:center;">
              <div style="font-size:24px;margin-bottom:8px;">✅</div>
              <div style="color:#2dc653;font-size:13px;font-weight:600;">
                Aucune tendance de dégradation continue
              </div>
              <div style="color:#4d7fa8;font-size:11px;margin-top:4px;">
                sur {int(nb_mois_tendance)} mois consécutifs
              </div>
            </div>""", unsafe_allow_html=True)

        # Compteurs statuts (mini-cards verticales)
        st.markdown("<br>", unsafe_allow_html=True)
        for label, val, col_s in [
            ("Conformes",       nb_conform, "#2dc653"),
            ("Écarts modérés",  nb_modere,  "#ffd200"),
            ("Écarts significatifs", nb_signif, "#e63946"),
            ("Arrêts / N.D.",   nb_arret,   "#445566"),
        ]:
            pct_val = round(val / nb_total * 100) if nb_total > 0 else 0
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        background:#0b1929;border-left:3px solid {col_s};
                        border-radius:4px;padding:8px 12px;margin-bottom:6px;">
              <span style="font-size:12px;color:#90c2e7;">{label}</span>
              <span style="font-size:15px;font-weight:700;color:{col_s};">{val}
                <span style="font-size:10px;color:#445566;">({pct_val}%)</span>
              </span>
            </div>""", unsafe_allow_html=True)

    with col_table:
        st.markdown('<div class="sec-hdr">🔎 Tableau des dérives — vue filtrée</div>',
                    unsafe_allow_html=True)

        f_col1, f_col2 = st.columns(2)
        with f_col1:
            kpi_filtre = st.multiselect(
                "KPI", df_derive["KPI"].unique().tolist(),
                default=df_derive["KPI"].unique().tolist(),
                key="filtre_kpi_derive2"
            )
        with f_col2:
            statut_filtre = st.multiselect(
                "Statut",
                ["✅ Conforme", "⚠️ Écart modéré", "❌ Écart significatif", "⛔ Arrêt / N.D."],
                default=["⚠️ Écart modéré", "❌ Écart significatif", "⛔ Arrêt / N.D."],
                key="filtre_statut_derive2"
            )

        df_derive_show = df_derive[
            df_derive["KPI"].isin(kpi_filtre) &
            df_derive["Statut"].isin(statut_filtre)
        ][["Mois","KPI","Valeur","Nominal","Écart/Nom","Var. M/M-1","Statut","Action"]].copy()

        if df_derive_show.empty:
            st.markdown("""
            <div style="background:rgba(45,198,83,0.08);border:1px solid #2dc653;
                        border-radius:8px;padding:20px;text-align:center;margin-top:10px;">
              <div style="font-size:20px;margin-bottom:6px;">✅</div>
              <div style="color:#2dc653;font-size:13px;">
                Aucune dérive selon les filtres sélectionnés.
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.dataframe(df_derive_show, use_container_width=True, hide_index=True)
            st.caption(f"{len(df_derive_show)} entrées affichées")

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 6 — ACTIONS RECOMMANDÉES (style cards, non plus liste)
    # ════════════════════════════════════════════════════════════════════════
    kpis_degrad = df_derive[
        df_derive["Statut"].isin(["❌ Écart significatif", "⚠️ Écart modéré"])
    ]["KPI"].unique().tolist()

    if kpis_degrad:
        st.markdown('<div class="sec-hdr">🔧 Actions correctives recommandées</div>',
                    unsafe_allow_html=True)

        actions_vues = {}
        for _, row in df_derive[df_derive["KPI"].isin(kpis_degrad)].iterrows():
            key = row["KPI"]
            if key not in actions_vues and row["Action"] != "—":
                actions_vues[key] = row

        action_cols = st.columns(min(len(actions_vues), 3))
        for i, (kpi_k, row) in enumerate(actions_vues.items()):
            is_crit = row["Statut"] == "❌ Écart significatif"
            bg_col  = "rgba(230,57,70,0.08)" if is_crit else "rgba(255,210,0,0.06)"
            brd_col = "#e63946" if is_crit else "#ffd200"
            badge   = "CRITIQUE" if is_crit else "MODÉRÉ"
            badge_c = "#e63946" if is_crit else "#ffd200"

            with action_cols[i % 3]:
                st.markdown(f"""
                <div style="background:{bg_col};border:1px solid {brd_col};
                            border-radius:8px;padding:14px 14px 12px;margin-bottom:10px;">
                  <div style="display:flex;justify-content:space-between;
                              align-items:center;margin-bottom:8px;">
                    <span style="font-size:14px;font-weight:700;color:#e0f0ff;">{kpi_k}</span>
                    <span style="background:{badge_c};color:#000;font-size:9px;
                                 font-weight:700;border-radius:20px;
                                 padding:2px 8px;">{badge}</span>
                  </div>
                  <div style="font-size:12px;color:#90c2e7;margin-bottom:8px;">
                    {row['Libellé']}
                  </div>
                  <div style="font-size:11px;color:#778da9;line-height:1.5;">
                    🔧 {row['Action']}
                  </div>
                </div>""", unsafe_allow_html=True)



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

    # ── SECTION CO₂ & TEP ─────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">Bilan CO₂ & TEP — Impact environnemental</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;margin-bottom:14px;padding:8px 12px;
                background:#0b1929;border-radius:6px;border:1px solid #162030;">
      <strong>Méthode (coefficients ANME — Tableau 1 &amp; 2, Audit ADWYA 2025) :</strong><br>
      Électricité : 0,283 TEP/MWh × 2,349 tCO₂/TEP (réseau STEG).<br>
      Gaz naturel : 0,9 TEP/kNm³ × 2,349 tCO₂/TEP.<br>
      Froid évité : kWh_froid / COP_GEG(3,1) = kWh_élec_STEG évités.<br>
      Chaleur évitée : kWh_chaleur / (η_chaud(0,90) × PCI) = Nm³ GN évités.
    </div>""", unsafe_allow_html=True)

    co2_c1, co2_c2, co2_c3 = st.columns(3)
    co2_c1.markdown(f"""<div class="kpi-card alert">
      <div class="kpi-label">CO₂ émis (gaz consommé)</div>
      <div class="kpi-value">{total_co2_gaz:.1f}<span class="kpi-unit"> tCO₂</span></div>
      <div class="kpi-delta delta-neg">{total_tep_gaz:.1f} TEP consommées</div>
    </div>""", unsafe_allow_html=True)
    co2_c2.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">CO₂ évité (énergie récupérée)</div>
      <div class="kpi-value" style="color:#2dc653;">{total_co2_evite:.1f}<span class="kpi-unit"> tCO₂</span></div>
      <div class="kpi-delta delta-pos">{total_tep_evite:.1f} TEP évitées au réseau</div>
    </div>""", unsafe_allow_html=True)
    co2_cls = "" if total_co2_net >= 0 else "alert"
    co2_c3.markdown(f"""<div class="kpi-card {co2_cls}">
      <div class="kpi-label">Bilan net CO₂</div>
      <div class="kpi-value" style="color:{'#2dc653' if total_co2_net>=0 else '#e63946'};">
        {total_co2_net:+.1f}<span class="kpi-unit"> tCO₂</span></div>
      <div class="kpi-delta {'delta-pos' if total_co2_net>=0 else 'delta-neg'}">
        {'Évitement net positif ✅' if total_co2_net>=0 else 'Bilan défavorable ⚠️'}</div>
    </div>""", unsafe_allow_html=True)

    # Graphique CO₂ mensuel
    fig_co2 = go.Figure()
    fig_co2.add_trace(go.Bar(x=df["mois"], y=df["co2_gaz"],
                             name="CO₂ émis (gaz)", marker_color="#e63946", opacity=0.85))
    fig_co2.add_trace(go.Bar(x=df["mois"], y=df["co2_evite_elec"],
                             name="CO₂ évité — élec", marker_color="#00b4d8", opacity=0.85))
    fig_co2.add_trace(go.Bar(x=df["mois"], y=df["co2_evite_chaud"],
                             name="CO₂ évité — chaleur", marker_color="#f7971e", opacity=0.85))
    fig_co2.add_trace(go.Bar(x=df["mois"], y=df["co2_evite_froid"],
                             name="CO₂ évité — froid", marker_color="#a0e878", opacity=0.85))
    fig_co2.add_trace(go.Scatter(x=df["mois"], y=df["co2_net"],
                                 mode="lines+markers", name="Bilan net",
                                 line=dict(color="#ffd200", width=2.5), marker=dict(size=9)))
    fig_co2.add_hline(y=0, line_color="#555", line_dash="dot")
    fig_co2.update_layout(
        barmode="group", title="Bilan CO₂ mensuel (tCO₂) — émissions vs évitements",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="tCO₂/mois", height=340,
        margin=dict(l=60, r=20, t=40, b=40),
        legend=dict(bgcolor="#0b1929", font_size=12)
    )
    st.plotly_chart(fig_co2, use_container_width=True)

    # TEP mensuel cumulé
    tep_c1, tep_c2 = st.columns(2)
    with tep_c1:
        fig_tep = go.Figure()
        fig_tep.add_trace(go.Bar(x=df["mois"], y=df["tep_gaz"],
                                 name="TEP consommées", marker_color="#e63946", opacity=0.8))
        fig_tep.add_trace(go.Bar(x=df["mois"], y=df["tep_evite_total"],
                                 name="TEP évitées", marker_color="#2dc653", opacity=0.8))
        fig_tep.add_trace(go.Scatter(x=df["mois"], y=df["tep_net"],
                                     mode="lines+markers", name="TEP nettes",
                                     line=dict(color="#ffd200", width=2), marker=dict(size=8)))
        fig_tep.update_layout(
            barmode="group", title="Bilan TEP mensuel",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="TEP", height=300,
            margin=dict(l=60, r=20, t=40, b=40),
            legend=dict(bgcolor="#0b1929", font_size=11)
        )
        st.plotly_chart(fig_tep, use_container_width=True)

    with tep_c2:
        # Décomposition du CO₂ évité par vecteur
        fig_co2_pie = px.pie(
            names=["Élec produite", "Chaleur évitée", "Froid évité"],
            values=[df["co2_evite_elec"].sum(),
                    df["co2_evite_chaud"].sum(),
                    df["co2_evite_froid"].sum()],
            color_discrete_sequence=["#00b4d8", "#f7971e", "#a0e878"],
            hole=0.5, title="Décomposition du CO₂ évité par vecteur"
        )
        fig_co2_pie.update_traces(textposition="outside", textinfo="label+percent",
                                   hovertemplate="<b>%{label}</b><br>%{value:.1f} tCO₂<extra></extra>")
        fig_co2_pie.update_layout(template="plotly_dark", paper_bgcolor="#070e1a",
                                   height=300, margin=dict(l=20, r=20, t=40, b=20),
                                   showlegend=False)
        st.plotly_chart(fig_co2_pie, use_container_width=True)

    # Tableau CO₂ mensuel
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Tableau bilan CO₂ & TEP mensuel</div>',
                unsafe_allow_html=True)
    df_co2_tab = df[["mois", "co2_gaz", "co2_evite_elec", "co2_evite_chaud",
                      "co2_evite_froid", "co2_evite_total", "co2_net",
                      "tep_gaz", "tep_evite_total", "tep_net"]].copy()
    df_co2_tab.columns = [
        "Mois", "CO₂ émis (t)", "CO₂ évité Élec (t)", "CO₂ évité Chaleur (t)",
        "CO₂ évité Froid (t)", "CO₂ évité total (t)", "Bilan CO₂ net (t)",
        "TEP gaz", "TEP évitées", "TEP nettes"
    ]
    for c_ in df_co2_tab.columns[1:]:
        df_co2_tab[c_] = df_co2_tab[c_].map(lambda x: f"{x:.2f}")
    st.dataframe(df_co2_tab, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — ÉNERGIE PAR ZONE
# ─────────────────────────────────────────────────────────────────────────────
with tab5:

    st.markdown("""
    <div style="background:linear-gradient(135deg,#0d1b2e 0%,#132438 100%);
                border:1px solid #1b3352;border-radius:10px;
                padding:18px 24px;margin-bottom:20px;">
      <div style="font-size:16px;font-weight:700;color:#90c2e7;
                  text-transform:uppercase;letter-spacing:2px;">
        &#127981; Consommation énergétique par zone de production
      </div>
      <div style="font-size:12px;color:#4d7fa8;margin-top:6px;">
        Source : Rapport d'audit énergétique ADWYA 2025 — Tableau 43 &amp; 44
        &nbsp;&middot;&nbsp; Référence année 2024
        &nbsp;&middot;&nbsp; Suivi mensuel : mai 2024 → mars 2026 (23 mois)
        &nbsp;&middot;&nbsp; Objectifs issus du plan d'actions (&#8722;17,6% élec / &#8722;39,2% GN)
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_sel1, col_sel2 = st.columns([3, 1])
    with col_sel1:
        zones_choisies = st.multiselect(
            "Zones à afficher", ZONES, default=ZONES, key="zone_select"
        )
    with col_sel2:
        vue_mode = st.radio(
            "Vue", ["Annuelle (réf. 2024)", "Mensuelle (estimée)"], key="vue_mode"
        )

    if not zones_choisies:
        st.warning("Sélectionnez au moins une zone.")
        st.stop()

    # ── A. ÉLECTRICITÉ ──────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">A — Électricité (kWh)</div>', unsafe_allow_html=True)

    cols_kpi = st.columns(len(zones_choisies))
    for i, z in enumerate(zones_choisies):
        pct     = totaux_elec[z] / total_usine_elec * 100
        gain    = totaux_elec[z] - totaux_elec_obj[z]
        gain_pct = gain / totaux_elec[z] * 100
        cols_kpi[i].markdown(f"""
        <div class="kpi-card">
          <div style="height:3px;background:{COULEURS_ZONE[z]};
                      margin:-16px -18px 12px;border-radius:8px 8px 0 0;"></div>
          <div class="kpi-label">Zone {z}</div>
          <div class="kpi-value">{totaux_elec[z]/1000:.0f}
            <span class="kpi-unit">MWh/an</span></div>
          <div class="kpi-delta delta-neu">{pct:.1f}% de l'usine</div>
          <div class="kpi-delta delta-pos">
            Objectif : {totaux_elec_obj[z]/1000:.0f} MWh/an
            &nbsp;(&#8722;{gain_pct:.1f}%)
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr" style="font-size:14px;">Réel 2024 vs Objectif par zone</div>',
                unsafe_allow_html=True)
    fig_zones_bar = go.Figure()
    fig_zones_bar.add_trace(go.Bar(
        name="Réel 2024",
        x=zones_choisies,
        y=[totaux_elec[z] / 1000 for z in zones_choisies],
        marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
        text=[f"{totaux_elec[z]/1000:.0f} MWh" for z in zones_choisies],
        textposition="outside", opacity=0.9,
    ))
    fig_zones_bar.add_trace(go.Bar(
        name="Objectif (&#8722;17,6%)",
        x=zones_choisies,
        y=[totaux_elec_obj[z] / 1000 for z in zones_choisies],
        marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
        text=[f"{totaux_elec_obj[z]/1000:.0f} MWh" for z in zones_choisies],
        textposition="outside", opacity=0.4, marker_pattern_shape="x",
    ))
    fig_zones_bar.update_layout(
        barmode="group", template="plotly_dark",
        paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="Consommation (MWh/an)", height=320,
        margin=dict(l=50,r=20,t=20,b=40),
        legend=dict(bgcolor="#0b1929", font_size=12),
    )
    st.plotly_chart(fig_zones_bar, use_container_width=True)

    st.markdown('<div class="sec-hdr" style="font-size:14px;">Décomposition par usage</div>',
                unsafe_allow_html=True)
    fig_usage = go.Figure()
    for usage, data_zone in ZONE_DATA_ANNUEL["elec"].items():
        fig_usage.add_trace(go.Bar(
            name=usage,
            x=zones_choisies,
            y=[data_zone[z] / 1000 for z in zones_choisies],
            marker_color=COULEURS_USAGE.get(usage, "#778da9"),
            hovertemplate=f"<b>{usage}</b><br>Zone %{{x}}<br>%{{y:.1f}} MWh/an<extra></extra>",
        ))
    fig_usage.update_layout(
        barmode="stack", template="plotly_dark",
        paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="Consommation (MWh/an)", height=340,
        margin=dict(l=50,r=20,t=20,b=40),
        legend=dict(bgcolor="#0b1929", font_size=11),
    )
    st.plotly_chart(fig_usage, use_container_width=True)

    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown('<div class="sec-hdr" style="font-size:14px;">Répartition usine par zone</div>',
                    unsafe_allow_html=True)
        fig_pie_zone = px.pie(
            names=zones_choisies,
            values=[totaux_elec[z] for z in zones_choisies],
            color_discrete_sequence=[COULEURS_ZONE[z] for z in zones_choisies],
            hole=0.50,
        )
        fig_pie_zone.update_traces(textposition="outside", textinfo="label+percent",
                                   hovertemplate="<b>Zone %{label}</b><br>%{value:,.0f} kWh<extra></extra>")
        fig_pie_zone.update_layout(template="plotly_dark", paper_bgcolor="#070e1a",
                                   height=280, margin=dict(l=20,r=20,t=20,b=20), showlegend=False)
        st.plotly_chart(fig_pie_zone, use_container_width=True)

    with cc2:
        st.markdown('<div class="sec-hdr" style="font-size:14px;">Répartition usine par usage</div>',
                    unsafe_allow_html=True)
        total_par_usage = {u: sum(ZONE_DATA_ANNUEL["elec"][u][z] for z in zones_choisies)
                           for u in ZONE_DATA_ANNUEL["elec"]}
        fig_pie_usage = px.pie(
            names=list(total_par_usage.keys()),
            values=list(total_par_usage.values()),
            color_discrete_sequence=[COULEURS_USAGE.get(u, "#778da9") for u in total_par_usage],
            hole=0.50,
        )
        fig_pie_usage.update_traces(textposition="outside", textinfo="label+percent",
                                    hovertemplate="<b>%{label}</b><br>%{value:,.0f} kWh<extra></extra>")
        fig_pie_usage.update_layout(template="plotly_dark", paper_bgcolor="#070e1a",
                                    height=280, margin=dict(l=20,r=20,t=20,b=20), showlegend=False)
        st.plotly_chart(fig_pie_usage, use_container_width=True)

    st.markdown('<div class="sec-hdr" style="font-size:14px;">Tableau récapitulatif électricité</div>',
                unsafe_allow_html=True)
    rows_elec = []
    for usage in ZONE_DATA_ANNUEL["elec"]:
        row = {"Usage": usage}
        for z in ZONES:
            row[f"{z} — Réel (MWh)"]     = round(ZONE_DATA_ANNUEL["elec"][usage][z] / 1000, 1)
            row[f"{z} — Objectif (MWh)"]  = round(ZONE_DATA_ANNUEL["elec_objectif"][usage][z] / 1000, 1)
            row[f"{z} — Gain (%)"]        = f"-{(ZONE_DATA_ANNUEL['elec'][usage][z] - ZONE_DATA_ANNUEL['elec_objectif'][usage][z]) / max(ZONE_DATA_ANNUEL['elec'][usage][z], 1) * 100:.1f}%"
        rows_elec.append(row)
    row_tot = {"Usage": "TOTAL ZONE"}
    for z in ZONES:
        row_tot[f"{z} — Réel (MWh)"]     = round(totaux_elec[z] / 1000, 1)
        row_tot[f"{z} — Objectif (MWh)"]  = round(totaux_elec_obj[z] / 1000, 1)
        row_tot[f"{z} — Gain (%)"]        = f"-{(totaux_elec[z] - totaux_elec_obj[z]) / max(totaux_elec[z], 1) * 100:.1f}%"
    rows_elec.append(row_tot)
    st.dataframe(pd.DataFrame(rows_elec), use_container_width=True, hide_index=True)

    # ── B. GAZ NATUREL ──────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">B — Gaz naturel (Nm³)</div>', unsafe_allow_html=True)

    cols_gaz = st.columns(len(zones_choisies))
    for i, z in enumerate(zones_choisies):
        pct_g = totaux_gaz[z] / max(total_usine_gaz, 1) * 100
        gain_g = totaux_gaz[z] - totaux_gaz_obj[z]
        gain_g_pct = gain_g / max(totaux_gaz[z], 1) * 100
        cols_gaz[i].markdown(f"""
        <div class="kpi-card warn">
          <div style="height:3px;background:{COULEURS_ZONE[z]};
                      margin:-16px -18px 12px;border-radius:8px 8px 0 0;"></div>
          <div class="kpi-label">Zone {z} — Gaz</div>
          <div class="kpi-value">{totaux_gaz[z]/1000:.1f}
            <span class="kpi-unit">kNm³/an</span></div>
          <div class="kpi-delta delta-neu">{pct_g:.1f}% des chaudières usine</div>
          <div class="kpi-delta delta-pos">
            Objectif : {totaux_gaz_obj[z]/1000:.1f} kNm³/an
            &nbsp;(&#8722;{gain_g_pct:.1f}%)
          </div>
        </div>""", unsafe_allow_html=True)

    gg1, gg2 = st.columns(2)
    with gg1:
        fig_gaz_bar = go.Figure()
        for usage, dz in ZONE_DATA_ANNUEL["gaz_nm3"].items():
            vals = [dz[z] / 1000 for z in zones_choisies]
            if any(v > 0 for v in vals):
                fig_gaz_bar.add_trace(go.Bar(
                    name=usage, x=zones_choisies, y=vals,
                    marker_color=COULEURS_USAGE.get(usage, "#778da9"),
                    hovertemplate=f"<b>{usage}</b><br>Zone %{{x}}: %{{y:.1f}} kNm³<extra></extra>",
                ))
        fig_gaz_bar.update_layout(
            barmode="stack", title="Consommation gaz par zone et usage (kNm³/an)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="kNm³/an", height=320,
            margin=dict(l=50,r=20,t=40,b=40), legend=dict(bgcolor="#0b1929"),
        )
        st.plotly_chart(fig_gaz_bar, use_container_width=True)

    with gg2:
        fig_gaz_obj = go.Figure()
        fig_gaz_obj.add_trace(go.Bar(
            name="Réel 2024", x=zones_choisies,
            y=[totaux_gaz[z] / 1000 for z in zones_choisies],
            marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
            text=[f"{totaux_gaz[z]/1000:.1f}" for z in zones_choisies],
            textposition="outside", opacity=0.9,
        ))
        fig_gaz_obj.add_trace(go.Bar(
            name="Objectif (&#8722;39,2%)", x=zones_choisies,
            y=[totaux_gaz_obj[z] / 1000 for z in zones_choisies],
            marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
            text=[f"{totaux_gaz_obj[z]/1000:.1f}" for z in zones_choisies],
            textposition="outside", opacity=0.4, marker_pattern_shape="x",
        ))
        fig_gaz_obj.update_layout(
            barmode="group", title="Réel vs Objectif gaz (kNm³/an)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="kNm³/an", height=320,
            margin=dict(l=50,r=20,t=40,b=40), legend=dict(bgcolor="#0b1929"),
        )
        st.plotly_chart(fig_gaz_obj, use_container_width=True)

    # ── C. SUIVI MENSUEL ESTIMÉ ─────────────────────────────────────────────
    if vue_mode == "Mensuelle (estimée)":
        st.markdown('<div class="sec-hdr">C — Évolution mensuelle estimée par zone</div>',
                    unsafe_allow_html=True)
        h_tot = df["h_service"].sum()
        if h_tot == 0:
            st.warning("Pas d'heures de service disponibles pour l'estimation mensuelle.")
        else:
            st.markdown("""
            <div style="font-size:12px;color:#4d7fa8;margin-bottom:12px;padding:8px 12px;
                        background:#0b1929;border-radius:6px;border:1px solid #162030;">
              <strong>Méthode :</strong> les consommations annuelles par zone sont distribuées
              mensuellement au prorata des heures de service de la trigénération.
              Il s'agit d'une estimation indicative — un suivi réel nécessite des compteurs
              divisionnaires par zone (Projet N°1 de l'audit).
            </div>""", unsafe_allow_html=True)

            records = []
            for _, row_m in df.iterrows():
                coef = row_m["h_service"] / h_tot
                r = {"Mois": row_m["mois"]}
                for z in ZONES:
                    r[f"Élec {z} (MWh)"]  = totaux_elec[z] * coef / 1000
                    r[f"Gaz {z} (kNm³)"]  = totaux_gaz[z]  * coef / 1000
                    r[f"Élec_obj {z}"]     = totaux_elec_obj[z] * coef / 1000
                records.append(r)
            df_mensuel = pd.DataFrame(records)

            fm_elec = go.Figure()
            for z in zones_choisies:
                fm_elec.add_trace(go.Scatter(
                    x=df_mensuel["Mois"], y=df_mensuel[f"Élec {z} (MWh)"],
                    mode="lines+markers", name=f"Zone {z}",
                    line=dict(color=COULEURS_ZONE[z], width=2.5), marker=dict(size=8),
                    hovertemplate=f"Zone {z}<br>%{{x}}<br>%{{y:.1f}} MWh<extra></extra>",
                ))
                fm_elec.add_trace(go.Scatter(
                    x=df_mensuel["Mois"], y=df_mensuel[f"Élec_obj {z}"],
                    mode="lines", name=f"Objectif {z}",
                    line=dict(color=COULEURS_ZONE[z], width=1.5, dash="dash"),
                    opacity=0.5, showlegend=True,
                    hovertemplate=f"Objectif {z}<br>%{{x}}<br>%{{y:.1f}} MWh<extra></extra>",
                ))
            fm_elec.update_layout(
                title="Consommation électrique mensuelle par zone (estimée)",
                template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                yaxis_title="MWh", height=340,
                margin=dict(l=50,r=20,t=40,b=40),
                legend=dict(bgcolor="#0b1929", font_size=11),
            )
            st.plotly_chart(fm_elec, use_container_width=True)

            fm_stk = go.Figure()
            for z in zones_choisies:
                fm_stk.add_trace(go.Bar(
                    name=f"Zone {z}", x=df_mensuel["Mois"],
                    y=df_mensuel[f"Élec {z} (MWh)"],
                    marker_color=COULEURS_ZONE[z], opacity=0.85,
                ))
            fm_stk.update_layout(
                barmode="stack",
                title="Répartition mensuelle par zone — électricité (MWh)",
                template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
                yaxis_title="MWh", height=300,
                margin=dict(l=50,r=20,t=40,b=40),
                legend=dict(bgcolor="#0b1929"),
            )
            st.plotly_chart(fm_stk, use_container_width=True)

            st.markdown('<div class="sec-hdr" style="font-size:14px;">Tableau mensuel estimé</div>',
                        unsafe_allow_html=True)
            cols_show = ["Mois"] + [f"Élec {z} (MWh)" for z in zones_choisies] + \
                        [f"Gaz {z} (kNm³)" for z in zones_choisies]
            df_show = df_mensuel[cols_show].copy()
            for c_ in df_show.columns[1:]:
                df_show[c_] = df_show[c_].map(lambda x: f"{x:.2f}")
            st.dataframe(df_show, use_container_width=True, hide_index=True)

    # ── D. IPE PAR ZONE ─────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">D — Indicateurs de performance énergétique (IPE)</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;margin-bottom:12px;padding:8px 12px;
                background:#0b1929;border-radius:6px;border:1px solid #162030;">
      <strong>Note :</strong> les ratios ci-dessous sont calculés avec la production de référence 2024
      (16 411 490 UP/an). La clé de répartition par zone (Alpha 40% / Béta 35% / Gamma 25%) est
      une hypothèse basée sur la capacité installée — à affiner avec les données réelles de
      production par zone.
    </div>""", unsafe_allow_html=True)

    ipe_data = []
    for z in ZONES:
        prod_z = prod_ref * PROD_ZONE[z]
        ratio_elec     = totaux_elec[z] / prod_z
        ratio_elec_obj = totaux_elec_obj[z] / prod_z
        ratio_gaz      = totaux_gaz[z] / prod_z * 1000
        ratio_gaz_obj  = totaux_gaz_obj[z] / prod_z * 1000
        ipe_data.append({
            "Zone": z,
            "Production estimée (UP/an)":       f"{prod_z:,.0f}",
            "Élec réel (kWh/UP)":               f"{ratio_elec:.4f}",
            "Élec objectif (kWh/UP)":           f"{ratio_elec_obj:.4f}",
            "Élec nominal audit (kWh/UP)":       "0.293",
            "GN réel (Nm³/UP ×10⁻³)":          f"{ratio_gaz:.3f}",
            "GN objectif (Nm³/UP ×10⁻³)":      f"{ratio_gaz_obj:.3f}",
            "GN nominal audit (Nm³/UP ×10⁻³)":  "N/A",
        })

    df_ipe = pd.DataFrame(ipe_data)
    st.dataframe(df_ipe, use_container_width=True, hide_index=True)

    fig_ipe = go.Figure()
    for z in zones_choisies:
        row_z = df_ipe[df_ipe["Zone"] == z].iloc[0]
        fig_ipe.add_trace(go.Bar(
            name=f"Zone {z}",
            x=["Réel 2024", "Objectif", "Nominal audit"],
            y=[float(row_z["Élec réel (kWh/UP)"]),
               float(row_z["Élec objectif (kWh/UP)"]),
               0.293],
            marker_color=COULEURS_ZONE[z], opacity=0.85,
        ))
    fig_ipe.add_hline(y=0.293, line_dash="dash", line_color="#ffd200",
                      annotation_text="Cible audit 0.293 kWh/UP",
                      annotation_font_color="#ffd200", annotation_position="right")
    fig_ipe.update_layout(
        barmode="group", title="IPE électrique par zone (kWh/UP)",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="kWh/UP", height=320,
        margin=dict(l=60,r=120,t=40,b=40), legend=dict(bgcolor="#0b1929"),
    )
    st.plotly_chart(fig_ipe, use_container_width=True)

    # ── E. EAU CHAUDE PAR ZONE ──────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">E — Eau Chaude (EC) par zone</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;margin-bottom:14px;padding:8px 12px;
                background:#0b1929;border-radius:6px;border:1px solid #162030;">
      <strong>Source :</strong> Audit ADWYA 2025 — Sections 3-6, Tableau 43 &amp; 44.
      Données 2024. La zone <strong>Béta</strong> est la seule sans récupération
      de chaleur depuis la trigénération.
    </div>""", unsafe_allow_html=True)

    # KPI cards EC
    ec_cols = st.columns(len(zones_choisies))
    for i, z in enumerate(zones_choisies):
        pu_ch  = EC_ZONES["pu_chaudiere_kw"][z]
        pu_rec = EC_ZONES["pu_recuperation_kw"][z]
        besoin = EC_ZONES["besoin_reel_kw"][z]
        bal_cl = EC_ZONES["ballon_calorifuge"][z]
        cls_b  = "" if bal_cl == "Oui" else "warn"
        ec_cols[i].markdown(f"""
        <div class="kpi-card {cls_b}">
          <div style="height:3px;background:{COULEURS_ZONE[z]};
                      margin:-16px -18px 12px;border-radius:8px 8px 0 0;"></div>
          <div class="kpi-label">Zone {z} — Eau Chaude</div>
          <div class="kpi-value">{pu_ch} <span class="kpi-unit">kW chaudière</span></div>
          <div class="kpi-delta delta-neu">Récup. TRI : {pu_rec} kW</div>
          <div class="kpi-delta delta-neu">Besoin réel : {besoin} kW</div>
          <div class="kpi-delta {'delta-pos' if bal_cl=='Oui' else 'delta-neg'}">
            Ballon ECS {EC_ZONES['ballon_ecs_L'][z]} L — {bal_cl}
          </div>
          <div class="kpi-delta delta-neu" style="font-size:11px;margin-top:4px;">
            VEV pompes : {EC_ZONES['vev_pompes'][z]}
          </div>
        </div>""", unsafe_allow_html=True)

    # Graphiques EC
    eg_row1_c1, eg_row1_c2 = st.columns(2)

    with eg_row1_c1:
        # Puissances disponibles vs besoins
        fig_ec_pu = go.Figure()
        fig_ec_pu.add_trace(go.Bar(
            name="Puissance chaudière (kW)",
            x=zones_choisies,
            y=[EC_ZONES["pu_chaudiere_kw"][z] for z in zones_choisies],
            marker_color="#ffd200", opacity=0.85,
            text=[f"{EC_ZONES['pu_chaudiere_kw'][z]} kW" for z in zones_choisies],
            textposition="inside",
        ))
        fig_ec_pu.add_trace(go.Bar(
            name="Puissance récup. TRI (kW)",
            x=zones_choisies,
            y=[EC_ZONES["pu_recuperation_kw"][z] for z in zones_choisies],
            marker_color="#f7971e", opacity=0.85,
            text=[f"{EC_ZONES['pu_recuperation_kw'][z]} kW" for z in zones_choisies],
            textposition="inside",
        ))
        fig_ec_pu.add_trace(go.Scatter(
            name="Besoin réel (kW)",
            x=zones_choisies,
            y=[EC_ZONES["besoin_reel_kw"][z] for z in zones_choisies],
            mode="markers+text",
            marker=dict(symbol="diamond", size=12, color="#e63946"),
            text=[f"Besoin: {EC_ZONES['besoin_reel_kw'][z]} kW" for z in zones_choisies],
            textposition="top center",
        ))
        fig_ec_pu.update_layout(
            barmode="group",
            title="Puissance EC installée vs besoins réels (kW)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="kW", height=320,
            margin=dict(l=50,r=20,t=40,b=40),
            legend=dict(bgcolor="#0b1929", font_size=11),
        )
        st.plotly_chart(fig_ec_pu, use_container_width=True)

    with eg_row1_c2:
        # Gaz naturel chaudière EC réel vs objectif
        gaz_ec_reel = [EC_ZONES["gaz_chaudiere_nm3"][z] / 1000 for z in zones_choisies]
        gaz_ec_obj  = [EC_ZONES["gaz_objectif_nm3"][z]  / 1000 for z in zones_choisies]
        fig_ec_gaz = go.Figure()
        fig_ec_gaz.add_trace(go.Bar(
            name="Gaz chaudière EC — Réel 2024 (kNm³)",
            x=zones_choisies,
            y=gaz_ec_reel,
            marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
            text=[f"{v:.1f} kNm³" for v in gaz_ec_reel],
            textposition="outside", opacity=0.9,
        ))
        fig_ec_gaz.add_trace(go.Bar(
            name="Objectif (−39,2%)",
            x=zones_choisies,
            y=gaz_ec_obj,
            marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
            text=[f"{v:.1f} kNm³" for v in gaz_ec_obj],
            textposition="outside", opacity=0.4, marker_pattern_shape="x",
        ))
        fig_ec_gaz.update_layout(
            barmode="group",
            title="Consommation gaz chaudières EC — Réel vs Objectif",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="kNm³/an", height=320,
            margin=dict(l=50,r=20,t=40,b=40),
            legend=dict(bgcolor="#0b1929", font_size=11),
        )
        st.plotly_chart(fig_ec_gaz, use_container_width=True)

    # Tableau récap EC
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Tableau récapitulatif — Eau Chaude</div>',
                unsafe_allow_html=True)
    rows_ec_tab = []
    for z in zones_choisies:
        rec_kwh = EC_ZONES["energie_recuperee_kwh"][z]
        gaz_nm3 = EC_ZONES["gaz_chaudiere_nm3"][z]
        gaz_obj = EC_ZONES["gaz_objectif_nm3"][z]
        rows_ec_tab.append({
            "Zone": z,
            "Source principale": EC_ZONES["source"][z][:55] + "...",
            "Pu chaudière (kW)": EC_ZONES["pu_chaudiere_kw"][z],
            "Pu récup. TRI (kW)": EC_ZONES["pu_recuperation_kw"][z],
            "Besoin réel (kW)": EC_ZONES["besoin_reel_kw"][z],
            "T départ (°C)": EC_ZONES["T_depart_c"][z],
            "T retour (°C)": EC_ZONES["T_retour_c"][z],
            "Gaz réel 2024 (kNm³)": f"{gaz_nm3/1000:.1f}",
            "Gaz objectif (kNm³)": f"{gaz_obj/1000:.1f}",
            "Gain gaz (kNm³)": f"{(gaz_nm3-gaz_obj)/1000:.1f}",
            "Récup. TRI estimée (MWh)": f"{rec_kwh/1000:.0f}",
            "Pompes inst./serv.": f"{EC_ZONES['pompes_installees'][z]}/{EC_ZONES['pompes_service'][z]}",
            "VEV pompes": EC_ZONES["vev_pompes"][z],
            "Ballon ECS": f"{EC_ZONES['ballon_ecs_L'][z]} L — {EC_ZONES['ballon_calorifuge'][z]}",
        })
    df_ec_tab = pd.DataFrame(rows_ec_tab)
    st.dataframe(df_ec_tab, use_container_width=True, hide_index=True)

    # Alertes EC
    st.markdown("""
    <div style="background:#0b1929;border:1px solid #1b3352;border-radius:8px;
                padding:14px 18px;margin-bottom:16px;">
      <div style="font-size:14px;font-weight:700;color:#f7971e;margin-bottom:8px;">
        ⚠️ Points de vigilance — Eau Chaude
      </div>
      <div class="arow-yel"><strong>Zone Béta :</strong>
        Aucune récupération de chaleur depuis la trigénération.
        La chaudière VIADRUS G700 (400 kW) consomme 277 860 Nm³/an seule.
        Extension de récupération recommandée → économie estimée ≈ 159 771 DT/an.
      </div>
      <div class="arow-yel"><strong>Zone Béta :</strong>
        Ballon ECS 1 000 L <em>non calorifugé</em> → pertes thermiques significatives.
        Action immédiate : calorifugeage.
      </div>
      <div class="arow-yel"><strong>Zones Alpha &amp; Gamma :</strong>
        Les énergimètres de récupération comptabilisent aussi l'énergie produite par
        les chaudières lors de leur fonctionnement → biais de mesure. Prévoir
        électrovannes de sectionnement.
      </div>
      <div class="arow-yel"><strong>Zone Alpha :</strong>
        Circuit ECS complexe (3 sources primaires). Simplification et réhabilitation recommandées.
      </div>
    </div>""", unsafe_allow_html=True)

    # ── F. EAU GLACÉE PAR ZONE ──────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">F — Eau Glacée (EG) par zone</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;margin-bottom:14px;padding:8px 12px;
                background:#0b1929;border-radius:6px;border:1px solid #162030;">
      <strong>Source :</strong> Audit ADWYA 2025 — Section 3-5, Tableau 43.
      La puissance absorption (TRI) de 635 kW est partagée entre les 3 zones.
      <strong>Problème majeur :</strong> la puissance réelle délivrée par l'absorbeur est
      de seulement ~261 kW (au lieu des 802 kW nominaux) en raison de défauts hydrauliques.
    </div>""", unsafe_allow_html=True)

    # KPI cards EG
    eg_kpi_cols = st.columns(len(zones_choisies))
    for i, z in enumerate(zones_choisies):
        pu_geg  = EG_ZONES["pu_geg_kw"][z]
        pu_abs  = EG_ZONES["pu_absorption_kw"][z]
        eer     = EG_ZONES["EER_moyen"][z]
        v3v_ok  = "défaillances" in EG_ZONES["v3v_etat"][z].lower() or "by-passées" in EG_ZONES["v3v_etat"][z].lower()
        cls_eg  = "alert" if v3v_ok else ""
        conso_geg = EG_ZONES["energie_geg_kwh"][z]
        conso_obj = EG_ZONES["energie_geg_obj_kwh"][z]
        gain_eg_pct = (conso_geg - conso_obj) / conso_geg * 100
        eg_kpi_cols[i].markdown(f"""
        <div class="kpi-card {cls_eg}">
          <div style="height:3px;background:{COULEURS_ZONE[z]};
                      margin:-16px -18px 12px;border-radius:8px 8px 0 0;"></div>
          <div class="kpi-label">Zone {z} — Eau Glacée</div>
          <div class="kpi-value">{pu_geg} <span class="kpi-unit">kW GEG</span></div>
          <div class="kpi-delta delta-neu">+ {pu_abs} kW absorption TRI</div>
          <div class="kpi-delta delta-neu">EER moyen : {eer:.2f}</div>
          <div class="kpi-delta delta-neu">Conso GEG : {conso_geg/1000:.0f} MWh/an</div>
          <div class="kpi-delta delta-pos">Objectif : {conso_obj/1000:.0f} MWh/an (&#8722;{gain_eg_pct:.1f}%)</div>
          <div class="kpi-delta {'delta-neg' if v3v_ok else 'delta-pos'}" style="font-size:11px;margin-top:4px;">
            V3V : {EG_ZONES['v3v_etat'][z]}
          </div>
        </div>""", unsafe_allow_html=True)

    # Graphiques EG — ligne 1
    eg_g1c1, eg_g1c2 = st.columns(2)

    with eg_g1c1:
        # Puissances frigorifiques installées
        fig_eg_pu = go.Figure()
        fig_eg_pu.add_trace(go.Bar(
            name="GEG (kW)",
            x=zones_choisies,
            y=[EG_ZONES["pu_geg_kw"][z] for z in zones_choisies],
            marker_color="#a0e878", opacity=0.85,
            text=[f"{EG_ZONES['pu_geg_kw'][z]} kW" for z in zones_choisies],
            textposition="inside",
        ))
        fig_eg_pu.add_trace(go.Bar(
            name="Absorption TRI (kW)",
            x=zones_choisies,
            y=[EG_ZONES["pu_absorption_kw"][z] for z in zones_choisies],
            marker_color="#48cae4", opacity=0.85,
            text=[f"{EG_ZONES['pu_absorption_kw'][z]} kW" for z in zones_choisies],
            textposition="inside",
        ))
        fig_eg_pu.add_trace(go.Scatter(
            name="⚠️ Absorption réelle actuelle (261 kW total)",
            x=zones_choisies,
            y=[87, 87, 87],  # 261 kW / 3 zones
            mode="lines+markers",
            line=dict(color="#e63946", dash="dot", width=2),
            marker=dict(symbol="x", size=10, color="#e63946"),
        ))
        fig_eg_pu.update_layout(
            barmode="stack",
            title="Puissance frigorifique installée (kW) — GEG + Absorption",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="kW", height=320,
            margin=dict(l=50,r=20,t=40,b=40),
            legend=dict(bgcolor="#0b1929", font_size=11),
        )
        st.plotly_chart(fig_eg_pu, use_container_width=True)

    with eg_g1c2:
        # Consommation électrique GEG + pompes réel vs objectif
        fig_eg_elec = go.Figure()
        fig_eg_elec.add_trace(go.Bar(
            name="GEG — Réel 2024",
            x=zones_choisies,
            y=[EG_ZONES["energie_geg_kwh"][z] / 1000 for z in zones_choisies],
            marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
            text=[f"{EG_ZONES['energie_geg_kwh'][z]/1000:.0f} MWh" for z in zones_choisies],
            textposition="outside", opacity=0.9,
        ))
        fig_eg_elec.add_trace(go.Bar(
            name="GEG — Objectif",
            x=zones_choisies,
            y=[EG_ZONES["energie_geg_obj_kwh"][z] / 1000 for z in zones_choisies],
            marker_color=[COULEURS_ZONE[z] for z in zones_choisies],
            text=[f"{EG_ZONES['energie_geg_obj_kwh'][z]/1000:.0f} MWh" for z in zones_choisies],
            textposition="outside", opacity=0.4, marker_pattern_shape="x",
        ))
        fig_eg_elec.update_layout(
            barmode="group",
            title="Consommation électrique GEG — Réel vs Objectif (MWh/an)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="MWh/an", height=320,
            margin=dict(l=50,r=20,t=40,b=40),
            legend=dict(bgcolor="#0b1929", font_size=11),
        )
        st.plotly_chart(fig_eg_elec, use_container_width=True)

    # Graphiques EG — ligne 2
    eg_g2c1, eg_g2c2 = st.columns(2)

    with eg_g2c1:
        # Pompes EG réel vs objectif
        fig_peg = go.Figure()
        fig_peg.add_trace(go.Bar(
            name="Pompes EG — Réel 2024",
            x=zones_choisies,
            y=[EG_ZONES["energie_pompes_kwh"][z] / 1000 for z in zones_choisies],
            marker_color="#48cae4", opacity=0.85,
            text=[f"{EG_ZONES['energie_pompes_kwh'][z]/1000:.0f} MWh" for z in zones_choisies],
            textposition="outside",
        ))
        fig_peg.add_trace(go.Bar(
            name="Pompes EG — Objectif",
            x=zones_choisies,
            y=[EG_ZONES["energie_pompes_obj_kwh"][z] / 1000 for z in zones_choisies],
            marker_color="#48cae4", opacity=0.4, marker_pattern_shape="x",
            text=[f"{EG_ZONES['energie_pompes_obj_kwh'][z]/1000:.0f} MWh" for z in zones_choisies],
            textposition="outside",
        ))
        fig_peg.update_layout(
            barmode="group",
            title="Consommation pompes EG — Réel vs Objectif (MWh/an)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="MWh/an", height=290,
            margin=dict(l=50,r=20,t=40,b=40),
            legend=dict(bgcolor="#0b1929", font_size=11),
        )
        st.plotly_chart(fig_peg, use_container_width=True)

    with eg_g2c2:
        # Part GEG + pompes dans la facture usine
        total_eg_reel = sum(
            EG_ZONES["energie_geg_kwh"][z] + EG_ZONES["energie_pompes_kwh"][z]
            for z in ZONES
        )
        labels_pie = []
        vals_pie   = []
        cols_pie   = []
        for z in zones_choisies:
            labels_pie.append(f"GEG {z}")
            vals_pie.append(EG_ZONES["energie_geg_kwh"][z])
            cols_pie.append(COULEURS_ZONE[z])
            labels_pie.append(f"Pompes {z}")
            vals_pie.append(EG_ZONES["energie_pompes_kwh"][z])
            cols_pie.append(COULEURS_ZONE[z])
        fig_pie_eg = px.pie(
            names=labels_pie, values=vals_pie,
            color_discrete_sequence=cols_pie,
            hole=0.50, title="Répartition consommation EG + Pompes par zone",
        )
        fig_pie_eg.update_traces(
            textposition="outside", textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} kWh<extra></extra>",
        )
        fig_pie_eg.update_layout(
            template="plotly_dark", paper_bgcolor="#070e1a",
            height=290, margin=dict(l=20,r=20,t=40,b=20), showlegend=False,
        )
        st.plotly_chart(fig_pie_eg, use_container_width=True)

    # Tableau récap EG
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Tableau récapitulatif — Eau Glacée</div>',
                unsafe_allow_html=True)
    rows_eg_tab = []
    for z in zones_choisies:
        geg_kwh   = EG_ZONES["energie_geg_kwh"][z]
        geg_obj   = EG_ZONES["energie_geg_obj_kwh"][z]
        peg_kwh   = EG_ZONES["energie_pompes_kwh"][z]
        peg_obj   = EG_ZONES["energie_pompes_obj_kwh"][z]
        total_kwh = geg_kwh + peg_kwh
        total_obj = geg_obj + peg_obj
        rows_eg_tab.append({
            "Zone": z,
            "GEG installés": f"{EG_ZONES['pu_geg_kw'][z]} kW ({EG_ZONES['pompes_installees'][z]} GEG)",
            "Puissance absorption TRI (kW)": EG_ZONES["pu_absorption_kw"][z],
            "T départ / retour (°C)": f"{EG_ZONES['T_depart_eg_c'][z]}°C / {EG_ZONES['T_retour_eg_c'][z]}°C",
            "EER moyen": EG_ZONES["EER_moyen"][z],
            "Conso GEG réel (MWh/an)": round(geg_kwh / 1000, 1),
            "Conso GEG objectif (MWh/an)": round(geg_obj / 1000, 1),
            "Gain GEG (MWh/an)": round((geg_kwh - geg_obj) / 1000, 1),
            "Conso pompes réel (MWh/an)": round(peg_kwh / 1000, 1),
            "Conso pompes objectif (MWh/an)": round(peg_obj / 1000, 1),
            "Total réel (MWh/an)": round(total_kwh / 1000, 1),
            "Total objectif (MWh/an)": round(total_obj / 1000, 1),
            "Gain total (%)": f"{(total_kwh-total_obj)/total_kwh*100:.1f}%",
            "V3V CTA": EG_ZONES["v3v_etat"][z],
            "VEV pompes": EG_ZONES["vev_pompes"][z],
        })
    df_eg_tab = pd.DataFrame(rows_eg_tab)
    st.dataframe(df_eg_tab, use_container_width=True, hide_index=True)

    # Recommandations EG par zone
    st.markdown("""
    <div style="background:#0b1929;border:1px solid #1b3352;border-radius:8px;
                padding:14px 18px;margin-bottom:16px;">
      <div style="font-size:14px;font-weight:700;color:#a0e878;margin-bottom:10px;">
        ✅ Recommandations — Eau Glacée par zone
      </div>""", unsafe_allow_html=True)

    zone_css = {"Alpha": "zone-alpha", "Béta": "zone-beta", "Gamma": "zone-gamma"}
    for z in zones_choisies:
        rec_txt = EG_ZONES["recommandations"][z]
        geg_kwh = EG_ZONES["energie_geg_kwh"][z]
        geg_obj = EG_ZONES["energie_geg_obj_kwh"][z]
        gain_dt = (geg_kwh - geg_obj) * prix_kwh_steg
        st.markdown(f"""
      <div class="{zone_css[z]}" style="margin-bottom:10px;padding:8px 14px;
                   background:#0d1b2e;border-radius:6px;">
        <strong style="color:{COULEURS_ZONE[z]};">Zone {z}</strong> &nbsp;—&nbsp;
        {rec_txt}
        <br><span style="color:#2dc653;font-size:12px;">
          💰 Gain potentiel : {(geg_kwh-geg_obj)/1000:.0f} MWh/an
          ≈ {gain_dt:,.0f} DT/an
        </span>
      </div>""", unsafe_allow_html=True)

    # Point critique absorbeur
    st.markdown("""
      <div class="arow-red">
        <strong>🔴 CRITIQUE — Machine à absorption (TRI) :</strong>
        Puissance nominale 802 kW — Puissance réelle mesurée ~261 kW (déc. 2024).
        Cause identifiée : débit eau de tour insuffisant (150 m³/h vs 230 m³/h nominal),
        pertes de charge réseau élevées, tamis colmaté.
        <br>Action prioritaire : redimensionner pompe eau tour, enlever tamis et
        détecter fuites hydrauliques côté tour et eau glacée.
      </div>
    </div>""", unsafe_allow_html=True)

    # ── H. ÉNERGIE FROID PRODUIT & RÉCUPÉRÉE MENSUELLE PAR ZONE ────────────
    st.markdown('<div class="sec-hdr">H — Énergie froid produit &amp; récupérée mensuelle par zone</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;margin-bottom:14px;padding:8px 12px;
                background:#0b1929;border-radius:6px;border:1px solid #162030;">
      <strong>Source :</strong> Suivi_trigénération.xlsx — Feuille Centrale — Dataset complet combiné : mai 2024 → mars 2026 (23 mois).<br>
      <strong>Froid produit</strong> (absorbeur TRI) : valeur globale répartie équitablement entre les 3 zones (≈33% chacune).
      <strong>Énergie récupérée</strong> : données réelles par zone — EC Alpha, EC Alpha Sanitaire, EC Gamma.
      La zone <strong>Béta</strong> ne bénéficie d'aucune récupération directe depuis la trigénération.
    </div>""", unsafe_allow_html=True)

    # KPI cumulés
    h_kpi1, h_kpi2, h_kpi3, h_kpi4 = st.columns(4)
    total_froid_mz  = df_zone_monthly["froid_total_kwh"].sum()
    total_rec_alpha = df_zone_monthly["ec_alpha_total_kwh"].sum()
    total_rec_gamma = df_zone_monthly["ec_gamma_total_kwh"].sum()
    total_rec_chil  = df_zone_monthly["ec_chiller_kwh"].sum()

    h_kpi1.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Froid total produit</div>
      <div class="kpi-value">{total_froid_mz/1e6:.2f}<span class="kpi-unit"> GWh</span></div>
      <div class="kpi-delta delta-neu">Mai 2024 → Mars 2026 (23 mois)</div>
    </div>""", unsafe_allow_html=True)
    h_kpi2.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Récup. Zone Alpha (EC+ECS)</div>
      <div class="kpi-value">{total_rec_alpha/1e6:.2f}<span class="kpi-unit"> GWh</span></div>
      <div class="kpi-delta delta-pos">EC : {df_zone_monthly['ec_alpha_kwh'].sum()/1000:.0f} MWh + ECS : {df_zone_monthly['ec_alpha_sani_kwh'].sum()/1000:.0f} MWh</div>
    </div>""", unsafe_allow_html=True)
    h_kpi3.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Récup. Zone Gamma</div>
      <div class="kpi-value">{total_rec_gamma/1e6:.2f}<span class="kpi-unit"> GWh</span></div>
      <div class="kpi-delta delta-pos">Circuit EC Gamma (600 kW nominal)</div>
    </div>""", unsafe_allow_html=True)
    h_kpi4.markdown(f"""<div class="kpi-card warn">
      <div class="kpi-label">Récup. vers absorbeur</div>
      <div class="kpi-value">{total_rec_chil/1e6:.2f}<span class="kpi-unit"> GWh</span></div>
      <div class="kpi-delta delta-neu">Chaleur vers machine absorption</div>
    </div>""", unsafe_allow_html=True)

    # Évolution mensuelle froid
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Froid produit mensuel par zone (répartition estimée)</div>',
                unsafe_allow_html=True)
    fig_froid_mz = go.Figure()
    for z, col_f, col_z in [
        ("Alpha", "froid_alpha_kwh", "#00b4d8"),
        ("Béta",  "froid_beta_kwh",  "#f7971e"),
        ("Gamma", "froid_gamma_kwh", "#a0e878"),
    ]:
        if z in zones_choisies:
            fig_froid_mz.add_trace(go.Bar(
                name=f"Zone {z}",
                x=df_zone_monthly["mois"],
                y=df_zone_monthly[col_f] / 1000,
                marker_color=col_z, opacity=0.85,
                hovertemplate=f"<b>Zone {z}</b><br>%{{x}}<br>%{{y:.1f}} MWh<extra></extra>",
            ))
    fig_froid_mz.update_layout(
        barmode="stack",
        title="Froid produit mensuel (MWh) — répartition ≈33%/33%/34% entre zones",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="MWh", height=310,
        margin=dict(l=50, r=20, t=40, b=60),
        legend=dict(bgcolor="#0b1929", font_size=11),
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig_froid_mz, use_container_width=True)

    # Récupération par zone
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Énergie thermique récupérée mensuelle par zone</div>',
                unsafe_allow_html=True)
    h3c1, h3c2 = st.columns(2)

    with h3c1:
        fig_rec_zones = go.Figure()
        if "Alpha" in zones_choisies:
            fig_rec_zones.add_trace(go.Scatter(
                x=df_zone_monthly["mois"], y=df_zone_monthly["ec_alpha_kwh"] / 1000,
                mode="lines+markers", name="EC Alpha",
                line=dict(color="#00b4d8", width=2), marker=dict(size=7),
                hovertemplate="<b>EC Alpha</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
            ))
            fig_rec_zones.add_trace(go.Scatter(
                x=df_zone_monthly["mois"], y=df_zone_monthly["ec_alpha_sani_kwh"] / 1000,
                mode="lines+markers", name="ECS Alpha",
                line=dict(color="#48cae4", width=1.5, dash="dot"), marker=dict(size=6),
                hovertemplate="<b>ECS Alpha</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
            ))
        if "Gamma" in zones_choisies:
            fig_rec_zones.add_trace(go.Scatter(
                x=df_zone_monthly["mois"], y=df_zone_monthly["ec_gamma_total_kwh"] / 1000,
                mode="lines+markers", name="EC Gamma",
                line=dict(color="#a0e878", width=2), marker=dict(size=7),
                hovertemplate="<b>EC Gamma</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
            ))
        if "Béta" in zones_choisies:
            fig_rec_zones.add_trace(go.Scatter(
                x=df_zone_monthly["mois"], y=[0] * len(df_zone_monthly),
                mode="lines", name="Zone Béta (0 — sans récup.)",
                line=dict(color="#f7971e", width=1, dash="dash"),
            ))
        fig_rec_zones.update_layout(
            title="Récupération thermique par zone (MWh/mois)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="MWh", height=310,
            margin=dict(l=50, r=20, t=40, b=60),
            legend=dict(bgcolor="#0b1929", font_size=11),
            xaxis=dict(tickangle=-45),
        )
        st.plotly_chart(fig_rec_zones, use_container_width=True)

    with h3c2:
        fig_rec_stack = go.Figure()
        if "Alpha" in zones_choisies:
            fig_rec_stack.add_trace(go.Bar(
                name="Récup. Alpha (EC+ECS)",
                x=df_zone_monthly["mois"], y=df_zone_monthly["ec_alpha_total_kwh"] / 1000,
                marker_color="#00b4d8", opacity=0.85,
                hovertemplate="<b>Récup. Alpha</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
            ))
        if "Gamma" in zones_choisies:
            fig_rec_stack.add_trace(go.Bar(
                name="Récup. Gamma",
                x=df_zone_monthly["mois"], y=df_zone_monthly["ec_gamma_total_kwh"] / 1000,
                marker_color="#a0e878", opacity=0.85,
                hovertemplate="<b>Récup. Gamma</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
            ))
        fig_rec_stack.add_trace(go.Bar(
            name="Vers absorbeur (chiller)",
            x=df_zone_monthly["mois"], y=df_zone_monthly["ec_chiller_kwh"] / 1000,
            marker_color="#9b72cf", opacity=0.7,
            hovertemplate="<b>Vers chiller</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
        ))
        fig_rec_stack.update_layout(
            barmode="stack", title="Répartition mensuelle récupération (MWh)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="MWh", height=310,
            margin=dict(l=50, r=20, t=40, b=60),
            legend=dict(bgcolor="#0b1929", font_size=11),
            xaxis=dict(tickangle=-45),
        )
        st.plotly_chart(fig_rec_stack, use_container_width=True)

    # Froid vs Récupération — vue globale
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Froid produit vs Récupération thermique totale</div>',
                unsafe_allow_html=True)
    fig_fvr = go.Figure()
    fig_fvr.add_trace(go.Scatter(
        x=df_zone_monthly["mois"], y=df_zone_monthly["froid_total_kwh"] / 1000,
        mode="lines+markers", name="Froid produit (absorption)",
        line=dict(color="#a0e878", width=2.5), marker=dict(size=8),
        fill="tozeroy", fillcolor="rgba(160,232,120,0.08)",
        hovertemplate="<b>Froid</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_fvr.add_trace(go.Scatter(
        x=df_zone_monthly["mois"], y=df_zone_monthly["rec_totale_kwh"] / 1000,
        mode="lines+markers", name="Récupération thermique totale",
        line=dict(color="#f7971e", width=2.5), marker=dict(size=8),
        fill="tozeroy", fillcolor="rgba(247,151,30,0.08)",
        hovertemplate="<b>Récup. totale</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_fvr.update_layout(
        title="Froid produit vs Récupération thermique totale (MWh/mois)",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="MWh", height=290,
        margin=dict(l=50, r=20, t=40, b=60),
        legend=dict(bgcolor="#0b1929", font_size=12),
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig_fvr, use_container_width=True)

    # Tableau récapitulatif mensuel
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Tableau mensuel — Froid &amp; Récupération par zone</div>',
                unsafe_allow_html=True)
    df_h_tab = df_zone_monthly[[
        "mois", "froid_total_kwh",
        "ec_alpha_kwh", "ec_alpha_sani_kwh", "ec_alpha_total_kwh",
        "ec_gamma_total_kwh", "ec_chiller_kwh", "rec_totale_kwh"
    ]].copy()
    df_h_tab.columns = [
        "Mois", "Froid produit (kWh)",
        "EC Alpha (kWh)", "ECS Alpha (kWh)", "Récup. Alpha total (kWh)",
        "Récup. Gamma (kWh)", "Vers absorbeur (kWh)", "Récup. totale (kWh)"
    ]
    for c in df_h_tab.columns[1:]:
        df_h_tab[c] = df_h_tab[c].apply(lambda x: f"{int(x):,}" if pd.notna(x) and x > 0 else "0")
    st.dataframe(df_h_tab, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="arow-yel" style="margin-top:10px;">
      <strong>⚠️ Zone Béta :</strong> Aucune énergie thermique récupérée depuis la trigénération.
      La chaudière EC VIADRUS G700 (400 kW) assure seule les besoins en eau chaude (277 860 Nm³/an).
      <strong>Action recommandée :</strong> raccorder la zone Béta au circuit TRI → économie estimée ~80 000 DT/an.
    </div>""", unsafe_allow_html=True)

    # ── G. POTENTIEL D'ÉCONOMIES PAR ZONE ───────────────────────────────────
    st.markdown('<div class="sec-hdr">G — Potentiel d\'économies par zone</div>',
                unsafe_allow_html=True)

    eco_rows = []
    for z in ZONES:
        eco_elec_kwh = totaux_elec[z] - totaux_elec_obj[z]
        eco_gaz_nm3  = totaux_gaz[z]  - totaux_gaz_obj[z]
        eco_elec_dt  = eco_elec_kwh * prix_kwh_steg
        eco_gaz_dt   = eco_gaz_nm3  * prix_gaz_nm3
        eco_total_dt = eco_elec_dt + eco_gaz_dt
        co2_elec_tep = eco_elec_kwh / 1_000_000 * 1e3 * 0.283
        co2_gaz_tep  = eco_gaz_nm3  / 1e3 * 0.9
        co2_evite    = (co2_elec_tep + co2_gaz_tep) * 2.349
        eco_rows.append({
            "Zone": z,
            "Éco élec (MWh/an)":  round(eco_elec_kwh / 1000, 1),
            "Éco gaz (kNm³/an)":  round(eco_gaz_nm3 / 1000, 2),
            "Gain élec (DT/an)":  round(eco_elec_dt),
            "Gain gaz (DT/an)":   round(eco_gaz_dt),
            "Gain total (DT/an)": round(eco_total_dt),
            "CO₂ évité (t/an)":   round(co2_evite, 1),
        })

    df_eco = pd.DataFrame(eco_rows)

    fig_eco = go.Figure()
    fig_eco.add_trace(go.Bar(
        name="Gain électricité",
        x=[r["Zone"] for r in eco_rows],
        y=[r["Gain élec (DT/an)"] for r in eco_rows],
        marker_color="#00b4d8",
        text=[f"{r['Gain élec (DT/an)']:,.0f} DT" for r in eco_rows],
        textposition="inside",
    ))
    fig_eco.add_trace(go.Bar(
        name="Gain gaz naturel",
        x=[r["Zone"] for r in eco_rows],
        y=[r["Gain gaz (DT/an)"] for r in eco_rows],
        marker_color="#f7971e",
        text=[f"{r['Gain gaz (DT/an)']:,.0f} DT" for r in eco_rows],
        textposition="inside",
    ))
    fig_eco.update_layout(
        barmode="stack",
        title="Potentiel d'économies financières par zone (DT/an)",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="DT/an", height=320,
        margin=dict(l=60,r=20,t=40,b=40), legend=dict(bgcolor="#0b1929"),
    )
    st.plotly_chart(fig_eco, use_container_width=True)
    st.dataframe(df_eco, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;margin-top:20px;padding:12px 16px;
                background:#0b1929;border-radius:8px;border:1px solid #162030;line-height:1.8;">
      <strong style="color:#90c2e7;">&#128204; Sources des données :</strong><br>
      &bull; <strong>Électricité par zone</strong> : Tableau 43, Rapport d'audit ADWYA 2025 (données réelles 2024).<br>
      &bull; <strong>Gaz naturel par zone</strong> : Tableau 44, Rapport d'audit ADWYA 2025.<br>
      &bull; <strong>Objectifs</strong> : Plan d'actions audit — Projet N°4 (&#8722;17,6% élec) et Projet N°7 (&#8722;39,2% GN).<br>
      &bull; <strong>IPE</strong> : Production 2024 = 16 411 490 UP (Tableau 11). Clé de répartition par zone à affiner.<br>
      <br>
      <strong style="color:#90c2e7;">&#128295; Recommandation :</strong>
      Pour un suivi réel par zone, mettre en place les 31 compteurs divisionnaires
      recommandés dans le Projet N°1 de l'audit (investissement 290 000 DT, TRB 2,3–4,6 ans).
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — COMPARAISON ANNUELLE 2024 / 2025 / 2026
# ─────────────────────────────────────────────────────────────────────────────
with tab6:

    st.markdown('<div class="sec-hdr">Comparaison annuelle — 2024 · 2025 · 2026</div>',
                unsafe_allow_html=True)

    # ── Segmentation des données par année ───────────────────────────────────
    ANNEES = {"2024": [], "2025": [], "2026": []}
    for label in ["2024", "2025", "2026"]:
        ANNEES[label] = df_raw[df_raw["mois"].str.contains(label)].copy()

    ann_couleurs = {"2024": "#0077b6", "2025": "#f7971e", "2026": "#a0e878"}
    ann_labels   = {
        "2024": f"2024 ({len(ANNEES['2024'])} mois)",
        "2025": f"2025 ({len(ANNEES['2025'])} mois)",
        "2026": f"2026 ({len(ANNEES['2026'])} mois)",
    }

    # ── Sélection des années à comparer ──────────────────────────────────────
    annees_choisies = st.multiselect(
        "Années à comparer", ["2024","2025","2026"],
        default=["2024","2025","2026"], key="comp_annees"
    )
    if not annees_choisies:
        st.warning("Sélectionnez au moins une année.")
        st.stop()

    # ── Agrégats annuels ─────────────────────────────────────────────────────
    def agreger_annee(dfann: pd.DataFrame) -> dict:
        if dfann.empty:
            return {}
        pg = dfann["P_gaz"].sum()
        safe = pg if pg > 0 else np.nan
        cop_v = dfann["COP"].dropna()
        cop_v = cop_v[cop_v > 0]
        return {
            "n_mois":       len(dfann),
            "h_service":    dfann["h_service"].sum(),
            "prod_nette":   dfann["prod_nette"].sum(),
            "chaleur":      dfann["chaleur"].sum(),
            "froid":        dfann["froid"].sum(),
            "gaz_nm3":      dfann["gaz"].sum(),
            "P_gaz":        pg,
            "eta_e":        dfann["prod_nette"].sum() / safe if safe else 0,
            "eta_th":       dfann["chaleur"].sum()    / safe if safe else 0,
            "eta_frig":     dfann["froid"].sum()      / safe if safe else 0,
            "eta_glob":    (dfann["prod_nette"].sum() + dfann["chaleur"].sum()
                            + dfann["froid"].sum()) / safe if safe else 0,
            "cop_moy":      float(cop_v.mean()) if len(cop_v) > 0 else np.nan,
            "cout_gaz":     dfann["cout_gaz_dt"].sum(),
            "val_elec":     dfann["val_elec_dt"].sum(),
            "val_chaleur":  dfann["val_chaleur_dt"].sum(),
            "val_froid":    dfann["val_froid_dt"].sum(),
            "gain":         dfann["gain_global_dt"].sum(),
            # CO₂ & TEP
            "co2_net":      dfann["co2_net"].sum(),
            "co2_evite":    dfann["co2_evite_total"].sum(),
            "co2_emis":     dfann["co2_gaz"].sum(),
            "tep_net":      dfann["tep_net"].sum(),
            "score_moy":    dfann["score_perf"].mean(),
        }

    agreg = {a: agreger_annee(ANNEES[a]) for a in annees_choisies if not ANNEES[a].empty}

    # ── KPI cards comparatifs ─────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">KPI annuels comparés</div>', unsafe_allow_html=True)

    kpis_comp = [
        ("η Global",    "eta_glob",  eta_glob_nom, "%",   100),
        ("η Élec",      "eta_e",     eta_e_nom,    "%",   100),
        ("η Thermique", "eta_th",    eta_th_nom,   "%",   100),
        ("COP",         "cop_moy",   cop_nom,      "",    1),
        ("Gain net (DT)","gain",     None,         "DT",  1),
        ("Gaz (MNm³)",  "gaz_nm3",  None,         "MNm³",1/1e6),
    ]

    cols_kpi_comp = st.columns(len(annees_choisies))
    for i, ann in enumerate(annees_choisies):
        ag = agreg.get(ann, {})
        if not ag:
            continue
        with cols_kpi_comp[i]:
            st.markdown(f"""
            <div style="border-left:4px solid {ann_couleurs[ann]};
                        padding-left:14px;margin-bottom:18px;">
              <div style="font-size:20px;font-weight:700;
                          color:{ann_couleurs[ann]};letter-spacing:2px;">
                {ann} &nbsp;
                <span style="font-size:13px;color:#4d7fa8;">
                  ({ag['n_mois']} mois · {ag['h_service']:,.0f} h)
                </span>
              </div>
            </div>""", unsafe_allow_html=True)

            for nom_k, col_k, nom_val, unit_k, facteur in kpis_comp:
                val = ag.get(col_k, np.nan)
                if pd.isna(val):
                    val_str = "N/A"
                    delta_html = ""
                elif unit_k == "%":
                    val_str = f"{val*facteur:.1f}%"
                    delta_html = (f'<span style="color:{"#2dc653" if val>=nom_val else "#e63946"}">'
                                  f'{"▲" if val>=nom_val else "▼"} '
                                  f'{abs(val-nom_val)*100:.1f}pp vs nominal</span>')
                elif unit_k == "DT":
                    val_str = f"{val*facteur:,.0f} DT"
                    delta_html = ""
                elif unit_k == "MNm³":
                    val_str = f"{val*facteur:.3f} MNm³"
                    delta_html = ""
                else:
                    val_str = f"{val*facteur:.3f}"
                    delta_html = (f'<span style="color:{"#2dc653" if val>=nom_val else "#e63946"}">'
                                  f'{"▲" if val>=nom_val else "▼"} '
                                  f'{abs(val-nom_val):.3f} vs nominal</span>'
                                  if nom_val else "")
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;
                            padding:5px 0;border-bottom:1px solid #162030;">
                  <span style="color:#4d7fa8;font-size:13px;">{nom_k}</span>
                  <span style="color:#e8f4ff;font-family:'Share Tech Mono',monospace;">
                    {val_str}</span>
                </div>
                <div style="text-align:right;font-size:11px;
                            margin-bottom:3px;">{delta_html}</div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Graphique 1 : Rendements annuels comparés ─────────────────────────────
    st.markdown('<div class="sec-hdr">Rendements annuels comparés</div>', unsafe_allow_html=True)

    gr1c, gr2c = st.columns(2)
    with gr1c:
        kpis_bar = ["η_e", "η_th", "η_frig", "η_global"]
        kpis_col_map = {"η_e":"eta_e","η_th":"eta_th","η_frig":"eta_frig","η_global":"eta_glob"}
        noms_ref     = {"η_e":eta_e_nom,"η_th":eta_th_nom,
                        "η_frig":eta_frig_nom,"η_global":eta_glob_nom}
        fig_rend = go.Figure()
        for ann in annees_choisies:
            ag = agreg.get(ann, {})
            if not ag:
                continue
            fig_rend.add_trace(go.Bar(
                name=ann_labels[ann],
                x=kpis_bar,
                y=[ag.get(kpis_col_map[k], 0)*100 for k in kpis_bar],
                marker_color=ann_couleurs[ann],
                opacity=0.85,
                text=[f"{ag.get(kpis_col_map[k],0)*100:.1f}%" for k in kpis_bar],
                textposition="outside",
            ))
        for kp in kpis_bar:
            fig_rend.add_scatter(
                x=[kp], y=[noms_ref[kp]*100],
                mode="markers", marker=dict(symbol="line-ew",size=24,
                color="#ffd200",line=dict(width=2,color="#ffd200")),
                name=f"Nominal {kp}" if kp=="η_e" else None,
                showlegend=(kp=="η_e"),
            )
        fig_rend.update_layout(
            barmode="group", title="Rendements annuels vs nominal (%)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="%", height=350,
            margin=dict(l=50,r=20,t=40,b=40),
            legend=dict(bgcolor="#0b1929", font_size=12),
        )
        st.plotly_chart(fig_rend, use_container_width=True)

    with gr2c:
        # COP annuel moyen comparé
        fig_cop = go.Figure()
        cop_vals = [agreg.get(a,{}).get("cop_moy", np.nan) for a in annees_choisies]
        fig_cop.add_trace(go.Bar(
            x=annees_choisies, y=cop_vals,
            marker_color=[ann_couleurs[a] for a in annees_choisies],
            text=[f"{v:.3f}" if not np.isnan(v) else "N/A" for v in cop_vals],
            textposition="outside", opacity=0.85,
        ))
        fig_cop.add_hline(y=cop_nom, line_dash="dash", line_color="#ffd200",
                          annotation_text=f"Nominal {cop_nom:.2f}",
                          annotation_font_color="#ffd200", annotation_position="right")
        fig_cop.update_layout(
            title="COP moyen annuel (mois actifs)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="COP", height=350,
            margin=dict(l=50,r=100,t=40,b=40), showlegend=False,
        )
        st.plotly_chart(fig_cop, use_container_width=True)

    # ── Graphique 2 : Évolution mensuelle superposée ──────────────────────────
    st.markdown('<div class="sec-hdr">Évolution mensuelle superposée par année</div>',
                unsafe_allow_html=True)

    # Mapping label affiché → nom de colonne dans df_raw / ANNEES[ann]
    KPI_COMP_OPTIONS = {
        "η_global":         "eta_glob",
        "η_e (élec)":       "eta_e",
        "η_th (thermique)": "eta_th",
        "η_frig (froid)":   "eta_frig",
        "COP absorption":   "COP",
        "Élec nette (kWh)": "prod_nette",
        "Chaleur (kWh)":    "chaleur",
        "Froid (kWh)":      "froid",
        "Gaz consommé (Nm³)":"gaz",
    }
    KPI_EST_RENDEMENT = {"eta_glob","eta_e","eta_th","eta_frig"}
    KPI_NOM_MAP = {
        "eta_e":    eta_e_nom,    "eta_th":  eta_th_nom,
        "eta_frig": eta_frig_nom, "eta_glob":eta_glob_nom,
        "COP":      cop_nom,
    }

    kpi_comp_label = st.selectbox(
        "KPI à superposer",
        list(KPI_COMP_OPTIONS.keys()),
        key="kpi_comp_sel"
    )
    kpi_comp_sel = KPI_COMP_OPTIONS[kpi_comp_label]

    # Mapping mois → numéro d'ordre 1-12 pour axe X commun
    MOIS_ORD = {
        "jan":1,"fév":2,"mar":3,"avr":4,"mai":5,
        "jun":6,"juin":6,"jul":7,"juil":7,
        "aoû":8,"août":8,"sep":9,"sept":9,
        "oct":10,"nov":11,"déc":12
    }
    MOIS_NOMS = {1:"Jan",2:"Fév",3:"Mar",4:"Avr",5:"Mai",6:"Jun",
                 7:"Jul",8:"Aoû",9:"Sep",10:"Oct",11:"Nov",12:"Déc"}
    MOIS_ORDRE_AFF = [MOIS_NOMS[i] for i in range(1,13)]  # ordre calendaire fixe

    def mois_num(label):
        low = label.strip().lower()[:4]
        for k, v in MOIS_ORD.items():
            if low.startswith(k):
                return v
        return 0

    facteur_aff = 100 if kpi_comp_sel in KPI_EST_RENDEMENT else 1

    fig_sup = go.Figure()
    for ann in annees_choisies:
        dfann = ANNEES[ann].copy()
        if dfann.empty:
            continue
        dfann["mois_n"] = dfann["mois"].apply(mois_num)
        dfann = dfann.sort_values("mois_n")
        # Construire série complète sur 12 mois (None si absent)
        y_full = []
        x_full = []
        for mn in range(1, 13):
            row = dfann[dfann["mois_n"] == mn]
            x_full.append(MOIS_NOMS[mn])
            if row.empty:
                y_full.append(None)
            else:
                val = row[kpi_comp_sel].values[0]
                y_full.append(
                    float(val) * facteur_aff if pd.notna(val) and val != 0 else None
                )
        fig_sup.add_trace(go.Scatter(
            x=x_full, y=y_full,
            mode="lines+markers",
            name=ann_labels[ann],
            line=dict(color=ann_couleurs[ann], width=2.5),
            marker=dict(size=9),
            connectgaps=False,   # NE PAS relier les None — gaps visibles
            hovertemplate=f"<b>{ann}</b><br>%{{x}}<br>{kpi_comp_label} = %{{y:.3f}}<extra></extra>",
        ))

    # Ligne nominale
    if kpi_comp_sel in KPI_NOM_MAP:
        nv = KPI_NOM_MAP[kpi_comp_sel]
        nv_aff = nv * 100 if kpi_comp_sel in KPI_EST_RENDEMENT else nv
        fig_sup.add_hline(
            y=nv_aff,
            line_dash="dash", line_color="#ffd200",
            annotation_text=f"Nominal {nv_aff:.2f}",
            annotation_font_color="#ffd200",
            annotation_position="top right",
        )

    ytitle = "%" if kpi_comp_sel in KPI_EST_RENDEMENT else (
             "COP" if kpi_comp_sel == "COP" else
             "Nm³" if kpi_comp_sel == "gaz" else "kWh")

    fig_sup.update_layout(
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title=ytitle, height=360,
        xaxis=dict(
            categoryorder="array",
            categoryarray=MOIS_ORDRE_AFF,   # force ordre Jan→Déc
            tickfont_size=12,
            title="Mois (axe commun toutes années)",
        ),
        margin=dict(l=60, r=30, t=30, b=50),
        legend=dict(bgcolor="#0b1929", font_size=13,
                    orientation="h", y=1.08, x=0),
    )
    st.plotly_chart(fig_sup, use_container_width=True)

    # ── Graphique 3 : Bilan énergétique annuel comparé ───────────────────────
    st.markdown('<div class="sec-hdr">Bilan énergétique annuel (MWh)</div>',
                unsafe_allow_html=True)

    fig_bilan = go.Figure()
    flux_labels = ["Élec produite","Chaleur récupérée","Froid récupéré","Gaz consommé (PCI)"]
    flux_cols   = ["prod_nette","chaleur","froid","P_gaz"]
    flux_colors = ["#00b4d8","#f7971e","#a0e878","#e63946"]

    for fi, (fl, fc, fcol) in enumerate(zip(flux_labels, flux_cols, flux_colors)):
        fig_bilan.add_trace(go.Bar(
            name=fl,
            x=annees_choisies,
            y=[agreg.get(a,{}).get(fc, 0)/1000 for a in annees_choisies],
            marker_color=fcol, opacity=0.85,
            text=[f"{agreg.get(a,{}).get(fc,0)/1000:.0f}" for a in annees_choisies],
            textposition="outside",
        ))
    fig_bilan.update_layout(
        barmode="group", template="plotly_dark",
        paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="MWh", height=340,
        margin=dict(l=50,r=20,t=20,b=40),
        legend=dict(bgcolor="#0b1929", font_size=12),
    )
    st.plotly_chart(fig_bilan, use_container_width=True)

    # ── Graphique 4 : Bilan financier annuel comparé ─────────────────────────
    st.markdown('<div class="sec-hdr">Bilan financier annuel (DT)</div>',
                unsafe_allow_html=True)

    fig_fin = go.Figure()
    for ann in annees_choisies:
        ag = agreg.get(ann, {})
        if not ag:
            continue
        fig_fin.add_trace(go.Bar(
            name=f"Coût gaz {ann}",
            x=[ann], y=[-ag.get("cout_gaz",0)],
            marker_color="#e63946", opacity=0.85,
            showlegend=(ann == annees_choisies[0]),
            legendgroup="cout",
        ))
        fig_fin.add_trace(go.Bar(
            name=f"Valeur élec {ann}",
            x=[ann], y=[ag.get("val_elec",0)],
            marker_color="#00b4d8", opacity=0.85,
            showlegend=(ann == annees_choisies[0]),
            legendgroup="elec",
        ))
        fig_fin.add_trace(go.Bar(
            name=f"Valeur ch+fr {ann}",
            x=[ann], y=[ag.get("val_chaleur",0)+ag.get("val_froid",0)],
            marker_color="#f7971e", opacity=0.85,
            showlegend=(ann == annees_choisies[0]),
            legendgroup="chfr",
        ))
        fig_fin.add_trace(go.Scatter(
            name=f"Gain net {ann}",
            x=[ann], y=[ag.get("gain",0)],
            mode="markers", marker=dict(size=14, color="#2dc653",
                symbol="diamond"),
            showlegend=(ann == annees_choisies[0]),
            legendgroup="gain",
        ))
    fig_fin.add_hline(y=0, line_color="#555", line_dash="dot")
    fig_fin.update_layout(
        barmode="group", template="plotly_dark",
        paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="DT", height=340,
        margin=dict(l=60,r=20,t=20,b=40),
        legend=dict(bgcolor="#0b1929", font_size=12),
    )
    st.plotly_chart(fig_fin, use_container_width=True)

    # ── Tableau récapitulatif de synthèse ────────────────────────────────────
    st.markdown('<div class="sec-hdr">Tableau récapitulatif de synthèse</div>',
                unsafe_allow_html=True)

    rows_synth = []
    for ann in annees_choisies:
        ag = agreg.get(ann, {})
        if not ag:
            continue
        rows_synth.append({
            "Année":            ann,
            "Mois couverts":    ag["n_mois"],
            "H service (h)":    f"{ag['h_service']:,.0f}",
            "Élec nette (MWh)": f"{ag['prod_nette']/1000:.1f}",
            "Chaleur (MWh)":    f"{ag['chaleur']/1000:.1f}",
            "Froid (MWh)":      f"{ag['froid']/1000:.1f}",
            "Gaz (MNm³)":       f"{ag['gaz_nm3']/1e6:.3f}",
            "η_e":              f"{ag['eta_e']:.1%}",
            "η_th":             f"{ag['eta_th']:.1%}",
            "η_frig":           f"{ag['eta_frig']:.1%}",
            "η_global":         f"{ag['eta_glob']:.1%}",
            "COP moy.":         f"{ag['cop_moy']:.3f}" if not np.isnan(ag.get('cop_moy',np.nan)) else "N/A",
            "Score /100":       f"{ag.get('score_moy',0):.1f}",
            "Gain net (DT)":    f"{ag['gain']:,.0f}",
            "CO₂ net (t)":      f"{ag.get('co2_net',0):.1f}",
            "TEP net":          f"{ag.get('tep_net',0):.1f}",
        })
    # Ligne nominale de référence
    rows_synth.append({
        "Année":            "⭐ Nominal",
        "Mois couverts":    "—",
        "H service (h)":    "—",
        "Élec nette (MWh)": "—",
        "Chaleur (MWh)":    "—",
        "Froid (MWh)":      "—",
        "Gaz (MNm³)":       "—",
        "η_e":              f"{eta_e_nom:.1%}",
        "η_th":             f"{eta_th_nom:.1%}",
        "η_frig":           f"{eta_frig_nom:.1%}",
        "η_global":         f"{eta_glob_nom:.1%}",
        "COP moy.":         f"{cop_nom:.3f}",
        "Score /100":       "100.0",
        "Gain net (DT)":    "—",
        "CO₂ net (t)":      "—",
        "TEP net":          "—",
    })
    st.dataframe(pd.DataFrame(rows_synth), use_container_width=True, hide_index=True)

    # ── Comparaison CO₂ par année ─────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">Bilan CO₂ comparé par année</div>',
                unsafe_allow_html=True)
    fig_co2_ann = go.Figure()
    for ann in annees_choisies:
        ag = agreg.get(ann, {})
        if not ag:
            continue
        fig_co2_ann.add_trace(go.Bar(
            name=f"CO₂ émis {ann}", x=[ann],
            y=[ag.get("co2_emis", 0)],
            marker_color="#e63946", opacity=0.85,
            showlegend=(ann == annees_choisies[0]), legendgroup="emis",
        ))
        fig_co2_ann.add_trace(go.Bar(
            name=f"CO₂ évité {ann}", x=[ann],
            y=[ag.get("co2_evite", 0)],
            marker_color="#2dc653", opacity=0.85,
            showlegend=(ann == annees_choisies[0]), legendgroup="evite",
        ))
        fig_co2_ann.add_trace(go.Scatter(
            name=f"Bilan net {ann}", x=[ann],
            y=[ag.get("co2_net", 0)],
            mode="markers", marker=dict(size=14, color="#ffd200", symbol="diamond"),
            showlegend=(ann == annees_choisies[0]), legendgroup="net",
        ))
    fig_co2_ann.add_hline(y=0, line_color="#555", line_dash="dot")
    fig_co2_ann.update_layout(
        barmode="group", template="plotly_dark",
        paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="tCO₂", height=300,
        margin=dict(l=60, r=20, t=20, b=40),
        legend=dict(bgcolor="#0b1929", font_size=12),
    )
    st.plotly_chart(fig_co2_ann, use_container_width=True)

    st.markdown("""
    <div style="font-size:12px;color:#4d7fa8;padding:10px 14px;
                background:#0b1929;border-radius:6px;border:1px solid #162030;
                margin-top:10px;">
      <strong>Note :</strong> 2024 couvre mai–décembre (7 mois, démarrage trigénération).
      2025 couvre 12 mois complets. 2026 couvre janvier–mars (3 mois).
      Les η annuels sont calculés sur les flux cumulés (pas moyenne des η mensuels).
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
with tab7:

    seuil_eg_crit_r = eta_glob_nom * (1 - seuil_derive_critique)
    seuil_ee_crit_r = eta_e_nom    * (1 - seuil_derive_critique)
    seuil_eth_crit_r= eta_th_nom   * (1 - seuil_derive_critique)
    seuil_cop_crit_r= cop_nom      * (1 - seuil_derive_critique)
    tg  = perf_tag(eta_glob_moy, seuil_eg_crit_r,  eta_glob_nom)
    te  = perf_tag(eta_e_moy,    seuil_ee_crit_r,  eta_e_nom)
    tth = perf_tag(eta_th_moy,   seuil_eth_crit_r, eta_th_nom)
    tc  = perf_tag(cop_moy if not np.isnan(cop_moy) else 0, seuil_cop_crit_r, cop_nom)

    df_derive_r  = detecter_derives_mensuelles(df)
    nb_al        = (df_derive_r["Statut"].isin(["❌ Écart significatif","⛔ Arrêt / N.D."])).sum()
    nb_ok        = (df_derive_r["Statut"] == "✅ Conforme").sum()
    jan_flag = any(df["mois"].str.strip().str.lower().str.startswith("jan"))

    jan_rows = df[df["mois"].str.strip().str.lower().str.startswith("jan")]
    froid_perdu_jan = 0
    if not jan_rows.empty:
        chaleur_jan = jan_rows["chaleur"].values[0]
        froid_perdu_jan = chaleur_jan * cop_nom

    # ── A. SYNTHÈSE GÉNÉRALE ────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">A — Synthèse générale</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rbox">
      <p>
        <strong>Centrale :</strong> Trigénération ADWYA &mdash; Moteur CAT CG170-12,
        P_élec = 1 200 kW &middot; Récupération thermique = 1 270 kW &middot;
        Absorption THERMAX TAC L5 E1 = 802 kW_frig<br>
        <strong>Période :</strong> {periode_t} ({nb_mois} mois analysés)
      </p>
      <h4>Score de performance global</h4>
      <p>
        Score composite (pondéré η_e 30% · η_th 25% · η_frig 20% · COP 25%) :
        <strong style="color:{'#2dc653' if score_perf_moy>=80 else '#ffd200' if score_perf_moy>=60 else '#e63946'};">
          {score_perf_moy:.1f} / 100
        </strong>
        {'<span class="tag-ok">BON</span>' if score_perf_moy>=80
         else '<span class="tag-warn">PARTIEL</span>' if score_perf_moy>=60
         else '<span class="tag-alert">DÉGRADÉ</span>'}
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
        Gaz consommé : <strong>{total_gaz_nm3:,.0f} Nm³</strong> ({total_pgaz/1e6:.3f} GWh_PCI)
      </p>
      <h4>Bilan environnemental (CO₂ &amp; TEP)</h4>
      <p>
        CO₂ émis (gaz consommé) : <strong>{total_co2_gaz:.1f} tCO₂</strong>
        ({total_tep_gaz:.1f} TEP)<br>
        CO₂ évité (énergie récupérée substituée) : <strong style="color:#2dc653;">{total_co2_evite:.1f} tCO₂</strong>
        ({total_tep_evite:.1f} TEP)<br>
        <strong>Bilan net :
          <span style="color:{'#2dc653' if total_co2_net>=0 else '#e63946'};">
            {total_co2_net:+.1f} tCO₂ &mdash; {total_tep_net:+.1f} TEP
          </span>
        </strong>
        {'<span class="tag-ok">ÉVITEMENT NET POSITIF</span>' if total_co2_net>=0
         else '<span class="tag-alert">BILAN DÉFAVORABLE</span>'}<br>
        <span style="font-size:12px;color:#4d7fa8;">
          Coefficients ANME : 0,283 TEP/MWh (élec STEG) · 0,9 TEP/kNm³ (GN) · 2,349 tCO₂/TEP
        </span>
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
      <h4>Alertes dérives</h4>
      <p>
        {nb_al} événements de dérive détectés ({nb_ok} mois conformes sur {nb_mois}).
        {'<span class="tag-alert">Interventions requises.</span>' if nb_al>0
         else '<span class="tag-ok">Aucune alerte.</span>'}
      </p>
    </div>""", unsafe_allow_html=True)

    # ── B. OBSERVATIONS & DIAGNOSTIC — CENTRALE ────────────────────────────
    st.markdown('<div class="sec-hdr">B — Observations & diagnostic technique — Centrale</div>',
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
        <strong>{froid_perdu_jan/1000:.0f} MWh</strong> de froid non produit.<br>
        <strong>COP moyen opérationnel :</strong>
        {f"{cop_moy:.3f}" if not np.isnan(cop_moy) else "N/A"} vs nominal {cop_nom:.2f}.
        Le COP d'août 2024 (0.118) est anormalement bas : la température élevée
        de l'eau de tour en été (&gt;35°C) dégrade fortement les performances de l'absorption.
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

    # ── C. OBSERVATIONS PAR ZONE ────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">C — Observations & diagnostic par zone de production</div>',
                unsafe_allow_html=True)

    # Calculs locaux pour les observations par zone
    _elec_alpha  = totaux_elec["Alpha"]
    _elec_beta   = totaux_elec["Béta"]
    _elec_gamma  = totaux_elec["Gamma"]
    _gaz_alpha   = totaux_gaz["Alpha"]
    _gaz_beta    = totaux_gaz["Béta"]
    _gaz_gamma   = totaux_gaz["Gamma"]
    _eco_alpha   = (_elec_alpha - totaux_elec_obj["Alpha"]) * prix_kwh_steg + \
                   (_gaz_alpha - totaux_gaz_obj["Alpha"]) * prix_gaz_nm3
    _eco_beta    = (_elec_beta  - totaux_elec_obj["Béta"])  * prix_kwh_steg + \
                   (_gaz_beta  - totaux_gaz_obj["Béta"])  * prix_gaz_nm3
    _eco_gamma   = (_elec_gamma - totaux_elec_obj["Gamma"]) * prix_kwh_steg + \
                   (_gaz_gamma - totaux_gaz_obj["Gamma"]) * prix_gaz_nm3

    st.markdown(f"""
    <div class="rbox">

      <div class="zone-alpha">
        <h4>&#128994; Zone Alpha — Fabrication (formes sèches : comprimés, gélules, poudres)</h4>
      </div>

      <p><strong>Profil de consommation :</strong>
        La Zone Alpha est la plus consommatrice en électricité avec
        <strong>{_elec_alpha/1000:.0f} MWh/an</strong>
        ({_elec_alpha/total_usine_elec*100:.1f}% de l'usine).
        Le poste GEG (froid) y représente à lui seul
        {ZONE_DATA_ANNUEL['elec']['GEG (froid)']['Alpha']/1000:.0f} MWh/an
        ({ZONE_DATA_ANNUEL['elec']['GEG (froid)']['Alpha']/_elec_alpha*100:.0f}% de la zone),
        ce qui traduit des besoins frigorifiques intenses liés au conditionnement d'air
        des salles classées.
      </p>

      <p><strong>Interprétation des écarts :</strong>
        Les CTA(s) de la zone Alpha consomment
        {ZONE_DATA_ANNUEL['elec']['CTA']['Alpha']/1000:.0f} MWh/an.
        L'audit révèle que 6 CTA(s) sont vétustes (CTA3, CTA5, CTA6, CTA10, CTA13, CTA14) :
        gaines non étanches, sondes de température erronées, vannes 3 voies by-passées.
        Ces défaillances contraignent le système à abaisser la consigne d'eau glacée en
        dessous de 6°C pour compenser, générant une surconsommation en cascade sur les GEG.
        La température de soufflage mesurée (~12°C) est 6°C en-dessous de l'optimum (18°C),
        ce qui représente une surconsommation d'environ <strong>48%</strong> sur les GEG correspondants.
      </p>

      <p><strong>Gaz naturel :</strong>
        La chaudière à vapeur Alpha consomme {_gaz_alpha/1000:.1f} kNm³/an
        avec un taux de charge moyen de seulement <strong>5,9%</strong> (117 kg/h produits
        sur une capacité de 2 000 kg/h). Ce sous-dimensionnement de charge amplifie les pertes
        fixes (déperditions surfaciques 2,9%, purges 26,8%) et porte le ratio gaz à
        <strong>85 Nm³/tonne</strong> de vapeur vs 70–72 Nm³/tonne en usage optimal.
      </p>

      <p><strong>Observations spécifiques :</strong>
        La récupération de chaleur issue de la trigénération est active pour la zone Alpha
        (circuit EC 300 kW + ECS 370 kW), ce qui réduit la dépendance à la chaudière EC.
        Toutefois, des compteurs d'énergie thermique comptabilisent indûment la chaleur
        de la chaudière EC comme chaleur récupérée lorsque les deux circuits fonctionnent
        simultanément.
      </p>

      <p><strong>Potentiel d'économies identifié :</strong>
        <span class="tag-warn">~{_eco_alpha:,.0f} DT/an réalisables</span>
        principalement via : remplacement des 6 CTA vétustes (économie 87 305 DT/an, TRB 5,5–6,9 ans)
        et centralisation de la production de vapeur (économie 15 633 DT/an, TRB 4,6–5,8 ans).
      </p>

      <div class="zone-beta" style="margin-top:20px;">
        <h4>&#129001; Zone Béta — Conditionnement & formes liquides (sirops, pommades)</h4>
      </div>

      <p><strong>Profil de consommation :</strong>
        La zone Béta consomme <strong>{_elec_beta/1000:.0f} MWh/an</strong> en électricité
        ({_elec_beta/total_usine_elec*100:.1f}% de l'usine) et
        <strong>{_gaz_beta/1000:.0f} kNm³/an</strong> en gaz naturel,
        ce qui en fait le plus grand consommateur de gaz parmi les 3 zones
        ({_gaz_beta/max(total_usine_gaz,1)*100:.0f}% des chaudières usine).
      </p>

      <p><strong>Interprétation des écarts :</strong>
        La spécificité technologique de la zone Béta réside dans ses exigences de
        déshumidification intensive assurées par des Munters à gaz naturel
        ({ZONE_DATA_ANNUEL['gaz_nm3']['Munters']['Béta']/1000:.0f} kNm³/an).
        Cette consommation est structurellement liée aux normes GMP pour les formes liquides.
        La chaudière à eau chaude ({ZONE_DATA_ANNUEL['gaz_nm3']['Chaudière EC']['Béta']/1000:.0f} kNm³/an)
        fonctionne en continu car <strong>aucune récupération de chaleur de la trigénération
        n'est raccordée à cette zone</strong>, contrairement aux zones Alpha et Gamma.
        Il s'agit du déficit structurel le plus significatif de l'installation actuelle.
      </p>

      <p><strong>Observations sur l'air comprimé :</strong>
        Le réseau interne de la zone Béta est en acier galvanisé de diamètre 3/4" (DN20),
        diamètre insuffisant pour le débit requis. La pression en bout de réseau chute à
        6,0–6,5 bars vs 7,5 bars à la sortie du compresseur (perte de charge de 13–20%).
        Ce réseau non bouclé aggrave la situation et contraint le compresseur à maintenir
        une pression de consigne élevée inutilement.
      </p>

      <p><strong>Observations sur les V3V :</strong>
        La majorité des vannes 3 voies (V3V) des CTA de la zone Béta sont by-passées
        (régulation non fonctionnelle). Cela engendre une surconsommation d'eau glacée
        et une moins bonne maîtrise de la température et de l'humidité des salles.
      </p>

      <p><strong>Potentiel d'économies identifié :</strong>
        <span class="tag-alert">~{_eco_beta:,.0f} DT/an réalisables</span>
        via : raccordement de la zone Béta à la récupération de chaleur
        (élimination de la chaudière EC pendant fonctionnement trigénération),
        réhabilitation réseau air comprimé (gain 5–7% consommation compresseur),
        et remplacement V3V (gain estimé 10% sur GEG de la zone).
      </p>

      <div class="zone-gamma" style="margin-top:20px;">
        <h4>&#129002; Zone Gamma — Extension & production mixte</h4>
      </div>

      <p><strong>Profil de consommation :</strong>
        La zone Gamma consomme <strong>{_elec_gamma/1000:.0f} MWh/an</strong> en électricité
        ({_elec_gamma/total_usine_elec*100:.1f}% de l'usine) et
        <strong>{_gaz_gamma/1000:.1f} kNm³/an</strong> en gaz naturel.
        Le poste chaufferies y représente
        {ZONE_DATA_ANNUEL['elec']['Chaufferies']['Gamma']/1000:.0f} MWh/an
        ({ZONE_DATA_ANNUEL['elec']['Chaufferies']['Gamma']/_elec_gamma*100:.0f}% de la zone),
        proportion plus élevée que les autres zones, reflétant la dépendance relative à
        la chaudière à vapeur dédiée.
      </p>

      <p><strong>Interprétation des écarts :</strong>
        La chaudière à vapeur Gamma ({ZONE_DATA_ANNUEL['gaz_nm3']['Chaudière vapeur']['Gamma']/1000:.0f} kNm³/an)
        présente un taux de charge moyen de <strong>21%</strong> (212 kg/h sur 1 000 kg/h de capacité),
        meilleur que la chaudière Alpha mais encore loin de l'optimum.
        Son ratio gaz de <strong>80 Nm³/tonne</strong> de vapeur dépasse de 11% le seuil de référence
        de 72 Nm³/tonne, principalement à cause d'un taux de purge élevé
        (salinité actuelle 1 260 ppm vs 3 000 ppm recommandés).
      </p>

      <p><strong>Points positifs :</strong>
        Les CTA(s) de la zone Gamma sont relativement récents et en meilleur état.
        La récupération de chaleur de la trigénération est active sur cette zone
        (circuit EC Gamma 600 kW), permettant de réduire significativement
        l'usage de la chaudière à eau chaude.
        Le système de gestion technique centralisée (GTC) des CTA Gamma est relativement
        fonctionnel, bien que quelques problèmes de supervision des paramètres persistent.
      </p>

      <p><strong>Anomalie identifiée :</strong>
        Un débordement de la bâche alimentaire de la chaudière Gamma a été constaté
        lors de l'audit, symptôme d'un dysfonctionnement du régulateur de niveau
        ou d'une consigne incorrecte, entraînant des pertes d'eau adoucie et
        une perturbation du bilan thermique de la chaudière.
      </p>

      <p><strong>Potentiel d'économies identifié :</strong>
        <span class="tag-warn">~{_eco_gamma:,.0f} DT/an réalisables</span>
        via : centralisation des deux chaudières vapeur (économie 15 633 DT/an, TRB 4,6–5,8 ans),
        correction de la salinité (réduction purges de 29% à 15%), et optimisation
        de la consigne eau glacée en hiver (+1°C = −3% consommation GEG).
      </p>

    </div>""", unsafe_allow_html=True)

    # ── C2. EAU CHAUDE & EAU GLACÉE — RAPPORT DÉTAILLÉ PAR ZONE ───────────────
    st.markdown('<div class="sec-hdr">C2 — Eau Chaude & Eau Glacée : Observations, Interprétations & Plan d\'action</div>',
                unsafe_allow_html=True)

    # ── C2-1 : OBSERVATIONS EAU CHAUDE ──────────────────────────────────────
    st.markdown("""
    <div class="rbox">
      <h4>&#128338; 1. Observations — Eau Chaude (EC)</h4>

      <div class="zone-alpha">
        <strong>Zone Alpha</strong>
      </div>
      <p>
        La zone Alpha dispose d'une chaudière à eau chaude CHAPPEE XR408 de <strong>348 kW</strong>
        et bénéficie d'une double récupération depuis la trigénération :
        circuit EC (300 kW) et circuit ECS sanitaire (370 kW), soit <strong>670 kW récupérables</strong>.
        Les besoins réels estimés sont de ~300 kW. Pendant le fonctionnement de la trigénération,
        la chaudière EC Alpha est mise à l'arrêt forcé, ce qui est favorable.
        Cependant, le système de comptage thermal ne distingue pas l'énergie produite par la chaudière
        de celle récupérée lorsque les deux circuits sont simultanément actifs, faussant les indicateurs.
        Par ailleurs, le circuit ECS sanitaire est complexe (3 sources primaires : chaudière, vapeur, récupération TRI)
        et nécessite une simplification.
      </p>

      <div class="zone-beta" style="margin-top:14px;">
        <strong>Zone Béta</strong>
      </div>
      <p>
        La zone Béta est alimentée uniquement par la chaudière VIADRUS G700 de <strong>400 kW</strong>.
        <span class="tag-alert">AUCUNE récupération de chaleur depuis la trigénération n'est prévue pour cette zone.</span>
        La chaudière fonctionne en continu, consommant <strong>277 860 Nm³/an</strong> de gaz naturel
        (16,5% de la facture globale usine), soit ~159 771 DT/an.
        Le ballon ECS de 1 000 L est <strong>non calorifugé</strong>, source de pertes thermiques supplémentaires.
        Les conduites d'eau chaude dans la chaufferie Béta sont en majorité non calorifugées.
      </p>

      <div class="zone-gamma" style="margin-top:14px;">
        <strong>Zone Gamma</strong>
      </div>
      <p>
        La zone Gamma dispose d'une chaudière EC de <strong>291 kW</strong> et bénéficie de la récupération
        de chaleur TRI à travers un échangeur de 600 kW. Cette récupération est la plus importante des
        trois zones. Pendant le fonctionnement de la trigénération, la chaudière EC Gamma est à l'arrêt.
        Le ballon ECS de 1 500 L est calorifugé, ce qui est positif.
        Un débordement de la bâche alimentaire de la chaudière vapeur Gamma a été constaté lors de l'audit,
        indiquant un dysfonctionnement du régulateur de niveau.
      </p>

      <h4>&#9203; 2. Interprétation — Eau Chaude</h4>
      <ul style="line-height:2.0;">
        <li>La puissance thermique récupérable totale depuis la TRI est de <strong>1 270 kW</strong>,
          mais ne peut satisfaire simultanément les besoins de l'absorbeur (1 146 kW) ET de l'eau chaude
          des zones. Le réglage à 70% vers le froid limite la chaleur disponible pour l'eau chaude.</li>
        <li>Les besoins réels en eau chaude sont estimés à <strong>~970 kW</strong> pour les 3 zones,
          soit supérieurs à la chaleur disponible après déduction de la part dédiée à l'absorption.
          La gestion de la vanne 3 voies (V3V) de répartition est donc déterminante.</li>
        <li>La zone Béta représente à elle seule <strong>36%</strong> des besoins totaux en EC
          (~350 kW), sans aucune récupération. C'est la lacune la plus critique.</li>
        <li>Les variations de récupération mensuelle observées (pic en hiver, creux en été et lors des pannes)
          confirment que la TRI ne peut pas être la seule source fiable sans contrat de maintenance renforcé.</li>
        <li>Le rendement thermique des chaudières EC est satisfaisant (~90% combustion) mais leur
          fonctionnement à très faible charge en parallèle de la récupération dégrade l'efficacité globale.</li>
      </ul>
    </div>""", unsafe_allow_html=True)

    # ── C2-2 : GRAPHIQUES MENSUELS EC ────────────────────────────────────────
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Énergie thermique récupérée mensuelle par zone (EC)</div>',
                unsafe_allow_html=True)

    # Filtre sur les mois sélectionnés
    df_zm_f = df_zone_monthly[df_zone_monthly["mois"].isin(df["mois"].tolist())].copy()

    fig_ec_month = go.Figure()
    fig_ec_month.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=df_zm_f["ec_alpha_kwh"] / 1000,
        mode="lines+markers", name="EC Alpha (circuit process)",
        line=dict(color="#00b4d8", width=2.5), marker=dict(size=8),
        hovertemplate="<b>EC Alpha</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
        fill="tozeroy", fillcolor="rgba(0,180,216,0.07)",
    ))
    fig_ec_month.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=df_zm_f["ec_alpha_sani_kwh"] / 1000,
        mode="lines+markers", name="ECS Alpha (sanitaire)",
        line=dict(color="#48cae4", width=1.8, dash="dot"), marker=dict(size=6),
        hovertemplate="<b>ECS Alpha</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_ec_month.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=df_zm_f["ec_gamma_total_kwh"] / 1000,
        mode="lines+markers", name="EC Gamma",
        line=dict(color="#a0e878", width=2.5), marker=dict(size=8),
        hovertemplate="<b>EC Gamma</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
        fill="tozeroy", fillcolor="rgba(160,232,120,0.07)",
    ))
    fig_ec_month.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=[0] * len(df_zm_f),
        mode="lines", name="Zone Béta — 0 (sans récup.)",
        line=dict(color="#f7971e", width=1.5, dash="dash"),
        hovertemplate="Zone Béta : aucune récupération<extra></extra>",
    ))
    fig_ec_month.update_layout(
        title="Récupération mensuelle eau chaude par zone (MWh) — Source : données TRI réelles",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="MWh/mois", height=340,
        margin=dict(l=50, r=20, t=50, b=70),
        legend=dict(bgcolor="#0b1929", font_size=11),
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig_ec_month, use_container_width=True)

    # Histogramme empilé EC par zone
    fig_ec_stack = go.Figure()
    fig_ec_stack.add_trace(go.Bar(
        name="EC + ECS Alpha", x=df_zm_f["mois"],
        y=df_zm_f["ec_alpha_total_kwh"] / 1000,
        marker_color="#00b4d8", opacity=0.85,
        hovertemplate="<b>Alpha EC+ECS</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_ec_stack.add_trace(go.Bar(
        name="EC Gamma", x=df_zm_f["mois"],
        y=df_zm_f["ec_gamma_total_kwh"] / 1000,
        marker_color="#a0e878", opacity=0.85,
        hovertemplate="<b>EC Gamma</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_ec_stack.add_trace(go.Bar(
        name="Vers absorbeur (chiller)", x=df_zm_f["mois"],
        y=df_zm_f["ec_chiller_kwh"] / 1000,
        marker_color="#9b72cf", opacity=0.75,
        hovertemplate="<b>Vers absorbeur</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_ec_stack.update_layout(
        barmode="stack",
        title="Répartition mensuelle récupération thermique — EC zones + absorbeur (MWh)",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="MWh", height=310,
        margin=dict(l=50, r=20, t=50, b=70),
        legend=dict(bgcolor="#0b1929", font_size=11),
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig_ec_stack, use_container_width=True)

    # Tableau mensuel EC
    df_ec_tab_r = df_zone_monthly[[
        "mois", "ec_alpha_kwh", "ec_alpha_sani_kwh", "ec_alpha_total_kwh",
        "ec_gamma_total_kwh", "ec_chiller_kwh", "rec_totale_kwh"
    ]].copy()
    df_ec_tab_r.columns = [
        "Mois", "EC Alpha (kWh)", "ECS Alpha (kWh)", "Récup. Alpha total (kWh)",
        "Récup. Gamma (kWh)", "Vers absorbeur (kWh)", "Récup. totale (kWh)"
    ]
    for c in df_ec_tab_r.columns[1:]:
        df_ec_tab_r[c] = df_ec_tab_r[c].apply(lambda x: f"{int(x):,}" if pd.notna(x) and x > 0 else "0")
    st.markdown("**Tableau mensuel — Récupération eau chaude par zone**")
    st.dataframe(df_ec_tab_r, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="arow-yel" style="margin-top:6px;">
      <strong>⚠️ Zone Béta non raccordée :</strong> 277 860 Nm³/an de gaz consommés inutilement
      pendant les heures de fonctionnement de la trigénération. Extension vers Béta estimée à
      ~159 771 DT/an d'économies — investissement ~60 000 DT, TRB &lt; 1 an.
    </div>
    <div class="arow-red" style="margin-top:6px;">
      <strong>🔴 Ballon ECS Béta non calorifugé :</strong> pertes thermiques continues estimées à
      ~5–8% de l'énergie stockée. Calorifugation immédiate recommandée (coût ~500 DT, ROI &lt; 1 mois).
    </div>""", unsafe_allow_html=True)

    # ── C2-3 : OBSERVATIONS EAU GLACÉE ──────────────────────────────────────
    st.markdown("""
    <div class="rbox" style="margin-top:20px;">
      <h4>&#10052; 3. Observations — Eau Glacée (EG)</h4>

      <div class="zone-alpha">
        <strong>Zone Alpha</strong>
      </div>
      <p>
        Le circuit eau glacée Alpha comprend <strong>2 GEG Carrier 30XA</strong>
        (391 kW + 274 kW = 665 kW) et reçoit de l'eau glacée de l'absorbeur TRI (≈ 211 kW partagé).
        3 pompes de retour sont installées mais <strong>toutes 3 fonctionnent simultanément</strong>
        quelle que soit la charge frigorifique, générant une surconsommation électrique.
        Les pompes ont des HMT non concordantes, ce qui crée des déséquilibres hydrauliques.
        <strong>Aucune pompe n'est équipée de variateur de vitesse (VEV).</strong>
        La majorité des V3V de régulation des CTA en zone Alpha sont by-passées.
        La consommation GEG Alpha est de <strong>755 955 kWh/an</strong> (13% de la facture usine).
      </p>

      <div class="zone-beta" style="margin-top:14px;">
        <strong>Zone Béta</strong>
      </div>
      <p>
        Le circuit eau glacée Béta comprend <strong>2 GEG Carrier 30XB</strong>
        (393 kW + 393 kW = 786 kW) et reçoit également de l'eau glacée absorbeur.
        3 pompes en parallèle dont les caractéristiques sont hétérogènes (HMT différentes),
        ce qui dégrade le fonctionnement hydraulique de l'ensemble. Des pompes additionnelles
        sont installées sur la toiture pour alimenter certaines CTA spécifiques.
        <strong>Aucune VEV</strong> sur les pompes EG Béta.
        Les V3V des CTA Béta sont majoritairement by-passées.
        Consommation GEG Béta : <strong>371 177 kWh/an</strong>.
      </p>

      <div class="zone-gamma" style="margin-top:14px;">
        <strong>Zone Gamma</strong>
      </div>
      <p>
        Le circuit eau glacée Gamma comprend <strong>2 GEG Carrier 30XA</strong>
        (503 kW + 503 kW = 1 006 kW) et reçoit de l'eau glacée absorbeur (≈ 213 kW).
        2 pompes identiques DAB (7,5 kW chacune) fonctionnent en permanence.
        <strong>Aucune VEV</strong> sur les pompes EG Gamma.
        L'interconnexion entre les circuits Alpha et Gamma (conduite maintenue fermée) présente
        des goulots d'étranglement hydrauliques limitant l'efficacité de la récupération absorbeur.
        Consommation GEG Gamma : <strong>279 603 kWh/an</strong>.
      </p>

      <h4>&#128200; 4. Interprétation — Eau Glacée</h4>
      <ul style="line-height:2.0;">
        <li>La consommation totale des GEG est de <strong>1 406 735 kWh/an</strong>,
          soit <strong>24,7% de la facture électrique globale</strong> — c'est le plus grand poste
          de consommation électrique de l'usine.</li>
        <li>Le fonctionnement permanent de toutes les pompes, indépendamment de la charge réelle,
          génère une surconsommation estimée à <strong>10% de la consommation des pompes EG</strong>
          (301 861 kWh/an × 10% = ~30 186 kWh/an inutiles).</li>
        <li>La température de consigne eau glacée fixée à <strong>6°C</strong> est trop basse,
          surtout en hiver. Chaque degré supplémentaire économise ~3% sur les GEG.
          Remonter à 7–8°C en hiver permettrait de gagner 3–6% (~42 200–84 400 kWh/an).</li>
        <li>L'arrêt des GEG sans fermeture des vannes correspondantes fait circuler inutilement
          de l'eau glacée dans les évaporateurs à l'arrêt, provoquant des pertes thermiques
          et réduisant l'efficacité des GEG en service.</li>
        <li>La récupération de froid via l'absorbeur TRI est perturbée par le
          sous-débit de la pompe eau de tour (~150 m³/h vs 230 m³/h nominal),
          limitant la puissance frigorifique de l'absorbeur à ~420 kW au lieu des 802 kW nominaux.</li>
        <li>Les COP mesurés des GEG (EER ~3,08–3,24) sont dans les plages nominales
          mais peuvent être dégradés par les températures d'eau glacée trop basses
          et les pertes de charge excessives dans les circuits hydrauliques.</li>
      </ul>
    </div>""", unsafe_allow_html=True)

    # ── C2-4 : GRAPHIQUES MENSUELS EG (FROID PRODUIT) ────────────────────────
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Froid produit mensuel par zone (Absorbeur TRI)</div>',
                unsafe_allow_html=True)

    c_fz1, c_fz2 = st.columns(2)

    with c_fz1:
        fig_froid_line = go.Figure()
        for z_lab, col_f, col_z in [
            ("Alpha", "froid_alpha_kwh", "#00b4d8"),
            ("Béta",  "froid_beta_kwh",  "#f7971e"),
            ("Gamma", "froid_gamma_kwh", "#a0e878"),
        ]:
            fig_froid_line.add_trace(go.Scatter(
                x=df_zm_f["mois"],
                y=df_zm_f[col_f] / 1000,
                mode="lines+markers", name=f"Zone {z_lab}",
                line=dict(color=col_z, width=2.2), marker=dict(size=7),
                hovertemplate=f"<b>Zone {z_lab}</b><br>%{{x}}<br>%{{y:.1f}} MWh<extra></extra>",
            ))
        fig_froid_line.update_layout(
            title="Froid produit (absorbeur) par zone — Évolution mensuelle",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="MWh/mois", height=310,
            margin=dict(l=50, r=20, t=50, b=70),
            legend=dict(bgcolor="#0b1929", font_size=11),
            xaxis=dict(tickangle=-45),
        )
        st.plotly_chart(fig_froid_line, use_container_width=True)

    with c_fz2:
        fig_froid_bar = go.Figure()
        for z_lab, col_f, col_z in [
            ("Alpha", "froid_alpha_kwh", "#00b4d8"),
            ("Béta",  "froid_beta_kwh",  "#f7971e"),
            ("Gamma", "froid_gamma_kwh", "#a0e878"),
        ]:
            fig_froid_bar.add_trace(go.Bar(
                name=f"Zone {z_lab}", x=df_zm_f["mois"],
                y=df_zm_f[col_f] / 1000,
                marker_color=col_z, opacity=0.85,
                hovertemplate=f"<b>Zone {z_lab}</b><br>%{{x}}<br>%{{y:.1f}} MWh<extra></extra>",
            ))
        fig_froid_bar.update_layout(
            barmode="stack",
            title="Froid produit mensuel — répartition par zone (MWh)",
            template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
            yaxis_title="MWh", height=310,
            margin=dict(l=50, r=20, t=50, b=70),
            legend=dict(bgcolor="#0b1929", font_size=11),
            xaxis=dict(tickangle=-45),
        )
        st.plotly_chart(fig_froid_bar, use_container_width=True)

    # Froid total vs Récupération thermique par zone — vue comparative
    st.markdown('<div class="sec-hdr" style="font-size:14px;">Froid produit vs Récupération thermique — Vue comparative mensuelle</div>',
                unsafe_allow_html=True)
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=df_zm_f["froid_total_kwh"] / 1000,
        mode="lines+markers", name="Froid total produit (absorbeur)",
        line=dict(color="#a0e878", width=2.5), marker=dict(size=8),
        fill="tozeroy", fillcolor="rgba(160,232,120,0.07)",
        hovertemplate="<b>Froid total</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_comp.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=df_zm_f["ec_alpha_total_kwh"] / 1000,
        mode="lines+markers", name="Récup. thermique Alpha (EC+ECS)",
        line=dict(color="#00b4d8", width=2), marker=dict(size=7),
        hovertemplate="<b>Récup. Alpha</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_comp.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=df_zm_f["ec_gamma_total_kwh"] / 1000,
        mode="lines+markers", name="Récup. thermique Gamma",
        line=dict(color="#a0e878", width=2, dash="dot"), marker=dict(size=7),
        hovertemplate="<b>Récup. Gamma</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_comp.add_trace(go.Scatter(
        x=df_zm_f["mois"], y=df_zm_f["rec_totale_kwh"] / 1000,
        mode="lines+markers", name="Récup. totale (toutes zones + absorbeur)",
        line=dict(color="#f7971e", width=2.5), marker=dict(size=8),
        hovertemplate="<b>Récup. totale</b><br>%{x}<br>%{y:.1f} MWh<extra></extra>",
    ))
    fig_comp.update_layout(
        title="Froid produit & Récupération thermique par zone — Évolution mensuelle (MWh)",
        template="plotly_dark", paper_bgcolor="#070e1a", plot_bgcolor="#0b1929",
        yaxis_title="MWh/mois", height=360,
        margin=dict(l=50, r=20, t=50, b=70),
        legend=dict(bgcolor="#0b1929", font_size=11),
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Tableau récapitulatif froid par zone
    df_froid_tab = df_zone_monthly[[
        "mois", "froid_total_kwh", "froid_alpha_kwh", "froid_beta_kwh", "froid_gamma_kwh"
    ]].copy()
    df_froid_tab.columns = [
        "Mois", "Froid total (kWh)", "Froid Zone Alpha (kWh)", "Froid Zone Béta (kWh)", "Froid Zone Gamma (kWh)"
    ]
    for c in df_froid_tab.columns[1:]:
        df_froid_tab[c] = df_froid_tab[c].apply(lambda x: f"{int(x):,}" if pd.notna(x) and x > 0 else "0")
    st.markdown("**Tableau mensuel — Froid produit par zone (répartition ≈ 33%/33%/34%)**")
    st.dataframe(df_froid_tab, use_container_width=True, hide_index=True)

    # ── C2-5 : CONCLUSIONS EC/EG ─────────────────────────────────────────────
    _total_rec_alpha_mwh = df_zone_monthly["ec_alpha_total_kwh"].sum() / 1000
    _total_rec_gamma_mwh = df_zone_monthly["ec_gamma_total_kwh"].sum() / 1000
    _total_froid_mwh     = df_zone_monthly["froid_total_kwh"].sum() / 1000
    _total_rec_chil_mwh  = df_zone_monthly["ec_chiller_kwh"].sum() / 1000

    st.markdown(f"""
    <div class="rbox" style="margin-top:16px;">
      <h4>&#9989; 5. Conclusions — Eau Chaude & Eau Glacée</h4>
      <ol style="line-height:2.2;">
        <li>Sur la période analysée ({nb_mois} mois), la trigénération a récupéré
          <strong>{_total_rec_alpha_mwh:.0f} MWh</strong> en Zone Alpha,
          <strong>{_total_rec_gamma_mwh:.0f} MWh</strong> en Zone Gamma et
          <strong>{_total_rec_chil_mwh:.0f} MWh</strong> vers l'absorbeur,
          produisant <strong>{_total_froid_mwh:.0f} MWh</strong> de froid total.
          La récupération est globalement efficace pour les zones Alpha et Gamma.</li>
        <li>La <strong>zone Béta est le point aveugle majeur</strong> du système :
          aucune récupération thermique ni frigorifique, chaudière EC fonctionnant en continu,
          réseau air comprimé sous-dimensionné, V3V by-passées.
          Elle cumule les déficiences et représente le potentiel d'amélioration le plus élevé.</li>
        <li>Le <strong>pompage eau glacée est surdimensionné</strong> dans les 3 zones :
          toutes les pompes fonctionnent en permanence sans asservissement à la charge,
          sans VEV, sans régulation adaptative. Le potentiel d'économies est estimé à
          ~10% de la consommation des GEG + pompes, soit &gt;170 MWh/an.</li>
        <li>Les <strong>V3V by-passées</strong> sur la majorité des CTA des zones Alpha et Béta
          rendent la régulation de l'eau glacée inefficace, forçant les GEG à maintenir
          une température de départ excessivement basse (6°C vs 7–8°C possible).
          C'est un facteur multiplicateur de consommation frigorifique.</li>
        <li>La <strong>machine à absorption fonctionne en dessous de sa capacité nominale</strong>
          (420 kW réels vs 802 kW nominaux), principalement à cause du sous-débit eau de tour.
          Le froid non récupéré représente ~380 kW de capacité inexploitée, obligeant les GEG
          à compenser inutilement.</li>
        <li>Les <strong>pertes thermiques sur canalisations et équipements</strong> sont significatives :
          ballon ECS Béta non calorifugé, vannes vapeur non calorifugées, conduites EC
          chaufferie Béta non isolées. Ces pertes s'accumulent pour représenter 5–8% de l'énergie
          thermique utile distribuée.</li>
      </ol>

      <h4>&#128295; 6. Recommandations & Plan d'action — EC & EG</h4>
      <table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:8px;">
        <tr style="background:#0d2a40;color:#90c2e7;text-align:left;">
          <th style="padding:8px 10px;">Action</th>
          <th style="padding:8px 10px;">Zone</th>
          <th style="padding:8px 10px;">Priorité</th>
          <th style="padding:8px 10px;">Impact</th>
          <th style="padding:8px 10px;">Investissement</th>
          <th style="padding:8px 10px;">TRB</th>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Calorifuger ballon ECS + conduites EC Béta</td>
          <td style="padding:7px 10px;color:#f7971e;font-weight:600;">Béta</td>
          <td style="padding:7px 10px;color:#e63946;font-weight:600;">CRITIQUE</td>
          <td style="padding:7px 10px;">−5 à 8% pertes thermiques</td>
          <td style="padding:7px 10px;">&lt; 1 000 DT</td>
          <td style="padding:7px 10px;">&lt; 1 mois</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Raccorder Zone Béta à la récupération TRI</td>
          <td style="padding:7px 10px;color:#f7971e;font-weight:600;">Béta</td>
          <td style="padding:7px 10px;color:#e63946;font-weight:600;">CRITIQUE</td>
          <td style="padding:7px 10px;">~159 771 DT/an (gaz Béta)</td>
          <td style="padding:7px 10px;">~60 000 DT</td>
          <td style="padding:7px 10px;">&lt; 0.8 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Remplacement pompe eau de tour (débit 230 m³/h)</td>
          <td style="padding:7px 10px;">TRI</td>
          <td style="padding:7px 10px;color:#e63946;font-weight:600;">CRITIQUE</td>
          <td style="padding:7px 10px;">+380 kW froid absorbeur récupéré</td>
          <td style="padding:7px 10px;">~15 000 DT</td>
          <td style="padding:7px 10px;">&lt; 0.5 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Réhabiliter V3V CTA — Zones Alpha & Béta</td>
          <td style="padding:7px 10px;color:#00b4d8;font-weight:600;">Alpha + Béta</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">URGENT</td>
          <td style="padding:7px 10px;">−10% consommation GEG zones</td>
          <td style="padding:7px 10px;">~30 000 DT</td>
          <td style="padding:7px 10px;">~1 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Asservir pompes EG + installer VEV</td>
          <td style="padding:7px 10px;">Toutes</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">URGENT</td>
          <td style="padding:7px 10px;">~51 429 DT/an</td>
          <td style="padding:7px 10px;">230 000 DT</td>
          <td style="padding:7px 10px;">3.3–4.5 ans</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Relever consigne EG 6°C → 7–8°C (hiver)</td>
          <td style="padding:7px 10px;">Toutes</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">URGENT</td>
          <td style="padding:7px 10px;">−3 à 6% conso GEG (~42–84 MWh/an)</td>
          <td style="padding:7px 10px;">0 DT</td>
          <td style="padding:7px 10px;">Immédiat</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Fermer vannes GEG à l'arrêt (procédure)</td>
          <td style="padding:7px 10px;color:#a0e878;font-weight:600;">Gamma</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">Évite pertes circulation à vide</td>
          <td style="padding:7px 10px;">0 DT</td>
          <td style="padding:7px 10px;">Immédiat</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Corriger comptage EC : inhiber chaudière si TRI active</td>
          <td style="padding:7px 10px;color:#00b4d8;font-weight:600;">Alpha</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">Fiabilise indicateurs de performance</td>
          <td style="padding:7px 10px;">~2 000 DT (électrovanne)</td>
          <td style="padding:7px 10px;">Immédiat</td>
        </tr>
        <tr style="background:#0b1929;">
          <td style="padding:7px 10px;">Remplacement CTA vétustes Zone Alpha (3 nouvelles)</td>
          <td style="padding:7px 10px;color:#00b4d8;font-weight:600;">Alpha</td>
          <td style="padding:7px 10px;color:#90c2e7;font-weight:600;">MOYEN TERME</td>
          <td style="padding:7px 10px;">87 305 DT/an (élec + froid)</td>
          <td style="padding:7px 10px;">600 000 DT</td>
          <td style="padding:7px 10px;">5.5–6.9 ans</td>
        </tr>
      </table>

      <div style="margin-top:18px;padding:12px 16px;background:#0d2a40;border-radius:8px;
                  border-left:4px solid #0077b6;font-size:13px;line-height:1.9;">
        <strong style="color:#90c2e7;">📌 Synthèse du potentiel EC & EG :</strong><br>
        &bull; <strong>Actions immédiates (0 investissement)</strong> :
        relever consigne EG, fermer vannes GEG à l'arrêt, corriger procédures d'exploitation
        → gain estimé <strong>~42–84 MWh/an froid</strong>, sans coût.<br>
        &bull; <strong>Court terme (&lt; 1 an)</strong> :
        calorifugation ballon Béta, correction pompe eau de tour, réhabilitation V3V
        → gain estimé <strong>~15 000–30 000 DT/an</strong> pour un investissement &lt; 50 000 DT.<br>
        &bull; <strong>Priorité stratégique</strong> :
        raccordement Béta à la récupération TRI → gain <strong>~159 771 DT/an</strong>
        pour 60 000 DT d'investissement. <span class="tag-ok">TRB &lt; 0.8 an</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── D. CONCLUSIONS ──────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">D — Conclusions</div>', unsafe_allow_html=True)
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
          mais <strong>sous-exploitée en zone Béta</strong> (aucune récupération prévue),
          forçant la chaudière EC Béta à fonctionner en permanence.</li>
        <li><strong>Zone Alpha</strong> : plus grande consommatrice d'électricité de l'usine
          ({totaux_elec["Alpha"]/total_usine_elec*100:.0f}%), avec 6 CTA vétustes à remplacer
          en priorité pour réduire les pertes frigorifiques en cascade.</li>
        <li><strong>Zone Béta</strong> : plus grande consommatrice de gaz naturel (chaudières +
          Munters), structurellement pénalisée par l'absence de récupération thermique de la
          trigénération. L'extension du réseau de récupération vers cette zone constitue
          la priorité d'investissement la plus rentable sur le plan thermique.</li>
        <li><strong>Zone Gamma</strong> : profil le plus équilibré des trois, avec une
          récupération thermique active et des CTA en meilleur état, mais des
          rendements de chaudière vapeur encore perfectibles.</li>
        <li>Le bilan économique est <strong>{'positif' if total_gain>=0 else 'négatif'}
          ({total_gain:+,.0f} DT)</strong> sur la période, confirmant la rentabilité
          de l'installation malgré les incidents.</li>
        <li>Le potentiel d'économies inter-zones identifié par l'audit s'élève à
          <strong>{sum([(totaux_elec[z]-totaux_elec_obj[z])*prix_kwh_steg + (totaux_gaz[z]-totaux_gaz_obj[z])*prix_gaz_nm3 for z in ZONES]):,.0f} DT/an</strong>
          pour un investissement global de 2 044 140 DT (TRB moyen 3,3–4,5 ans).</li>
      </ol>
    </div>""", unsafe_allow_html=True)

    # ── E. PLAN D'ACTIONS & RECOMMANDATIONS ────────────────────────────────
    st.markdown('<div class="sec-hdr">E — Plan d\'actions & recommandations</div>',
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
          <strong>Réhabilitation des vannes 3 voies (V3V) — Zones Alpha & Béta</strong><br>
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
          <strong>Optimisation consigne eau glacée (toutes zones)</strong><br>
          Augmenter la consigne de 6°C à 7–8°C en hiver (gain ~3%/°C sur GEG).
          Automatiser la variation saisonnière. Impact immédiat sur GEG Alpha et Gamma.
        </li>
        <li>
          <strong>Réhabilitation réseau air comprimé zone Béta</strong><br>
          Remplacer la conduite 3/4" par DN40 PPR et boucler le réseau.
          Gain sur la pression de consigne : −0,5 bar → gain ~5% sur consommation compresseur.
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
        <li>
          <strong>Correction salinité chaudières vapeur Alpha & Gamma</strong><br>
          Ajuster les temporisations de purge pour atteindre 3 000 ppm (vs 1 260 ppm actuel).
          Réduction estimée des purges : de 47% à 15% du débit vapeur. Gain GN direct.
        </li>
      </ol>
      <h4>&#128640; Améliorations moyen terme (6–18 mois)</h4>
      <ol style="line-height:2.2;" start="10">
        <li>
          <strong>Extension récupération vers zone Béta</strong><br>
          Installer un 4ème échangeur à plaques + 2 pompes secondaires.
          Éliminer la dépendance à la chaudière eau chaude Béta (277 860 Nm³/an)
          pendant le fonctionnement de la trigénération.
          Économie estimée : 159 771 DT/an sur le seul poste gaz Béta.
        </li>
        <li>
          <strong>Remplacement CTA vétustes — Zone Alpha</strong><br>
          Regrouper 6 CTA en 3 nouvelles unités : double flux, roue libre,
          free-cooling, variateurs de vitesse. Économie : 87 305 DT/an. TRB : 5.5–6.9 ans.
        </li>
        <li>
          <strong>Centralisation chaudières vapeur Alpha + Gamma</strong><br>
          Une seule chaudière de 2 T/h suffit pour les deux zones.
          Réduire le ratio GN de 82 à 72 Nm³/tonne. Économie : 15 633 DT/an. TRB : 4.6–5.8 ans.
        </li>
        <li>
          <strong>GTC zones Alpha & Béta</strong><br>
          Installer un système de gestion technique centralisée avec sondes de
          température et d'humidité fiables, servomoteurs, automate.
          Gain comportemental et énergétique estimé : 10% sur froid et GN. TRB : 10–13.9 ans.
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
          <th style="padding:8px 10px;">Zone(s)</th>
          <th style="padding:8px 10px;">Priorité</th>
          <th style="padding:8px 10px;">Économie estimée</th>
          <th style="padding:8px 10px;">Investissement</th>
          <th style="padding:8px 10px;">TRB</th>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Fiabilisation absorption + pompe tour</td>
          <td style="padding:7px 10px;">Toutes</td>
          <td style="padding:7px 10px;color:#e63946;font-weight:600;">CRITIQUE</td>
          <td style="padding:7px 10px;">&gt;200 MWh froid/an récupéré</td>
          <td style="padding:7px 10px;">Maintenance</td>
          <td style="padding:7px 10px;">&lt; 1 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Batteries condensateurs</td>
          <td style="padding:7px 10px;">Toutes</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">URGENT</td>
          <td style="padding:7px 10px;">89 464 DT/an</td>
          <td style="padding:7px 10px;">23 000 DT</td>
          <td style="padding:7px 10px;">0.2 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Extension récupération vers Béta</td>
          <td style="padding:7px 10px;color:#f7971e;font-weight:600;">Béta</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">~80 000 DT/an (GN)</td>
          <td style="padding:7px 10px;">~60 000 DT</td>
          <td style="padding:7px 10px;">~0.8 an</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Comptabilité énergétique étendue</td>
          <td style="padding:7px 10px;">Toutes</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">62 830 DT/an</td>
          <td style="padding:7px 10px;">290 000 DT</td>
          <td style="padding:7px 10px;">2.3–4.6 ans</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;">
          <td style="padding:7px 10px;">Remplacement CTA vétustes</td>
          <td style="padding:7px 10px;color:#00b4d8;font-weight:600;">Alpha</td>
          <td style="padding:7px 10px;color:#ffd200;font-weight:600;">IMPORTANT</td>
          <td style="padding:7px 10px;">87 305 DT/an</td>
          <td style="padding:7px 10px;">600 000 DT</td>
          <td style="padding:7px 10px;">5.5–6.9 ans</td>
        </tr>
        <tr style="border-bottom:1px solid #1b3352;background:#0b1929;">
          <td style="padding:7px 10px;">Centralisation chaudières vapeur</td>
          <td style="padding:7px 10px;color:#a0e878;font-weight:600;">Alpha+Gamma</td>
          <td style="padding:7px 10px;color:#90c2e7;font-weight:600;">MOYEN TERME</td>
          <td style="padding:7px 10px;">15 633 DT/an</td>
          <td style="padding:7px 10px;">90 000 DT</td>
          <td style="padding:7px 10px;">4.6–5.8 ans</td>
        </tr>
        <tr style="background:#0b1929;">
          <td style="padding:7px 10px;">GTC Alpha & Béta</td>
          <td style="padding:7px 10px;color:#00b4d8;font-weight:600;">Alpha+Béta</td>
          <td style="padding:7px 10px;color:#90c2e7;font-weight:600;">MOYEN TERME</td>
          <td style="padding:7px 10px;">41 150 DT/an</td>
          <td style="padding:7px 10px;">570 000 DT</td>
          <td style="padding:7px 10px;">10–13.9 ans</td>
        </tr>
      </table>
    </div>""", unsafe_allow_html=True)

    # ── F. EXPORT DES DONNÉES ───────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">F — Export des données</div>', unsafe_allow_html=True)

    df_exp = df[["mois","h_service","gaz","prod_nette","chaleur","froid","COP",
                 "eta_e","eta_th","eta_frig","eta_glob",
                 "cout_gaz_dt","val_elec_dt","val_chaleur_dt",
                 "val_froid_dt","gain_global_dt",
                 "tep_gaz","tep_evite_total","tep_net",
                 "co2_gaz","co2_evite_total","co2_net",
                 "score_perf","cause_cop"]].copy()
    df_exp.columns = [
        "Mois","H service (h)","Gaz (Nm³)","Élec nette (kWh)",
        "Chaleur (kWh)","Froid (kWh)","COP",
        "η_e","η_th","η_frig","η_global",
        "Coût gaz (DT)","Valeur élec (DT)","Valeur chaleur (DT)",
        "Valeur froid (DT)","Gain global (DT)",
        "TEP gaz","TEP évitées","TEP nettes",
        "CO₂ émis (t)","CO₂ évité (t)","CO₂ net (t)",
        "Score performance /100","Remarque"
    ]

    # Feuille Énergie par Zone
    rows_zone_export = []
    for usage in ZONE_DATA_ANNUEL["elec"]:
        for z in ZONES:
            rows_zone_export.append({
                "Zone": z, "Type": "Électricité", "Usage": usage,
                "Réel 2024 (kWh/an)":   ZONE_DATA_ANNUEL["elec"][usage][z],
                "Objectif (kWh/an)":     ZONE_DATA_ANNUEL["elec_objectif"][usage][z],
                "Réel 2024 (Nm³/an)":    0,
                "Objectif (Nm³/an)":     0,
            })
    for usage in ZONE_DATA_ANNUEL["gaz_nm3"]:
        for z in ZONES:
            rows_zone_export.append({
                "Zone": z, "Type": "Gaz naturel", "Usage": usage,
                "Réel 2024 (kWh/an)":   0,
                "Objectif (kWh/an)":     0,
                "Réel 2024 (Nm³/an)":    ZONE_DATA_ANNUEL["gaz_nm3"][usage][z],
                "Objectif (Nm³/an)":     ZONE_DATA_ANNUEL["gaz_nm3_objectif"][usage][z],
            })
    df_zone_export = pd.DataFrame(rows_zone_export)

    ce1, ce2 = st.columns(2)
    with ce1:
        csv_b = df_exp.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button("📥 Télécharger CSV (KPI mensuel)", csv_b,
                           "kpi_trigeneration_adwya.csv", mime="text/csv")
    with ce2:
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_exp.to_excel(w, sheet_name="KPI Mensuels", index=False)
            bilan.to_excel(w, sheet_name="Bilan Flux", index=False)
            df_zone_export.to_excel(w, sheet_name="Énergie par Zone", index=False)
            df_eco.to_excel(w, sheet_name="Économies par Zone", index=False)
            # Feuille Eau Chaude par zone
            df_ec_export = pd.DataFrame([{
                "Zone": z,
                "Pu chaudière (kW)": EC_ZONES["pu_chaudiere_kw"][z],
                "Pu récup. TRI (kW)": EC_ZONES["pu_recuperation_kw"][z],
                "Besoin réel (kW)": EC_ZONES["besoin_reel_kw"][z],
                "T départ (°C)": EC_ZONES["T_depart_c"][z],
                "T retour (°C)": EC_ZONES["T_retour_c"][z],
                "Gaz chaudière EC réel (Nm³/an)": EC_ZONES["gaz_chaudiere_nm3"][z],
                "Gaz chaudière EC objectif (Nm³/an)": EC_ZONES["gaz_objectif_nm3"][z],
                "Récup. TRI estimée (kWh/an)": EC_ZONES["energie_recuperee_kwh"][z],
                "Ballon ECS (L)": EC_ZONES["ballon_ecs_L"][z],
                "Ballon calorifugé": EC_ZONES["ballon_calorifuge"][z],
            } for z in ZONES])
            df_ec_export.to_excel(w, sheet_name="Eau Chaude par Zone", index=False)
            # Feuille Eau Glacée par zone
            df_eg_export = pd.DataFrame([{
                "Zone": z,
                "Puissance GEG (kW)": EG_ZONES["pu_geg_kw"][z],
                "Puissance absorption TRI (kW)": EG_ZONES["pu_absorption_kw"][z],
                "Puissance totale (kW)": EG_ZONES["pu_totale_kw"][z],
                "T départ EG (°C)": EG_ZONES["T_depart_eg_c"][z],
                "T retour EG (°C)": EG_ZONES["T_retour_eg_c"][z],
                "EER moyen": EG_ZONES["EER_moyen"][z],
                "Conso GEG réel (kWh/an)": EG_ZONES["energie_geg_kwh"][z],
                "Conso GEG objectif (kWh/an)": EG_ZONES["energie_geg_obj_kwh"][z],
                "Conso pompes réel (kWh/an)": EG_ZONES["energie_pompes_kwh"][z],
                "Conso pompes objectif (kWh/an)": EG_ZONES["energie_pompes_obj_kwh"][z],
                "V3V CTA": EG_ZONES["v3v_etat"][z],
                "VEV pompes": EG_ZONES["vev_pompes"][z],
            } for z in ZONES])
            df_eg_export.to_excel(w, sheet_name="Eau Glacée par Zone", index=False)
            if not df_derive_r.empty:
                df_derive_r[["Mois","KPI","Valeur","Nominal","Écart/Nom",
                              "Var. M/M-1","Statut","Action"]].to_excel(
                    w, sheet_name="Dérives Mensuelles", index=False)
            eco_sheet = df[["mois","cout_gaz_dt","val_elec_dt","val_chaleur_dt",
                            "val_froid_dt","gain_global_dt"]].copy()
            eco_sheet.columns = ["Mois","Coût gaz (DT)","Valeur élec (DT)",
                                  "Valeur chaleur (DT)","Valeur froid (DT)","Gain global (DT)"]
            eco_sheet.to_excel(w, sheet_name="Analyse Économique", index=False)
        buf.seek(0)
        st.download_button("📊 Télécharger Excel (multi-onglets)", buf.read(),
                           "rapport_trigeneration_adwya.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("""
    <div style="font-size:11px;color:#2a4a6a;margin-top:28px;text-align:center;
                padding:10px;border-top:1px solid #162030;">
      Outil de suivi des performances &eacute;nerg&eacute;tiques &mdash;
      Centrale Trig&eacute;n&eacute;ration ADWYA &nbsp;&middot;&nbsp;
      PFE RANIM ZAMMEL 2026
    </div>""", unsafe_allow_html=True)
