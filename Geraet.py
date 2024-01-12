class Device:
    def __init__(self, name, reservierungsbedarf_start, reservierungsbedarf_ende, verantwortlicher, wartungsdatum):
        self.name = name
        self.verantwortlicher = verantwortlicher  # Hier wird ein Objekt der Klasse Nutzer übergeben
        self.wartungsdatum = wartungsdatum
        
        self.reservierungsbedarf_start = reservierungsbedarf_start
        self.reservierungsbedarf_ende = reservierungsbedarf_ende
        self.reservierungs_queue = []
        self.reservierungen = []


    def reservierung_hinzufuegen(self, start_datum, end_datum, reservierender_nutzer):
        neue_reservierung = {
            'start_datum': start_datum,
            'end_datum': end_datum,
            'reservierender_nutzer': reservierender_nutzer
        }

        # Überprüfen, ob die Reservierung mit bestehenden Reservierungen kollidiert
        for reservierung in self.reservierungen:
            if not (neue_reservierung['end_datum'] < reservierung['start_datum'] or neue_reservierung['start_datum'] > reservierung['end_datum']):
                raise ValueError("Reservierung überschneidet sich mit einer bestehenden Reservierung.")

        # Reservierung hinzufügen
        self.reservierungen.append(neue_reservierung)

    def reservierung_entfernen(self, start_datum, end_datum, reservierender_nutzer):
        # Reservierung entfernen
        self.reservierungen = [reservierung for reservierung in self.reservierungen if
                               not (reservierung['start_datum'] == start_datum and reservierung['end_datum'] == end_datum and
                                    reservierung['reservierender_nutzer'] == reservierender_nutzer)]

    def reservierungen_anzeigen(self):
        return self.reservierungen
    
    def wartungsdatum_aendern(self, neues_wartungsdatum):
        self.wartungsdatum = neues_wartungsdatum

    def __str__(self):
        return f"{self.name} (Verantwortlich: {self.verantwortlicher}, Wartungsdatum: {self.wartungsdatum})"