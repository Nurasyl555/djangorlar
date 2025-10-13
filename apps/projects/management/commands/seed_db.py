import random
from faker import Faker

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from apps.projects.models import Project, Task


class Command(BaseCommand):
    help = 'Seeds the database with 20 projects, tasks, and users.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Creating admin user...")
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            self.stdout.write(self.style.SUCCESS("Admin 'admin' (pass: 'adminpassword') created."))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists. Skipping."))

        if Project.objects.exists():
            self.stdout.write(self.style.WARNING("Data seems to exist already. Aborting seed."))
            return

        fake = Faker()

        self.stdout.write("Creating 20 test users...")
        users = [User.objects.create_user(username=fake.user_name(), password='password123') for _ in range(20)]
        admin_user = User.objects.get(username='admin')
        all_users = users + [admin_user]
        self.stdout.write(self.style.SUCCESS("Users created."))

        self.stdout.write("Creating 20 projects...")
        projects = []
        for _ in range(20):
            author = random.choice(all_users)
            project = Project.objects.create(
                name=fake.company() + " Initiative",
                author=author
            )
            project.users.set(random.sample(all_users, k=random.randint(1, min(5, len(all_users)))))
            projects.append(project)
        self.stdout.write(self.style.SUCCESS("Projects created."))

        self.stdout.write("Creating tasks for projects...")
        for project in projects:
            for _ in range(random.randint(1, 5)):
                task_assignees = list(project.users.all())
                if not task_assignees:
                    task_assignees = random.sample(all_users, k=1)

                task = Task.objects.create(
                    name=fake.bs().capitalize(),
                    description=fake.text(max_nb_chars=200),
                    status=random.choice([c[0] for c in Task.STATUS_CHOICES]),
                    project=project,
                )
                k = random.randint(1, len(task_assignees))
                task.assignees.set(random.sample(task_assignees, k=k))
        self.stdout.write(self.style.SUCCESS("Tasks created."))
        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))