class AccessRequest:
    """Базовый класс запроса на доступ к базе данных."""
    access_type = 'UNKNOWN'

    def __init__(self, username, database):
        self.username = username
        self.database = database

    def get_info(self):
        raise NotImplementedError('Метод get_info() должен быть переопределён')

    def __str__(self):
        return self.get_info()


class ReadAccess(AccessRequest):
    access_type = 'READ'

    def get_info(self):
        return f"READ-доступ: пользователь {self.username}, БД {self.database}"


class WriteAccess(AccessRequest):
    access_type = 'WRITE'

    def get_info(self):
        return f"WRITE-доступ: пользователь {self.username}, БД {self.database}"


class AdminAccess(AccessRequest):
    access_type = 'ADMIN'

    def get_info(self):
        return f"ADMIN-доступ: пользователь {self.username}, БД {self.database}"


class AccessRequestFactory:
    """Factory: создаёт нужный тип запроса по строковому обозначению."""
    _registry = {
        'read': ReadAccess,
        'write': WriteAccess,
        'admin': AdminAccess,
    }

    @classmethod
    def create(cls, access_type, username, database):
        normalized_type = access_type.lower()
        if normalized_type not in cls._registry:
            available = ', '.join(cls._registry)
            raise ValueError(f"Неизвестный тип доступа: {access_type}. Доступны: {available}")
        return cls._registry[normalized_type](username, database)

    @classmethod
    def get_available_types(cls):
        return list(cls._registry.keys())
