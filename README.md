# Проект YaCut — это сервис укорачивания ссылок

## Автор: Михалицын А.С. ([misterio92](https://github.com/asmikhalitsyn)) 


## **Стек**

[Python](https://www.python.org/)
[Flask](https://flask.palletsprojects.com/en/2.2.x/).

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/asmikhalitsyn/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```


Создание БД и выполнений миграций:

```

flask db init
flask db migrate
flask db upgrade
```

Запуск сервера:

```

flask run
```
