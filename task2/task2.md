## Скрипт для подсчёта количества животных по алфавиту

Этот проект реализует скрипт, который получает с русскоязычной Википедии список всех животных из категории [Животные по алфавиту](https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту) и сохраняет в файл `beasts.csv` количество животных на каждую букву алфавита.

### Пример содержимого результирующего файла

```csv
А,642
Б,412
В,....
```

> **Примечание:**  
> Анализ текста не производится — учитывается любая запись из категории (в том числе роды и другие таксоны).

### Быстрый старт

1. Создайте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # для Linux/Mac
    venv\Scripts\activate     # для Windows
    ```

2. Установите необходимые библиотеки:

    ```bash
    pip install aiohttp beautifulsoup4 tqdm
    ```


После выполнения скрипта файл `beasts.csv` появится в рабочей директории.
