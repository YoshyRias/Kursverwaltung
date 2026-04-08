import sqlite3

def setup_database():
    # 1. Verbindung zur Datenbank herstellen (erstellt die Datei, falls nicht vorhanden)
    db_name = "Marte_Jonas_fitnessstudio.db"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # 2. Tabellen anlegen
    # Tabelle: Trainer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Trainer (
            TID INTEGER PRIMARY KEY,
            Vorname VARCHAR(50),
            Nachname VARCHAR(50),
            Spezialgebiet VARCHAR(30)
        )
    ''')

    # Tabelle: Kurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Kurs (
            KID INTEGER PRIMARY KEY,
            Bezeichnung VARCHAR(50),
            Wochentag VARCHAR(10),
            Uhrzeit VARCHAR(10),
            Max_Teilnehmer INTEGER,
            TID INTEGER,
            FOREIGN KEY (TID) REFERENCES Trainer(TID)
        )
    ''')

    # Tabelle: Teilnehmer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teilnehmer (
            TeID INTEGER PRIMARY KEY,
            Nachname VARCHAR(50),
            Vorname VARCHAR(50),
            EMail VARCHAR(50),
            Beitrittsdatum VARCHAR(10)
        )
    ''')

    # Tabelle: Kurs_Teilnehmer (Verknüpfungstabelle)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Kurs_Teilnehmer (
            KTID INTEGER PRIMARY KEY,
            Anmeldedatum VARCHAR(10),
            KID INTEGER,
            TeID INTEGER,
            FOREIGN KEY (KID) REFERENCES Kurs(KID),
            FOREIGN KEY (TeID) REFERENCES Teilnehmer(TeID)
        )
    ''')

    # 3. Sinnvolle Beispieldaten einfügen
    # Mind. 3 Trainer
    trainer_data = [
        ('Max', 'Mustermann', 'Yoga'),
        ('Sarah', 'Sportlich', 'HIIT'),
        ('Jonas', 'Kraft', 'Bodybuilding')
    ]
    cursor.executemany('INSERT INTO Trainer (Vorname, Nachname, Spezialgebiet) VALUES (?, ?, ?)', trainer_data)

    # Mind. 5 Kurse (TIDs sind 1, 2, 3 nach dem Einfügen)
    kurs_data = [
        ('Morgen Yoga', 'Montag', '08:00', 15, 1),
        ('Power HIIT', 'Dienstag', '18:00', 10, 2),
        ('Rückentraining', 'Mittwoch', '17:00', 12, 1),
        ('Bankdrücken Pro', 'Donnerstag', '19:00', 8, 3),
        ('Stretch & Relax', 'Freitag', '16:00', 20, 2)
    ]
    cursor.executemany('INSERT INTO Kurs (Bezeichnung, Wochentag, Uhrzeit, Max_Teilnehmer, TID) VALUES (?, ?, ?, ?, ?)', kurs_data)

    # Mind. 6 Mitglieder (Teilnehmer)
    teilnehmer_data = [
        ('Müller', 'Anna', 'anna@web.de', '01.01.2024'),
        ('Schmidt', 'Bernd', 'bernd@gmx.de', '15.01.2024'),
        ('Fischer', 'Clara', 'clara@gmail.com', '10.02.2024'),
        ('Weber', 'David', 'david@outlook.com', '20.02.2024'),
        ('Wagner', 'Elena', 'elena@web.de', '05.03.2024'),
        ('Becker', 'Frank', 'frank@gmx.de', '12.03.2024')
    ]
    cursor.executemany('INSERT INTO Teilnehmer (Nachname, Vorname, EMail, Beitrittsdatum) VALUES (?, ?, ?, ?)', teilnehmer_data)

    # Mind. 8 Anmeldungen (Verknüpfung Kurs <-> Teilnehmer)
    anmeldungen_data = [
        ('02.01.2024', 1, 1), # Anna in Yoga
        ('03.01.2024', 1, 2), # Bernd in Yoga
        ('16.01.2024', 2, 2), # Bernd in HIIT
        ('11.02.2024', 2, 3), # Clara in HIIT
        ('21.02.2024', 3, 4), # David in Rückentraining
        ('06.03.2024', 4, 5), # Elena in Bankdrücken
        ('13.03.2024', 5, 6), # Frank in Stretch
        ('14.03.2024', 1, 6)  # Frank in Yoga
    ]
    cursor.executemany('INSERT INTO Kurs_Teilnehmer (Anmeldedatum, KID, TeID) VALUES (?, ?, ?)', anmeldungen_data)

    # Änderungen speichern und Verbindung schließen
    connection.commit()
    connection.close()
    print(f"Datenbank '{db_name}' wurde erfolgreich erstellt und befüllt.")

if __name__ == "__main__":
    setup_database()