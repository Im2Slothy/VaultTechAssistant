"""Render the checked-in command directory and shared static navigation."""
from pathlib import Path
import json
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
INVITE = 'https://discord.com/oauth2/authorize?client_id=1107428963246166026'
SUPPORT = 'https://discord.gg/RQBhmWEzTx'
SYMBOL = '<svg class="brand-symbol" viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M24 3 30 7 37 7 40 14 45 19 43 27 43 34 36 38 31 44 24 42 17 44 12 38 5 34 5 27 3 19 8 14 11 7 18 7Z" stroke="currentColor" stroke-width="2"/><circle cx="24" cy="24" r="13" stroke="currentColor" stroke-width="2"/><path d="m16 19 8 13 8-13M24 13v5" stroke="currentColor" stroke-width="3"/></svg>'

def head(title, description):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#214e76"><meta name="description" content="{escape(description, quote=True)}"><title>{escape(title)} | Vault-Tec Assistant</title><link rel="icon" href="favicon.png" type="image/png"><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script></head>'''

def command_page():
    commands = json.loads((ROOT/'assets/commands.json').read_text(encoding='utf-8-sig'))
    categories = list(dict.fromkeys(c['category'] for c in commands))
    filters = '<button type="button" class="filter-button" data-filter="all" aria-pressed="true">All entry points</button>'
    filters += ''.join(f'<button type="button" class="filter-button" data-filter="{escape(c)}" aria-pressed="false">{escape(c)}</button>' for c in categories)
    cards = []
    for c in commands:
        slug = c['name'].strip('/').split()[0]
        details = ''.join(f'<li>{escape(d)}</li>' for d in c['details'])
        cards.append(f'''<article class="command-card" id="{slug}" data-category="{escape(c['category'])}" data-keywords="{escape(c['keywords'], quote=True)}"><span class="category">{escape(c['category'])}</span><h2><code>{escape(c['name'])}</code></h2><p>{escape(c['summary'])}</p><details><summary>Menu paths &amp; field notes</summary><ul>{details}</ul></details><button type="button" class="copy-command" data-command="{escape(c['name'])}" aria-label="Copy {escape(c['name'])}">Copy command</button></article>''')
    html = head('Command field manual', 'The current Vault-Tec Assistant commands and menu paths. Search radio, expeditions, fishing, raids, trading, settlements, and the Chicago campaign.') + f'''<body data-page="commands"><!-- SITE_HEADER --><main id="main-content"><section class="page-hero"><div class="container"><p class="eyebrow">Vault-Tec field manual / Revised October 2026</p><h1>Command directory.</h1><p class="lead">Find a current command, then follow its menu paths in Discord. Search by activity to see where radio, fishing, crafting, and other features live.</p><div class="notice"><strong>Returning survivor?</strong> Activities such as radio, fishing, raids, and your daily allowance now live inside menus. The old slash commands have moved. Open <code>/wasteland</code> to get your bearings.</div></div></section><section class="section container"><div class="search-box"><label for="command-search">FIND A COMMAND OR ACTIVITY</label><input type="search" id="command-search" placeholder="Try radio, crafting, daily contracts, or Chicago…" aria-controls="command-results" autocomplete="off"></div><div class="filter-row" role="group" aria-label="Filter commands by category">{filters}</div><p class="result-status" id="result-status" role="status">{len(commands)} entry points</p><noscript><p class="notice">All commands and their menu paths are listed below. Enable JavaScript for search and filters.</p></noscript><div class="command-list" id="command-results">{''.join(cards)}<div class="empty-state" id="command-empty" hidden><h2>No matching commands.</h2><p>Try a different activity or select All entry points.</p></div></div></section><section class="container section"><div class="section-heading"><div><p class="eyebrow">Quick reference</p><h2>Using the menus.</h2></div></div><div class="card-grid"><article class="card"><h3>Your menu is yours.</h3><p>Open a command yourself to operate its controls. When a panel expires, reopen its entry point to continue.</p></article><article class="card"><h3>Check before you go.</h3><p>Cooldowns, supplies, access, and settlement roles affect which actions you can take. The bot shows requirements at the point of use.</p></article><article class="card"><h3>Need a hand?</h3><p>Use <code>/help</code>, send <code>/feedback</code>, or <a href="{SUPPORT}" target="_blank" rel="noopener noreferrer">visit the community</a>. For the campaign, start with the <a href="story.html">story guide</a>.</p></article></div></section></main><!-- SITE_FOOTER --></body></html>'''
    (ROOT/'commands.html').write_text(html, encoding='utf-8')

def header(prefix, active):
    items = [('home','index.html','Overview'),('commands','commands.html','Commands'),('story','story.html','Story guide'),('wiki','wiki.html','Story wiki')]
    links = ''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if key == active else '')+f'>{label}</a>' for key,url,label in items)
    return f'''<!-- SITE_HEADER_BEGIN --><a class="skip-link" href="#main-content">Skip to content</a><header class="site-header"><div class="container header-inner"><a class="brand" href="{prefix}index.html" aria-label="Vault-Tec Assistant home">{SYMBOL}<span class="brand-name">VAULT-TEC ASSISTANT<small>RESIDENT SERVICES · DISCORD BOT</small></span></a><a class="header-invite" href="{INVITE}" target="_blank" rel="noopener noreferrer">Add to Discord <span aria-hidden="true">↗</span></a><nav class="site-nav" id="site-nav" aria-label="Main navigation">{links}<a href="{SUPPORT}" target="_blank" rel="noopener noreferrer">Community ↗</a></nav></div></header><!-- SITE_HEADER_END -->'''

def footer(prefix):
    return f'''<!-- SITE_FOOTER_BEGIN --><footer class="site-footer"><div class="container"><div class="footer-top"><a class="footer-brand" href="{prefix}index.html">Vault-Tec Assistant</a><nav class="footer-links" aria-label="Footer"><a href="{prefix}commands.html">Commands</a><a href="{SUPPORT}" target="_blank" rel="noopener noreferrer">Support server</a><a href="https://ko-fi.com/im2slothy" target="_blank" rel="noopener noreferrer">Ko-fi</a><a href="{prefix}privacy.html">Privacy</a><a href="{prefix}terms.html">Terms</a></nav></div><div class="footer-bottom"><p>A fan project by Im2Slothy. Fallout, Vault-Tec, and related names belong to their respective owners. Not affiliated with or endorsed by Bethesda Softworks or ZeniMax.</p><span>HANDBOOK · OCTOBER 2026</span></div></div></footer><!-- SITE_FOOTER_END -->'''

def shared_shell():
    count=0
    for path in ROOT.rglob('*.html'):
        if any(p.startswith('.') for p in path.relative_to(ROOT).parts):
            continue
        html=path.read_text(encoding='utf-8-sig')
        if '<!-- SITE_HEADER' not in html:
            continue
        prefix='../' * (len(path.relative_to(ROOT).parts)-1)
        match=re.search(r'<body[^>]*data-page=[\'"]([^\'"]+)', html)
        active=match.group(1) if match else ''
        html=re.sub(r'<!-- SITE_HEADER_BEGIN -->.*?<!-- SITE_HEADER_END -->|<!-- SITE_HEADER -->',lambda m:header(prefix,active),html,flags=re.S)
        html=re.sub(r'<!-- SITE_FOOTER_BEGIN -->.*?<!-- SITE_FOOTER_END -->|<!-- SITE_FOOTER -->',lambda m:footer(prefix),html,flags=re.S)
        path.write_text(html,encoding='utf-8')
        count+=1
    print(f'Rendered command directory and shared navigation for {count} pages.')

if __name__=='__main__':
    command_page()
    shared_shell()
