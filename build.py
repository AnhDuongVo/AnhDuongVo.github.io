#!/usr/bin/env python3
"""Build the site: src/ (content, templates, static) -> _site/.

    pip install markdown pyyaml jinja2
    python build.py            # writes _site/
    python -m http.server -d _site 8000
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "_site"
MEDIA = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".webm", ".pdf"}

env = Environment(loader=FileSystemLoader(SRC / "templates"), autoescape=select_autoescape(["html"]))
md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list"])


def load_yaml(name: str):
    return yaml.safe_load((SRC / "content" / name).read_text())


def split_front(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def render_md(text: str, folder: Path | None = None) -> str:
    def video(m):
        src = m.group(1)
        poster = Path(src).with_suffix(".jpg")
        poster_attr = f' poster="{poster}"' if folder and (folder / poster).exists() else ""
        return f'<video controls preload="metadata" playsinline{poster_attr} src="{src}"></video>'

    text = re.sub(r'{{<\s*video\s+src="([^"]+)"[^>]*>}}', video, text)
    md.reset()
    return md.convert(text)


def load_projects() -> list[dict]:
    out = []
    for d in sorted((SRC / "content" / "projects").iterdir()):
        if not (d / "index.md").exists():
            continue
        front, body = split_front((d / "index.md").read_text())
        out.append(
            {
                "slug": d.name,
                "dir": d,
                "title": front.get("title", d.name),
                "summary": front.get("summary", ""),
                "tags": front.get("tags", []),
                "short": front.get("short", d.name),
                "card_text": front.get("card", front.get("summary", "")),
                "cover": front.get("cover", "featured.png"),
                "card_cover": front.get("card_cover", front.get("cover", "featured.png")),
                "weight": front.get("weight", 0),
                "html": Markup(render_md(body, d)),
            }
        )
    return out


def fmt_date(s: str) -> str:
    return dt.date.fromisoformat(str(s)).strftime("%-d %b %Y")


def load_events() -> list[dict]:
    rows = load_yaml("events.yml")
    rows.sort(key=lambda r: str(r["start"]), reverse=True)
    for r in rows:
        start, end = str(r["start"]), str(r.get("end") or r["start"])
        r["date"] = fmt_date(start) if start == end else f"{fmt_date(start)} to {fmt_date(end)}"
    return rows


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)


def main() -> None:
    site = load_yaml("site.yaml")
    site["email_href"] = "mailto:" + site["email"]
    story = load_yaml("story.yaml")
    story["bio_html"] = Markup(render_md(story["bio"]))
    story["where_i_stand_html"] = Markup(render_md(story["where_i_stand"]))
    projects = {p["slug"]: p for p in load_projects()}
    ordered = [projects[s] for s in site["projects"]]
    year = dt.date.today().year

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(SRC / "static" / "css", OUT / "assets" / "css")
    shutil.copytree(SRC / "static" / "img", OUT / "assets" / "img")
    shutil.copy(SRC / "static" / "favicon.svg", OUT / "favicon.svg")
    (OUT / ".nojekyll").write_text("")

    common = {"site": site, "year": year}
    write(
        OUT / "index.html",
        env.get_template("work.html").render(
            **common, root="./", path="/", nav="projects", title=f"{site['name']} · Projects", description=site["description"],
            projects=ordered, og_image=f"/projects/{ordered[0]['slug']}/{ordered[0]['cover']}",
        ),
    )
    write(
        OUT / "about" / "index.html",
        env.get_template("about.html").render(
            **common, root="../", path="/about/", nav="about", theme="dark", title=f"{site['name']} · About me", description=site["description"],
            story=story, events=load_events(), og_image="/assets/img/portrait.png",
        ),
    )
    for p in projects.values():
        dest = OUT / "projects" / p["slug"]
        dest.mkdir(parents=True)
        for f in p["dir"].iterdir():
            if f.suffix.lower() in MEDIA:
                shutil.copy(f, dest / f.name)
        write(
            dest / "index.html",
            env.get_template("project.html").render(
                **common, root="../../", path=f"/projects/{p['slug']}/", nav="projects", title=f"{p['title']} · {site['name']}",
                description=p["summary"], p=p, og_image=f"/projects/{p['slug']}/{p['cover']}",
            ),
        )
    n = sum(1 for _ in OUT.rglob("*.html"))
    print(f"built {n} pages into {OUT}")


if __name__ == "__main__":
    main()
