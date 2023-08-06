.. |license| image:: https://img.shields.io/github/license/mghorbani2357/Mockend
    :target: https://raw.githubusercontent.com/mghorbani2357/Mockend/master/LICENSE
    :alt: GitHub Licence

.. |downloadrate| image:: https://img.shields.io/pypi/dm/Mockend
    :target: https://pypistats.org/packages/Mockend

.. |wheel| image:: https://img.shields.io/pypi/wheel/Mockend  
    :target: https://pypi.python.org/pypi/Mockend
    :alt: PyPI - Wheel

.. |pypiversion| image:: https://img.shields.io/pypi/v/Mockend  
    :target: https://pypi.python.org/pypi/Mockend
    :alt: PyPI

.. |format| image:: https://img.shields.io/pypi/format/Mockend
    :target: https://pypi.python.org/pypi/Mockend
    :alt: PyPI - Format

.. |downloads| image:: https://static.pepy.tech/personalized-badge/Mockend?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/Mockend

.. |lastcommit| image:: https://img.shields.io/github/last-commit/mghorbani2357/Mockend 
    :alt: GitHub last commit
    
.. |lastrelease| image:: https://img.shields.io/github/release-date/mghorbani2357/Mockend   
    :alt: GitHub Release Date

*****************
Mockend API
*****************

.. class:: center

 |license| |downloadrate| |downloads| |pypiversion| |format| |wheel| |lastcommit| |lastrelease|


Mockend is a Python library that can be used to mock any REST API endpoint.

Installation
============

.. code-block:: bash

    pip install mockend


Quick Start
===========

Mockend is a simple, lightweight, and extensible REST API mocking Python library.
It can be used to mock any REST API endpoint, and can be used to mock any HTTP method.
the library is very easy to use and easy to extend. It just need configuration file, then it
will simulate the REST API response.

Configuration examples
=======================

.. code-block:: json

    {
      "user": {
        "id": {
          "3": {
            "post": {
              "status": 403,
              "response": "User not authorized!"
            }
           }
          },
        "get": {
        "status": 200,
        "response":{
            "user-ids":[1,2,3],
          }
        }
      }
    }

How to use
=======================

.. code-block:: bash

    mockend -c config.json