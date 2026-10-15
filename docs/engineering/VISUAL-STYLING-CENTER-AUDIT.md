# Visual Styling Center – Bubble Card v3.4.2 Audit und Teststand

**Stand:** 15. Oktober 2026 · [PR #7](https://github.com/HyperCriSiS/Bubble-Card-Modules/pull/7) · VSC v2026.10.15

## Behobene Fehler und Modernisierung

- Beschädigte Modul-Markdown-/YAML-Definition und Anzeigeeinheiten repariert.
- Obsoleten eigenen Slider-Update-Stub entfernt; native Bubble Card verwaltet Haupt- und Subslider.
- Kompatibilität: Modul-ID `visual_styling_center` und alle 46 Editor-Option-IDs erhalten.
- Dynamische Icon-Farben, CSS-Overrides und Entity-Vererbung korrigiert; auch gemischte Main-/Bottom-Gruppen haben die tatsächliche upstream-konforme Nummerierung.
- Numerische Nullwerte bleiben erhalten, keine Mutation der gespeicherten Konfiguration.
- CSS-Eigentümerschaft verhindert Löschen fremder Inline-Werte einschließlich Priorität; native `onTeardown`-Bereinigung hinzugefügt.
- `trackedHass` zur Erfassung genutzter Entities, `hasChanged` zur Vermeidung unnötiger Gradientenberechnungen; keine zusätzlichen HA-WebSocket-Abonnements/Polling-Intervalle.
- Slider-bezogene CSS-Regeln auf native Bubble-Card-v3.4.2-Darstellung abgestimmt; Hauptkartengradienten beeinflussen native Subslider nicht pauschal.
- `AGENTS.md` verweist auf die automatisch aktualisierte, schreibgeschützte Upstream-Referenz.

## Automatisierte Nachweise

| Ebene | Nachweis |
| --- | --- |
| PyYAML/Node.js | Modulstruktur, Editor-Keys, Zustandswechsel, Konfigurationswerte, Farben, Gradienten, Teardown |
| Chromium mit Referenz-CSS | Layouts, responsive Abstände, Gradient, Iconfarben, CSS-Kaskade und Rücksetzung |
| Original-Bundle-Smoketest | SHA-256-prüft echtes Bubble-Card-v3.4.2-Bundle und registriertes Custom Element |
| **Echtes Home Assistant** | **9/9 reale Lovelace-/Backend-/WebSocket-/Pointer-/Lifecycle-Tests bestanden** |

**Beleg:** [GitHub Actions Run #38799165242](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38799165242), Home Assistant Core 2026.10.1 mit originalem Bubble Card v3.4.2. [Browser-Screenshots](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38799165242/artifacts/12003956507).

Die neun E2E-Testfälle prüfen Rendering, externen Zustandswechsel, Child-RGB-Abhängigkeiten, nativen Hauptslider, native Baseline, Navigation/Reconnect, gemischte Gruppen-Farben, nativen Subslider und echten Card-Disconnect. Details: [tests/ha_e2e/README.md](../../tests/ha_e2e/README.md).

## Historische Diagnose

Ein früher Chromium-Versuch mit dem Original-Bundle scheiterte am unvollständigen künstlichen `hass`-Objekt bereits **ohne VSC**. Diese unbrauchbaren Render-Fälle bleiben ausdrücklich als `skipped` gekennzeichnet.

Beim Aufbau des echten HA-Containers wurden zuerst fehlende Schreibrechte für das temporäre `/config/deps` festgestellt und behoben. Anschließend scheiterte zunächst ein Test, weil `always_visible`-Subslider absichtlich kein separates Icon-Element haben. Der Test prüft jetzt die echte Klasse `.bubble-sub-button-slider`; alle neun tatsächlichen Tests bestehen.

## Noch nicht nachgewiesen

- Visueller Karten-/Moduleditor mit allen 46 Einstellungen, inklusive Speicherung und Live-Umschaltung ohne Card-Disconnect.
- Vollständige mobile Touch-Gesten, Pop-up-, Sections-, Grid- und alternative Subslider-Layouts.
- Konkrete Wechselwirkungen mit Drittmodulen, verschiedenen Themes, langen Laufzeiten und Performance.
- Explizites Deaktivieren des Moduls bei weiterhin gemounteter Karte.

Ein bestandener Testlauf bedeutet nicht, dass alle potentiellen Bugs behoben oder alle neuen Features genutzt werden. Folgeverifikation: [Issue #11](https://github.com/HyperCriSiS/Bubble-Card-Modules/issues/11). **PR #7 bleibt offen**, bis die Freigabe separat bewertet ist.
