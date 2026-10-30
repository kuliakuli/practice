from django.http import HttpResponse
from .singleton import AccessManager
from .models import AccessRequestFactory


def index(request):
    """Главная страница: демонстрация Singleton и Factory."""
    manager = AccessManager()
    read_request = AccessRequestFactory.create('read', 'user1', 'production_db')
    write_request = AccessRequestFactory.create('write', 'dba1', 'production_db')
    manager.register_request(read_request)
    manager.register_request(write_request)

    html = f"""
    <html><head><meta charset='utf-8'><title>Управление доступом к БД</title></head>
    <body>
      <h1>Система управления доступом к БД (DAM)</h1>
      <h2>Singleton</h2>
      <p>Идентификатор экземпляра AccessManager: {id(manager)}</p>
      <p>Всего зарегистрировано запросов: {len(manager.get_all_requests())}</p>
      <h2>Factory</h2>
      <ul><li>{read_request.get_info()}</li><li>{write_request.get_info()}</li></ul>
      <p><a href='/access/requests/'>Посмотреть все запросы</a></p>
    </body></html>
    """
    return HttpResponse(html)


def requests_list(request):
    manager = AccessManager()
    rows = ''.join(f'<li>{item.get_info()}</li>' for item in manager.get_all_requests())
    return HttpResponse(
        "<html><head><meta charset='utf-8'></head><body>"
        "<h1>Журнал запросов доступа</h1>"
        f"<p>Всего запросов: {len(manager.get_all_requests())}</p><ul>{rows}</ul>"
        "<a href='/access/'>На главную</a></body></html>"
    )
