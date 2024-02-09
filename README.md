# Treenipäiväkirja

Sovellusta käytetään treenipäiväkirjana.

Sovelluksen ominaisuuksia:

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään ja ulos.
- Käyttäjä voi lisätä uuden päiväkirjamerkinnän eli treenin.
- Käyttäjä voi valita treenin päivämäärän, lajin, keston, haastavuuden ja sijainnin sekä kirjoittaa treeniin kuvauksen.
- Käyttäjä voi muokata treeniä ja poistaa treenin.
- Käyttäjä voi hakea sovelluksesta toisen käyttäjän profiilia hakutoiminnolla.
- Käyttäjä voi lisätä toisen käyttäjän kaveriksi.
- Käyttäjä voi määritellä, näkyykö treenipäiväkirja ainoastaan kavereille vai kaikille käyttäjille.
- Käyttäjä voi lisätä treeniin kaverin, jolloin treeni näkyy myös kaverin päiväkirjassa.
- Käyttäjä näkee sovelluksen etusivulla omat sekä mahdollisten kavereiden treenit lisäysjärjestyksessä.
- Käyttäjä näkee statistiikkasivulla treenien määrän viikon, kuukauden ja vuoden aikana.
- Käyttäjä voi määritellä näkyykö statistiikkasivu ainoastaan kavereille vai kaikille käyttäjille.

## Tällä hetkellä

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään ja ulos.
- Käyttäjä voi lisätä uuden päiväkirjamerkinnän eli treenin.
- Käyttäjä näkee sovelluksen etusivulla omat treenit

## Ota sovellus käyttöön näin

Kloonaa tämä repositorio ja siirry sen juurikansioon.

Luo juurikansioon ```bash .env```niminen tiedosto ja määritä sen sisältö näin:
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





