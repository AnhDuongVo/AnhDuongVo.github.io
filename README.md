# anhduongvo.github.io

Personal website of Maria (Anh Duong Vo), built with a small Python script instead of a site generator.

```
src/
  content/
    site.yaml            name, links, headline, tagline, repo list
    story.yaml           bio, experience, education, publications, skills
    events.yml           news table (newest first on the page)
    projects/<slug>/     index.md with front matter (title, summary, tags, short, card)
                         plus the page's images and videos
  templates/             Jinja2 templates: base, work, story, project
  static/                CSS, images, favicon
build.py                 renders everything into _site/
```

Edit the YAML and Markdown files, then:

```bash
pip install -r requirements.txt
python build.py
python -m http.server -d _site 8000     # preview at http://localhost:8000
```

Pushing to `main` builds and deploys through GitHub Actions. Videos in a project page are written as
`{{< video src="name.mp4" >}}`; a `name.jpg` next to it is used as the poster.

The previous HugoBlox site is kept in `_hugoblox-archive/` and is no longer built.
