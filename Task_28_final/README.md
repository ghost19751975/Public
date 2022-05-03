Описание
--------

Этот репозиторий содержит учебную работу с использованием паттерна PageObject, Selenium и Python (PyTest + Selenium).

Файлы
-----

[conftest.py](conftest.py) содержит весь необходимый код для запуска браузера, обнаружения неудачных тестов и создания скриншота страницы в таком случае

[pages/base.py](pages/base.py) содержит паттерн PageObject, реализованный для Python.

[pages/elements.py](pages/elements.py) содержит вспомогательный класс для определения элементов на страницах.

[pages/labirint.py](pages/labirint.py) содержит объявление класса MainPage с методами для тестирования указанного сайта.

[tests/test_labirint.py](tests/test_labirint.py) содержит несколько дымовых Web UI тестов для книжного магазина Лабиринт (https://www.labirint.ru)

Запуск тестов
-------------

1) Установить все требуемые модули:

    ```bash
    pip3 install -r requirements.txt
    ```

2) Тесты используют Selenium WebDriver из https://github.com/mozilla/geckodriver/releases (выберите совместимый с вашим браузером драйвер). 


3) В файле [conftest.py](conftest.py) в фикстуре start_browser() измените путь к драйверу на свой. Фикстуру можно адаптировать под любой драйвер, но тестирование проводилось только в браузере FireFox.


4) Запуск всех тестов (по отдельности тесты можно запустить, скопировав в консоль соответствующую команду из скрипта):

    ```bash
    .\run_tests.bat
    ```
