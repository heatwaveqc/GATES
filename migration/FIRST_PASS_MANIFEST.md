# GATES Wiki First-Pass Migration Manifest

This manifest is the execution checklist for the first population pass defined in `WORK_HANDOFF.md`.

Status values: **Queued / Mapping / Migrating / Validation / Complete / Needs Revisit**

| Section | Source / Entity | Drive ID | Status | Target tiddlers / notes |
|---|---|---|---|---|
| Navigation | GATES Home + section indexes | repo-native | Queued | Domains, Species, Setting, Gods, Monsters, Technology, Campaigns, System |
| Domains | Kung Fu | 138Rw052iOGusYVsBcpDPUZHmtQERXktD95EwqHpBBCI | Queued | Root + Gaoshou + Shadow Arts |
| Domains | Shadow Arts — Water Breathing | 138Rw052iOGusYVsBcpDPUZHmtQERXktD95EwqHpBBCI | Queued | Complete tree instance + composite Jutsu |
| Domains | Foundational | 1H3-_qwSQZWB8bFAvQquusxw5Hf2oM6iJGSskCy8x4Lo | Queued | Root + Low Magic + Innovator + High Magic |
| Domains | Eldritch Gifts | 1_F8il7EGu-k4mOHJwZDx2_7l0EZJPcPFN9QmmACyfSU | Queued | Root + Revelator + Dreadhound + Spawn |
| Species | Species framework rules | 1al1svM0dKcm4E150iH6LuwUuoPcSZY1LdSZBgy61_C0 | Queued | Central species-rule tiddlers |
| Species | Firrerreo | 1al1svM0dKcm4E150iH6LuwUuoPcSZY1LdSZBgy61_C0 | Queued | Atomic Species components |
| Species | Perfectly Normal Cat | 1al1svM0dKcm4E150iH6LuwUuoPcSZY1LdSZBgy61_C0 | Queued | Atomic Species components |
| Species | Worgen | 1al1svM0dKcm4E150iH6LuwUuoPcSZY1LdSZBgy61_C0 | Queued | Modification Species |
| Species | Goldblood | 1al1svM0dKcm4E150iH6LuwUuoPcSZY1LdSZBgy61_C0 | Queued | Atomic Species components |
| Setting | GATES Earth root | 1zk6aHWu3EybLwSeriF_d2EV5DsiQHrVMuw_ZoAzihVA | Queued | Setting root + useful atomic setting rules |
| Setting | France under the Blood Moon | 1dCjSis-3euD-EgTd134vOH33RkIETBaQaHWg9TWhfUM | Queued | Composite setting/nation entity |
| Setting | The Veltrass System | 1vhe-wZrvUWA8Ow0jvSvGSiSGq9vqVkz9msUYfKFwyLM | Queued | System hub/setting entity |
| Gods | Celestial Dragons group | 1l9sefqa0UAycpmkxJto9pRPRcPnljvbvBJl1og6DV9M | Queued | Group + Gold Dragon + Jade Dragon |
| Gods | Barbarian Gods group | 1IRwsCixEUUTV9yfmF5zjTGoK0kwjqF6cIH9Gs4WU80k | Queued | Group + Father Sky + Friend Darkness |
| Monsters | Undead | 11QeSCcOb0yhCk71NWp43sPZ3uYGxtRyj1W4LIe2RvCo | Queued | Index + Vampires + Demon Slayer Demons |
| Monsters | Demons | 1X5TQKfcj49zNYiV1jQjy5V28w9n8rtHKh02qBG3ZtnI | Queued | Index + Balseraphs + Djinn |
| Technology | Cybernetics | 1NTr6GTV4QI3BIeH-oShuHraa6VoGIyJLdhcLl3EsWgg | Queued | Framework + Tactical Cyber-Eyes + Combat Bionic Arm + Total Cyborg Body |
| Technology | Chems | 1yP4YxCaRRroUsORJ-LpOMSEzlGSmLLD2kjMEJxoewe0 | Queued | Design rules + Commercial Jet + Stimpak + Mentats |
| Campaigns | Starbucks Adventuring Division | 1SrNtdazV9bEp6sRrr3Ma_t_V-reU0vu9CkQ2T4VlLeM | Queued | Campaign root/index |
| Campaigns | Fall of Tokyo | 1-lgMToA6x-oeX-6tzgitobsfoILo5XPOSTVteLDDplI | Queued | Campaign root/index |
| System | Godmath | 19-zr0zLjEEanMedfv-lxCbrIByik7-vByLafg4rqU98 | Queued | Central reusable rules |
| System | Supernatural Power Abundance | 1So1EtjXdwr38tlv4dmA-FZaTZXeh6Xavc9C97Arh3Nc | Queued | Central reusable rules |
| System | Drive and Mark Framework | 1YUpe2p-LSdzFwTplBJ4yG97iAU2gbJFisiYc5pD_sFM | Queued | Central reusable rules |

## Decisions / questions

Record nonblocking authority, visibility, schema, or inheritance questions here rather than halting the entire migration.

## Validation

- [ ] `node scripts/validate-metadata.js`
- [ ] Player build
- [ ] GM build
- [ ] No GM/AI leakage into Player
- [ ] Navigation works
- [ ] Water Breathing recursive composition works
- [ ] Setting tag hubs work
- [ ] GitHub Actions deploy succeeds
