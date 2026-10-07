---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

design:
  spacing: '6rem'

sections:
  - block: resume-biography-3
    content:
      username: admin
      text: ''
      headings:
        about: ''
        education: ''
        interests: ''
    design:
      css_class: hbx-bg-gradient
      avatar:
        size: medium
        shape: circle
  - block: collection
    id: projects
    content:
      title: 'Research & Projects'
      text: |-
        I build agentic AI and work across disciplines, from clinical and biomedical teams to neuroscience, hardware, and computer vision, with both academic and industry partners. My focus: (1) LLM agents and evaluation for high-stakes domains such as healthcare, (2) machine learning methods for multimodal data, and (3) open, reproducible tools that other developers can build on.
      filters:
        folders:
          - projects
        exclude_featured: false
      sort_by: weight          # or 'date'
      sort_ascending: false
    design:
      view: article-grid               # or 'article-grid' if you prefer
      columns: 3               # number, not string, also fine as '3'
      show_image: true         # set to false for text-only
      show_date: false
      show_author: false
  - block: markdown
    id: news
    content:
      title: "News"
      text: |-
        {{< events_table limit="5" seeall="/news/" seeall_text="See all news" >}}
    design:
      columns: '1'
---
