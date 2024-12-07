# LocalFinder

A tool for calculating the local correlation and fold change of two tracks to find significantly different genomic regions.

## Installation Requirements

Before installing and using `LocalFinder`, please ensure that the following external tools are installed on your system:

- **bedtools**: Used for genomic interval operations.
  - Installation: [https://bedtools.readthedocs.io/en/latest/content/installation.html](https://bedtools.readthedocs.io/en/latest/content/installation.html)
- **ucsc-bigwigtobedgraph**: Used for converting BigWig files to BedGraph format.
  - Download: [http://hgdownload.soe.ucsc.edu/admin/exe/](http://hgdownload.soe.ucsc.edu/admin/exe/)
- **samtools**: Used for processing SAM/BAM files.
  - Installation: [http://www.htslib.org/download/](http://www.htslib.org/download/)

These tools are required for processing genomic data and must be installed separately.

## Installation

Install `LocalFinder` using `pip`:

```bash
pip install LocalFinder
```
To check whether the package LocalFinder is successfully installed, run tests/scripts/test.sh

