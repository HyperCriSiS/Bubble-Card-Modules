# Visual Styling Center – echte Home-Assistant-End-to-End-Tests

## Nachweis

Der erste vollständige **echte HA-Testlauf** ist erfolgreich:
[GitHub Actions #38797293013](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38797293013)
(15. Oktober 2026; alle sechs Tests bestanden).

Der Workflow startet einen isolierten Home-Assistant-Core-Container **2026.10.1**, lädt das unveränderte Release-Bundle **Bubble Card v3.4.2** und prüft dessen SHA-256-Hash
`d526dfd815af6a022b8f7355874fc96f2df859aa213cff7b374f7d913a6436ae`.
Die Version des Visual Styling Center stammt direkt aus der Modul-Markdown-Datei des Pull Requests.

## Sicherheitsgrenzen

- Home Assistant ist ausschließlich über `127.0.0.1:8123` erreichbar.
- Keine Verbindung oder Zugangsdaten zur produktiven HA-Instanz; ausschließlich virtuelle RGB-Lampen, `input_*`-Helfer und eine Gruppe.
- Temporärer OAuth-Nutzer aus der offiziellen HA-Onboarding-API.
- Token werden nur in einer Modus-0600-Datei des GitHub-Runners gespeichert, weder in Git-Commits noch in den Actions-Artefakten.
- Nach jedem Lauf werden Container und Token entfernt.
- Für den GitHub-Container benötigt das temporäre Konfigurationsverzeichnis Schreibrechte für die nichtprivilegierte HA-Prozessidentität; dieses Verzeichnis enthält keine Produktivdaten.

## Aktuelle Tests

| Test | Was geprüft wird |
| --- | --- |
| Rendering | Echte Bubble Card und VSC in authentifiziertem Lovelace, inklusive Hauptslider und permanent sichtbarem Sub-Button-Slider |
| HA → Browser | Externes Abschalten/Einschalten der virtuellen Hauptlampe führt über echte HA-State/WebSocket-Updates zu einer geänderten VSC-Icon-Farbe |
| Gruppen-Gradient | RGB-Änderung eines Kindlichts aktualisiert den VSC-Gradienten |
| Browser → HA | Native Slider-Pointer-Geste ändert die Helligkeit des echten HA-Licht-Entities |
| Baseline | Unveränderte Bubble Card ohne VSC bleibt funktionsfähig |
| Navigation | Dashboard-Navigation und Rückkehr rendern das Modul erneut korrekt |

Das ist eine echte **Browser-/Backend-Integration** mit HA und originaler Bubble Card, im Gegensatz zu den separat bestehenden Mock-/CSS-Tests.

## Nicht abgedeckt

Alle 46 Optionen im visuellen Modul-Konfigurationseditor, sämtliche mobilen Touch-Gesten, alle Pop-up-/Sections-/Grid-Varianten, das Zusammenspiel mit fremden Modulen und längere Laufzeit-/Performance-Untersuchungen sind weiterhin offen. Die nachgewiesenen Testfälle können nicht ausschließen, dass in anderen Kombinationen Fehler bestehen. Siehe [Issue #11](https://github.com/HyperCriSiS/Bubble-Card-Modules/issues/11).

## Reproduktion

Der Workflow liegt in `.github/workflows/test-vsc-ha-e2e.yml`.
Die drei Python-Bausteine `generate_fixture.py`, `bootstrap.py` und `test_lovelace.py` befinden sich unter `tests/ha_e2e/`.
Zum lokalen Start sind ein frischer Docker-fähiger Rechner, Python 3, Playwright/Chromium, PyYAML und Requests nötig.
Ein Container wird niemals mit produktiven Geräten oder einem entfernten HA-Host verbunden.
