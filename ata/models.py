from django.db import models


class TimestampedModel(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=200, blank=True)

	class Meta:
		abstract = True


class Member(TimestampedModel):
	class Sex(models.TextChoices):
		MASCULINO = 'Masculino'
		FEMININO = 'Feminino'

	class Classification(models.TextChoices):
		GIDEAO = 'Gideão'
		AUXILIAR = 'Auxiliar'

	class Bond(models.TextChoices):
		MEMBRO = 'Membro'
		OFICIAL = 'Oficial'

	class OfficialRole(models.TextChoices):
		PRESIDENTE = 'Presidente'
		VICE_PRESIDENTE = 'Vice-presidente'
		CAPELAO = 'Capelão'
		SECRETARIO = 'Secretário'
		TESOUREIRO = 'Tesoureiro'
		NENHUM = 'Nenhum'

	class Status(models.TextChoices):
		ATIVO = 'Ativo'
		INATIVO = 'Inativo'

	full_name = models.CharField(max_length=200)
	sex = models.CharField(max_length=20, choices=Sex.choices)
	classification = models.CharField(max_length=20, choices=Classification.choices)
	bond = models.CharField(max_length=20, choices=Bond.choices)
	official_role = models.CharField(
		max_length=30,
		choices=OfficialRole.choices,
		default=OfficialRole.NENHUM,
	)
	phone = models.CharField(max_length=20, blank=True)
	email = models.EmailField(blank=True)
	field = models.CharField(max_length=100, blank=True)
	status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVO)

	class Meta:
		ordering = ['full_name']

	def __str__(self) -> str:
		return self.full_name


class Meeting(TimestampedModel):
	class MeetingType(models.TextChoices):
		ADMINISTRATIVA = 'Administrativa'
		ORDINARIA = 'Ordinária'
		EXTRAORDINARIA = 'Extraordinária'
		CULTO = 'Culto'
		ORACAO = 'Oração'

	class Status(models.TextChoices):
		AGENDADA = 'Agendada'
		REALIZADA = 'Realizada'
		CANCELADA = 'Cancelada'

	title = models.CharField(max_length=200)
	meeting_type = models.CharField(max_length=20, choices=MeetingType.choices)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField(null=True, blank=True)
	location = models.CharField(max_length=200)
	leader = models.CharField(max_length=200, blank=True)
	bible_reading = models.CharField(max_length=200, blank=True)
	observations = models.TextField(blank=True)
	allow_attendance = models.BooleanField(default=True)
	agenda_items = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADA)

	class Meta:
		ordering = ['-date', '-created_date']

	def __str__(self) -> str:
		return f'{self.title} ({self.date})'


class Minutes(TimestampedModel):
	class Status(models.TextChoices):
		RASCUNHO = 'Rascunho'
		REVISAO = 'Revisão'
		APROVADA = 'Aprovada'
		ARQUIVADA = 'Arquivada'

	meeting = models.OneToOneField(
		Meeting,
		on_delete=models.CASCADE,
		related_name='minutes',
	)
	opening_time = models.CharField(max_length=10, blank=True)
	closing_time = models.CharField(max_length=10, blank=True)
	full_text = models.TextField()
	approval_date = models.DateField(null=True, blank=True)
	signers = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.RASCUNHO)

	class Meta:
		ordering = ['-created_date']
		verbose_name_plural = 'minutes'

	def __str__(self) -> str:
		return self.meeting.title


class Attendance(TimestampedModel):
	class Status(models.TextChoices):
		PRESENTE = 'Presente'
		AUSENTE = 'Ausente'
		JUSTIFICADA = 'Justificada'

	meeting = models.ForeignKey(
		Meeting,
		on_delete=models.CASCADE,
		related_name='attendances',
	)
	member = models.ForeignKey(
		Member,
		on_delete=models.CASCADE,
		related_name='attendances',
	)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.AUSENTE)
	arrival_time = models.CharField(max_length=10, blank=True)
	observations = models.TextField(blank=True)

	class Meta:
		ordering = ['meeting', 'member__full_name']
		constraints = [
			models.UniqueConstraint(fields=['meeting', 'member'], name='unique_attendance_per_meeting_member'),
		]

	def __str__(self) -> str:
		return f'{self.member.full_name} - {self.meeting.title}'


class PartnerChurch(TimestampedModel):
	class PartnershipStatus(models.TextChoices):
		ATIVA = 'Ativa'
		INATIVA = 'Inativa'
		PENDENTE = 'Pendente'

	name = models.CharField(max_length=200)
	pastor_name = models.CharField(max_length=200, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	email = models.EmailField(blank=True)
	address = models.CharField(max_length=300, blank=True)
	neighborhood = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100)
	observations = models.TextField(blank=True)
	partnership_status = models.CharField(
		max_length=20,
		choices=PartnershipStatus.choices,
		default=PartnershipStatus.ATIVA,
	)

	class Meta:
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class ChurchSchedule(TimestampedModel):
	class CommitmentType(models.TextChoices):
		REUNIAO = 'Reunião'
		VISITA = 'Visita'
		APRESENTACAO = 'Apresentação'
		CULTO_PARCEIRO = 'Culto Parceiro'
		ACAO_EVANGELISTICA = 'Ação Evangelística'

	class Status(models.TextChoices):
		AGENDADO = 'Agendado'
		CONFIRMADO = 'Confirmado'
		REALIZADO = 'Realizado'
		CANCELADO = 'Cancelado'

	church = models.ForeignKey(
		PartnerChurch,
		on_delete=models.SET_NULL,
		related_name='schedules',
		null=True,
		blank=True,
	)
	church_name = models.CharField(max_length=200)
	pastor_name = models.CharField(max_length=200, blank=True)
	church_phone = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=300, blank=True)
	neighborhood = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100, blank=True)
	date = models.DateField()
	time = models.TimeField()
	commitment_type = models.CharField(max_length=30, choices=CommitmentType.choices)
	responsible = models.CharField(max_length=200, blank=True)
	observations = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADO)

	class Meta:
		ordering = ['-date', '-created_date']

	def __str__(self) -> str:
		return f'{self.church_name} - {self.date} {self.time}'
