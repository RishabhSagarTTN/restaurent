from django.core.management.base import BaseCommand

import uvicorn

class Command(BaseCommand):
    help="run django server"
    def handle(self, *args, **options):
        uvicorn.run("restaurent.asgi:application", reload=True)