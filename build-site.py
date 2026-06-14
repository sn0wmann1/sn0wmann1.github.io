#!/usr/bin/env python3
"""Build landing page from content.md"""

import re, sys
from pathlib import Path

PARTICLE_SCRIPT = """
    const c=document.getElementById('bg-canvas'),x=c.getContext('2d');
    let w,h,p=[],n=80;
    function r(){w=c.width=innerWidth;h=c.height=innerHeight}
    onresize=r;r();
    for(let i=0;i<n;i++)p.push({x:Math.random()*w,y:Math.random()*h,vx:(Math.random()-.5)*.3,vy:(Math.random()-.5)*.3,ri:Math.random()*1.5+.5,al:Math.random()*.4+.1});
    function d(){
      x.clearRect(0,0,w,h);
      for(let o of p){o.x+=o.vx;o.y+=o.vy;if(o.x<0)o.x=w;if(o.x>w)o.x=0;if(o.y<0)o.y=h;if(o.y>h)o.y=0;
      x.beginPath();x.arc(o.x,o.y,o.ri,0,7);x.fillStyle=`rgba(124,111,240,${o.al})`;x.fill()}
      for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let dx=p[i].x-p[j].x,dy=p[i].y-p[j].y,di=Math.sqrt(dx*dx+dy*dy);
      if(di<120){x.beginPath();x.moveTo(p[i].x,p[i].y);x.lineTo(p[j].x,p[j].y);x.strokeStyle=`rgba(124,111,240,${.08*(1-di/120)})`;x.stroke()}}
      requestAnimationFrame(d)
    }d()
"""

ROOT = Path(__file__).parent
CONTENT = ROOT / "content.md"
OUTPUT = ROOT / "index.html"

def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                import json
                fm[k] = json.loads(v.replace("'", '"'))
            elif v.startswith(">"):
                fm[k] = v[1:].strip()
            else:
                fm[k] = v
    return fm, text[m.end():]

def parse_sections(body):
    sections = {}
    current = None
    lines = []
    for line in body.split("\n"):
        if line.startswith("## ") and not line.startswith("### "):
            if current:
                sections[current] = "\n".join(lines).strip()
            current = line[3:].strip().lower()
            lines = []
        elif current is not None:
            lines.append(line)
    if current:
        sections[current] = "\n".join(lines).strip()
    return sections

def parse_projects(text):
    projects = []
    for line in text.split("\n"):
        m = re.match(r"-\s+\[(.+?)\]\((.+?)\)\s*—\s*(.*?)\s*—\s*(.+)", line)
        if m:
            projects.append({
                "name": m.group(1), "url": m.group(2),
                "desc": m.group(3).strip(), "lang": m.group(4).strip()
            })
    return projects

def parse_skills(text):
    skills = []
    for line in text.split("\n"):
        m = re.match(r"###\s+(.+)", line)
        if m:
            current_cat = m.group(1).strip()
            continue
        if "current_cat" in dir() and line.strip() and not line.startswith("#"):
            items = [i.strip() for i in line.split(",") if i.strip()]
            skills.append({"cat": current_cat, "items": items})
    return skills

def parse_hobbies(text):
    hobbies = []
    for line in text.split("\n"):
        m = re.match(r"-\s+(\S+)\s+(.+?)\s*—\s*(.+)", line)
        if m:
            hobbies.append({
                "icon": m.group(1), "name": m.group(2).strip(),
                "desc": m.group(3).strip()
            })
    return hobbies

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def gen_html(fm, sections):
    bio = fm.get("bio", "")
    bio = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', bio)

    social = ""
    for s in fm.get("social", []):
        social += f'<a href="{esc(s["url"])}">{esc(s["label"])}</a>\n        '

    projects = parse_projects(sections.get("projects", ""))
    icons = ["◆", "🎨", "🎵", "📦", "🎮"]
    colors = ["var(--blue)", "var(--green)", "var(--pink)", "var(--blue)", "var(--accent)"]
    bg_colors = [
        "rgba(96, 165, 250, 0.15)", "rgba(74, 222, 128, 0.15)",
        "rgba(244, 114, 182, 0.15)", "rgba(96, 165, 250, 0.15)",
        "rgba(124, 111, 240, 0.15)"
    ]
    proj_html = ""
    for i, p in enumerate(projects):
        ci = i % len(icons)
        proj_html += f"""        <a href="{esc(p["url"])}" class="project-card">
          <div class="icon" style="background: {bg_colors[ci]}; color: {colors[ci]};">{icons[ci]}</div>
          <div class="info">
            <h3>{esc(p["name"])}</h3>
            <p>{esc(p["desc"])}</p>
          </div>
          <span class="lang">{esc(p["lang"])}</span>
        </a>
"""

    skills = parse_skills(sections.get("skills", ""))
    cat_icons = {
        "development": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
        "config": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
        "infrastructure": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>',
    }
    skill_html = ""
    for s in skills:
        icon = cat_icons.get(s["cat"].lower(), "")
        items = "".join(f"<li>{esc(i)}</li>" for i in s["items"])
        skill_html += f"""        <div class="skill-cat">
          <h3>{icon} {esc(s["cat"])}</h3>
          <ul>{items}</ul>
        </div>
"""

    hobbies = parse_hobbies(sections.get("hobbies", ""))
    hobby_html = ""
    for h in hobbies:
        hobby_html += f"""        <div class="hobby-card">
          <div class="h-icon">{h["icon"]}</div>
          <h3>{esc(h["name"])}</h3>
          <p>{esc(h["desc"])}</p>
        </div>
"""

    blog_url = next((s["url"] for s in fm.get("social", []) if s["label"] == "blog"), "/blog/")

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(fm.get("name", "snow"))} ❄️</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300..900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0b0b0e;
      --surface: #121216;
      --surface-hover: #1a1a20;
      --border: #22222a;
      --text: #e8e8ed;
      --text-secondary: #8888a0;
      --text-tertiary: #5c5c72;
      --accent: #7c6ff0;
      --accent-glow: rgba(124, 111, 240, 0.2);
      --green: #4ade80;
      --blue: #60a5fa;
      --orange: #fb923c;
      --pink: #f472b6;
      --radius: 10px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Rubik', system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }}
    #bg-canvas {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; opacity: 0.3; }}
    .layout {{ position: relative; z-index: 1; max-width: 820px; margin: 0 auto; padding: 0 2rem; min-height: 100vh; }}

    nav {{ display: flex; align-items: center; justify-content: space-between; padding: 1.2rem 0; border-bottom: 1px solid var(--border); }}
    .logo {{ font-size: 1.4rem; font-weight: 600; color: var(--text); }}
    .nav-links {{ display: flex; gap: 0.25rem; list-style: none; }}
    .nav-links a {{ color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; font-weight: 500; padding: 0.4rem 0.8rem; border-radius: 6px; transition: all 0.15s; }}
    .nav-links a:hover {{ color: var(--text); background: var(--surface-hover); }}
    .nav-links a.active {{ color: var(--accent); background: var(--accent-glow); }}

    .hero {{ padding: 4rem 0 2rem; }}
    .hero .greeting {{ font-size: 2.8rem; font-weight: 700; line-height: 1.15; margin-bottom: 1rem; }}
    .hero .greeting span {{ background: linear-gradient(135deg, var(--accent), var(--blue)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
    .hero .bio {{ max-width: 580px; color: var(--text-secondary); font-size: 1rem; line-height: 1.7; }}
    .hero .bio a {{ color: var(--accent); text-decoration: none; font-weight: 500; }}
    .hero .bio a:hover {{ text-decoration: underline; }}

    section {{ margin: 3rem 0; }}
    .section-title {{ font-size: 0.9rem; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.2rem; }}
    .section-desc {{ color: var(--text-tertiary); font-size: 0.85rem; margin-bottom: 1.5rem; }}

    .projects-grid {{ display: grid; gap: 0.75rem; }}
    .project-card {{ display: flex; align-items: center; gap: 1rem; padding: 1rem 1.2rem; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none; transition: all 0.15s; }}
    .project-card:hover {{ border-color: var(--accent); background: var(--surface-hover); transform: translateY(-1px); }}
    .project-card .icon {{ width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }}
    .project-card .info {{ flex: 1; min-width: 0; }}
    .project-card .info h3 {{ font-size: 0.95rem; font-weight: 500; color: var(--text); margin-bottom: 0.15rem; }}
    .project-card .info p {{ font-size: 0.82rem; color: var(--text-tertiary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .project-card .lang {{ font-size: 0.75rem; color: var(--text-tertiary); font-family: monospace; padding: 0.2rem 0.5rem; background: var(--bg); border-radius: 4px; border: 1px solid var(--border); flex-shrink: 0; }}

    .skills-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1.5rem; }}
    .skill-cat h3 {{ font-size: 0.8rem; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.7rem; display: flex; align-items: center; gap: 0.35rem; }}
    .skill-cat h3 svg {{ flex-shrink: 0; }}
    .skill-cat ul {{ list-style: none; display: flex; flex-wrap: wrap; gap: 0.4rem; }}
    .skill-cat li {{ font-size: 0.82rem; padding: 0.3rem 0.75rem; border-radius: 6px; border: 1px solid var(--border); background: var(--surface); color: var(--text-secondary); transition: all 0.15s; }}
    .skill-cat li:hover {{ border-color: var(--accent); color: var(--text); }}

    .hobbies-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 0.75rem; }}
    .hobby-card {{ padding: 1.2rem; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); text-align: center; transition: all 0.15s; }}
    .hobby-card:hover {{ border-color: var(--accent); background: var(--surface-hover); transform: translateY(-1px); }}
    .hobby-card .h-icon {{ font-size: 1.8rem; margin-bottom: 0.4rem; }}
    .hobby-card h3 {{ font-size: 0.9rem; font-weight: 500; color: var(--text); margin-bottom: 0.2rem; }}
    .hobby-card p {{ font-size: 0.78rem; color: var(--text-tertiary); }}

    .blog-card {{ background: linear-gradient(135deg, var(--surface), var(--surface-hover)); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem 2rem; display: flex; justify-content: space-between; align-items: center; transition: all 0.15s; }}
    .blog-card:hover {{ border-color: var(--accent); }}
    .blog-card p {{ color: var(--text-secondary); font-size: 0.92rem; }}
    .blog-card a {{ color: var(--accent); text-decoration: none; font-weight: 500; font-size: 0.9rem; display: flex; align-items: center; gap: 0.3rem; }}
    .blog-card a:hover {{ text-decoration: underline; }}

    .social-links {{ display: flex; gap: 0.5rem; margin-top: 1rem; }}
    .social-links a {{ color: var(--text-tertiary); text-decoration: none; font-size: 0.85rem; padding: 0.4rem 0.8rem; border-radius: 6px; border: 1px solid var(--border); background: var(--surface); transition: all 0.15s; }}
    .social-links a:hover {{ color: var(--accent); border-color: var(--accent); }}

    footer {{ text-align: center; padding: 3rem 0 2rem; color: var(--text-tertiary); font-size: 0.8rem; }}
    footer .f-links {{ display: flex; justify-content: center; gap: 1rem; margin-bottom: 0.5rem; }}
    footer .f-links a {{ color: var(--text-tertiary); text-decoration: none; transition: color 0.15s; }}
    footer .f-links a:hover {{ color: var(--accent); }}

    @media (max-width: 600px) {{ .layout {{ padding: 0 1.2rem; }} .hero .greeting {{ font-size: 2rem; }} .project-card .lang {{ display: none; }} .project-card .icon {{ display: none; }} }}
  </style>
</head>
<body>
  <canvas id="bg-canvas"></canvas>
  <div class="layout">
    <nav>
      <div class="logo">❄️</div>
      <ul class="nav-links">
        <li><a href="/" class="active">Home</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="https://github.com/sn0wmann1">GitHub</a></li>
      </ul>
    </nav>

    <header class="hero">
      <h1 class="greeting">Hi, I'm <span>{esc(fm.get("name", "snow"))}</span></h1>
      <div class="bio"><p>{bio}</p></div>
      <div class="social-links">
        {social}
      </div>
    </header>

    <section>
      <h2 class="section-title">projects</h2>
      <p class="section-desc">things i've built</p>
      <div class="projects-grid">
{proj_html}      </div>
    </section>

    <section>
      <h2 class="section-title">skills</h2>
      <p class="section-desc">tools and technologies</p>
      <div class="skills-grid">
{skill_html}      </div>
    </section>

    <section>
      <h2 class="section-title">hobbies</h2>
      <p class="section-desc">what I do when not coding</p>
      <div class="hobbies-grid">
{hobby_html}      </div>
    </section>

    <section>
      <h2 class="section-title">blog</h2>
      <p class="section-desc">notes and writing</p>
      <div class="blog-card">
        <p>configs, keyboard hacking, project builds</p>
        <a href="{esc(blog_url)}">read →</a>
      </div>
    </section>

    <footer>
      <div class="f-links">
        <a href="/">home</a>
        <a href="/blog/">blog</a>
        <a href="https://github.com/sn0wmann1">github</a>
      </div>
      <p>snow · 2026</p>
      <p style="margin-top: 0.3rem; color: var(--text-tertiary);">MIT — use freely, change freely</p>
    </footer>
  </div>
  <script>PARTICLE_SCRIPT</script>
</body>
</html>"""

def main():
    text = CONTENT.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    sections = parse_sections(body)
    html = gen_html(fm, sections)
    html = html.replace("PARTICLE_SCRIPT", PARTICLE_SCRIPT)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Built {OUTPUT} from {CONTENT}")

if __name__ == "__main__":
    main()
