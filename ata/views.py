from io import BytesIO

from django.db.models import Count, Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import (
	AttendanceFilter,
	ChurchScheduleFilter,
	MeetingFilter,
	MemberFilter,
	MinutesFilter,
	PartnerChurchFilter,
)
from .models import Attendance, ChurchSchedule, Meeting, Member, Minutes, PartnerChurch
from .serializers import (
	AttendanceSerializer,
	BulkAttendanceItemSerializer,
	ChurchScheduleSerializer,
	MeetingSerializer,
	MemberSerializer,
	MinutesSerializer,
	PartnerChurchSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	ordering = ['-created_date']
	ordering_fields = '__all__'

	def perform_create(self, serializer):
		created_by = self.request.user.get_full_name() or self.request.user.get_username()
		serializer.save(created_by=created_by)


class MemberViewSet(BaseViewSet):
	queryset = Member.objects.all()
	serializer_class = MemberSerializer
	filterset_class = MemberFilter
	search_fields = ['full_name', 'email', 'phone', 'field', 'created_by']


class MeetingViewSet(BaseViewSet):
	serializer_class = MeetingSerializer
	filterset_class = MeetingFilter
	search_fields = ['title', 'location', 'leader', 'bible_reading', 'created_by']
	ordering = ['-date', '-created_date']

	def get_queryset(self):
		return Meeting.objects.annotate(
			attendances_count=Count('attendances', distinct=True),
			present_count=Count('attendances', filter=Q(attendances__status=Attendance.Status.PRESENTE), distinct=True),
			absent_count=Count('attendances', filter=Q(attendances__status=Attendance.Status.AUSENTE), distinct=True),
			justified_count=Count('attendances', filter=Q(attendances__status=Attendance.Status.JUSTIFICADA), distinct=True),
		).select_related('minutes')

	@action(detail=True, methods=['get'], url_path='attendances')
	def attendances(self, request, pk=None):
		meeting = self.get_object()
		queryset = meeting.attendances.select_related('member', 'meeting').all()
		serializer = AttendanceSerializer(queryset, many=True)
		return Response(serializer.data)

	@action(detail=True, methods=['post'], url_path='attendances/bulk')
	def bulk_attendances(self, request, pk=None):
		meeting = self.get_object()
		serializer = BulkAttendanceItemSerializer(data=request.data, many=True)
		serializer.is_valid(raise_exception=True)

		created_by = request.user.get_full_name() or request.user.get_username()
		items = []
		for item in serializer.validated_data:
			attendance, _ = Attendance.objects.update_or_create(
				meeting=meeting,
				member=item['member'],
				defaults={
					'status': item.get('status', Attendance.Status.AUSENTE),
					'arrival_time': item.get('arrival_time', ''),
					'observations': item.get('observations', ''),
					'created_by': created_by,
				},
			)
			items.append(attendance)

		return Response(AttendanceSerializer(items, many=True).data, status=status.HTTP_200_OK)


class MinutesViewSet(BaseViewSet):
	queryset = Minutes.objects.select_related('meeting').all()
	serializer_class = MinutesSerializer
	filterset_class = MinutesFilter
	search_fields = ['meeting__title', 'full_text', 'signers', 'created_by']

	@action(detail=True, methods=['get'], url_path='print')
	def print_view(self, request, pk=None):
		minute = self.get_object()
		participants = minute.meeting.attendances.select_related('member').filter(status=Attendance.Status.PRESENTE)
		participants_html = ''.join(f'<li>{attendance.member.full_name}</li>' for attendance in participants)
		html = f"""
		<!doctype html>
		<html lang="pt-br">
		<head>
			<meta charset="utf-8" />
			<title>Ata - {minute.meeting.title}</title>
			<style>
				body {{ font-family: Arial, sans-serif; margin: 40px; color: #111827; line-height: 1.55; }}
				h1 {{ text-align: center; text-transform: uppercase; font-size: 20px; }}
				.meta {{ margin: 24px 0; padding: 16px; border: 1px solid #d1d5db; border-radius: 8px; }}
				.content {{ white-space: pre-wrap; text-align: justify; }}
				.signers {{ margin-top: 48px; white-space: pre-wrap; }}
			</style>
		</head>
		<body>
			<h1>Ata da Reunião</h1>
			<div class="meta">
				<p><strong>Reunião:</strong> {minute.meeting.title}</p>
				<p><strong>Data:</strong> {minute.meeting.date}</p>
				<p><strong>Local:</strong> {minute.meeting.location}</p>
				<p><strong>Abertura:</strong> {minute.opening_time or '-'} | <strong>Encerramento:</strong> {minute.closing_time or '-'}</p>
				<p><strong>Status:</strong> {minute.status}</p>
			</div>
			<h2>Participantes presentes</h2>
			<ul>{participants_html or '<li>Sem presenças lançadas.</li>'}</ul>
			<h2>Texto da ata</h2>
			<div class="content">{minute.full_text}</div>
			<h2>Assinantes</h2>
			<div class="signers">{minute.signers or '-'}</div>
		</body>
		</html>
		"""
		return HttpResponse(html, content_type='text/html; charset=utf-8')

	@action(detail=True, methods=['get'], url_path='pdf')
	def pdf(self, request, pk=None):
		minute = self.get_object()
		try:
			from reportlab.lib.pagesizes import A4
			from reportlab.lib.styles import getSampleStyleSheet
			from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
		except ImportError:
			return Response(
				{'detail': 'Instale a dependência reportlab para gerar PDF: pip install reportlab'},
				status=status.HTTP_501_NOT_IMPLEMENTED,
			)

		buffer = BytesIO()
		doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
		styles = getSampleStyleSheet()
		story = [
			Paragraph('ATA DA REUNIÃO', styles['Title']),
			Spacer(1, 16),
			Paragraph(f'<b>Reunião:</b> {minute.meeting.title}', styles['Normal']),
			Paragraph(f'<b>Data:</b> {minute.meeting.date}', styles['Normal']),
			Paragraph(f'<b>Local:</b> {minute.meeting.location}', styles['Normal']),
			Paragraph(f'<b>Status:</b> {minute.status}', styles['Normal']),
			Spacer(1, 16),
			Paragraph('<b>Texto da ata</b>', styles['Heading2']),
			Paragraph(minute.full_text.replace('\n', '<br/>'), styles['BodyText']),
			Spacer(1, 16),
			Paragraph('<b>Assinantes</b>', styles['Heading2']),
			Paragraph((minute.signers or '-').replace('\n', '<br/>'), styles['BodyText']),
		]
		doc.build(story)
		buffer.seek(0)
		filename = f'ata-{minute.id}.pdf'
		return FileResponse(buffer, as_attachment=True, filename=filename)


class AttendanceViewSet(BaseViewSet):
	queryset = Attendance.objects.select_related('meeting', 'member').all()
	serializer_class = AttendanceSerializer
	filterset_class = AttendanceFilter
	search_fields = ['member__full_name', 'member__official_role', 'observations', 'created_by', 'meeting__title']


class PartnerChurchViewSet(BaseViewSet):
	queryset = PartnerChurch.objects.all()
	serializer_class = PartnerChurchSerializer
	filterset_class = PartnerChurchFilter
	search_fields = ['name', 'pastor_name', 'city', 'email', 'phone', 'created_by']
	ordering = ['name', '-created_date']


class ChurchScheduleViewSet(BaseViewSet):
	queryset = ChurchSchedule.objects.select_related('church').all()
	serializer_class = ChurchScheduleSerializer
	filterset_class = ChurchScheduleFilter
	search_fields = ['church_name', 'pastor_name', 'responsible', 'city', 'observations', 'created_by']
	ordering = ['-date', '-created_date']

	def perform_create(self, serializer):
		church = serializer.validated_data.get('church')
		created_by = self.request.user.get_full_name() or self.request.user.get_username()
		if church:
			serializer.save(
				church_name=serializer.validated_data.get('church_name') or church.name,
				pastor_name=serializer.validated_data.get('pastor_name') or church.pastor_name,
				church_phone=serializer.validated_data.get('church_phone') or church.phone,
				address=serializer.validated_data.get('address') or church.address,
				neighborhood=serializer.validated_data.get('neighborhood') or church.neighborhood,
				city=serializer.validated_data.get('city') or church.city,
				created_by=created_by,
			)
		else:
			serializer.save(created_by=created_by)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
	meetings_qs = Meeting.objects.all()
	minutes_qs = Minutes.objects.select_related('meeting')
	schedules_qs = ChurchSchedule.objects.all()

	return Response({
		'counts': {
			'members': Member.objects.count(),
			'meetings': meetings_qs.count(),
			'minutes': minutes_qs.count(),
			'attendances': Attendance.objects.count(),
			'partner-churches': PartnerChurch.objects.count(),
			'church-schedules': schedules_qs.count(),
			'pending-minutes': minutes_qs.exclude(status=Minutes.Status.APROVADA).count(),
		},
		'recent_meetings': MeetingSerializer(meetings_qs.order_by('-date', '-created_date')[:5], many=True).data,
		'recent_minutes': MinutesSerializer(minutes_qs.order_by('-created_date')[:5], many=True).data,
		'recent_schedules': ChurchScheduleSerializer(schedules_qs.order_by('-date', '-created_date')[:5], many=True).data,
	})
