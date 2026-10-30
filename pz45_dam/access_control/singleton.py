class AccessManager:
    """Singleton: единый менеджер доступа к базам данных."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.access_log = []
        return cls._instance

    def register_request(self, request):
        self.access_log.append(request)
        return f"Запрос зарегистрирован: {request.get_info()}"

    def get_all_requests(self):
        return self.access_log
