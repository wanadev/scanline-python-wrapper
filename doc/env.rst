Environment
===========


SCANLINE_CMD
------------

This lib needs scanline_ to be installed on the user machine in order to work. By default, the ``scanline`` executable is searched through the ``PATH``, but you can override its name or its path using the ``SCANLINE_CMD`` environment varialbe::

    export SCANLINE_CMD="./MyFolder/scanline.bin"


.. _scanline: https://github.com/klep/scanline
