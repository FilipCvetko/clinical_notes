import airtable
import pandas as pd
import streamlit as st

def insert_app():
    with open("./data/raw/specializacije.txt", "r") as file:
        specializacije = [line.strip() for line in file.readlines()]

    klinicni_primeri = airtable.Airtable(
        st.secrets["AIRTABLE_BASE_ID"], "klinicni_primeri", st.secrets["AIRTABLE_API_KEY"]
    )

    predloge = airtable.Airtable(
        base_id=st.secrets["AIRTABLE_BASE_ID"],
        table_name="specializacije_predloge",
        api_key=st.secrets["AIRTABLE_API_KEY"],
    )

    pomoč = airtable.Airtable(
        base_id=st.secrets["AIRTABLE_BASE_ID"], table_name="pomoč", api_key=st.secrets["AIRTABLE_API_KEY"]
    )

    icd10 = pd.read_csv("./data/raw/icd10.csv")
    icd10_list = [item.values[0] + ": " + item.values[1] for _, item in icd10.iterrows()]

    specializacija = st.multiselect("Specializacija", options=specializacije)

    if len(specializacija) > 0:
        izbrana_specializacija = specializacija[0]

        predloga = predloge.search("Specializacija", izbrana_specializacija)
        if len(predloga) == 0:
            predloga_anamneza = predloga_status = ""
        else:
            predloga_anamneza = predloga[0]["fields"]["Anamneza"]
            predloga_status = predloga[0]["fields"]["Status"]

        anamneza = st.text_area("ANAMNEZA", value=predloga_anamneza, height=200)
        status = st.text_area("STATUS", value=predloga_status, height=300)

        diferencialne = st.multiselect("DIFERENCIALNA DIAGNOZA", options=icd10_list)

        if st.button("Oddaj"):
            klinicni_primeri.insert(
                {
                    "Specializacija": specializacija,
                    "Anamneza": anamneza,
                    "Status": status,
                    "Diferencialna diagnoza": diferencialne,
                },
                typecast=True,
            )
            st.balloons()

        if st.button("Pomoč"):
            najdena_pomoč = pomoč.search("Specializacija", izbrana_specializacija)
            if len(najdena_pomoč) == 0:
                st.write(
                    "Trenutno še ni spisane predloge za to specializacijo.\n Lahko pa pomagaš pri soustvaritvi: \n https://airtable.com/appfquHGRiLr47uFk/tblV9kOjOqJwzsR7Z/viwxVCWilSrHVRahy?blocks=hide"
                )
            else:
                najdena_pomoč = najdena_pomoč[0]["fields"]["Vsebina"]
                st.write(najdena_pomoč)
