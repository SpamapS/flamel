# flamel - flip YAML to JSON, and/or JSON to YAML

Just like Nicholas Flamel, who could simply grab a pile of lead and turn it in
to gold when he needed gold, flamel will turn your pile of YAML in to JSON when
you need JSON. It will also turn your JSON in to YAML if that's what you want
it to do.

A few features:

* Tries to detect input and flip to the alternative
* Maintains the order of keys in mappings from input to output

## Install

Flamel is available in the cheese shop: [https://pypi.org/project/flamel/](https://pypi.org/project/flamel/)

You can install it with `pip install flamel`

## See it in action

```
$ cat foo.yaml
things:
  - thing1
  - thing2
other:
  mapping: 9999
$ flamel foo.yaml
{
  "things": [
    "thing1",
    "thing2"
  ],
  "other": {
    "mapping": 9999
  }
}
$ flamel foo.yaml > foo.json
$ flamel foo.json
things:
- thing1
- thing2
other:
  mapping: 9999
```
