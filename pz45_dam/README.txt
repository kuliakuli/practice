ПЗ №4–5. Вариант 8 — система управления доступом к БД (DAM)

Содержимое:
- config/ — настройки и маршрутизация Django-проекта
- access_control/singleton.py — Singleton AccessManager
- access_control/models.py — базовый класс, наследники и AccessRequestFactory
- access_control/views.py — страницы Django
- access_control/urls.py — два URL приложения
- access_control/test_singleton.py — проверка Singleton
- access_control/test_factory.py — проверка Factory

Запуск в Windows PowerShell из папки проекта:
1. python -m venv venv
2. .\venv\Scripts\Activate.ps1
3. pip install django
4. python manage.py runserver
5. Открыть http://127.0.0.1:8000/access/
6. Вторая страница: http://127.0.0.1:8000/access/requests/

Запуск тестов из корневой папки проекта:
python -m access_control.test_singleton
python -m access_control.test_factory

В проекте используется учебная демонстрация доступа: объекты запросов не подключаются к реальной БД и не выдают реальные права.
