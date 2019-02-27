---
title: Terms
permalink: /doc/terms
---

# RDF Terms

To use these terms you may wish to add a prefix in your RDF like so:

```turtle
@prefix roc: <{{ site.data.terms.prefix }}>
```

{% for term in site.data.terms.properties %}
### `{{ term.name }}`

<table class="table">
  <tbody>
    <tr>
      <th scope="row">IRI</th>
      <td>
        <a href="{{ site.data.terms.prefix }}{{ term.name }}">
          {{ site.data.terms.prefix }}{{ term.name }}
        </a>
      </td>
    </tr>
  </tbody>
</table>

{{ term.description }}
{% endfor %}
