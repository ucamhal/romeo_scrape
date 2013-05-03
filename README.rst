Romeo Scrape
============

A command line tool to screen scrape Journal titles from SHERPA RoMEO.

It (ab)uses a bug in the Journal Browse page to fetch a list of all
RoMEO journals in one go.

The data comes from the `RoMEO Journal Browse page <http://www.sherpa.ac.uk/romeo/journalbrowse.php?la=en&fIDnum=|&mode=simple>`_.


Usage
-----

When run with no arguments, `romeo_scrape.py` will download & parse the
RoMEO journal data, then print it to stdout. You should therefore
redirect stdout to a file in most cases. Here's how you'd fetch the
journals and save them to `scrape.json`::

  $ romeo_scrape.py > scrape.json

Note that this will take a minute or two to run. It produces ~ 5MiB of
data typically.

The output will be like::

    {
      "source": "http://www.sherpa.ac.uk/romeo/",
      "license": "Creative Commons Attribution-NonCommercial-ShareAlike 2.5",
      "journals": [
        {
          "title": "1616: Anuario de Literatura Comparada",
          "issn": [],
          "essn": [],
          "colour": "blue",
          "publisher": "Ediciones Universidad de Salamanca",
          "notes": "Other parties"
        },
        {
          "title": "19th-Century Music",
          "issn": [
            "0148-2076"
          ],
          "essn": [
            "1533-8606"
          ],
          "colour": "green",
          "publisher": "University of California Press",
          "notes": null
        },

        [...]
      ]
    }

For full usage, run::

  $ romeo_scrape.py -h


Install
-------

Run::

  $ python setup.py install
