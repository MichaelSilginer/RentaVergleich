
import streamlit as st
import pandas as pd
import math

st.title("Rentabilitätsvergleich Wohnbaukredite")

euribor = st.number_input("Euribor 6M (%)", value=2.154) / 100
irs = st.number_input("IRS 15 Jahre (%)", value=2.64) / 100

aufschlag_fix = st.number_input("Aufschlag Fix (%)", value=1.00) / 100
aufschlag_var = st.number_input("Aufschlag Variabel (%)", value=0.90) / 100
aufschlag_mix = st.number_input("Aufschlag Gemischt (%)", value=0.90) / 100

neuproduktion = st.number_input("Jahres-Neuproduktion (€)", value=20000000)

anteil_fix = st.slider("Fix %", 0, 100, 50)
anteil_var = st.slider("Variabel %", 0, 100 - anteil_fix, 30)
anteil_mix = 100 - anteil_fix - anteil_var

def runde_auf_viertel(zins):
    return math.ceil(zins * 4) / 4

def berechne_ertrag(np, z_fix, z_var, z_mix, f, v, m):
    z_gesamt = (z_fix * f + z_var * v + z_mix * m) / 100
    return round(np * z_gesamt, 2)

# Szenarien
szenarien = {
    "IST": (neuproduktion, aufschlag_fix, aufschlag_var, aufschlag_mix),
    "1. Halbierte Produktion": (neuproduktion / 2, aufschlag_fix, aufschlag_var, aufschlag_mix),
    "2. Angepasste Preisliste (+0,25%)": (neuproduktion, aufschlag_fix + 0.0025, aufschlag_var + 0.0025, aufschlag_mix + 0.0025),
    "3. Reduzierte Preisliste bei Halbierung (-0,25%)": (neuproduktion / 2, aufschlag_fix - 0.0025, aufschlag_var - 0.0025, aufschlag_mix - 0.0025)
}

data = []
for name, (np, af, av, am) in szenarien.items():
    z_fix = runde_auf_viertel(irs) + af
    z_var = runde_auf_viertel(euribor) + av
    z_mix = ((runde_auf_viertel(irs) + am) + z_var) / 2
    ertrag = berechne_ertrag(np, z_fix, z_var, z_mix, anteil_fix, anteil_var, anteil_mix)
    data.append([name, np, z_fix, z_var, z_mix, ertrag])

df = pd.DataFrame(data, columns=["Szenario", "Neuproduktion", "Zins Fix", "Zins Variabel", "Zins Gemischt", "Zinsertrag"])

st.dataframe(df.style.format({
    "Neuproduktion": "€{:,.0f}", 
    "Zinsertrag": "€{:,.0f}", 
    "Zins Fix": "{:.2%}", 
    "Zins Variabel": "{:.2%}", 
    "Zins Gemischt": "{:.2%}"}))
