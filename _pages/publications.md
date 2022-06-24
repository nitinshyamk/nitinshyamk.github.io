---
layout: archive
title: "Publications and Projects"
permalink: /publications/
author_profile: true
---

Also listed at my [Google Scholar profile](https://scholar.google.com/citations?user=lF0ZyBQAAAAJ&hl=en&oi=ao)

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
