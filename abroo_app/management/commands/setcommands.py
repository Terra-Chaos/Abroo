from django.core.management.base import BaseCommand
from abroo_app.setup_commands import set_bot_commands
import asyncio

class Command(BaseCommand):
    help = 'Sets the bot commands for command hints in Telegram'

    def handle(self, *args, **options):
        self.stdout.write('Setting bot commands...')
        asyncio.run(set_bot_commands())
        self.stdout.write(self.style.SUCCESS('Bot commands have been set.'))