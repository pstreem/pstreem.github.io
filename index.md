---
title: Blog
---

<header class="site-header">

    <span> <section class="site-title"><a href="{{ site.baseurl }}/">{{ site.title }}</a></section> 
      <section class="site-meta">{{ site.tagline }}</section> </span>

    <nav class="site-nav">
      <div class="trigger">
        {% for page in site.pages %}
        {% if page.title %}
        <a class="page-link" href="{{ page.url | prepend: site.baseurl }}">{{ page.title }}</a>
        {% endif %}
        {% endfor %}
      </div>
    </nav>

</header>


<h1>Latest Posts</h1>

<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
      <p>{{ post.excerpt }}</p>
    </li>
  {% endfor %}
</ul>
