ARIA
====

TOSCA
-----

ARIA adheres strictly and meticulously to the [TOSCA Simple Profile v1.0 specification](http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html).
The ARIA API documentation always links to the relevant section of the specification, and
likewise we provide an annotated version of the specification that links back to the API
documentation.

There are seven possible levels of validation errors:

0. Platform errors. E.g. network, hardware, of even an internal bug in ARIA (let us know, please!).
1. Syntax and format errors. E.g. non-compliant YAML, XML, JSON.
2. Field validation. E.g. assigning a string where an integer is expected, using a list instead of a dict.
3. Relationships between fields within a type. This is "grammar" as it applies to rules for setting the values of fields in relation to each other.
4. Relationships between types. E.g. referring to an unknown type, causing a type inheritance loop. 
5. Topology. These errors happen if requirements and capabilities cannot be matched in order to assemble a valid topology.
6. External dependencies. These errors happen if requirement/capability matching fails due to external resources missing, e.g. the lack of a valid virtual machine, API credentials, etc. 


Quick Start
-----------

You need Python. Use a [virtualenv](https://virtualenv.pypa.io/en/stable/):

	pip install virtualenv
	virtualenv env
	. env/bin/activate
	make aria-requirements

Now run a quick TOSCA blueprint validation:

	./aria blueprints/node-cellar.yaml 


`aria.parsing`
---------------

The ARIA parser's generates a representation of TOSCA profiles in Python, such that they
can be validated, consumed, or manipulated.

Importantly, it keeps the original TOSCA data intact, such that modifications can be
written back to files. This includes keeping all the original comments in the YAML
file in their right places.

It is furthermore possible to use ARIA in order to generate a complete TOSCA profile
programmatically, in Python, and then write it to files. The same technique can be
used to convert from one DSL (parse it) to another (write it).

The parser works in three phases, represented by packages and classes in the API:

* `aria.loading`: Loaders are used to read the TOSCA data, usually as text.
  For example UriTextLoader will load text from URIs (including files).
* `aria.reading`: Readers convert data from the loaders into agnostic raw
  data. For example, YamlReader converts YAML text into Python dicts, lists, and
  primitives.
* `aria.presentation`: Presenters wrap the agnostic raw data in a nice
  Python facade (a "presentation") that makes it much easier to work with the data,
  including utilities for validation, querying, etc. Note that presenters are
  _wrappers_: the agnostic raw data is always maintained intact, and can always be
  accessed directly or written back to files.

The term "agnostic raw data" (ARD?) appears often in the documentation. It denotes
data structures comprising _only_ Python dicts, lists, and primitives, such that
they can always be converted to and from language-agnostic formats such as YAML,
JSON, and XML. A considerable effort has been made to conserve the agnostic raw
data at all times. Thus, though ARIA makes good use of the dynamic power of Python,
you will _always_ be able to use ARIA with other systems.


Consumers
---------

ARIA also comes with various "consumers" that do things with presentations. Consumers
can be generic, or can be designed to work only with specific kinds of presentations.

Though you can simply make use of presentation without using the ARIA consumer API,
the advantage of using it is that you may benefit from other tools that make use of
the API.

### Validator

One important built-in consumer is the validator. It actually works quite simply:
it goes over the entire presentation, attempts to read all the fields, and accumulates
all the error messages into a single report. Error messages include the exact location
(file, line, column) where the error occurred.

### Implementer

This converts the presentation into an "implementation", which is the Python class
structure implied by TOSCA. Thus, node types become classes, the instances being
nodes, interfaces can be turned into methods, and these are connected to each other
via special relationship classes. You can use these classes directly in your product,
allowing a quick and easy way to move from a TOSCA blueprint to a topology.

The TOSCA specification defines a large set of common node and relationship types,
for virtual machines, networks, databases, IP addresses, etc. ARIA comes with
ready-made implementations for all of these in the `tosca` pacakge. For example,
if a TOSCA artifact type derives from `tosca.artifacts.Deployment.Image.VM`, this
would be implemented as normal Python inheritance from a class that is already
defined in ARIA.

Note that the implementer is entirely optional: it is very much possible to consume
the validated TOSCA presentation as is appropriate for your product without converting
it into an implementation.


CLI Tool
--------

Though ARIA is fully exposed as an API, it also comes with a CLI tool to allow you to
work from the shell:

   aria blueprints/node-cellar.yaml

The tool loads YAML files and run consumers on them. It can be useful for quickly
validating a blueprint.

If other consumers are in the Python path, it can run them, too: it can thus serve as
a useful entry point for complex TOSCA-based tools, such as deployers, orchestractors,
etc.

REST Tool
---------

The ARIA REST tool starts a RESTful HTTP server that can do basic validation over the
wire:

    aria-rest

With the server started, you can hit a few endpoints:

    curl http://localhost:8080/validate/blueprints/simple-blueprint.yaml

You will get a JSON response with a list of validation issues. You can also POST a
blueprint over the wire:

    curl --data-binary @blueprints/simple-blueprint.yaml http://localhost:8080/validate/
