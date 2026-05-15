import django_filters

from .models import Attendance, ChurchSchedule, Meeting, Member, Minutes, PartnerChurch


class MemberFilter(django_filters.FilterSet):
    class Meta:
        model = Member
        fields = {
            'status': ['exact'],
            'classification': ['exact'],
            'bond': ['exact'],
            'official_role': ['exact'],
        }


class MeetingFilter(django_filters.FilterSet):
    class Meta:
        model = Meeting
        fields = {
            'status': ['exact'],
            'meeting_type': ['exact'],
            'date': ['exact', 'gte', 'lte'],
            'allow_attendance': ['exact'],
        }


class MinutesFilter(django_filters.FilterSet):
    meeting_id = django_filters.NumberFilter(field_name='meeting_id')

    class Meta:
        model = Minutes
        fields = {
            'status': ['exact'],
            'approval_date': ['exact', 'gte', 'lte'],
        }


class AttendanceFilter(django_filters.FilterSet):
    meeting_id = django_filters.NumberFilter(field_name='meeting_id')
    member_id = django_filters.NumberFilter(field_name='member_id')
    member_classification = django_filters.CharFilter(field_name='member__classification')

    class Meta:
        model = Attendance
        fields = {
            'status': ['exact'],
        }


class PartnerChurchFilter(django_filters.FilterSet):
    class Meta:
        model = PartnerChurch
        fields = {
            'partnership_status': ['exact'],
            'city': ['exact'],
        }


class ChurchScheduleFilter(django_filters.FilterSet):
    church_id = django_filters.NumberFilter(field_name='church_id')

    class Meta:
        model = ChurchSchedule
        fields = {
            'status': ['exact'],
            'church_name': ['exact'],
            'commitment_type': ['exact'],
            'date': ['exact', 'gte', 'lte'],
            'responsible': ['exact'],
        }
