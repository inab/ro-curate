---
title: Terms
permalink: /doc/terms
---

# RDF Terms

To use these terms you may wish to add a prefix in your RDF like so:

```turtle
@prefix roc: <{{ site.data.terms.prefix }}>
```

This documentation assumes the following prefixes:

```turtle
{{ site.data.terms.ext_prefixes }}
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
    {% for attr in term.attributes %}
      <tr>
        <th scope="row">{{ attr.name }}</th>
        <td>{{ attr.value }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

{{ term.description }}
{% endfor %}
