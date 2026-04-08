import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

@anvil.server.callable
def query_database_kursid(name:str):
  query = f'SELECT kid FROM Kurs WHERE bezeichnung="{name}"'
  with sqlite3.connect(data_files["Marte_Jonas_fitnessstudio.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result

@anvil.server.callable
def query_database_dict_kurse():
  query = """
    SELECT 
      K.Bezeichnung, 
      K.Wochentag, 
      K.Uhrzeit, 
      T.Nachname || ' ' || T.Vorname AS Name,
      (SELECT COUNT(*) FROM Kurs_Teilnehmer KT WHERE KT.KID = K.KID) || '/' || K.Max_Teilnehmer AS Anz_Teilnehmer
    FROM Kurs K
    JOIN Trainer T ON K.TID = T.TID"""
  
  with sqlite3.connect(data_files["Marte_Jonas_fitnessstudio.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def query_database_namen(id:int):
  query = f'''
    SELECT vorname || " " || nachname AS name 
    FROM Teilnehmer 
    WHERE TeID NOT IN (
        SELECT TeID 
        FROM Kurs_Teilnehmer 
        WHERE KID = {id})'''
  with sqlite3.connect(data_files["Marte_Jonas_fitnessstudio.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result

@anvil.server.callable
def query_database_insert_into_kurs(id:int, name:str):
  query = f'''
    INSERT INTO Kurs_Teilnehmer (Anmeldedatum, KID, TeID)
    VALUES (date('now'), {id}, (SELECT TeID FROM Teilnehmer WHERE nachname || " " || vorname = "{name}" LIMIT 1))'''
  with sqlite3.connect(data_files["Marte_Jonas_fitnessstudio.db"]) as conn:
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()