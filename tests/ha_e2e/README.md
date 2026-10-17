# Visual Styling Center – echte Home-Assistant-End-to-End-Tests

## Stand und Nachweise

**9/9 E2E-Tests erfolgreich:** [GitHub Actions #38799165242](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38799165242), 15. Oktober 2026.

[Browser-Screenshots (neun Fälle)](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38799165242/artifacts/12003956507)

Der GitHub-Workflow startet Home Assistant Core **2026.10.1** als isolierten Docker-Container. Das offizielle, unveränderte Bubble-Card-Bundle **v3.4.2** wird anhand seines SHA-256-Hashes `d526dfd815af6a022b8f7355874fc96f2df859aa213cff7b374f7d913a6436ae` geprüft. Der VSC-Code stammt aus dem aktuellen Pull Request, nicht aus einem separaten Mock.

## Sicherheitsgrenzen

- HTTP-Bindung ausschließlich an `127.0.0.1:8123`; kein Zugriff auf das produktive Home Assistant.
- Nur temporäre `input_*`-Helfer, zwei virtuelle RGB-Lampen und eine Lampengruppe.
- Einweg-OAuth-Testnutzer über die echte Onboarding-API. Authentifizierungsdaten nur als lokale temporäre Datei mit Modus 0600, niemals in Git oder Screenshot-Artefakten.
- Das Docker-Konfigurationsverzeichnis enthält keine Produktivdaten; es ist für den nichtprivilegierten HA-Prozess beschreibbar.
- Container und Authentifizierungsdatei werden nach jedem Testlauf gelöscht.

## Getestete Fälle

| # | Prüfung |
| --- | --- |
| 01 | Echtes Lovelace-Rendering: VSC-Icon, Hauptslider, permanent sichtbarer Subslider und Gradient |
| 02 | Externes Ausschalten/Einschalten einer virtuellen Lampe ändert die VSC-Icon-Farbe über HA-State/WebSocket |
| 03 | RGB-Änderung eines einzelnen Kindlichts aktualisiert den gruppenbasierten VSC-Gradienten |
| 04 | Native Slider-Pointer-Geste verändert den tatsächlichen Helligkeitswert im HA-Backend |
| 05 | Unveränderte Bubble Card ohne VSC funktioniert parallel |
| 06 | Dashboard-Navigation und Wiederaufbau aktualisieren die Karte korrekt |
| 07 | Gemischte Main-/Bottom-/Gruppen-Sub-Buttons behalten korrekte Icon-Indizes und Farben bei Zustandsänderungen |
| 08 | Pointer-Geste auf einem nativen Inline-Subslider verändert den Helligkeitswert des Kindlichts |
| 09 | Nativer Card-Disconnect räumt VSC-eigene Inline-CSS-Variablen und Gradienten auf |

Diese Tests verwenden **echte HA-Backend-Entities, das authentifizierte Lovelace-Frontend und die originale Bubble Card**. Die ergänzenden Python-/Node-/Chromium-Simulationstests bleiben separat bestehen.

## Grenzen

Nicht vollständig geprüft: alle 46 Optionen im visuellen Modul-Editor, mobile Touch-Drag-Gesten, sämtliche Pop-up-/Sections-/Grid-Varianten, Drittmodul-Kombinationen, lange Laufzeit- und Performance-Szenarien sowie das reine Deaktivieren eines Moduls, während die Karte verbunden bleibt. Siehe [Issue #11](https://github.com/HyperCriSiS/Bubble-Card-Modules/issues/11).

## Ausführung

GitHub Actions: `.github/workflows/test-vsc-ha-e2e.yml`. Fixture- und Browsercode: `tests/ha_e2e/`. Lokal werden Docker, Python 3, Playwright/Chromium, PyYAML und Requests benötigt. Keine produktive HA-Instanz darf verwendet werden.

## 17. Oktober 2026 – zusätzliche Testabdeckung

- Desktop-Pointer-Tests warten vor Drag-Events auf ein stabil positioniertes, sichtbar gerendertes natives Slider-Element. Ein fehlgeschlagener Drag wird **nicht** automatisch wiederholt oder ignoriert.
- Die echten Bubble-Card-Editor-Custom-Elements werden in HA Chromium erzeugt und auf unveränderte Übernahme aller 46 bestehenden Modul-Options-IDs sowie Wert- und Nullwert-Erhalt bei erneuter `setConfig`-Konfiguration geprüft.
- **Abgrenzung:** Dieser Editor-Smoke-Test prüft den nativen Editor-Konfigurations-Lebenszyklus. Er belegt **noch nicht** das tatsächliche Anzeigen, Verändern oder Speichern sämtlicher 46 Felder über den Bubble Card Tools (BCT) Modul-Editor; BCT wird in der isolierten Fixture bislang nicht installiert.

## Isolierter BCT-Backend-Test

Der CI-Container erhält zusätzlich **Bubble Card Tools v1.1.1**, auf Git-Commit `2708319696513f5916f062723847c6cd80715dcc` fixiert. Der VSC-Modulquelltext wird als eigene YAML-Datei nach `/config/bubble_card/modules/visual_styling_center.yaml` übertragen. Ein eigener Browser-Test aktiviert BCT über die echten HA-Konfigurationsflows und prüft dessen WebSocket-API für Lesen, Schreiben und Löschen der Module. Die produktive Home-Assistant-Installation wird nicht berührt.

Das ist unabhängig von der vollständigen manuellen Feldbedienung im BCT-Moduleditor. Dieser UI-Teil bleibt gesondert zu verifizieren.
