# Generated by Django 4.2.11 on 2024-04-29 01:04

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('currency', models.CharField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('BGN', 'Bulgarian Lev'), ('CZK', 'Czech Republic Korun'), ('DKK', 'Danish Krone'), ('GBP', 'British Pound Sterling'), ('HUF', 'Hungarian Forint'), ('PLN', 'Polish Zloty'), ('RON', 'Romanian Leu'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('ISK', 'Icelandic Króna'), ('NOK', 'Norwegian Krone'), ('HRK', 'Croatian Kuna'), ('RUB', 'Russian Ruble'), ('TRY', 'Turkish Lira'), ('AUD', 'Australian Dollar'), ('BRL', 'Brazilian Real'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('HKD', 'Hong Kong Dollar'), ('IDR', 'Indonesian Rupiah'), ('ILS', 'Israeli New Sheqel'), ('INR', 'Indian Rupee'), ('KRW', 'South Korean Won'), ('MXN', 'Mexican Peso'), ('MYR', 'Malaysian Ringgit'), ('NZD', 'New Zealand Dollar'), ('PHP', 'Philippine Peso'), ('SGD', 'Singapore Dollar'), ('THB', 'Thai Baht'), ('ZAR', 'South African Rand')], max_length=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=1000, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
