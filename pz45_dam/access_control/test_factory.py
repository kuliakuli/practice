"""Проверка создания разных типов запросов через Factory."""
from access_control.models import AccessRequestFactory, ReadAccess, WriteAccess, AdminAccess

print('=' * 60)
print('ТЕСТ FACTORY')
print('=' * 60)
read = AccessRequestFactory.create('read', 'user1', 'test_db')
write = AccessRequestFactory.create('write', 'dba1', 'test_db')
admin = AccessRequestFactory.create('admin', 'admin1', 'test_db')
print(read.get_info())
print(write.get_info())
print(admin.get_info())
assert isinstance(read, ReadAccess)
assert isinstance(write, WriteAccess)
assert isinstance(admin, AdminAccess)
print('Доступные типы:', AccessRequestFactory.get_available_types())
try:
    AccessRequestFactory.create('unknown', 'user1', 'test_db')
except ValueError as error:
    print('Ошибка перехвачена:', error)
else:
    raise AssertionError('Ожидалась ошибка ValueError')
print('Factory работает корректно!')
