from typing import Optional

from telegram.ext import filters, CommandHandler, MessageHandler
from telegram.ext.filters import BaseFilter


class HandlerDecorators:
    def __init__(self) -> None:
        self.handlers_list = []
    
    def command(self, command_name: str, filters: Optional[BaseFilter] = None, block: bool = True, has_args: Optional[bool | int] = None):
        """Decorator to set a CommandHandler for a callback function."""
        def decorator(func):
            self.handlers_list.append(CommandHandler(command_name, func, filters, block, has_args))
            return func
        return decorator
    
    def message(self, filters: Optional[BaseFilter] = filters.TEXT & ~filters.COMMAND, block: bool = True) -> CommandHandler:
        """Decorator to set a MessageHandler for a callback function."""
        def decorator(func):
            self.handlers_list.append(MessageHandler(filters, func, block))
            return func
        return decorator
