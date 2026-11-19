"""Käytettävyystestit U01–U08: esimerkit, välilehdet, tallennus, klikkaukset ja varoitukset."""
import json


def test_U01_esimerkit_latautuvat(sim):
    """Jokainen esimerkki latautuu ilman virheitä ja piirtää kovuusprofiilin."""
    for e in sim.call("examples"):
        assert sim.call("loadExample", e["id"])
        sim.page.wait_for_timeout(80)
        rows = sim.js("document.querySelectorAll('#htRes tr').length")
        assert rows >= 5, f"U01 ({e['id']}): tulostaulukko puuttuu"


def test_U02_valilehdet(sim):
    for t in ["ht", "xs", "fec", "tt"]:
        assert sim.call("setTab", t)
        assert sim.js(f"document.querySelector('#p-{t}').classList.contains('on')")
        assert sim.js("document.querySelector('#ctl').children.length") > 1
    assert not sim.call("setTab", "xx")


def test_U03_asetusten_tallennus_ja_lataus(sim):
    sim.call("loadExample", "nc42")
    s = sim.call("serialize")
    sim.call("loadExample", "qt42")
    assert json.loads(sim.call("serialize"))["ht"]["proc"] == "qt"
    assert sim.call("load", s)
    d = json.loads(sim.call("serialize"))
    assert d["ht"]["proc"] == "nc" and d["ht"]["T"] == 580 and d["version"] == sim.js("MatSim.version")
    assert sim.call("mode") == "ht:nc:42CrMo4"


def test_U04_ohjauskentta_paivittaa_tuloksen(sim):
    """Päästölämpötilan muutos lomakkeessa muuttaa tulostaulukkoa."""
    sim.call("loadExample", "qt42")
    before = sim.js("document.querySelector('#htRes').innerText")
    sim.page.fill('input[data-k="ht.Tt"]', "200")
    sim.page.dispatch_event('input[data-k="ht.Tt"]', "change")
    sim.page.wait_for_timeout(300)
    assert sim.call("state")["ht"]["Tt"] == 200
    assert sim.js("document.querySelector('#htRes').innerText") != before
    sim.page.fill('input[data-k="ht.Tt"]', "5000")
    sim.page.dispatch_event('input[data-k="ht.Tt"]', "change")
    assert sim.call("state")["ht"]["Tt"] == 700, "U04: raja-arvo ei rajannut syötettä"


def test_U05_syvyyden_valinta_klikkaamalla(sim):
    sim.call("loadExample", "ind10")
    sim.page.wait_for_timeout(200)
    box = sim.page.locator("#cvM").bounding_box()
    sim.page.mouse.click(box["x"] + box["width"] * 0.9, box["y"] + box["height"] / 2)
    sel = sim.call("state")["ht"]["sel"]
    assert sel is not None and sel > 3
    assert "ferriitti" not in sim.js("document.querySelector('#phaseTxt').innerText")
    assert "päästetty martensiitti" in sim.js("document.querySelector('#phaseTxt').innerText")


def test_U06_fec_klikkaus(sim):
    sim.call("setTab", "fec")
    box = sim.page.locator("#cvF").bounding_box()
    sim.page.mouse.click(box["x"] + box["width"] * 0.5, box["y"] + box["height"] * 0.3)
    f = sim.call("state")["fec"]
    assert 0.5 < f["C"] < 1.6 and f["T"] > 850
    assert "austeniitti" in sim.js("document.querySelector('#fecRes').innerText")


def test_U07_lampokasittelyn_tulos_vetokokeeseen(sim):
    sim.call("loadExample", "qt42")
    sim.page.wait_for_timeout(200)
    sim.js("document.querySelector('#toTT').click()")
    sim.page.wait_for_timeout(3900)
    r = sim.call("ttResult")
    hv = [q for q in sim.call("heatTreat", {"proc": "qt", "steel": "42CrMo4", "D": 30, "medium": "oljy", "Taus": 850, "Tt": 600, "tt": 1})["prof"]]
    hv125 = min(hv, key=lambda q: abs(q["x"] - 12.5))["hv"]
    assert abs(r["Rm"] - 3.1 * hv125) < 3
    assert "Lämpökäsittely-välilehti" in sim.js("document.querySelector('#ttRes').innerText")


def test_U08_varoitukset(sim):
    """Varoitukset syntyvät tilanteissa, joissa materiaalitekniikka sen edellyttää."""
    w = sim.call("heatTreat", {"proc": "qt", "steel": "42CrMo4", "Taus": 760})["warnings"]
    assert any("Ac3" in x for x in w)
    w = sim.call("heatTreat", {"proc": "qt", "steel": "42CrMo4", "medium": "vesi"})["warnings"]
    assert any("säröjen" in x for x in w)
    w = sim.call("heatTreat", {"proc": "ind", "steel": "42CrMo4", "qs": 0.4, "th": 1})["warnings"]
    assert any("austenitoidu" in x for x in w)
    w = sim.call("heatTreat", {"proc": "ind", "steel": "42CrMo4", "qs": 3, "th": 3})["warnings"]
    assert any("ylikuumeneminen" in x for x in w)
    w = sim.call("heatTreat", {"proc": "nc", "steel": "42CrMo4", "T": 590, "TpN": 600})["warnings"]
    assert any("ydin pehmenee" in x for x in w)
    assert sim.call("heatTreat", {"proc": "nc", "steel": "42CrMo4", "T": 580, "TpN": 620})["warnings"] == []
