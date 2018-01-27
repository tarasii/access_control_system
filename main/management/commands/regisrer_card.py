from django.core.management.base import BaseCommand, CommandError

import os
from django.conf import settings
from main.models import Registration
import csv


class Command(BaseCommand):
    help = "register card"


    def handle(self, *args, **options):



        print "--------------------------"