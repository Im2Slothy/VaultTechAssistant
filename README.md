# Vault-Tec Assistant website

Static HTML, CSS, and JavaScript. The October 2026 redesign uses a blue-and-yellow resident handbook, the project's existing assistant mascot, source-verified commands, and current campaign artwork. The existing Vercel API rewrites remain in `vercel.json`.

## Preview and check

From this directory:

```powershell
python scripts/build_site.py
python scripts/check_site.py
node --check assets/site.js
python -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765. Stop the server with Ctrl+C. No package installation or framework build is required. All content and command paths are in the checked-in HTML; JavaScript adds search/filtering, clipboard assistance, and the optional public activity feed. If the feed fails, the page reports unavailability without implying the bot is offline.

## Maintaining content

- `assets/commands.json`: current public entry points and actual menu paths. `scripts/build_site.py` renders the command directory and shared header/footer into all pages. Its generated header/footer regions are marked in HTML. Other page content is authored directly.
- `story.html`: spoiler-light start guide, acts, field tools, optional districts, and records.
- `wiki.html` and `wiki/`: deeper reference, with optional endings and character revelations in closed details sections. Existing routes remain, including `wiki/characters/profile-template.html`, which now contains Mara's file.
- `assets/site.css` and `assets/site.js`: shared appearance and browser behavior. The previous CSS files are retained for history and are no longer loaded by the rebuilt pages.
- `assets/campaign-*.webp`: compressed copies of existing bot artwork. `assets/assistant.webp` is the existing project mascot. Source PNGs and other existing media were preserved.

Before changing claims, compare against the bot working tree in `C:\Users\chris\Documents\[scripts]\fallout-bot`. The audit includes local changes and does not certify what version the live Discord process has loaded.

Command authority: `fallout_bot/command_hubs.py`, `bot.py`, and cogs for campaign, community, feedback, contracts, settlements, combat and fishing. Most historical slash commands are removed by `install_command_hubs`; they are menu paths, not runnable public commands. `/stop` is a DM-only feedback conversation control. Deprecated `/use`, owner and beta utilities are deliberately excluded.

Campaign authority: `campaign_chapters_early.py`, `campaign_chapters_late.py`, `campaign_expansion_*`, `campaign_district_*`, `campaign_field_tools.py`, `campaign_navigation.py`, `campaign_hints.py`, `campaign_commendations.py`, and `campaign_survivor_rewards.py`. Source takes priority over older writing plans. Persistent commendations and explicit once-only survivor payouts are the exception to otherwise separate campaign resources.

## Verification boundary

Local link and structure checks plus interactive browser checks are required after changes. The bot API's live uptime, installed Discord command schema, and deployed bot revision need separate operational verification. No fabricated player counts, online status, testimonials, or playtime claims are used. No hosting migration was made; publication remains through the existing repository/hosting workflow.

## Visual references

The manual direction follows the user's preference for Vault-Tec corporate blue/yellow and retro printed instructions. Research consulted The Wand Company's Pip-Boy manual and Refero's anti-AI-slop guidance. Neither reference's artwork or layout files were copied into this repository. Google Fonts supplies Archivo Narrow, Libre Franklin, and Courier Prime, with local fallbacks.
