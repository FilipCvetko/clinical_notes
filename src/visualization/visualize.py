import streamlit as st
import pandas as pd
import requests
import json
import airtable

with open("./data/raw/specializacije.txt", "r") as file:
    specializacije = [line.strip() for line in file.readlines()]

airtable = airtable.Airtable(base_id='appfquHGRiLr47uFk', table_name='klinicni_primeri', api_key=st.secrets["AIRTABLE_API_KEY"])

icd10 = pd.read_csv("./data/raw/icd10.csv")
icd10_list = [item.values[0] + ": " + item.values[1] for _, item in icd10.iterrows()]

specializacija = st.multiselect("SPECIALIZACIJA", options=specializacije)

if len(specializacija) > 0:
    izbrana_specializacija = specializacija[0].lower()

    with open(f"./data/raw/specializacije_predloge/{izbrana_specializacija}.json") as file:
        predloga = json.load(file)

        anamneza = st.text_area("ANAMNEZA", value=predloga["anamneza"], key="anamneza", height=200)
        status = st.text_area("STATUS", value=predloga["status"], height=200)

        diferencialne = st.multiselect("DIFERENCIALNA DIAGNOZA", options=icd10_list)

        if st.button("Oddaj"):
            airtable.insert({
                "Specializacija" : specializacija,
                "Anamneza" : anamneza,
                "Status" : status,
                "Diferencialna diagnoza" : diferencialne
            }, typecast=True)

        if st.button("Pomoč"):
            st.write("Pomoč na poti")
