ARIA
====

TOSCA
-----

ARIA adheres strictly and meticulously to the [TOSCA Simple Profile v1.0 specification](http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html).
The ARIA API documentation always links to the relevant section of the specification, and
likewise we provide an annotated version of the specification that links back to the API
documentation.


`aria.parser.Parser`
--------------------

The ARIA parser's goal is to generation a representation of TOSCA profiles in Python,
such that they can be validated, consumed, or manipulated.

Importantly, it keeps the original TOSCA data intact, such that modifications can be
written back to files.

It is furthermore possible to use ARIA in order to generate a complete TOSCA profile
programmatically, in Python, and then write it to files. The same technique can be
used to convert from one DSL (parse it) to another (write it).

The parser has three phases, represented by packages and classes in the API:

* `aria.loader.Loader`: Loaders are used to read the TOSCA data, usually as text.
  For example UriTextLoader will load text from URIs (including files).
* `aria.reader.Reader`: Readers convert data from the loaders into agnostic raw
  data. For example, YamlReader converts YAML text into Python dicts, lists, and
  primitives.
* `aria.presenter.Presenter`: Presenters wrap the agnostic raw data in a nice
  Python facade (a "presentation") that makes it much easier to work with the data,
  including utilities for validation, querying, etc. Note that presenters are
  _wrappers_: the agnostic raw data is always maintained intact, and can always be
  accessed directly or written back to files.

The term "agnostic raw data" (ARD?) is used a lot in the documentation. It denotes
data structures comprising _only_ Python dicts, lists, and primitives, such that
they can always be converted to and from language-agnostic formats such as YAML,
JSON, and XML. Thus, though ARIA makes good use of the dynamic power of Python, you
will _always_ be able to use ARIA with other systems.


Consumers
---------

ARIA also comes with various "consumers" that do things with presentation. Consumers
can be generic, or can be designed to work only with specific kinds of presentations.

Though you can simply make use of presentation without using the ARIA consumer API,
the advantage of using it is that you may benefit from other tools that make use of
the API.


CLI Tool
--------

Though ARIA is fully exposed as an API, it also comes with a CLI tool to allow you to
work from the shell.
