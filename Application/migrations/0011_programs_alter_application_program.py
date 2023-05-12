# Generated by Django 4.1.7 on 2023-04-16 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0010_alter_application_program_delete_programs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.department')),
                ('qualification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.qualification')),
            ],
        ),
        migrations.AlterField(
            model_name='application',
            name='program',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Application.programs'),
            preserve_default=False,
        ),
    ]
