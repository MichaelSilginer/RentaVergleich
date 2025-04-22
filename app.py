
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

st.markdown("**Verteilung nach Produkten (Summe = 100 %)**")
anteil_fix = st.slider("Fix (%)", 0, 100, 50)
anteil_var = st.slider("Variabel (%)", 0, 100 - anteil_fix, 30)
anteil_mix = 100 - anteil_fix - anteil_var
st.markdown(f"**Gemischt (%) automatisch berechnet: {anteil_mix}%**")

def runde_auf_naechstes_viertel(zins):
    return math.ceil(zins * 400) / 400  # 1/4 % = 0.0025

def berechne_ertrag(np, z_fix, z_var, z_mix, f, v, m):
    np_fix = np * f / 100
    np_var = np * v / 100
    np_mix = np * m / 100
    ertrag = np_fix * z_fix + np_var * z_var + np_mix * z_mix
    return round(ertrag, 2)

# Szenarien
szenarien = {
    "IST": (neuproduktion, aufschlag_fix, aufschlag_var, aufschlag_mix),
    "1. Halbierte Produktion": (neuproduktion / 2, aufschlag_fix, aufschlag_var, aufschlag_mix),
    "2. Reduzierter Aufschlag (-0,50%)": (neuproduktion, aufschlag_fix - 0.005, aufschlag_var - 0.005, aufschlag_mix - 0.005),
    "3. Halbierte Produktion & -0,50%-Aufschlag": (neuproduktion / 2, aufschlag_fix - 0.005, aufschlag_var - 0.005, aufschlag_mix - 0.005)
}

data = []
for name, (np, af, av, am) in szenarien.items():
    zins_fix = runde_auf_naechstes_viertel(irs) + af
    zins_var = runde_auf_naechstes_viertel(euribor) + av
    zins_mix_fix = runde_auf_naechstes_viertel(irs) + am
    zins_mix_var = runde_auf_naechstes_viertel(euribor) + am
    zins_mix = (zins_mix_fix * 15 + zins_mix_var * 15) / 30  # 15 Jahre fix + 15 Jahre variabel

    ertrag = berechne_ertrag(np, zins_fix, zins_var, zins_mix, anteil_fix, anteil_var, anteil_mix)
    data.append([name, np, zins_fix, zins_var, zins_mix, ertrag])

df = pd.DataFrame(data, columns=["Szenario", "Neuproduktion", "Zins Fix", "Zins Variabel", "Zins Gemischt", "Zinsertrag"])

st.dataframe(df.style.format({
    "Neuproduktion": "€{:,.0f}", 
    "Zinsertrag": "€{:,.0f}", 
    "Zins Fix": "{:.2%}", 
    "Zins Variabel": "{:.2%}", 
    "Zins Gemischt": "{:.2%}"}))
