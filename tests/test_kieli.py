"""Kieliversioiden testit K01–K05."""
import re
from conftest import INDEX

API_NAME = "MatSim"

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
    assert ajo("fi") == ajo("en") == ajo("de"), "K02: kieli vaikutti tulokseen"


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




# ---------- Saksa (DE) ----------
DE_SALLITUT = {"Feedback", "42CrMo4 (0,42 % C)", "34CrNiMo6 (0,34 % C)"}
DE_NAKYMAT = [
    "",
    "MatSim.setTab('xs')",
    "MatSim.setTab('fec')",
    "MatSim.setTab('tt')",
    "MatSim.setTab('tt');MatSim.runTT()",
    "MatSim.loadExample('qt42')",
    "MatSim.loadExample('qt42b')",
    "MatSim.loadExample('qt346')",
    "MatSim.loadExample('c45w')",
    "MatSim.loadExample('c45o')",
    "MatSim.loadExample('ind10')",
    "MatSim.loadExample('ind200')",
    "MatSim.loadExample('nc42')",
    "MatSim.loadExample('nc45')",
    "MatSim.load({tab:'ht',ht:{proc:'qt',steel:'42CrMo4',Taus:780,medium:'vesi',Tt:300,D:300}})",
    "MatSim.load({tab:'ht',ht:{proc:'qt',steel:'42CrMo4',Taus:1000,Tt:100}})",
    "MatSim.load({tab:'ht',ht:{proc:'ind',prior:'n',qs:20,th:12,Di:20}})",
    "MatSim.load({tab:'ht',ht:{proc:'ind',qs:0.3,th:1}})",
    "MatSim.load({tab:'ht',ht:{proc:'nc',T:600,t:30,TpN:590}})",
    "MatSim.load({tab:'ht',ht:{proc:'nc',T:540,t:2}})",
    "MatSim.setTab('xs');MatSim.set('xs.kind','bcc')",
    "MatSim.setTab('xs');MatSim.set('xs.kind','fcc')",
    "MatSim.setTab('xs');MatSim.set('xs.kind','bct')",
    "MatSim.setTab('xs');MatSim.set('xs.kind','bain')",
    "MatSim.setTab('xs');MatSim.set('xs.kind','gp')",
    "MatSim.setTab('xs');MatSim.set('xs.kind','eps')",
    "MatSim.setTab('fec');MatSim.set('fec.C',0.2);MatSim.set('fec.T',900)",
    "MatSim.setTab('fec');MatSim.set('fec.C',0.2);MatSim.set('fec.T',750)",
    "MatSim.setTab('fec');MatSim.set('fec.C',0.2);MatSim.set('fec.T',600)",
    "MatSim.setTab('fec');MatSim.set('fec.C',0.8);MatSim.set('fec.T',900)",
    "MatSim.setTab('fec');MatSim.set('fec.C',0.8);MatSim.set('fec.T',750)",
    "MatSim.setTab('fec');MatSim.set('fec.C',0.8);MatSim.set('fec.T',600)",
    "MatSim.setTab('fec');MatSim.set('fec.C',1.2);MatSim.set('fec.T',900)",
    "MatSim.setTab('fec');MatSim.set('fec.C',1.2);MatSim.set('fec.T',750)",
    "MatSim.setTab('fec');MatSim.set('fec.C',1.2);MatSim.set('fec.T',600)",
    "MatSim.setTab('tt');MatSim.set('tt.mat','S235');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','S355');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','C45N');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','CrMoQT');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','HT');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','SS');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','AL6082');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','AL7075');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','CU');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','TI');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','GJS');MatSim.runTT()",
    "MatSim.setTab('tt');MatSim.set('tt.mat','GJL');MatSim.runTT()",
    "MatSim.setTab('ht');document.querySelector('#helpBtn').click()",
    "document.querySelectorAll('.modal,#modal').forEach(m=>m.classList.remove('open'));document.querySelector('#palauteBtn').click()",
]


def _rivit(page):
    return page.evaluate("""(()=>{const out=[];const add=t=>t.split('\\n').map(x=>x.trim()).filter(x=>x&&/[A-Za-zÄÖÜäöüß]{3,}/.test(x)).forEach(x=>out.push(x));
      add(document.body.innerText);return out;})()""")


def _luvut(x):
    return re.sub(r"[−-]?\d+([.,]\d+)?", "#", x)


def test_K04_saksankieliset_tekstit_kattavat(sim):
    """Saksankielisessä näkymässä ei ole suomen- tai englanninkielisiä rivejä: jokainen rivi, joka eroaa suomen ja englannin välillä, on käännetty."""
    jaljella = {}
    for js in DE_NAKYMAT:
        T = {}
        for l in ("fi", "en", "de"):
            sim.call("setLang", l)
            sim.page.wait_for_timeout(250)  # piirtosilmukka päivittää lukemat seuraavalla kehyksellä
            if js:
                sim.js(js)
                sim.page.wait_for_timeout(150)
            T[l] = _rivit(sim.page)
        fi, en = set(T["fi"]), set(T["en"])
        for x in T["de"]:
            if x in DE_SALLITUT or _luvut(x) in {_luvut(y) for y in T["en"]} & {_luvut(y) for y in T["fi"]}:
                continue  # rivi eroaa vain desimaalierottimen osalta (29,8 / 29.8)
            if (x in en and x not in fi) or (x in fi and x not in en):
                jaljella.setdefault(x, js or "alku")
    assert not jaljella, f"K04: kääntämättömiä rivejä saksankielisessä näkymässä: {list(jaljella.items())[:8]}"


def test_K05_saksa_ei_vaikuta_tuloksiin_ja_url(browser):
    """?lang=de avaa saksankielisen näkymän; kielivalitsimessa on DE."""
    page = browser.new_page()
    page.goto(INDEX.as_uri() + "?lang=de")
    page.wait_for_function(f"window.{API_NAME} !== undefined")
    assert page.evaluate(f"{API_NAME}.lang()") == "de"
    assert page.evaluate("document.documentElement.lang") == "de"
    assert page.locator('.langsw [data-lang="de"]').count() == 1
    page.evaluate("localStorage.clear()")
    page.close()
