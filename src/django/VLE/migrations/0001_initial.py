# Generated by Django 2.1 on 2018-09-27 21:27

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import VLE.utils.file_handling


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(null=True)),
                ('points_possible', models.IntegerField(default=10, verbose_name='points_possible')),
                ('unlock_date', models.DateTimeField(blank=True, null=True, verbose_name='unlock_date')),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='due_date')),
                ('lock_date', models.DateTimeField(blank=True, null=True, verbose_name='lock_date')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=True)),
                ('last_edited', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('abbreviation', models.TextField(default='XXXX', max_length=10)),
                ('startdate', models.DateField(null=True)),
                ('enddate', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('grade', models.FloatField(default=None, null=True)),
                ('published', models.BooleanField(default=False)),
                ('last_edited', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('t', 'text'), ('rt', 'rich text'), ('i', 'img'), ('p', 'pdf'), ('f', 'file'), ('v', 'vid'), ('u', 'url'), ('d', 'date')], default='t', max_length=4)),
                ('title', models.TextField()),
                ('description', models.TextField(null=True)),
                ('location', models.IntegerField()),
                ('required', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_type', models.TextField(choices=[('PE', 'percentage'), ('GR', 'from 0 to 10')], default='PE', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('lti_id', models.TextField(null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sourcedid', models.TextField(null=True, verbose_name='sourcedid')),
                ('grade_url', models.TextField(null=True, verbose_name='grade_url')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Lti_ids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lti_id', models.TextField()),
                ('for_model', models.TextField(choices=[('Assignment', 'Assignment'), ('Course', 'Course')])),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.Assignment')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('p', 'progress'), ('e', 'entry'), ('d', 'entrydeadline')], max_length=4)),
                ('entry', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='VLE.Entry')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Journal')),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Course')),
                ('group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.Group')),
            ],
        ),
        migrations.CreateModel(
            name='PresetNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('p', 'progress'), ('d', 'entrydeadline')], max_length=4)),
                ('target', models.IntegerField(null=True)),
                ('deadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('can_add_course', models.BooleanField(default=False)),
                ('can_edit_course_details', models.BooleanField(default=False)),
                ('can_delete_course', models.BooleanField(default=False)),
                ('can_edit_course_roles', models.BooleanField(default=False)),
                ('can_view_course_users', models.BooleanField(default=False)),
                ('can_add_course_users', models.BooleanField(default=False)),
                ('can_delete_course_users', models.BooleanField(default=False)),
                ('can_add_course_user_group', models.BooleanField(default=False)),
                ('can_delete_course_user_group', models.BooleanField(default=False)),
                ('can_edit_course_user_group', models.BooleanField(default=False)),
                ('can_add_assignment', models.BooleanField(default=False)),
                ('can_delete_assignment', models.BooleanField(default=False)),
                ('can_edit_assignment', models.BooleanField(default=False)),
                ('can_view_assignment_journals', models.BooleanField(default=False)),
                ('can_grade', models.BooleanField(default=False)),
                ('can_publish_grades', models.BooleanField(default=False)),
                ('can_have_journal', models.BooleanField(default=False)),
                ('can_comment', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('max_grade', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=VLE.utils.file_handling.get_path)),
                ('file_name', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.TextField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('verified_email', models.BooleanField(default=False)),
                ('lti_id', models.TextField(blank=True, null=True, unique=True)),
                ('profile_picture', models.TextField(null=True)),
                ('is_teacher', models.BooleanField(default=False)),
                ('grade_notifications', models.BooleanField(default=True)),
                ('comment_notifications', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
        migrations.AddField(
            model_name='userfile',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='presetnode',
            name='forced_template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='VLE.Template'),
        ),
        migrations.AddField(
            model_name='presetnode',
            name='format',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Format'),
        ),
        migrations.AddField(
            model_name='participation',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role', to='VLE.Role'),
        ),
        migrations.AddField(
            model_name='participation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='node',
            name='preset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.PresetNode'),
        ),
        migrations.AddField(
            model_name='journal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='format',
            name='available_templates',
            field=models.ManyToManyField(related_name='available_templates', to='VLE.Template'),
        ),
        migrations.AddField(
            model_name='format',
            name='unused_templates',
            field=models.ManyToManyField(related_name='unused_templates', to='VLE.Template'),
        ),
        migrations.AddField(
            model_name='field',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Template'),
        ),
        migrations.AddField(
            model_name='entry',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='VLE.Template'),
        ),
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='users',
            field=models.ManyToManyField(related_name='participations', through='VLE.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='content',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Entry'),
        ),
        migrations.AddField(
            model_name='content',
            name='field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='VLE.Field'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VLE.Entry'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignment',
            name='courses',
            field=models.ManyToManyField(to='VLE.Course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='format',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='VLE.Format'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('name', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together={('user', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='lti_ids',
            unique_together={('lti_id', 'for_model')},
        ),
        migrations.AlterUniqueTogether(
            name='journal',
            unique_together={('assignment', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together={('name', 'course')},
        ),
    ]
