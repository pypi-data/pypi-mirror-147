# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_pg_fts']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.3.24,<2.0.0']

setup_kwargs = {
    'name': 'sqlalchemy-pg-fts',
    'version': '0.1.1',
    'description': 'SqlAlchemy Postgres tsquery functionality',
    'long_description': '# SqlAlchemy Postgres Full Text Search\n\nThis provides the `websearch_to_tsquery` functionality that postgres\nprovides out of the box, but it adds support for using `*` as a wildcard.\n\n## Usage\n\n### Saving a TSQuery\n\n```python\nclass Query(Base):\n    __tablename__ = \'query\'\n    query = Column(TSQuery) # english query by default\n    spanish_query = Column(TSQuery(language = \'spanish\'))\n    simple_query = Column(TSQuery(language = None)) # or \'simple\'\n```\n\n### Saving a TSVector\n\nNote: there isn\'t much value in doing this as opposed to creating the\nindexes on a `TEXT` column unless the original text does not matter.\n\n```python\nclass Vector(Base):\n    __tablename__ = \'vector\'\n    vector = Column(TSVector) # english by default\n    spanish_vector = Column(TSVector(language = \'spanish\'))\n    simple_vector = Column(TSVector(language = None)) # or \'simple\'\n```\n\n### Filtering with `to_tsquery`\n\n```python\nfrom sql_alchemy_fts import to_tsquery\n\nvecs = session.\n    query(Vector).\n    filter(\n        Vector.vector.op("@@")(to_tsquery(\'english\', \'dinosaur & extinction\')),\n    ).all()\n\n```\n\nNote: `vector` is a `TSVector`. This will also work as text, but it will\nnot give a chance to specify language (so will be `\'simple\'` by default,\nunless postgres has been configured otherwise).\n\n### Filtering with `websearch`\n\n```python\nfrom sql_alchemy_fts import to_tsquery, websearch\nquery = websearch(\'dinosaur "long time" -"jurassic park"\')\nvecs = session.\n    query(Vector).\n    filter(\n        Vector.vector.op("@@")(to_tsquery(\'english\', query),\n    ).all()\n```\n\n### Creating a TSVector index\n\n```python\nfrom sql_alchemy_fts import to_tsvector\n\nclass Document(Base):\n    __tablename__ = \'document\'\n    body = Column(Text)\n    # track language so we can create partial indexes for language matches\n    language = Column(Text)\n\n    __tableargs__ = [Index("ix_document_body_english_gin_tsvector", to_tsvector(\n        # Create english language index\n        Index(\n            "ix_document_body_english_gin_tsvec",\n            text("to_tsvector(\'english\', body)"),\n            postgresql_using="gin",\n            postgresql_where=text("language = \'english\'"),\n        ),\n        # Create spanish language index\n        Index(\n            "ix_document_body_spanish_gin_tsvec",\n            text("to_tsvector(\'spanish\', body)"),\n            postgresql_using="gin",\n            postgresql_where=text("language = \'spanish\'"),\n        ),\n    ]\n\n# querying spanish docs:\nsession.\n    query(Document).\n    filter(\n        # convert the text type to_tsvector to match the index\n        to_tsvector(\'spanish\', Document.body).\n            op("@@")(to_tsquery("spanish", "dinosaurios & vivieron"))\n    ).\n    # required for postgres to match the index to be used\n    filter(Document.language == "spanish").\n    all()\n\n```\n\nNote: an index is likely going to be useful even if the `TEXT` was dropped\nand only a `TSVector` was saved on the table.\n\n\n### Websearch Syntax\n\nThis is inspired by the `websearch_to_tsquery` function that is defined in\npostgres, but it does not allow a `"*"` to wildcard after a prefix,\ndespite that `tsquery` supports it. Therefore, to make this work, the\nentire websearch to tsquery has to be done within python.\n\n1. `websearch("dinosaur stomp")`: Dinosaur and stomp both must show up.\n1. `websearch("dinosaur or stomp")`: Either must show up.\n1. `websearch("dinosaur "long time ago")`: Dinosaur must show up and the\n   phrase "long time ago" must show up.\n1. `websearch("the of a an by dinosaur")`: Dinosaur must show up and the\n   other words are of no value so they are filtered (by postgres itself).\n1. `websearch("super*")`: Word with the prefix of super* is required such\n   as superman, superb, or superior.\n1. `websearch("-dinosaur")` Anything without the word dinosaur.\n1. `websearch("dinosuar -"jurassic park")`: The phrase jurassic park must\n   not be present, but dinosaur must show up.\n\nThe `websearch` class only renders out a tsquery text fragment. It is\nintended to be composed with `to_tsquery`.\n\n## Development\n\n### Setup\n\n1. Install [asdf](https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies).\n1. Add python plugin: `asdf plugin-add python`.\n    1. Add a `$HOME/.default-python-packages` containing `poetry`.\n1. Optionally, add postgres plugin: `asdf plugin-add postgres.\n1. `asdf install` to install python and postgres.\n\n### Tests\n\nRun `poetry run tox` or `poetry run tox --asdf-install` if some versions of python are missing.\n\nNote: make sure postgres is running. If installed through asdf, it needs to be started with `pg_ctl`.\n\n',
    'author': 'Joel Johnson',
    'author_email': 'johnson.joel.b@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/liaden/sqlalchemy-pg-fts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.15,<4.0.0',
}


setup(**setup_kwargs)
