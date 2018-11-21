#!/usr/bin/env fish

assert -- pyshacl -s shapes.ttl prefixes.ttl
assert -- not pyshacl -s shapes.ttl blankro.ttl
assert -- pyshacl -s shapes.ttl minimalro.ttl
