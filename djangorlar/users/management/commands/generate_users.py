import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

# Management command to generate fake users
class Command(BaseCommand):
    help = 'Generate 10,000 fake users and bulk inserts them in batches'

    def handle(self, *args, **options):
        fake = Faker()

        DEPARTMENTS = ['HR', 'Sales', 'IT', 'Finance', 'Marketing', 'Operations']
        ROLES = ['admin', 'manager', 'employee']
        BATCH_SIZE = 1000

        users_to_create = []

        hashed_password = make_password("12345") # Pre-hash the password once

        self.stdout.write('Starting user generation...')
        start_time = timezone.now()

        for i in range(10000):
            # birthdate between 20 and 50 years ago
            birthdate = fake.date_of_birth(minimum_age=20, maximum_age=50)
            # uniqe suffix to ensure unique email and username
            unique_suffix = f"{i}_{random.randint(1000, 9999)}"
            email = f"{fake.user_name()}{unique_suffix}@gmail.com"
            username = f"{fake.user_name()}{unique_suffix}"

            user = User(
                email=email,
                username=username,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                city=fake.city(),
                country=fake.country(),
                department=random.choice(DEPARTMENTS),
                role=random.choice(ROLES),
                birth_date=birthdate,
                salary = Decimal(random.randint(150000, 1500000)),
                password=hashed_password,
                is_active=True,
                is_staff=random.choice([True, False, False]) # 1/3 chance to be staff
            )
            users_to_create.append(user)

            # Bulk create in batches
            if len(users_to_create) == BATCH_SIZE:
                User.objects.bulk_create(users_to_create)
                users_to_create = [] # Reset the list
                self.stdout.write(self.style.SUCCESS(f'Successfully created batch of {BATCH_SIZE} users.'))
        
        
        if users_to_create:
            User.objects.bulk_create(users_to_create)
            self.stdout.write(self.style.SUCCESS(f'Successfully created final batch of {len(users_to_create)} users.'))
        end_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(
            f'Total time taken: {(end_time - start_time).total_seconds()} seconds.'
        ))
        self.stdout.write(self.style.SUCCESS('All users generated.'))
