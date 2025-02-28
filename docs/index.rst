Amazon Product Recommendation System
================================

A graph-based recommendation system using Amazon product review data.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   modules
   development
   testing
   api

Installation
-----------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/yourusername/amazon-recommendation-system.git
   cd amazon-recommendation-system

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   # Install dependencies
   pip install -r requirements.txt

Quick Start
----------

.. code-block:: bash

   # Run the recommendation pipeline
   cd scripts
   ./run_recommendation_pipeline.sh -c electronics -r 4 -n 20

Features
--------

* Graph-based recommendation system
* Community detection using Louvain method
* Network centrality metrics
* Link prediction algorithms
* Time-based analysis
* Performance evaluation

Development
----------

Contributing
~~~~~~~~~~~

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Testing
~~~~~~~

Run the tests using:

.. code-block:: bash

   python -m pytest tests/

Type checking with mypy:

.. code-block:: bash

   mypy src/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 