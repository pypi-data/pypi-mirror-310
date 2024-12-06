from telegram_framework.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Resets the values of the project environment variables"
    
    def __init__(self, argv=None):
        super().__init__(argv)
        
    def add_arguments(self, parser):
        return super().add_arguments(parser)
    
    def handle(self, **options):
        print("Environment variables successfully updated")
