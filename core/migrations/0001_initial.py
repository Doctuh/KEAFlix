# Generated by Django 4.0.3 on 2022-05-26 11:25

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('original_title', models.CharField(blank=True, max_length=255, null=True)),
                ('file', models.FileField(upload_to='movies')),
                ('description', models.TextField(blank=True, null=True)),
                ('backdrop_path', models.TextField(blank=True, null=True)),
                ('release_date', models.TextField(blank=True, null=True)),
                ('runtime', models.CharField(blank=True, max_length=255, null=True)),
                ('vote_average', models.CharField(blank=True, max_length=255, null=True)),
                ('tagline', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('type', models.CharField(blank=True, choices=[('serie', 'Serie'), ('film', 'Film')], max_length=10, null=True)),
                ('thumbnail', models.ImageField(blank=True, default='/thumbnails/default_thumbnail.jpg', null=True, upload_to='thumbnails')),
                ('age_limit', models.CharField(blank=True, choices=[('Alle', 'Alle'), ('Børn', 'Børn')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age_limit', models.CharField(choices=[('Alle', 'Alle'), ('Børn', 'Børn')], max_length=15)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(blank=True, max_length=10, null=True)),
                ('genre_id', models.UUIDField(default=uuid.uuid4)),
                ('movies', models.ManyToManyField(to='core.movie')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('movies', models.ManyToManyField(to='core.movie')),
                ('profiles', models.ManyToManyField(blank=True, to='core.profile')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
