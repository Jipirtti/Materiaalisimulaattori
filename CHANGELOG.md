# Muutosloki

## Julkaisematon

- Kopioi kuva: kuvan otsikko ja PNG-tiedoston nimi valitulla kielellä (aiemmin piirikaavion ja oskilloskoopin otsikko jäi suomeksi englannin- ja saksankielisessä kuvassa). Uusi testi KV10 tarkistaa, että jokaisen kaavion kuvassa on vain valitun kielen tekstejä.
- Saksankielinen käyttöliittymä (FI | EN | DE -valitsin, `?lang=de`, selaimen kieli de). Termit tarkistettu saksalaisista standardeista ja alan termistöstä. Kielitestit tarkistavat, ettei saksankielisessä näkymässä ole kääntämättömiä rivejä.
- Käyttöohje englanniksi (`docs/user-manual.md`) ja saksaksi (`docs/bedienungsanleitung.md`) omilla kuvakaappauksilla (`docs/kuvat/en/`, `docs/kuvat/de/`). `tools/rakenna_ohje.py` rakentaa kaikki kolme HTML-sivua, ja simulaattorin Käyttöohje-linkki avaa valitun kielen ohjeen.
- Kopioi kuva -painike jokaiseen kaavioon: kaavio leikepöydälle PNG-kuvana vaalealla taustalla ja kaksinkertaisella tarkkuudella, otsikon, selitteen ja lähdemerkinnän kanssa. Jos selain estää kopioinnin, kuva avautuu ikkunaan tallennettavaksi. Yhteinen SimKuva-moduuli kaikissa simulaattoreissa. Testit KV01–KV04.

## 1.0.0 – 2026-11-19

- Ensimmäinen julkaisu.
- Lämpökäsittely teräksille C45E, 42CrMo4 ja 34CrNiMo6:
  - nuorrutus: säteittäinen lämmönjohtumismalli, Jominy-ekvivalenssi, martensiittiosuus ja Hollomon–Jaffe-päästö
  - induktiokarkaisu: taajuudesta ja lämpötilasta riippuva tehon tunkeutuminen, austenitoituminen huippulämpötilasta, lähtötilan lisäpäästö ja SHD
  - nitrohiiletys ja mustanitraus: yhdistekerros, diffuusiovyöhyke, NHD, oksidikerros ja ytimen pehmeneminen
  - kaavamainen mikrorakenne syvyyden funktiona, faasiosuudet valitulla syvyydellä ja varoitukset
- Kiderakenne: tkk, pkk, martensiitti, Bainin muunnos, γ′-Fe₄N ja ε-Fe₂₋₃N, välisijat.
- Fe–C-piirros ja vipusääntö.
- Vetokoe: 12 materiaalia, lämpökäsittelyn tulos, vertailukäyrä ja kovuusmuunnin.
- Suomi ja englanti, Palaute-painike, käyttöohje.
- Validointitestit M01–M12, kielitestit K01–K03, käyttötestit U01–U08 ja palautetestit P01–P07.
