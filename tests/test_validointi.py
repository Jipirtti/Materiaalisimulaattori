"""Validointitestit M01–M12.

Jokainen testi vertaa simulaattorin tulosta riippumattomaan lähteeseen: teknisen kortin arvoon,
standardin vaatimusväliin, kirjallisuusarvoon tai Pythonissa erikseen laskettuun käsinlaskuun.
Lähteet ja toleranssien perusteet on kuvattu tiedostossa VALIDOINTI.md.
Kalibrointipisteet (M04a, M06a, M08a) on merkitty erikseen: ne tarkistavat, että sovitus pysyy voimassa,
mutta eivät ole riippumatonta validointia.
"""
import math
import pytest

# ---------- apufunktiot (riippumattomat käsinlaskut) ----------
CONV_HRC = [20, 22, 24, 25, 26, 28, 30, 32, 34, 35, 36, 38, 40, 42, 44, 45, 46, 48, 50, 52, 54, 55, 56, 57, 58, 60, 62, 64, 65, 66, 68]
CONV_HV = [238, 248, 260, 266, 272, 286, 302, 318, 336, 345, 354, 372, 392, 412, 434, 446, 458, 484, 513, 544, 577, 595, 613, 633, 653, 697, 746, 800, 832, 865, 940]


def interp(xs, ys, x):
    if x <= xs[0]:
        return ys[0]
    for i in range(1, len(xs)):
        if x <= xs[i]:
            t = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return ys[i - 1] + t * (ys[i] - ys[i - 1])
    return ys[-1]


def ht(sim, **o):
    return sim.call("heatTreat", o)


def at_depth(res, depth):
    return min(res["prof"], key=lambda q: abs(q["x"] - depth))


# ---------- M01 Ms-lämpötila ----------
@pytest.mark.parametrize("steel,comp,ms_kortti", [
    ("C45", dict(C=0.46, Mn=0.65, Cr=0.20, Mo=0.05, Ni=0.20), 350),
    ("42CrMo4", dict(C=0.42, Mn=0.75, Cr=1.05, Mo=0.22, Ni=0.0), 335),
    ("34CrNiMo6", dict(C=0.34, Mn=0.65, Cr=1.50, Mo=0.22, Ni=1.50), 320),
])
def test_M01_ms_andrews(sim, check, steel, comp, ms_kortti):
    """Andrewsin yhtälö (käsinlasku) ja teknisen kortin Ms (Lucefin)."""
    hand = 539 - 423 * comp["C"] - 30.4 * comp["Mn"] - 12.1 * comp["Cr"] - 7.5 * comp["Mo"] - 17.7 * comp["Ni"]
    ms = sim.call("msAndrews", steel)
    check("M01", f"{steel} Ms Andrews = käsinlasku", ms, hand, 0.001, "°C")
    check("M01", f"{steel} Ms Andrews vs tekninen kortti", ms, ms_kortti, 0.10, "°C")


# ---------- M02 martensiitin kovuus ----------
@pytest.mark.parametrize("steel,C,jd", [("C45", 0.46, 1), ("42CrMo4", 0.42, 1.5), ("34CrNiMo6", 0.34, 1.5)])
def test_M02_martensiitin_kovuus(sim, check, steel, C, jd):
    """100 % martensiitin kovuus (ASTM A255) vs Jominy-kaistan keskiarvo sammutetussa päässä (EN ISO 683-1/-2, Lucefin)."""
    s = sim.call("steels")[steel]
    band = (interp(s["jd"], s["jmin"], jd) + interp(s["jd"], s["jmax"], jd)) / 2
    check("M02", f"{steel} 100 % martensiitti vs Jominy J{jd}", sim.call("hrcM100", C), band, 0.05, "HRC")
    assert sim.call("hrcM100", C) > sim.call("hrcM50", C)


# ---------- M03 Jominy-malli ----------
def test_M03_jominy_jaahtymisnopeus(sim, check):
    """Jäähtymisnopeus 700 °C:ssa: Jominy-käyrästöjen yläakselin likiarvot (ASM Handbook Vol. 4)."""
    J = sim.call("jominy")
    for d, ref in [(1.6, 300.0), (6.4, 70.0), (12.7, 23.0), (25.4, 8.0)]:
        check("M03", f"Jominy {d} mm jäähtymisnopeus 700 °C", interp(J["d"], J["r700"], d), ref, 0.35, "°C/s")
    t = J["t85"]
    assert all(t[i] < t[i + 1] for i in range(0, 100)), "t8/5 ei kasva etäisyyden mukana"


# ---------- M04 nuorrutus 42CrMo4 ----------
def test_M04_42CrMo4_koesauva(sim, check):
    """Kalibrointi (M04a) ja päästökäyrä (M04b): Lucefin 42CrMo4, Ø10 mm, öljy 850 °C."""
    r = ht(sim, proc="qt", steel="42CrMo4", D=10, medium="oljy", Taus=850, Tt=100, tt=1)
    check("M04a", "42CrMo4 Ø10 öljy, sammutettu (kalibrointi)", r["surf"]["hrcq"], 57, 0.05, "HRC")
    r = ht(sim, proc="qt", steel="42CrMo4", D=10, medium="oljy", Taus=850, Tt=600, tt=1)
    check("M04b", "42CrMo4 Ø10 öljy, päästö 600 °C 1 h", r["surf"]["hrc"], 36, 0.05, "HRC")
    r = ht(sim, proc="qt", steel="42CrMo4", D=10, medium="oljy", Taus=850, Tt=400, tt=1)
    check("M04b", "42CrMo4 Ø10 öljy, päästö 400 °C 1 h", r["surf"]["hrc"], 47, 0.05, "HRC")


def test_M05_42CrMo4_EN_ISO_683_2(sim, inrange):
    """Riippumaton tarkistus: EN ISO 683-2, 42CrMo4 +QT, Rm koon mukaan. Koesauva 12,5 mm pinnasta (d > 25 mm)."""
    for D, lo, hi in [(30, 1000, 1200), (60, 900, 1100)]:
        r = ht(sim, proc="qt", steel="42CrMo4", D=D, medium="oljy", Taus=850, Tt=600, tt=1)
        hv = at_depth(r, 12.5)["hv"]
        inrange("M05", f"42CrMo4 Ø{D} öljy, päästö 600 °C: Rm 12,5 mm syvyydellä", 3.1 * hv, lo, hi, "MPa")


# ---------- M06 C45 ----------
def test_M06_C45_karkenevuus(sim, check, inrange):
    """C45: kalibrointi Ø10 vesi (M06a) ja riippumaton karkenevuuden raja (M06b, M06c)."""
    r = ht(sim, proc="qt", steel="C45", D=10, medium="vesi", Taus=830, Tt=100, tt=1)
    check("M06a", "C45 Ø10 vesi, sammutettu (kalibrointi)", r["surf"]["hrcq"], 58, 0.05, "HRC")
    r40 = ht(sim, proc="qt", steel="C45", D=40, medium="vesi", Taus=830, Tt=100, tt=1)
    inrange("M06b", "C45 Ø40 vesi: keskustan martensiittiosuus (ei läpikarkene)", r40["core"]["fM"] * 100, 0, 50, "%")
    r16 = ht(sim, proc="qt", steel="C45", D=16, medium="vesi", Taus=830, Tt=600, tt=1)
    inrange("M06c", "C45 Ø16 vesi, päästö 600 °C: Rm keskustassa (EN ISO 683-1, d ≤ 16 mm)", 3.1 * r16["core"]["hv"], 700, 850, "MPa")


# ---------- M07 induktiokarkaisu ----------
def test_M07_induktio(sim, check, inrange):
    """Tunkeutumissyvyys (käsinlasku) ja pinnan kovuus (EN ISO 683-2, liite: 42CrMo4 vähintään 53 HRC)."""
    for f, T in [(10, 20), (10, 850), (200, 850)]:
        rho = 1.9e-7 + 1.1e-9 * T
        mu = 50 if T < 770 else 1
        hand = 503 * math.sqrt(rho / (mu * f * 1000)) * 1000
        check("M07", f"δ {f} kHz, {T} °C", sim.call("delta", f, T), hand, 0.001, "mm")
    r = ht(sim, proc="ind", steel="42CrMo4", Di=40, prior="qt", Tp=600, f=10, qs=1.0, th=2.0, td=0.3, tqI=10, TtI=180, ttI=1)
    inrange("M07", "42CrMo4 induktio 10 kHz: pinnan kovuus", r["surf"]["hrc"], 53, 60, "HRC")
    inrange("M07", "42CrMo4 induktio 10 kHz: SHD", r["shd"], 1.0, 4.0, "mm")
    r2 = ht(sim, proc="ind", steel="42CrMo4", Di=40, prior="qt", Tp=600, f=200, qs=1.5, th=0.5, td=0.2, tqI=10, TtI=180, ttI=1)
    assert r2["shd"] < r["shd"], "korkeampi taajuus ja lyhyempi aika eivät ohentaneet kerrosta"
    assert r["core"]["hv"] == pytest.approx(sim.call("temperHV", "42CrMo4", 600, 1), rel=0.02), "ytimen nuorrutuskovuus muuttui"


# ---------- M08 nitrohiiletys ----------
def test_M08_nitrohiiletys(sim, check, inrange):
    """Kalibrointi 580 °C 4 h (M08a); riippumattomat: HEF Tufftride (M08b) ja Yildiz ym. 2024 (M08c)."""
    r = ht(sim, proc="nc", steel="42CrMo4", T=580, t=4, ox=False, priorN="qt", TpN=620)
    check("M08a", "42CrMo4 580 °C 4 h yhdistekerros (kalibrointi)", r["cl"], 20, 0.02, "µm")
    check("M08a", "42CrMo4 580 °C 4 h NHD (kalibrointi)", r["nhd"], 0.35, 0.02, "mm")
    for t in (1, 2):
        r = ht(sim, proc="nc", steel="42CrMo4", T=580, t=t, ox=False, priorN="qt", TpN=620)
        inrange("M08b", f"42CrMo4 580 °C {t} h yhdistekerros (HEF: 10–20 µm)", r["cl"], 10, 20, "µm")
    r = ht(sim, proc="nc", steel="42CrMo4", T=570, t=1, ox=False, priorN="qt", TpN=620)
    check("M08c", "42CrMo4 570 °C 1 h NHD (Yildiz ym. 2024: 0,133 mm)", r["nhd"], 0.133, 0.30, "mm")
    assert 600 <= r["HVs"] <= 750 and 700 <= r["HVcl"] <= 1100


# ---------- M09 Fe–C ja vipusääntö ----------
def test_M09_vipusaanto(sim, check):
    """Vipusääntö (käsinlasku) tasapainopiirroksen pisteistä."""
    r = sim.call("lever", 0.4, 700)
    micro = {m["n"]: m["f"] for m in r["micro"]}
    check("M09", "0,40 % C: perliittiosuus", micro["P"] * 100, (0.4 - 0.022) / (0.77 - 0.022) * 100, 0.002, "%")
    xg = interp([738, 756, 773, 795], [0.7, 0.6, 0.5, 0.4], 780)
    r = sim.call("lever", 0.3, 780)
    g = [p for p in r["ph"] if p["n"] == "γ"][0]
    check("M09", "0,30 % C, 780 °C: austeniitin hiili (A3-käyrä)", g["x"], xg, 0.01, "%")
    xa = r["ph"][0]["x"]
    check("M09", "0,30 % C, 780 °C: austeniittiosuus", g["f"] * 100, (0.3 - xa) / (xg - xa) * 100, 0.002, "%")
    r = sim.call("lever", 1.2, 720)
    micro = {m["n"]: m["f"] for m in r["micro"]}
    check("M09", "1,2 % C: esieutektoidinen sementiitti", micro["Fe₃C_pro"] * 100, (1.2 - 0.77) / (6.67 - 0.77) * 100, 0.002, "%")
    assert sim.call("lever", 0.4, 900)["reg"] == "g"


# ---------- M10 martensiitin tetragonaalisuus ----------
@pytest.mark.parametrize("C", [0.4, 0.8, 1.2])
def test_M10_ca_suhde(sim, check, C):
    """c/a = 1 + 0,045·C (Roberts 1953; Bhadeshia & Honeycombe)."""
    L = sim.call("lattice", "bct", C)
    check("M10", f"martensiitin c/a, {C} % C", L["ca"], 1 + 0.045 * C, 0.003)


# ---------- M11 vetokoe ----------
@pytest.mark.parametrize("mat", ["S235", "S355", "C45N", "CrMoQT", "SS", "AL6082", "AL7075", "CU", "TI", "GJS", "GJL"])
def test_M11_vetokoe(sim, check, mat):
    """Käyrästä määritetyt suureet (EN ISO 6892-1) vastaavat materiaalin syöttöarvoja."""
    ev = sim.call("tensile", mat)
    mats = sim.call("materialData")[mat]
    check("M11", f"{mat} Rm", ev["Rm"], mats["Rm"], 0.01, "MPa")
    check("M11", f"{mat} A", ev["A"], mats["A"], 0.02, "%")
    if mats.get("brittle"):
        return
    check("M11", f"{mat} Ag", ev["Ag"], mats["Ag"], 0.02, "%")
    if mats.get("ReH"):
        check("M11", f"{mat} ReH", ev["ReH"], mats["ReH"], 0.01, "MPa")
        check("M11", f"{mat} ReL", ev["ReL"], mats["ReL"], 0.02, "MPa")
    else:
        check("M11", f"{mat} Rp0,2", ev["Rp"], mats["Rp"], 0.01, "MPa")


# ---------- M12 Hollomon–Jaffe ----------
def test_M12_hollomon_jaffe(sim, check):
    """P = T(K)·(20 + log t) (käsinlasku) ja ajan ja lämpötilan vastaavuus."""
    check("M12", "P 600 °C 1 h", sim.call("hjP", 600, 1), 873.15 * 20, 1e-6)
    check("M12", "P 550 °C 10 h", sim.call("hjP", 550, 10), 823.15 * 21, 1e-6)
    hv1 = sim.call("temperHV", "42CrMo4", 550, 1)
    check("M12", "42CrMo4 päästö 550 °C 1 h = päästökäyrä", hv1, interp(CONV_HRC, CONV_HV, 39), 0.005, "HV")
    # sama P: 600 °C 1 h vastaa noin 576 °C 10 h
    T10 = 873.15 * 20 / 21 - 273.15
    check("M12", "sama P eri ajalla", sim.call("temperHV", "42CrMo4", T10, 10), sim.call("temperHV", "42CrMo4", 600, 1), 0.001, "HV")
