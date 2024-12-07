conda-forge-only
================

.. image:: https://github.com/sfinkens/conda-forge-only/workflows/CI/badge.svg
    :target: https://github.com/sfinkens/conda-forge-only/actions/workflows/ci.yml

.. image:: https://codecov.io/gh/sfinkens/conda-forge-only/graph/badge.svg?token=5MMOU081WQ
    :target: https://codecov.io/gh/sfinkens/conda-forge-only


A pre-commit hook to check that conda environment files use conda-forge only.

Usage
-----

Add the following lines to your project's ``.pre-commit-config.yaml``:

.. code-block:: yaml

    repos:
      - repo: https://github.com/sfinkens/conda-forge-only
        rev: v0.1.0
        hooks:
          - id: conda-forge-only
