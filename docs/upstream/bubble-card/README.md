# Bubble Card upstream reference

Read-only, SHA-verified sources from https://github.com/Clooos/Bubble-Card.
These copies are not dependencies or executable build inputs.

| Channel | Reference commit | Files | Module documentation |
| --- | --- | ---: | --- |
| [stable](./stable/manifest.json) | [v3.4.1](https://github.com/Clooos/Bubble-Card/tree/061ed8376134307ba1086446869d0ab736265fcf) | 54 | [Specification](./stable/src/modules/module-documentation.md) |
| [main](./main/manifest.json) | [061ed8376134](https://github.com/Clooos/Bubble-Card/tree/061ed8376134307ba1086446869d0ab736265fcf) | 54 | [Specification](./main/src/modules/module-documentation.md) |

## Reference layout

- CHANNEL/src/modules/ : parser, editor schema, lifecycle
- CHANNEL/src/components/sub-button/ : sub-button DOM and CSS
- CHANNEL/src/cards/sub-buttons/ : card integration
- CHANNEL/src/tools/ : conditions and style helpers
- CHANNEL/README.md : official public documentation

CHANNEL means stable or main. The manifest records the last commit that changed
a tracked source. Unrelated upstream commits do not cause noisy pull requests.
See CHANNEL-DIFF.md for stable/main differences and UPDATES.md for update history.

Update: python3 scripts/sync_bubble_card_reference.py
Verify offline: python3 scripts/sync_bubble_card_reference.py --verify
