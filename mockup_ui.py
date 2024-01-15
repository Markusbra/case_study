# mockup_ui.py
import streamlit as st
from Geraet import Device
from Nutzer import User
from datetime import datetime, timedelta

# Beispiel-Nutzer und -Gerät für das Mockup
beispiel_nutzer = User(id="nutzer@example.com", name="Max Mustermann", email="nutzer@example.com")
beispiel_geraet = Device(name="Laser-Cutter", verantwortlicher=beispiel_nutzer, wartungsdatum="2024-03-01", reservierungsbedarf_start="2021-03-01", reservierungsbedarf_ende="2021-03-31")

Geräte = ["3D-Drucker", "Laser-Cutter", "CNC-Fräse", "CNC-Drehbank", "Schweißgerät", "Lötkolben", "Oszilloskop", "Multimeter", "Bandsäge", "Ständerbohrmaschine"]

# Hauptablauf für die Nutzerverwaltung
def nutzer_verwaltung():
    st.title("Nutzer-Verwaltung")

    nutzer_name = st.text_input("Name des Nutzers:")
    nutzer_email = st.text_input("E-Mail-Adresse des Nutzers:")

    if st.button("Nutzer anlegen"):
        neuer_nutzer = User(id=nutzer_email, name=nutzer_name, email=nutzer_email)
        st.success(f"Nutzer '{neuer_nutzer.name}' mit E-Mail '{neuer_nutzer.email}' wurde angelegt.")

# Funktion zur Eingabe des Datums und der Uhrzeit im Stunden-Takt zwischen 7:00 und 17:00 Uhr
def get_datetime_input(label):
    current_time = datetime.now()

    # Kalender für die Auswahl des Datums
    selected_date = st.date_input(f"{label} Datum:", min_value=current_time, value=current_time)

    # Überprüfung, ob der ausgewählte Tag ein Sonntag ist
    if selected_date.weekday() == 6:  # Sonntag hat den Wochentags-Index 6
        st.warning("Ruhetag - Sonntags sind keine Termine verfügbar, da die Hochschule geschlossen ist.")
        return None

    # Samstagsbedingung für Uhrzeiten zwischen 8:00 und 12:00 Uhr
    is_saturday = selected_date.weekday() == 5  # Samstag hat den Wochentags-Index 5

    if is_saturday:
        start_time = datetime.combine(selected_date, datetime.strptime("08:00", "%H:%M").time())
        end_time = datetime.combine(selected_date, datetime.strptime("12:00", "%H:%M").time())
    else:
        start_time = datetime.combine(selected_date, datetime.strptime("07:00", "%H:%M").time())
        end_time = datetime.combine(selected_date, datetime.strptime("17:00", "%H:%M").time())

    # Liste aller möglichen Termine im vollen Stunden-Takt
    possible_times = [start_time + timedelta(hours=i) for i in range((end_time - start_time).seconds // 3600 + 1)]

    if not possible_times:
        st.warning("Es sind keine Termine für diesen Tag verfügbar.")
        return None

    # Dropdown-Menü für die Auswahl der Uhrzeit
    selected_time = st.selectbox(f"{label} Uhrzeit:", possible_times, format_func=lambda x: x.strftime("%H:%M"))

    # Zusammenfügen von Datum und ausgewählter Uhrzeit
    selected_datetime = datetime.combine(selected_date, selected_time.time())

    # Überprüfung, ob der ausgewählte Termin in der Zukunft liegt
    if selected_datetime <= current_time:
        st.error("Der ausgewählte Termin liegt in der Vergangenheit. Bitte wählen Sie einen Termin in der Zukunft.")
        return None

    # Anzeige des ausgewählten Datums und der Uhrzeit
    st.write(f"Ausgewählter {label}: {selected_datetime.strftime('%Y-%m-%d %H:%M')}Uhr")

    return selected_datetime

# Hauptablauf für die Geräteverwaltung
def geraet_verwaltung():
    st.title("Geräte-Verwaltung")

    geraet_name = st.selectbox("Gerät:", Geräte)

    # Vorauswahl für Aktion (Warten oder Reservieren)
    aktion = st.radio("Aktion auswählen:", ["Wartungstermin auswählen", "Reservierungszeitraum auswählen"])

    if aktion == "Wartungstermin auswählen":
        # Wartungstermin mit Stundenangabe
        st.write("Wählen Sie einen Wartungstermin:")
        geraet_wartungsdatum = get_datetime_input("Wartungstermin")
        geraet_reservierungsbedarf_start = None
        geraet_reservierungsbedarf_ende = None
    else:  # Reservierungszeitraum auswählen
        geraet_reservierungsbedarf_start = st.date_input("Reservierungsbedarf Startdatum:")
        geraet_reservierungsbedarf_ende = st.date_input("Reservierungsbedarf Enddatum:")

        # Überprüfung, ob der ausgewählte Reservierungszeitraum in der Zukunft liegt
        current_time = datetime.now()
        if geraet_reservierungsbedarf_start < current_time.date():
            st.error("Der ausgewählte Reservierungszeitraum liegt in der Vergangenheit. Bitte wählen Sie einen Termin in der Zukunft.")
            return

        # Überprüfung, ob das Enddatum vor dem Startdatum liegt
        if geraet_reservierungsbedarf_start > geraet_reservierungsbedarf_ende:
            st.error("Das Enddatum darf nicht vor dem Startdatum liegen.")
            return

        # Überprüfung, ob der ausgewählte Start- oder Endtermin ein Sonntag ist
        if geraet_reservierungsbedarf_start.weekday() == 6 or geraet_reservierungsbedarf_ende.weekday() == 6:
            st.warning("Reservierung/ Rückgabe an Sonntagen nicht möglich, da Hochschule geschlossen.")
            return

        # Anzeige des ausgewählten Reservierungszeitraums
        st.write(f"Ausgewählter Reservierungszeitraum: Von {geraet_reservierungsbedarf_start} bis {geraet_reservierungsbedarf_ende}")

        geraet_wartungsdatum = None

    if st.button("Gerät anlegen/ändern"):
        if aktion == "Wartungstermin auswählen":
            # Logik für Wartungstermin
            beispiel_geraet.wartungsdatum_aendern(geraet_wartungsdatum)
            st.success(f"Wartungstermin für '{geraet_name}' wurde auf '{geraet_wartungsdatum}' festgelegt.")
        elif aktion == "Reservierungszeitraum auswählen":
            # Logik für Reservierungszeitraum
            beispiel_geraet.reservierung_hinzufuegen(geraet_reservierungsbedarf_start, geraet_reservierungsbedarf_ende, beispiel_nutzer)
            st.success(f"Gerät '{geraet_name}' wurde mit Reservierungsbedarf von '{geraet_reservierungsbedarf_start}' bis '{geraet_reservierungsbedarf_ende}' angelegt/geändert.")

# Auswahl des Hauptablaufs basierend auf Benutzeraktion
auswahl = st.sidebar.selectbox("Wählen Sie eine Option:", ["Nutzer-Verwaltung", "Geräte-Verwaltung"])

if auswahl == "Nutzer-Verwaltung":
    nutzer_verwaltung()
elif auswahl == "Geräte-Verwaltung":
    geraet_verwaltung()
