# FastAPI_SQLAlchemy_template
## Описание
......

## Для разработчиков:
### Пример файла с переменными среды:
".env.example"

### Линтер:
`black`

### Pre-commit:
Настроен pre-commit для проверки оформления кода.
Для проверки кода перед выполнением операции commit, выполнить команду:

```bash
pre-commit run --all-files
```

## Как запустить проект:

1. Клонировать проект
```bash
git clone git@github.com:PentiukPavel/.....
```

2. Переименовать файл .env.example и изменить содержимое на актуальные данные.
```bash
mv .env.example .env
```

### 1) Запуск проекта на локальной машине:

1. Создать виртуальное окружение:
```bash
py -3 -m venv venv
```
2. Активировать виртуальное окружение:
```bash
source venv/Scripts/activate
```
3. Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
4. При необходимости установить дополнительные зависимости для разработчиков из файла requirements_dev.txt:
```bash
pip install -r requirements_dev.txt
```
5. перейти в корневую папку проекта:
```bash
cd src
```
6. Выполнить миграции c помощью команды:
```bash
alembic upgrade head
```
7. Запустить проект:
```bash
uvicorn main:app --reload
```

### 2) Запуск на локальной машине через Docker

1. Установка [Docker](https://www.docker.com/get-started/)
2. Для запуска проекта в корневой папке выполнить команду:
    ```bash
    docker-compose up -d
    ```
3. Выполнить миграции c помощью команды:
    ```bash
    docker-compose exec backend alembic upgrade head
    ```
4. Для остановки проекта в корневой папке выполнить команду:
    ```bash
    docker-compose down -v
    ```

Документация к API (swagger) будет доступна по ссылке: http://127.0.0.1/docs/
## Системные требования
### Python==3.12

## Стек
### FastAPI
### pytest
### SQLAlchemy
### PosrgreSQL
### Redis
### Nginx
