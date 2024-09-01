# Treenipäiväkirja

# 🚀 <https://treeniapp.fly.dev/>

Sovellusta käytetään treenipäiväkirjana.

Sovelluksen ominaisuuksia:

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään ja ulos.
- Käyttäjä voi lisätä uuden päiväkirjamerkinnän eli treenin.
- Käyttäjä voi valita treenin päivämäärän, lajin, keston, ja haastavuuden sekä kirjoittaa treeniin kuvauksen.
- Käyttäjä voi kustomoida treenivalikkoa lisäämällä muun treenin. 
- Käyttäjä näkee sovelluksen etusivulla omat treenit lisäysjärjestyksessä.
- Käyttäjä voi hakea sovelluksesta toisen käyttäjän profiilia hakutoiminnolla.
- Käyttäjä voi lisätä toisen käyttäjän kaveriksi.
- Käyttäjä näkee kaverin treenipäiväkirjan.
- Käyttäjä voi lisätä treeniin kaverin, jolloin treeni näkyy myös kaverin päiväkirjassa.
- Käyttäjä näkee statistiikkasivulla tilaston omista treeneistä.

## Ota sovellus käyttöön näin

Kloonaa tämä repositorio ja siirry sen juurikansioon.

Luo juurikansioon ``` .env``` niminen tiedosto ja määritä sen sisältö näin:
```bash
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
Luo virtuaaliympäristö sovellusta varten
```bash
python3 -m venv venv
```
Aktivoi virtuaaliympäristö
```bash
source venv/bin/activate
```
Asenna riippuvuudet
```bash
pip install -r requirements.txt
```
Ota tietokanta käyttöön
```bash
psql < schema.sql
```
Käynnistä sovellus
```bash
flask run
```





