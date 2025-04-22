
import streamlit as st
import pandas as pd

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

def runde_zins(z):
    return round(z * 4) / 4

def berechne_ertrag(np, z_fix, z_var, z_mix, f, v, m):
    z_gesamt = (z_fix * f + z_var * v + z_mix * m) / 100
    return round(np * z_gesamt, 2)

# Szenarien
szenarien = {
    "IST": (neuproduktion, aufsclag_fix, aufsclag_var, aufsclag_mix),
    "1. Halbierte Produktion": (neuproduktion / 2, aufsclag_fix, aufsclag_var, aufsclag_mix),
    "2. Angepasste Preisliste (+0,25%)": (neuproduktion, aufsclag_fix + 0.0025, aufsclag_var + 0.0025, aufsclag_mix + 0.0025),
    "3. Reduzierte Preisliste bei Halbierung (-0,25%)": (neuproduktion / 2, aufsclag_fix - 0.0025, aufsclag_var - 0.0025, aufsclag_mix - 0.0025)
}

data = []
for name, (np, af, av, am) in szenarien.items():
    z_fix = runde_zins(irs) + af
    z_var = runde_zins(euribor) + av
    z_mix = ((runde_zins(irs) + am) + z_var) / 2
    ertrag = berechne_ertrag(np, z_fix, z_var, z_mix, anteil_fix, anteil_var, anteil_mix)
    data.append([name, np, z_fix, z_var, z_mix, ertrag])

df = pd.DataFrame(data, columns=["Szenario", "Neuproduktion", "Zins Fix", "Zins Variabel", "Zins Gemischt", "Zinsertrag"])

st.dataframe(df.style.format({
    "Neuproduktion": "€{:,.0f}", 
    "Zinsertrag": "€{:,.0f}", 
    "Zins Fix": "{:.2%}", 
    "Zins Variabel": "{:.2%}", 
    "Zins Gemischt": "{:.2%}"}))
