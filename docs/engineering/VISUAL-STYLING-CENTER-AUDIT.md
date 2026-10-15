# Visual Styling Center – Architektur-Audit und Testnachweise

Stand: **15. Oktober 2026** · PR [#7](https://github.com/HyperCriSiS/Bubble-Card-Modules/pull/7) · Bubble Card **v3.4.2** · VSC **v2026.10.15**

## Code-Audit und Kompatibilität

- Veralteten Initial-Slider-Update-Stub entfernt. Haupt- und Sub-Button-Slider werden nativ durch Bubble Card aktualisiert.
- Beschädigte YAML-/Markdown-Struktur, problematische Einheiten und alte Beschreibungen repariert.
- Modul-ID `visual_styling_center` sowie alle **46 gespeicherten Editor-Optionsnamen** unverändert erhalten.
- Numerische Nullwerte korrekt behandelt; keine direkte Mutation von `this.config`.
- Entity-basierte Haupt- und Sub-Icon-Farben reagieren auf Zustandsänderungen. Sub-Buttons erben ohne eigenes Entity-Feld die Haupt-Entity.
- Unterstützung für explizite und implizite `main`-/`bottom`-Gruppen anhand tatsächlicher Bubble-Card-Klassenindizes.
- Fremde Inline-CSS-Variablen werden nicht überschrieben oder dauerhaft gelöscht. Für eigene CSS-Variablen, Icon-Farben und Klassen sind Rücksetzung und nativer `onTeardown`-Hook implementiert.
- `hasChanged` verhindert unnötige Sortierung identischer Gradientendaten; `trackedHass` zeichnet Entity-Abhängigkeiten auf. Es werden keine zusätzlichen HA-WebSocket-Listener oder Polling-Intervalle benötigt.
- Gradientengestaltung auf die Hauptkarte eingegrenzt; native Sub-Slider-Darstellung bleibt grundsätzlich Bubble Card überlassen.
- `AGENTS.md` enthält direkte Verweise auf die synchronisierte, schreibgeschützte Upstream-Referenz.

## Automatische Tests

| Stufe | Umfang | Stand |
| --- | --- | --- |
| Python + PyYAML | Vollständiger Modulimport, Kompatibilitätsnamen, Upstream-Quellcode-Verträge | Bestanden |
| Node.js | Farben, Nullwerte, dynamische Gradienten, Gruppen, Konfiguration und Teardown | Bestanden |
| Chromium (simuliertes DOM) | Berechnete CSS-Werte mit v3.4.2-Referenz-Stylesheets, Layout, responsive Verhalten und Style-Cleanup | Bestanden |
| Original-Bundle-Smoke | SHA-256-verified Release-Bundle, tatsächliche `bubble-card`-Registrierung | Bestanden |
| **Home Assistant + Lovelace E2E** | Echter HA-Backend-Container und originale Bubble-Card-Komponente; API/WebSocket-/Pointer-Interaktionen | **6 von 6 bestanden** |

**Echte HA-Nachweise:** [GitHub Actions Run #38797293013](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38797293013), Home Assistant Core **2026.10.1**, Original-Bubble-Card-Bundle **v3.4.2** mit SHA-256 `d526dfd815af6a022b8f7355874fc96f2df859aa213cff7b374f7d913a6436ae`.

Die sechs E2E-Prüfungen:
1. Echte Lovelace-Karte mit VSC, Hauptslider, dauerhaft sichtbarem Sub-Button-Slider und dynamischem Gradienten.
2. Externe API-Lichtzustände werden per echter HA-State/WebSocket-Kette bis zur Icon-Farbe übernommen.
3. RGB-Änderungen eines einzelnen Kindlichts aktualisieren den gruppenbasierten VSC-Gradienten.
4. Echte Pointer-Slider-Geste verändert die Helligkeit des HA-Backends.
5. Unveränderte Bubble Card ohne VSC läuft parallel als native Baseline.
6. Dashboard-Navigation und Neuerstellung der Karte funktionieren.

Testdateien und Isolation: [tests/ha_e2e/README.md](../../tests/ha_e2e/README.md).

## Historischer Testaufbau und Fehlerdiagnose

Vor dieser vollständigen HA-E2E-Suite wurde das Original-Bubble-Card-Bundle bereits in Chromium geladen. Eine rein simulierte `hass`-Umgebung konnte jedoch nicht den kompletten Render-Lifecycle bereitstellen – selbst **ohne VSC**. Diese unvollständigen Original-Bundle-Render-Tests sind daher ausdrücklich übersprungen und nicht als erfolgreiche Tests gezählt.

Der erste echte HA-Testlauf wurde durch fehlende Schreibrechte auf dem temporären Docker-Mount blockiert. Nach Korrektur startete die Instanz; fünf von sechs Tests liefen sofort erfolgreich. Die sechste Prüfung erwartete fälschlich ein Icon für einen `always_visible`-Subslider. Bubble Card verwendet dafür tatsächlich `.bubble-sub-button-slider` ohne Icon-Host. Nach Anpassung bestanden sechs von sechs Tests.

## Verbleibende Grenzen und Risiken

- **Nicht getestet:** alle 46 Felder im *visuellen* Modul-Editor einschließlich Konfigurationspersistenz und Umschalten ohne Card-Disconnect.
- Mobile Touch-Drags, weitere Slider-Typen, Pop-up-/Sections-/Grid-Varianten und sämtliche Gruppenanordnungen sind nicht vollständig durch echte HA-E2E-Tests abgedeckt.
- Drittmodule, Themes, `!important`-Kaskaden und Langzeit-/Performance-Verhalten benötigen weitere Systemtests.
- `onTeardown` bei Card-Disconnect ist im simulierten Browser getestet. Der vollständige reale Deaktivierungspfad ohne Disconnect ist noch nicht abgesichert.
- Ein bestandener Testlauf garantiert nicht die Abwesenheit weiterer Fehler oder vollständige Ausschöpfung aller neuen Bubble-Card-Funktionen.

Weitere Aufgaben stehen in [Issue #11](https://github.com/HyperCriSiS/Bubble-Card-Modules/issues/11). PR #7 bleibt bis zur gesonderten Freigabe offen.
