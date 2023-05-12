import json
from django.core.management.base import BaseCommand
from Application.models import Qualification, School, Department, Programs

class Command(BaseCommand):
    help = 'Load data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('/home/samtech/Desktop/My_Code/Bugema-Univ/programs.json', type=str)

    def handle(self, *args, **options):
        file_path = options['/home/samtech/Desktop/My_Code/Bugema-Univ/programs.json']

        with open(file_path, 'r') as f:
            data = json.load(f)

        qualifications = data['qualifications']
        schools = data['schools']

        for q in qualifications:
            qualification = Qualification.objects.create(id=q['id'], name=q['name'])

        for s in schools:
            school = School.objects.create(id=s['id'], name=s['name'])
            departments = s['departments']

            for d in departments:
                department = Department.objects.create(id=d['id'], name=d['name'], school=school)
                programs = d['programs']

                for p in programs:
                    program = Programs.objects.create(id=p['id'], name=p['name'], qualification_id=p['qualification_id'], department=department)
