# HTML-Template für MISTA

Die HTML-Datei hat folgende Struktur. Alle CSS-Klassen und JavaScript-Logik exakt so übernehmen.

---

## Grundstruktur

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MISTA — KBV-Kategorisierung [DATUM]</title>
  <style>
    /* → CSS einfügen (siehe unten) */
  </style>
</head>
<body>
  <div class="header">
    <div class="header-left">
      <h1>KBV-Kategorisierung</h1>
      <div class="header-meta">[DATUM] · [ANZAHL] Cases</div>
      <div class="stats">
        <span class="badge badge-s">[N] S</span>
        <span class="badge badge-m">[N] M</span>
        <span class="badge badge-l">[N] L</span>
      </div>
    </div>
    <div class="header-right">
      <input type="text" class="search" id="search" placeholder="Suche nach Titel, Case-ID, JIRA-ID...">
    </div>
  </div>

  <div class="container">
    <!-- Abschnitt: My Action Required -->
    <div class="section-title">My Action Required</div>
    <!-- Case-Cards hier -->

    <!-- Abschnitt: Neue Cases (nur wenn angefordert) -->
    <div class="section-title">Neue Cases</div>
    <!-- Case-Cards hier -->
  </div>

  <script>
    /* → JavaScript einfügen (siehe unten) */
  </script>
</body>
</html>
```

---

## CSS

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 14px; background: #f1f4f8; color: #1a1a2e; }

.header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: white; padding: 24px 32px;
  display: flex; justify-content: space-between; align-items: flex-start;
  flex-wrap: wrap; gap: 16px;
}
.header h1 { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.header-meta { font-size: 12px; opacity: 0.6; margin-bottom: 10px; }
.stats { display: flex; gap: 8px; }
.badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.badge-s { background: #d4edda; color: #155724; }
.badge-m { background: #fff3cd; color: #856404; }
.badge-l { background: #f8d7da; color: #721c24; }
.search {
  padding: 10px 16px; border-radius: 8px; border: none;
  font-size: 14px; width: 300px; outline: none;
  background: rgba(255,255,255,0.15); color: white;
}
.search::placeholder { color: rgba(255,255,255,0.5); }
.search:focus { background: rgba(255,255,255,0.25); }

.container { max-width: 960px; margin: 32px auto; padding: 0 16px; }
.section-title { font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin: 24px 0 12px; }

.case-card { background: white; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
.case-header {
  display: flex; align-items: center; gap: 12px;
  padding: 16px 20px; cursor: pointer;
  transition: background 0.15s;
}
.case-header:hover { background: #f8fafc; }
.cat-badge { padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.cat-s { background: #d4edda; color: #155724; }
.cat-m { background: #fff3cd; color: #856404; }
.cat-l { background: #f8d7da; color: #721c24; }
.case-title { font-weight: 600; font-size: 14px; flex: 1; }
.case-id { font-size: 12px; color: #6b7280; flex-shrink: 0; }
.jira-link { font-size: 12px; color: #3b82f6; text-decoration: none; flex-shrink: 0; }
.jira-link:hover { text-decoration: underline; }
.chevron { color: #9ca3af; font-size: 12px; flex-shrink: 0; transition: transform 0.2s; }
.chevron.open { transform: rotate(90deg); }

.meta-tags { display: flex; gap: 6px; flex-wrap: wrap; padding: 0 20px 12px; }
.meta-tag { background: #f1f4f8; color: #6b7280; padding: 2px 8px; border-radius: 4px; font-size: 11px; }

.case-body { padding: 0 20px 20px; display: none; }
.case-body.open { display: block; }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.info-card { padding: 16px; border-radius: 8px; background: #f8fafc; }
.info-card.blue { border-left: 3px solid #3b82f6; }
.info-card.purple { border-left: 3px solid #8b5cf6; }
.info-card h4 { font-size: 12px; font-weight: 600; color: #6b7280; text-transform: uppercase; margin-bottom: 8px; }
.info-card p { font-size: 13px; line-height: 1.6; }

.mitigation-block { margin-bottom: 16px; }
.mitigation-block h4 { font-size: 12px; font-weight: 600; color: #6b7280; text-transform: uppercase; margin-bottom: 10px; }
.mitigation-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.mitigation-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.mit-card { background: #f8fafc; border-radius: 8px; padding: 12px; }
.mit-card h5 { font-size: 11px; font-weight: 600; color: #374151; margin-bottom: 6px; }
.mit-card ul { padding-left: 16px; }
.mit-card li { font-size: 12px; color: #6b7280; line-height: 1.6; margin-bottom: 2px; }

.gutachten-toggle {
  background: none; border: 1px solid #e5e7eb; border-radius: 6px;
  padding: 6px 14px; font-size: 12px; color: #6b7280; cursor: pointer;
  margin-bottom: 12px; transition: all 0.15s;
}
.gutachten-toggle:hover { background: #f1f4f8; color: #374151; }
.gutachten-content { display: none; background: #f8fafc; border-radius: 8px; padding: 16px; font-size: 13px; line-height: 1.7; white-space: pre-wrap; }
.gutachten-content.open { display: block; }

.fazit-s { background: #d4edda; color: #155724; padding: 10px 14px; border-radius: 6px; font-size: 13px; margin-top: 10px; }
.fazit-m { background: #fff3cd; color: #856404; padding: 10px 14px; border-radius: 6px; font-size: 13px; margin-top: 10px; }
.fazit-l { background: #f8d7da; color: #721c24; padding: 10px 14px; border-radius: 6px; font-size: 13px; margin-top: 10px; }

@media (max-width: 700px) {
  .grid-2, .mitigation-grid-2, .mitigation-grid-3 { grid-template-columns: 1fr; }
  .search { width: 100%; }
  .case-header { flex-wrap: wrap; }
}
```

---

## Case-Card HTML-Struktur

```html
<div class="case-card" data-search="[TITEL] [CASE-ID] [JIRA-ID]">
  <div class="case-header" onclick="toggleCase(this)">
    <span class="cat-badge cat-[s|m|l]">[S|M|L]</span>
    <span class="case-title">[TITEL]</span>
    <span class="case-id">[CASE-ID]</span>
    <a href="[JIRA-URL]" class="jira-link" onclick="event.stopPropagation()" target="_blank">[JIRA-ID]</a>
    <span class="chevron">▶</span>
  </div>
  <div class="meta-tags">
    <span class="meta-tag">[Solution Type]</span>
    <span class="meta-tag">[Service Package]</span>
    <span class="meta-tag">[Status]</span>
  </div>
  <div class="case-body">
    <div class="grid-2">
      <div class="info-card blue">
        <h4>Personenbezogene Daten</h4>
        <p>[Beschreibung der verarbeiteten Daten]</p>
      </div>
      <div class="info-card purple">
        <h4>Auswirkungen auf Mitarbeitende</h4>
        <p>[Beschreibung der Auswirkungen]</p>
      </div>
    </div>

    <!-- Mitigation: 2-spaltig bei S, 3-spaltig bei M/L -->
    <div class="mitigation-block">
      <h4>Mitigationsmaßnahmen</h4>
      <div class="mitigation-grid-[2|3]">
        <div class="mit-card">
          <h5>Geplante Maßnahmen</h5>
          <ul><li>[Maßnahme]</li></ul>
        </div>
        <div class="mit-card">
          <h5>Empfohlene Maßnahmen</h5>
          <ul><li>[Maßnahme]</li></ul>
        </div>
        <!-- Nur bei M oder L: -->
        <div class="mit-card">
          <h5>Upgrade zu S möglich wenn</h5>
          <ul><li>[Bedingung]</li></ul>
        </div>
      </div>
    </div>

    <button class="gutachten-toggle" onclick="toggleGutachten(this); event.stopPropagation()">Gutachten anzeigen</button>
    <div class="gutachten-content">[GUTACHTEN-FLIESSTEXT]</div>
  </div>
</div>
```

---

## JavaScript

```javascript
function toggleCase(header) {
  const body = header.parentElement.querySelector('.case-body');
  const chevron = header.querySelector('.chevron');
  body.classList.toggle('open');
  chevron.classList.toggle('open');
}

function toggleGutachten(btn) {
  const content = btn.nextElementSibling;
  content.classList.toggle('open');
  btn.textContent = content.classList.contains('open') ? 'Gutachten verbergen' : 'Gutachten anzeigen';
}

document.getElementById('search').addEventListener('input', function() {
  const q = this.value.toLowerCase();
  document.querySelectorAll('.case-card').forEach(card => {
    const text = card.dataset.search.toLowerCase();
    card.style.display = text.includes(q) ? '' : 'none';
  });
});
```
