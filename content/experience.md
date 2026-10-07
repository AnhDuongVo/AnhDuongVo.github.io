---
title: 'Experience'
date: 2023-10-24
type: landing

design:
  spacing: '5rem'

# Note: `username` refers to the user's folder name in `content/authors/`

# Page sections
sections:
  - block: resume-experience
    content:
      username: admin
    design:
      # Hugo date format
      date_format: 'January 2006'
      # Education or Experience section first?
      is_education_first: false
  - block: resume-skills
    content:
      title: Skills & Hobbies
      username: admin
    design:
      show_skill_percentage: false
  - block: collection
    id: publications
    content:
      title: Publications and conferences
      text: |-
        Journal articles, preprints and conference presentations from my PhD and earlier work.
      filters:
        folders:
          - publications
        exclude_featured: false
      sort_by: date
      sort_ascending: false
    design:
      view: citation
      columns: '1'
  - block: resume-awards
    content:
      title: Awards
      username: admin
  - block: resume-languages
    content:
      title: Languages
      username: admin
---
