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
| **Echtes Home Assistant** | **12/12 reale Lovelace-/Backend-/WebSocket-/Pointer-/Lifecycle-Tests im Wiederholungslauf bestanden** |

**Früherer Beleg:** [GitHub Actions Run #38799165242](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38799165242), Home Assistant Core 2026.10.1 mit originalem Bubble Card v3.4.2. [Browser-Screenshots](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38799165242/artifacts/12003956507).

Die ursprünglichen neun E2E-Testfälle prüfen Rendering, externen Zustandswechsel, Child-RGB-Abhängigkeiten, nativen Hauptslider, native Baseline, Navigation/Reconnect, gemischte Gruppen-Farben, nativen Subslider und echten Card-Disconnect. Details: [tests/ha_e2e/README.md](../../tests/ha_e2e/README.md).

## Historische Diagnose

Ein früher Chromium-Versuch mit dem Original-Bundle scheiterte am unvollständigen künstlichen `hass`-Objekt bereits **ohne VSC**. Diese unbrauchbaren Render-Fälle bleiben ausdrücklich als `skipped` gekennzeichnet.

Beim Aufbau des echten HA-Containers wurden zuerst fehlende Schreibrechte für das temporäre `/config/deps` festgestellt und behoben. Anschließend scheiterte zunächst ein Test, weil `always_visible`-Subslider absichtlich kein separates Icon-Element haben. Der Test prüft jetzt die echte Klasse `.bubble-sub-button-slider`; alle ursprünglichen neun tatsächlichen Tests bestehen.

## Noch nicht nachgewiesen

- Visueller Karten-/Moduleditor mit allen 46 Einstellungen, inklusive Speicherung und Live-Umschaltung ohne Card-Disconnect.
- Ein mobiler Chromium-Touch-Drag auf dem nativen Hauptslider ist jetzt real bestanden. Zusätzliche Gesten, Pop-up-, Sections-, Grid- und alternative Subslider-Layouts bleiben offen.
- Konkrete Wechselwirkungen mit Drittmodulen, verschiedenen Themes, langen Laufzeiten und Performance.
- Änderungen der Modulkonfiguration bei gemounteter Karte sind jetzt inklusive Deaktivierung und Reaktivierung als E2E-Test abgedeckt. Das erfordert einen VSC-eigenen `setConfig`-Cleanup, weil Bubble Cards Teardown bei einer reinen `setConfig`-Änderung nicht automatisch ausgelöst wurde.

Ein bestandener Testlauf bedeutet nicht, dass alle potentiellen Bugs behoben oder alle neuen Features genutzt werden. Folgeverifikation: [Issue #11](https://github.com/HyperCriSiS/Bubble-Card-Modules/issues/11). **PR #7 bleibt offen**, bis die Freigabe separat bewertet ist.

## Zusätzlicher Konfigurations-/Touch-Nachweis, 16. Oktober 2026

Neue Tests `test_10`–`test_12` prüfen CSS-Isolation zur unmodifizierten Karte, das Deaktivieren und Reaktivieren der Modul-Styles **ohne** Card-Disconnect sowie mobilen Touch-Drag auf dem nativen Slider. Der erste Lauf [#38817607322](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38817607322) deckte einen echten VSC-Cleanup-Fehler auf: Bei `setConfig()` ohne VSC-Stil blieben CSS-Gradienten und Klassen erhalten. Der neue idempotente `setConfig`-Cleanup-Pfad beseitigt das Problem.

Im Folgelauf [#38818020327](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/38818020327) bestanden Cleanup- und Touch-Tests, aber zwei ältere Desktop-Pointer-Drag-Tests schlugen einmalig fehl. Der **Wiederholungslauf desselben Commits** bestand mit **12/12 Tests** (20,237 s). Die Desktop-Drag-Tests sind daher als potenziell flüchtig zu beobachten; ein einzelner erfolgreicher Wiederholungslauf beweist noch keine vollständige Zuverlässigkeit. Bei erneutem Auftreten die Ursache diagnostizieren, nicht stillschweigend Tests deaktivieren.

Weiterhin offen: visueller Editor/Speichern aller 46 Optionen, die vollständige Layout-/Theme-/Drittmodulmatrix, Performancemessungen und Langzeitstabilität.

## BCT-Moduleditor-Integration, 17. Oktober 2026

Der isolierte HA-Core-2026.10.1-Container installiert jetzt offiziell veröffentlichtes **Bubble Card Tools v1.1.1** von fest gepinntem Git-Commit `2708319696513f5916f062723847c6cd80715dcc`. Aus der VSC-Definition wird die tatsächliche YAML-Datei `bubble_card/modules/visual_styling_center.yaml` in einem ausschließlich temporären Verzeichnis erzeugt. Die BCT-Integration wird nach der HA-Ersteinrichtung per offiziellem REST-Konfigurationsflow aktiviert; die BCT-Dateioperationen laufen ausschließlich über die echte authentifizierte Home-Assistant-WebSocket-API.

Die eigentliche VSC-UI wird jetzt mit der offiziellen `bubble-card-editor`-Komponente von Bubble Card v3.4.2 in authentifiziertem Lovelace gerendert. Abgedeckt:

- BCT-Konfigurationsflow und `read_module`, `write_module`, `delete_module` mit exakter Speicher-Rücklesung.
- Aus BCT geladene YAML-Module enthalten exakt die 46 bisherigen VSC-Editor-Feldnamen, ohne Umbenennung oder Dubletten.
- Echtes Module-Panel des Editors enthält ein gerendertes `ha-form` mit exakt 46 Optionen.
- Ein an dieses tatsächlich gerenderte `ha-form` gesendetes `value-changed`-Ereignis löst `config-changed` aus; `inner_padding: 7` und `enable_entity_colored_subicons: false` werden in die Editor-Konfiguration übertragen und nach erneutem `setConfig` erhalten.
- **CI-Nachweis: [17 von 17 echte HA-E2E-Tests bestanden, Run #39000966123](https://github.com/HyperCriSiS/Bubble-Card-Modules/actions/runs/39000966123)**. CI nutzt nur virtuelle HA-Entities, keine Produktivinstanz.

**Noch nicht belegt:** Manuelle Maus-/Touch-Interaktion mit sämtlichen 46 einzelnen Formularfeldern, die echte Lovelace-Dashboard-Speicher-API samt erneutem Öffnen des Dashboards, Speichern/Ändern des **Modulquelltexts** über den BCT-UI-Speichern-Button sowie umfangreiche Layout-/Theme-/Drittmodul- und Langzeittests. Der synthetische `value-changed`-Event prüft den *realen* Editor-Eventhandler, ersetzt aber keine physische UI-Interaktion. Issue #11 bleibt deshalb offen.


## Nachprüfung und Menü-Umbau, 19. Oktober 2026 (VSC v2026.10.19)

**Kompatibilität:** Alle 46 bisherigen Options-IDs sind unverändert. Die Editor-Abschnitte (`expandable`) haben weiterhin kein `name`, deshalb bleiben die Werte flach unter `visual_styling_center` gespeichert. Eine Migration ist nicht nötig. Bewusst wurde kein namenloses `grid` eingesetzt, weil nicht belegt ist, dass Bubble Card es flach speichert.

Behoben:

- **Cleanup beim Entfernen über `modules:`**: Der `setConfig`-Cleanup erkannte VSC bisher nur, wenn der Quelltext in `styles` eingebettet war (so wie im E2E-Fixture). Wird das Modul auf dem normalen Weg aus der `modules:`-Liste entfernt (auch per `!visual_styling_center`), räumt es jetzt ebenfalls auf. Der neue Runtime-Test schlägt auf dem vorherigen Stand fehl. Ein globales Modul (`is_global`) taucht in keiner der beiden Stellen auf, seine Entfernung bleibt hier unerkannt.
- **Editor-Defaults widersprachen dem Verhalten**: `enable_helper_fade` und `enable_slider_helper_fade` zeigten `true`, der Code wendet den Fade aber nur bei explizitem `true` an. Die Defaults sind jetzt `false`. Die Anzeige stimmt damit, und keine bestehende Karte sieht anders aus.
- **Abstände in Sub-Button-Gruppen**: Seit v3 können Buttons in `.bubble-sub-button-group` liegen, dort griffen die Abstands-Optionen nicht. Sie gelten jetzt auch in Gruppen. Ohne gesetzten Wert bleibt der native 8px-Abstand.

Neu und rückwärtskompatibel:

- `enable_interaction_effects` (Standard `true`): Hover-Aufhellung, aufgehelltes aktives Icon und Sub-Icon-Deckkraft 0,9 waren bisher fest aktiv und lassen sich jetzt abschalten.

Menü:

- Neue Reihenfolge: Karte, Haupt-Icon, Sub-Buttons, Zustandsfarben, Icon-Kontrast, Verlauf, Slider-Kontrast (direkt nach dem Verlauf, weil nur mit Hintergrundverlauf wirksam), Interaktionseffekte.
- Felder, die gerade nichts bewirken, werden per `visible:` ausgeblendet (HA ab 2026.9, ältere Versionen zeigen alle Felder).
- Die Labels beschreiben das tatsächliche Verhalten (Abstand auf allen Seiten, manuelle Farbe hat Vorrang, Regenbogen-Fallback).

Bewusst **nicht** geändert, weil sich sonst die Optik bestehender Karten ändern würde. Das ist offen und braucht eine Entscheidung:

- `.bubble-icon-container { background-color: … !important }` überschreibt möglicherweise den nativen, zustandsabhängigen Icon-Hintergrund. Das ist nicht in HA nachgeprüft.
- Die feste Sub-Button-Höhe von 32px × Faktor gilt auch für Sub-Button-Slider, Dropdowns und die untere Reihe und ignoriert `--bubble-sub-button-height` (nativ 36px).
- `margin-right` am Sub-Button-Container kommt zum nativen `inset-inline-end: 8px` hinzu und berücksichtigt kein RTL.
- Die Zustandsfarben sind fest (Grün/Grau) statt der Theme-Farben `--state-*-color`.
- `unsupported` enthält die neuen Kartentypen `sub-buttons` und `calendar` nicht.

Lokal geprüft: `test_visual_styling_center.py` (inkl. Node-Runtime), 13/13 Chromium-Tests in `test_vsc_browser.py`, `test_fixture_structure.py`. Nicht lokal ausführbar: der Test mit dem offiziellen Bundle (`test_vsc_upstream_runtime.py`) und die echten HA-E2E-Tests. Beide laufen in CI.

## Messungen und Erweiterung, 29. Oktober 2026 (VSC v2026.10.29)

Geprüft am SHA-verifizierten Original-Bundle `bubble-card.js` v3.4.2 (`d526dfd8…`), nicht nur an der Quellspiegelung:

- **Lichtfarbe am Haupt-Icon:** Bubble Card färbt bei eingeschaltetem Licht nur das Icon selbst (Inline-`color` am Icon-Container), nicht den Kreis dahinter. Das Modul erbt diese Farbe korrekt. Die frühere Vermutung, der Kreis verliere seine Lichtfarbe, ist damit widerlegt.
- **Icon-Hintergrund ohne Bubble-Theme:** Der Modul-Fallback endete bei `--bubble-secondary-background-color`, die nur Bubble-Themes definieren. In Chromium mit dem nativen CSS gemessen: ohne Modul `rgb(40, 40, 40)` (Kartenfarbe), mit Modul und leeren Einstellungen `rgba(0, 0, 0, 0)` (durchsichtig). Mit Bubble-Theme sind beide gleich. Das Modul überschreibt den Kreis jetzt nur noch bei eigener Farbe oder „Hide Icon Background“, analog zur Sub-Button-Regel aus PR #7. **Sichtbare Änderung:** Ohne Bubble-Theme erscheint der Icon-Kreis wieder. Wer ihn unsichtbar haben will, nutzt „Hide Icon Background“.
- **Sub-Button-Höhe:** Bubble Card schreibt die Sub-Button-Option `custom_height` als `--bubble-sub-button-height` an den einzelnen Button. Die feste Modul-Höhe hat diese Option bisher per `!important` überschrieben. Jetzt gewinnt `custom_height`, ohne sie bleibt die bisherige Modul-Höhe (32px × Faktoren). Für bestehende Karten ohne `custom_height` ändert sich nichts.
- **Kartentypen `sub-buttons` und `calendar`:** Beide haben Sub-Buttons, aber kein Haupt-Icon, keinen Namen und keinen Slider. Das Modul läuft dort fehlerfrei, und die Sub-Button-Optionen wirken. Sie bleiben deshalb unterstützt, statt in `unsupported` zu wandern (das hätte bestehenden Nutzern die Wirkung genommen). Ein echter HA-E2E-Test prüft die `sub-buttons`-Karte. Für `calendar` gibt es in der Fixture keine Kalender-Entity, der Kalender ist daher nur über den gleichen Sub-Button-Codepfad abgedeckt.

Neu (alle optional, ohne Wert gilt das Theme bzw. das bisherige Verhalten), damit 61 Optionen:

- Name/Status: `custom_name_color`, `manual_name_color`, `name_font_size`, `custom_state_color`, `manual_state_color`, `state_font_size`
- Radien über Bubble Cards eigene Variablen: `card_border_radius` → `--bubble-button-border-radius`, `icon_border_radius` → `--bubble-button-icon-border-radius`, `subbutton_border_radius` → `--bubble-sub-button-border-radius`
- Hintergrund: `custom_card_background_color`, `manual_card_background_color`, `card_background_opacity` → `--bubble-button-main-background-color` (Deckkraft per `color-mix`)
- `gradient_angle` (Standard 90° = bisher „to right“)
- `use_theme_state_colors` (Standard aus): `--state-<domain>-active-color`, `--state-active-color` usw., mit den bisherigen festen Farben als Fallback

Weiterhin offen: `margin-right` am Sub-Button-Container addiert sich zum nativen `inset-inline-end: 8px` und berücksichtigt kein RTL. Eine Korrektur würde bestehende Layouts verschieben.

Lokal geprüft: Node-Runtime (23 Fälle), Chromium mit nativem CSS (16 Fälle), Fixture-Struktur. Die neuen echten HA-Tests `test_18` (rote Lampe, Icon-Hintergrund mit und ohne Modul) und `test_19` (`sub-buttons`-Karte, `custom_height`) laufen in CI, weil lokal kein Docker läuft.
