from django.core.management.base import BaseCommand
from faker import Faker
from lemmo_apps.authentication.models import UserSession, UserActivity
import random
from datetime import timedelta
from django.utils import timezone
from lemmo_apps.authentication.models import User

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake user data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=10,
            help="Number of users to create (default: 10)",
        )
        parser.add_argument(
            "--sessions",
            type=int,
            default=50,
            help="Number of user sessions to create (default: 50)",
        )
        parser.add_argument(
            "--activities",
            type=int,
            default=100,
            help="Number of user activities to create (default: 100)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before generating new data",
        )

    def handle(self, *args, **options):
        users_count = options["users"]
        sessions_count = options["sessions"]
        activities_count = options["activities"]
        clear_data = options["clear"]

        if clear_data:
            self.stdout.write("Clearing existing data...")
            UserSession.objects.all().delete()
            UserActivity.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write(f"Generating {users_count} users...")

        # Generate users
        users = []
        roles = [role[0] for role in User.ROLE_CHOICES]

        for i in range(users_count):
            user_data = {
                "email": fake.unique.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "password": "password123",  # Default password for testing
                "role": random.choice(roles),
                "phone_number": fake.phone_number(),
                "employee_id": f"EMP{fake.unique.random_number(digits=6)}",
                "department": fake.job(),
                "license_number": fake.unique.random_number(digits=8)
                if random.choice([True, False])
                else None,
                "is_active": random.choice([True, True, True, False]),  # 75% active
                "is_staff": random.choice([True, False]),
                "last_login_ip": fake.ipv4(),
                "profile_picture": None,  # Skip file uploads for now
            }

            user = User.objects.create_user(**user_data)
            users.append(user)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1} users...")

        self.stdout.write(f"Successfully created {len(users)} users")

        # Generate user sessions
        self.stdout.write(f"Generating {sessions_count} user sessions...")

        for i in range(sessions_count):
            user = random.choice(users)
            session_data = {
                "user": user,
                "session_key": fake.unique.uuid4(),
                "ip_address": fake.ipv4(),
                "user_agent": fake.user_agent(),
                "expires_at": timezone.now() + timedelta(hours=random.randint(1, 24)),
                "is_active": random.choice([True, False]),
            }

            UserSession.objects.create(**session_data)

            if (i + 1) % 20 == 0:
                self.stdout.write(f"Created {i + 1} sessions...")

        self.stdout.write(f"Successfully created {sessions_count} user sessions")

        # Generate user activities
        self.stdout.write(f"Generating {activities_count} user activities...")

        activity_types = [activity[0] for activity in UserActivity.ACTIVITY_TYPES]

        for i in range(activities_count):
            user = random.choice(users)
            activity_data = {
                "user": user,
                "activity_type": random.choice(activity_types),
                "description": fake.sentence(),
                "ip_address": fake.ipv4(),
                "user_agent": fake.user_agent(),
                "metadata": {
                    "browser": fake.chrome(),
                    "os": fake.linux_platform_token(),
                    "device": fake.android_platform_token(),
                },
            }

            UserActivity.objects.create(**activity_data)

            if (i + 1) % 20 == 0:
                self.stdout.write(f"Created {i + 1} activities...")

        self.stdout.write(f"Successfully created {activities_count} user activities")

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Data generation complete!\n"
                f"📊 Summary:\n"
                f"   • Users: {User.objects.count()}\n"
                f"   • Sessions: {UserSession.objects.count()}\n"
                f"   • Activities: {UserActivity.objects.count()}\n"
                f"\n🔑 Default password for all users: password123"
            )
        )
