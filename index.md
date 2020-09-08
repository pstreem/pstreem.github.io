---
title: Blog
---

<nav class="site-nav">
  <div class="trigger">
    {% for page in site.pages %}
    {% if page.title %}
    {% if page.group = 'navigation' %}
    <a class="page-link" href="{{ page.url | prepend: site.baseurl }}">{{ page.title }}</a>
    {% endif %}
    {% endfor %}
  </div>
</nav>



<h1>Latest Posts</h1>

<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
      <p>{{ post.excerpt }}</p>
    </li>
  {% endfor %}
</ul>
