SimSig Collation API
====================

This will provide a conventional API interface to data parsed from SimSig
gateway messages.

It will run on a server somewhere, or on someone's PC. The administrator will
give it the URI of the SimSig host games (which could be localhost:51515 or
could be several games in a chain). It will subscribe to the interface gateways
of those games via STOMP, and build a picture of the world via their update
messages. This collated image of the game's state can then be queried via a
unstartling REST API for use by client apps.

At this point, this is just the bare bones, largely copied from examples such
as David Baumgold's "Build a Flask API" talk
<https://github.com/singingwolfboy/build-a-flask-api>

Installation on a PC
====================
::

    git clone https://github.com/JDeeth/SimSigCollate
    cd SimSigCollate
    python3 -m venv venv
    source venv/bin/activate
    pip install .

You'd then run it from within the virtual environment with `simsig-collate-api`
except at the moment it doesn't do anything.

Installation for development
============================
::

    git clone https://github.com/JDeeth/SimSigCollate
    cd SimSigCollate
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .[dev]
    pre-commit install

This should install everything needed, including `black`, `pylint`, and 
`pytest`, for which there are pre-commit hooks and configuration files in this
repository.
