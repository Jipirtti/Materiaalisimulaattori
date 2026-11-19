"""Kieliversioiden testit K01–K03."""
import re
from conftest import INDEX

SALLITUT = ("Seinäjoki", "Tenifer", "JSON-muodossa")


def _fi_rivit(text):
    return [l for l in text.split("\n") if re.search("[äöÄÖ]", l) and not any(s in l for s in SALLITUT)]


def test_K01_englanninkieliset_tekstit_kattavat(sim):
    """Englanninkielisessä näkymässä ei ole suomenkielisiä rivejä millään välilehdellä, esimerkillä eikä ohjeikkunassa."""
    sim.call("setLang", "en")
    for ex in [e["id"] for e in sim.call("examples")]:
        sim.call("loadExample", ex)
        sim.page.wait_for_timeout(60)
        left = _fi_rivit(sim.js("document.body.innerText"))
        assert not left, f"K01 ({ex}): suomenkielistä tekstiä: {left[:5]}"
        assert not _fi_rivit("\n".join(sim.call("warnings"))), f"K01 ({ex}): suomenkielinen varoitus"
    for tab in ["xs", "fec", "tt"]:
        sim.call("setTab", tab)
        if tab == "tt":
            sim.call("runTT")
        if tab == "xs":
            for k in ["bcc", "fcc", "bct", "bain", "gp", "eps"]:
                sim.call("set", "xs.kind", k)
                left = _fi_rivit(sim.js("document.body.innerText"))
                assert not left, f"K01 (kide {k}): {left[:5]}"
        left = _fi_rivit(sim.js("document.body.innerText"))
        assert not left, f"K01 ({tab}): suomenkielistä tekstiä: {left[:5]}"
    sim.js("document.querySelector('#helpBtn').click()")
    left = _fi_rivit(sim.js("document.querySelector('#mbox').innerText"))
    assert not left, f"K01: suomea ohjeikkunassa: {left[:5]}"


def test_K02_kielen_vaihto_ei_vaikuta_tuloksiin(sim):
    def ajo(l):
        sim.call("setLang", l)
        r = sim.call("heatTreat", {"proc": "ind", "steel": "42CrMo4"})
        return round(r["surf"]["hv"], 6), round(r["shd"], 6)
    assert ajo("fi") == ajo("en"), "K02: kieli vaikutti tulokseen"


def test_K03_url_parametri(browser):
    page = browser.new_page()
    page.goto(INDEX.as_uri() + "?lang=en")
    page.wait_for_function("window.MatSim !== undefined")
    assert page.evaluate("MatSim.lang()") == "en"
    assert page.inner_text("#helpBtn") == "Help"
    page.goto(INDEX.as_uri() + "?lang=fi")
    page.wait_for_function("window.MatSim !== undefined")
    assert page.evaluate("MatSim.lang()") == "fi"
    assert page.inner_text("#helpBtn") == "Ohje"
    page.evaluate("localStorage.clear()")
    page.close()
