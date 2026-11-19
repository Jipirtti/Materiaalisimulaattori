# Validointisuunnitelma

Simulaattorin tulokset validoidaan kahdella tasolla:

1. **Automaattinen regressiovalidointi:** testit kansiossa `tests/` vertaavat simulaattorin tuloksia teknisiin kortteihin, standardien vaatimusväleihin, kirjallisuusarvoihin ja Pythonissa erikseen laskettuihin käsinlaskuihin. GitHub Actions ajaa testit jokaisesta muutoksesta ja maanantaisin.
2. **Opettajan validointi:** vastuuopettaja tarkistaa jokaisen rivin simulaattorissa ja vertaa sitä lähteeseen, standardiin tai laboratoriomittaukseen (esim. Jominy-koe, kovuusprofiili, vetokoe). Tulos kirjataan tähän tiedostoon (päivämäärä, validoija, menetelmä). Validointikierros avautuu issueksi automaattisesti 15.1. ja 15.8.

Kun laskentamallia muutetaan, muutoksen koskemat rivit palautetaan tilaan *Ei validoitu*.

**Kalibrointi ja validointi erotetaan.** Kolme vakiota on sovitettu yksittäiseen lähdearvoon (taulukko alla). Näitä vastaavat testit (M04a, M06a, M08a) varmistavat vain, että sovitus pysyy voimassa. Riippumaton validointi tehdään muilla arvoilla.

## Mallit ja vakiot

| Suure | Arvo | Peruste |
| --- | --- | --- |
| Teräksen lämmönjohtavuus λ(T) | max(24, 48 − 0,03·T) W/(m·K) | Seostamattoman ja niukkaseosteisen teräksen likiarvo |
| Ominaislämpö c(T) | 460 + 0,33·T + 450·exp(−((T − 745)/45)²) J/(kg·K) | Magneettisen muutoksen huippu noin 745 °C; faasimuutosten latenttia lämpöä ei mallinneta |
| Tiheys | 7800 kg/m³ | |
| Sammutusaineet, tehollinen h välillä 800–500 °C | öljy 2000, polymeeri 3500, vesi 6000, suihku 15 000 W/(m²·K); ilma: konvektio + säteily | Kirjallisuuden vaihteluväleiltä (Totten 2006; Liščić). **Kalibrointi:** öljy → M04a, vesi → M06a |
| Jominy-sauva | Ø25 × 100 mm, päädyn h = 15 000 W/(m²·K), vaipalla ilma | Jäähtymisnopeus 700 °C:ssa vastaa Jominy-käyrästöjen likiarvoja (M03) |
| Sammutuskovuus | t8/5 → Jominy-etäisyys samalla t8/5:llä → Jominy-kaista (Lucefin) | Jominy-ekvivalenssi (Krauss 2015; Totten 2006) |
| Martensiittiosuus | 100 %: ASTM A255 -polynomi; 50 %: Hodge–Orehoski | |
| Päästö | P = T(K)·(20 + log₁₀ t[h]); päästökäyrä 1 h; HV_t = HV_q − f_M·max(0, HV_M − HV_taulukko(P)) | Hollomon & Jaffe 1945; tekninen kortti |
| Lujuus | Rm ≈ 3,1·HV; Rp0,2/Rm ja A teknisen kortin päästötaulukosta samalla Rm:llä | ISO 18265 -tyyppinen likiarvo |
| Induktio: sähkönjohtavuus ja permeabiliteetti | ρ = 1,9·10⁻⁷ + 1,1·10⁻⁹·T Ω·m; μr = 50 (T < 770 °C), 1 (T ≥ 770 °C) | Rudnev ym. 2017 (suuruusluokat) |
| Induktio: austenitoituminen | lineaarisesti Ac1 + 50 °C … Ac3 + 100 °C huippulämpötilasta | Nopean kuumennuksen muunnospisteiden siirtymä (Rudnev ym. 2017) |
| Induktio: SHD | syvyys, jossa kovuus = 0,8 × pinnan kovuus | ISO 18203 |
| Nitrohiiletys: yhdistekerros | x = k·√t, k(580 °C) = 10 µm/√h, Q = 100 kJ/mol | **Kalibrointi:** 580 °C 4 h → 20 µm (M08a) |
| Nitrohiiletys: NHD | kD(580 °C) = 0,175 mm/√h · √(1,77/(X + 0,5)), X = Cr + Mo; Q = 77 kJ/mol | Wagnerin sisäisen nitrauksen skaalaus; **kalibrointi:** 42CrMo4 580 °C 4 h → 0,35 mm |
| Nitrohiiletys: kovuudet | diffuusiovyöhykkeen pinta 300 + 280·X HV, yhdistekerros 700 + 200·X HV; profiili eksponentiaalinen, NHD = ydin + 50 HV | ISO 18203; suuruusluokat Mittemeijer & Somers 2015 |
| Oksidikerros | ≈ 1 µm, 400 °C 15 min (likiarvo) | Suuruusluokka QPQ-prosesseissa (HEF) |
| Fe–C | A3-pisteet taulukosta, Acm suora (0,77; 727)–(2,11; 1148), A1 = 727 °C, P = 0,022 % | Fe–Fe₃C-tasapainopiirros |
| Martensiitin hila | a = 2,866 − 0,013·C Å, c = 2,866 + 0,116·C Å | c/a = 1 + 0,045·C (Roberts 1953) |
| Vetokoe | σt = σu·(1 + c − c·exp((εu − εp)/c)), Considèren ehto Ag:ssä | Sovitus Rp0,2:een tai Lüdersin venymän loppuun |

## M. Automaattisesti testatut suureet (tests/test_validointi.py)

| ID | Suure | Lähde | Odotettu | Tol. | Opettajan validointi |
| --- | --- | --- | --- | --- | --- |
| M01 | Ms Andrewsin yhtälöllä, C45, 42CrMo4, 34CrNiMo6 | Käsinlasku; Lucefin tekninen kortti | 318 / 324 / 329 °C; kortti 350 / 335 / 320 °C | 0,1 % / 10 % | Ei validoitu |
| M02 | 100 % martensiitin kovuus | Jominy-kaistan keskiarvo sammutetussa päässä (Lucefin, EN ISO 683) | 58,5 / 57 / 54 HRC | 5 % | Ei validoitu |
| M03 | Jominy-sauvan jäähtymisnopeus 700 °C:ssa 1,6 / 6,4 / 12,7 / 25,4 mm | Jominy-käyrästöjen yläakselin likiarvot (ASM Handbook Vol. 4). **Tarkista lähdearvot opettajan validoinnissa.** | 300 / 70 / 23 / 8 °C/s | 35 % | Ei validoitu |
| M04a | 42CrMo4 Ø10 öljy, sammutettu (kalibrointi) | Lucefin, päästökäyrän koesauva | 57 HRC | 5 % | Ei validoitu |
| M04b | 42CrMo4 Ø10 öljy, päästö 400 ja 600 °C | Lucefin päästökäyrä | 47 / 36 HRC | 5 % | Ei validoitu |
| M05 | 42CrMo4 Ø30 ja Ø60 öljy, päästö 600 °C, Rm 12,5 mm syvyydellä | EN ISO 683-2, +QT: 16 < d ≤ 40 mm 1000–1200 MPa; 40 < d ≤ 100 mm 900–1100 MPa | vaatimusväli | – | Ei validoitu |
| M06a | C45 Ø10 vesi, sammutettu (kalibrointi) | Lucefin, päästökäyrän koesauva | 58 HRC | 5 % | Ei validoitu |
| M06b | C45 Ø40 vesi, keskustan martensiittiosuus | Seostamattoman teräksen heikko karkenevuus | < 50 % | – | Ei validoitu |
| M06c | C45 Ø16 vesi, päästö 600 °C, Rm keskustassa | EN ISO 683-1, +QT d ≤ 16 mm: 700–850 MPa | vaatimusväli | – | Ei validoitu |
| M07 | Tunkeutumissyvyys δ; 42CrMo4 induktiokarkaisun pintakovuus ja SHD | Käsinlasku; EN ISO 683-2 (pintakarkaisu, 42CrMo4 vähintään 53 HRC) | δ käsinlaskusta; 53–60 HRC; SHD 1–4 mm | 0,1 % / väli | Ei validoitu |
| M08a | 42CrMo4 580 °C 4 h: yhdistekerros ja NHD (kalibrointi) | Sovituspiste | 20 µm, 0,35 mm | 2 % | Ei validoitu |
| M08b | 42CrMo4 580 °C 1 h ja 2 h: yhdistekerros | HEF Tufftride: 10–20 µm 1–2 h:ssa | vaatimusväli | – | Ei validoitu |
| M08c | 42CrMo4 570 °C 1 h: NHD | Yildiz ym. 2024 | 0,133 mm | 30 % | Ei validoitu |
| M09 | Vipusääntö: perliitti 0,40 % C; austeniitti 0,30 % C 780 °C; sementiitti 1,2 % C | Käsinlasku piirroksen pisteistä | 50,5 % / 62,8 % / 7,3 % | 0,2 % | Ei validoitu |
| M10 | Martensiitin c/a 0,4 / 0,8 / 1,2 % C | Roberts 1953 | 1,018 / 1,036 / 1,054 | 0,3 % | Ei validoitu |
| M11 | Vetokokeen suureet käyrästä, 11 materiaalia | Syöttöarvot (EN ISO 6892-1:n määritelmät) | Rm, Rp0,2, ReH, ReL, Ag, A | 1–2 % | Ei validoitu |
| M12 | Hollomon–Jaffe-parametri ja ajan–lämpötilan vastaavuus | Käsinlasku | P(600 °C, 1 h) = 17 463 | 0,1 % | Ei validoitu |

## Viimeisimmän ajon tulokset

Ajo 2026-11-19: 87 tarkistusta, kaikki hyväksytty. Huomioita:

- M05: Ø30 antaa Rm 1004 MPa ja Ø60 901 MPa, eli molemmat ovat vaatimusvälin alarajalla. Malli arvioi läpikarkenevuuden varovaisesti.
- M08c: NHD 0,164 mm vs 0,133 mm (+23 %).
- M03: 1,6 mm:n jäähtymisnopeus on 347 °C/s vs 300 °C/s (+16 %).

## Mallin rajoitukset

- Faasimuutosten latenttia lämpöä ja muutosjännityksiä ei mallinneta. Säröriskistä annetaan vain varoitus.
- Sammutuskovuus perustuu Jominy-ekvivalenssiin. Jatkuvan jäähtymisen (CCT) muutoskinetiikkaa ei lasketa erikseen.
- Induktiokuumennus on paikallaan tapahtuva koko vaipan kuumennus ilman induktorin geometriaa. Sähkömagneettinen kenttä on yksinkertaistettu eksponentiaaliseksi tehojakaumaksi.
- Nitrohiiletyksen kerrospaksuudet ovat parabolisen kasvulain likiarvoja. Kaasun nitrauspotentiaalia, suolan koostumusta ja huokoisuutta ei mallinneta.
- Mikrorakennekuva on kaavamainen: faasiosuudet ovat mallin mukaiset, mutta raekoko ja muodot eivät ole mittakaavassa.
- Tulokset ovat opetuskäyttöön tarkoitettuja likiarvoja. Niitä ei voi käyttää lämpökäsittelyohjeena tai lujuuslaskennan lähtöarvoina.

## B. Opettajan validointi ilman automaattitestiä

| ID | Asia | Menetelmä | Tila |
| --- | --- | --- | --- |
| MB1 | Mikrorakennekuvien vastaavuus oikeisiin hieisiin (martensiitti, bainiitti, perliitti, yhdistekerros) | Vertailu laboratorion hieisiin tai ASM Micrograph Database -kuviin | Ei validoitu |
| MB2 | Induktiokarkaisun kovuusprofiilin muoto | Vertailu mitattuun kovuusprofiiliin (HV1) | Ei validoitu |
| MB3 | Kidehilojen esitys ja selitystekstit | Vertailu oppikirjaan (Bhadeshia & Honeycombe) | Ei validoitu |
