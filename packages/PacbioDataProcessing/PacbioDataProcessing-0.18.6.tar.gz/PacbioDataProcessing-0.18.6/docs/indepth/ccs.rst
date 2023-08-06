.. highlight:: shell

.. _ccs:

CCS
===

Installing CCS
--------------

The easiest way to install ``ccs`` is described in `PacBio & Bioconda`_.
One way to do that and make the result usable by |project| would be to follow
the instructions to install ``pbbioconda`` (as described in
`PacBio & Bioconda`_) and pass the path to the ``ccs`` executable to
``sm-analysis`` if needed.


How to produce CCS files for methylation analysis
-------------------------------------------------

1. Install ``pbbam``
2. Follow these steps:

.. prompt:: bash

  ccs --hifi-kinetcis input.bam intermediate.bam
  ccs-kinetics-bystrandify intermediate.bam output.bam
  

.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda


Issues
------

Multimapping
^^^^^^^^^^^^

In some cases an aligned CCS file presents multimapping. Two examples take from the
``st1A09`` file::

  m54099_200720_153206/4194505/ccs        0       U00096.3        392180  0       150=    *       0       0       ATCTGTACGTAAGTACGTGATGTCTCCTGCCCACTTCT...
  m54099_200720_153206/4194505/ccs        256     U00096.3        1094716 0       150=    *       0       0       ATCTGTACGTAAGTACGTGATGTCTCCTGCCCACTTCT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        2170808 0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        567414  0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        315863  0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  ...
  m54099_200720_153206/4194627/ccs        0       U00096.3        274198  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        574834  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        688094  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        272     U00096.3        3130803 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        256     U00096.3        2101992 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        2289162 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        272     U00096.3        1396701 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        272     U00096.3        1300156 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        256     U00096.3        3365799 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        3652279 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...

How do we decide the position? In the current implementation, the first
subread of each molecule is taken (for details, see
``pacbio_data_processing.sm_analysis.map_molecules_with_highest_sim_ratio``),
because all the subreads are *perfect*. But notice that the positions (4th
column) differ.
