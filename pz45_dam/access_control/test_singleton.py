"""Проверка того, что AccessManager создаёт только один экземпляр."""
from access_control.singleton import AccessManager

print('=' * 60)
print('ТЕСТ SINGLETON')
print('=' * 60)
manager1 = AccessManager()
manager2 = AccessManager()
print('manager1 is manager2:', manager1 is manager2)
print('id(manager1):', id(manager1))
print('id(manager2):', id(manager2))
assert manager1 is manager2
print('Singleton работает корректно!')
