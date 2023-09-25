# EBANX project by Lucas Dionatan Torres

### How to execute this project

This project requires:
    
   * Python 3.11

## installation
1 - Install dependencies
We need install project dependencies with `poetry`:
###### obs: Can you install poetry in [this link](https://python-poetry.org/docs/)

```
 poetry install
```

3 - Execute the virtualenv

```
poetry shell
```

4 - Execute the project server:

```
uvicorn apps.main:app --reload
```

- Update dependencies:

```
poetry update
```

- Run tests:

```
pytest
```

## Test result with ipkiss:
![image](https://github.com/lucasldtdionatan/ebanx_project/assets/55671737/88976d05-e6a3-4deb-b27f-3ae1ebc59885)

