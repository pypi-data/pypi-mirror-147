.. highlight:: shell

.. _blasr:

Blasr
=====

Installing Blasr
----------------

The easiest way to install ``blasr`` is described in `PacBio & Bioconda`_.
One way to do that and make the result usable by |project| would be to follow
the instructions to install ``pbbioconda`` (as described in
`PacBio & Bioconda`_) and pass the path to the ``blasr`` executable to
``sm-analysis`` if needed. For example:

.. prompt:: bash

   sm-analysis my.bam my.fasta -b /path/to/blasr


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
