from telegram_framework.core.decorators import HandlerDecorators


class Module(HandlerDecorators):
    def __init__(self, name: str, import_name: str) -> None:
        super().__init__()
        self.name = name
        self.import_name = import_name
