What is Alabester?
==================

Alabaster with some CSS bugs squashed. See it live at `introt docs <https://introt.github.io/docs/>`_.

How to use Alabester?
.....................

``pip install alabester``

After installation, just ``s/labaster/labester/g`` across your project,
requirements included (if Alabaster was indirectly pulled by Sphinx,
make sure to add Alabester to your list!) - the 0.7.x versions will
try not to break compatibility.

However, it's not a drop-in replacement; due to Sphinx hard-coding
some extra defaults for Alabaster, your sidebar might not look as
expected without the following modification.

For the default Alabaster experience, put this in your ``conf.py``:

.. code-block:: python

   html_sidebars = {
           '**': [
               'about.html',
               'navigation.html',
               'relations.html',
               'searchbox.html',
               'donate.html'
           ]
   }

If you'd like to know more, check out eg. sphinx-doc/sphinx#5066. (I also wrote a debugging murder mystery on my `bleg <https://introt.github.io/bleg>`_ on 4/20).

Changelog
.........

`Available on GitHub <https://github.com/introt/alabester/releases>`_.

For max combatibility, you can pin version 0.7.20. Upstream docs apply.

Want to improve Alabester? `Join in on the fun <https://github.com/introt/alabester>`_!

-----

What is Alabaster?
==================

Alabaster is a visually (c)lean, responsive, configurable theme for the `Sphinx
<http://sphinx-doc.org>`_ documentation system. It is Python 2+3 compatible.

It began as a third-party theme, and is still maintained separately, but as of
Sphinx 1.3, Alabaster is an install-time dependency of Sphinx and is selected
as the default theme.

Live examples of this theme can be seen on `this project's own website
<http://alabaster.readthedocs.io>`_, `paramiko.org <http://paramiko.org>`_,
`fabfile.org <http://fabfile.org>`_ and `pyinvoke.org <http://pyinvoke.org>`_.

For more documentation, please see http://alabaster.readthedocs.io.

.. note::
    You can install the development version via ``pip install -e
    git+https://github.com/bitprophet/alabaster/#egg=alabaster``.
