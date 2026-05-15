# Generated manually during project hardening.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('meeting_type', models.CharField(choices=[('Administrativa', 'Administrativa'), ('Ordinária', 'Ordinária'), ('Extraordinária', 'Extraordinária'), ('Culto', 'Culto'), ('Oração', 'Oração')], max_length=20)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(max_length=200)),
                ('leader', models.CharField(blank=True, max_length=200)),
                ('bible_reading', models.CharField(blank=True, max_length=200)),
                ('observations', models.TextField(blank=True)),
                ('allow_attendance', models.BooleanField(default=True)),
                ('agenda_items', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('Agendada', 'Agendada'), ('Realizada', 'Realizada'), ('Cancelada', 'Cancelada')], default='Agendada', max_length=20)),
            ],
            options={'ordering': ['-date', '-created_date']},
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('full_name', models.CharField(max_length=200)),
                ('sex', models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], max_length=20)),
                ('classification', models.CharField(choices=[('Gideão', 'Gideão'), ('Auxiliar', 'Auxiliar')], max_length=20)),
                ('bond', models.CharField(choices=[('Membro', 'Membro'), ('Oficial', 'Oficial')], max_length=20)),
                ('official_role', models.CharField(choices=[('Presidente', 'Presidente'), ('Vice-presidente', 'Vice-presidente'), ('Capelão', 'Capelão'), ('Secretário', 'Secretário'), ('Tesoureiro', 'Tesoureiro'), ('Nenhum', 'Nenhum')], default='Nenhum', max_length=30)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('field', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo')], default='Ativo', max_length=10)),
            ],
            options={'ordering': ['full_name']},
        ),
        migrations.CreateModel(
            name='PartnerChurch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('pastor_name', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('neighborhood', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('observations', models.TextField(blank=True)),
                ('partnership_status', models.CharField(choices=[('Ativa', 'Ativa'), ('Inativa', 'Inativa'), ('Pendente', 'Pendente')], default='Ativa', max_length=20)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Minutes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('opening_time', models.CharField(blank=True, max_length=10)),
                ('closing_time', models.CharField(blank=True, max_length=10)),
                ('full_text', models.TextField()),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('signers', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('Rascunho', 'Rascunho'), ('Revisão', 'Revisão'), ('Aprovada', 'Aprovada'), ('Arquivada', 'Arquivada')], default='Rascunho', max_length=20)),
                ('meeting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='minutes', to='ata.meeting')),
            ],
            options={'verbose_name_plural': 'minutes', 'ordering': ['-created_date']},
        ),
        migrations.CreateModel(
            name='ChurchSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('church_name', models.CharField(max_length=200)),
                ('pastor_name', models.CharField(blank=True, max_length=200)),
                ('church_phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('neighborhood', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('commitment_type', models.CharField(choices=[('Reunião', 'Reunião'), ('Visita', 'Visita'), ('Apresentação', 'Apresentação'), ('Culto Parceiro', 'Culto Parceiro'), ('Ação Evangelística', 'Ação Evangelística')], max_length=30)),
                ('responsible', models.CharField(blank=True, max_length=200)),
                ('observations', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('Agendado', 'Agendado'), ('Confirmado', 'Confirmado'), ('Realizado', 'Realizado'), ('Cancelado', 'Cancelado')], default='Agendado', max_length=20)),
                ('church', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedules', to='ata.partnerchurch')),
            ],
            options={'ordering': ['-date', '-created_date']},
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('Presente', 'Presente'), ('Ausente', 'Ausente'), ('Justificada', 'Justificada')], default='Ausente', max_length=20)),
                ('arrival_time', models.CharField(blank=True, max_length=10)),
                ('observations', models.TextField(blank=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='ata.meeting')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='ata.member')),
            ],
            options={'ordering': ['meeting', 'member__full_name']},
        ),
        migrations.AddConstraint(
            model_name='attendance',
            constraint=models.UniqueConstraint(fields=('meeting', 'member'), name='unique_attendance_per_meeting_member'),
        ),
    ]
