---
layout: page
title: Tags
permalink: /ttags/
---

<ul class="tags-box">

{% if site.posts != empty %}
  
  
{% for tag in site.tags %}
<a href="#{{ tag[0] }}" title="{{ tag[0] }}" rel="{{ tag[1].size }}">{{ tag[0] }}<span class="size"> {{ tag[1].size }}</span></a>
{% endfor %}
</ul>



{% else %}
<span>No posts</span>
{% endif %}



</ul>

