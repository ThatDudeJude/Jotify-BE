from django.core.management.base import BaseCommand
from base.models import CustomUser
from environs import Env

env = Env()
env.read_env()


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(email=env.str("SU_EMAIL")).exists():
            CustomUser.objects.create_superuser(
                name="that-dude-jude",
                email=env.str("SU_EMAIL"),
                password=env.str("SU_PASSWORD"),
                is_staff=True,
            )

        print("Superuser has been created!")
