# distribution

1. bump the version in `pyproject.toml`

2. commands to build and test new plugin versions
    ```bash
    llm uninstall llm-council -y
    rm -r dist/
    python -m build

    llm install dist/llm_council*.whl
    ```


3. distribute via pypi
    ```bash
    python -m twine upload  dist/*
    ```