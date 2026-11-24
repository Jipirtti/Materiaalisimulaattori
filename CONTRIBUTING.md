# Kehitysohjeet

Materiaalisimulaattoria kehitetään avoimesti Seinäjoen ammattikorkeakoulussa (SEAMK). Muutokset ja palaute ovat tervetulleita.

## Periaatteet

- Simulaattori on yksi tiedosto (`index.html`) ilman ulkoisia kirjastoja ja käännösvaihetta.
- Laskentamallia koskeva muutos vaatii kaksi asiaa:
  - testin tiedostoon `tests/test_validointi.py`
  - rivin tiedostoon `VALIDOINTI.md`

  Muutetun suureen opettajan validoinnin tila palautetaan arvoon *Ei validoitu*.
- Testin odotusarvo tulee teknisestä kortista, standardista, kirjallisuudesta tai käsinlaskusta. Simulaattorin omia välituloksia ei käytetä odotusarvona.
- Jos vakio sovitetaan lähdearvoon, testi merkitään kalibroinniksi (esim. M04a). Lisäksi tarvitaan vähintään yksi riippumaton tarkistus.

## Koodin rakenne (index.html)

| Osa | Sisältö |
| --- | --- |
| `STEELS` | Teräkset: koostumus, muunnospisteet, Jominy-kaista, päästökäyrä, lujuustaulukko, nitridejä muodostavat seosaineet |
| `MEDIA`, `MATS`, `XS`, `latt` | Sammutusaineet, vetokoemateriaalit, kidehilat |
| `jominy`, `quenchHV`, `martFrac` | Jominy-sauvan simulointi ja sammutuskovuus jäähtymisajasta |
| `radialSim` | Säteittäinen lämmönjohtuminen ja induktiokuumennus |
| `htQT`, `htIND`, `htNC` | Prosessit: nuorrutus, induktiokarkaisu, nitrohiiletys |
| `feC` | Fe–C-piirros ja vipusääntö |
| `tensileCurve`, `tensileEval` | Vetokoekäyrä ja suureiden määritys |
| `cellAtoms`, `drawCell` | Alkeiskopit ja 3D-piirto |
| `drawMicro` | Kaavamainen mikrorakenne |
| `EXAMPLES` | Esimerkit |
| `SimPalaute` | Palautekanava (sama moduuli kuin muissa simulaattoreissa; tekstit ja lomakepohja `1-materiaali.yml` annetaan init-kutsussa) |
| `SimKuva` | Kaavion kopiointi kuvana (sama moduuli kaikissa simulaattoreissa; kaaviot, otsikot, selitteet ja painikkeiden paikat annetaan init-kutsussa) |
| `window.MatSim` | Testirajapinta |

### Uusi teräs

Lisää `STEELS`-olioon koostumus, Ac1, Ac3, Ms, austenitointilämpötilat, Jominy-kaista (`jd`, `jmin`, `jmax`), päästökäyrä (`temper`) ja sen koesauva (`ref`) sekä `nit.X`. Lisää testi M01- ja M02-tyyppisesti ja lähde VALIDOINTI.md:hen.

## Testit

```
pip install -r requirements-test.txt
python -m playwright install chromium
python -m pytest tests -v
```

Ajo kirjoittaa tiedoston `validointiraportti.md`.

## Palaute

Käytä issue-malleja (Tulos ei vastaa odotusta, Virheilmoitus, Kehitysehdotus) tai simulaattorin Palaute-painiketta. Lomake liittää asetukset JSON-muodossa, jotta tilanne voidaan toistaa.
