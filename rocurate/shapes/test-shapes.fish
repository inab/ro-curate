#!/usr/bin/env fish

assert -- pyshacl -s shapes.ttl prefixes.ttl
and assert -- not pyshacl -s shapes.ttl blankro.ttl
and assert -- pyshacl -s shapes.ttl minimalro.ttl
and assert -- pyshacl -s shapes.ttl ro.ttl
and assert -- not pyshacl -s shapes.ttl ro-noprov.ttl
and assert -- pyshacl -s shapes.ttl ro.json
and assert -- not pyshacl -s shapes.ttl ro-mixedprov.ttl
and assert -- not pyshacl -s shapes.ttl ro-halfprov.ttl
and assert -- not pyshacl -s shapes.ttl ro-halfprov.json
