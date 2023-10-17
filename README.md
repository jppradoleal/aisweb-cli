# Como executar o projeto?

## Docker
```bash
docker build -t aisweb .
docker run aisweb -i SJBD
```


## Poetry
```bash
poetry install
poetry run aisweb -i SBJD
```

## Python
```bash
pip install -r requirements.txt
python aisweb_cli/main.py -i SJBD
```

# Cache
Para evitar sobrecarga no servidor alvo, a CLI tem um Cache opcional usando Redis, basta rodar o próximo comando antes de executar a CLI.

```bash
docker-compose up -d
```
