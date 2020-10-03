---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

Here are some selected publications. For the full list, see my [Google Scholar profile](https://scholar.google.com/citations?user=lF0ZyBQAAAAJ&hl=en&oi=ao)

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
