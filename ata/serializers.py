from rest_framework import serializers

from .models import Attendance, ChurchSchedule, Meeting, Member, Minutes, PartnerChurch, GideonFriend


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class MinutesSummarySerializer(serializers.ModelSerializer):
    meeting_id = serializers.IntegerField(source='meeting.id', read_only=True)
    meeting_title = serializers.CharField(source='meeting.title', read_only=True)

    class Meta:
        model = Minutes
        fields = ['id', 'meeting_id', 'meeting_title', 'status', 'approval_date', 'created_date', 'updated_date']


class AttendanceSummarySerializer(serializers.ModelSerializer):
    meeting_id = serializers.IntegerField(source='meeting.id', read_only=True)
    meeting_title = serializers.CharField(source='meeting.title', read_only=True)
    member_id = serializers.IntegerField(source='member.id', read_only=True)
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    member_classification = serializers.CharField(source='member.classification', read_only=True)
    member_role = serializers.CharField(source='member.official_role', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'meeting_id',
            'meeting_title',
            'member_id',
            'member_name',
            'member_classification',
            'member_role',
            'status',
            'arrival_time',
            'observations',
        ]


class MeetingSerializer(serializers.ModelSerializer):
    minutes = MinutesSummarySerializer(read_only=True)
    attendances_count = serializers.IntegerField(read_only=True)
    present_count = serializers.IntegerField(read_only=True)
    absent_count = serializers.IntegerField(read_only=True)
    justified_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Meeting
        fields = '__all__'


class MinutesSerializer(serializers.ModelSerializer):
    meeting_id = serializers.PrimaryKeyRelatedField(
        source='meeting',
        queryset=Meeting.objects.all(),
        write_only=False,
    )
    meeting_title = serializers.CharField(source='meeting.title', read_only=True)

    class Meta:
        model = Minutes
        fields = [
            'id',
            'meeting_id',
            'meeting_title',
            'opening_time',
            'closing_time',
            'full_text',
            'approval_date',
            'signers',
            'status',
            'created_date',
            'updated_date',
            'created_by',
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    meeting_id = serializers.PrimaryKeyRelatedField(
        source='meeting',
        queryset=Meeting.objects.all(),
        write_only=False,
    )
    meeting_title = serializers.CharField(source='meeting.title', read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(
        source='member',
        queryset=Member.objects.all(),
        write_only=False,
    )
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    member_classification = serializers.CharField(source='member.classification', read_only=True)
    member_role = serializers.CharField(source='member.official_role', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'meeting_id',
            'meeting_title',
            'member_id',
            'member_name',
            'member_classification',
            'member_role',
            'status',
            'arrival_time',
            'observations',
            'created_date',
            'updated_date',
            'created_by',
        ]


class PartnerChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerChurch
        fields = '__all__'


class GideonFriendSerializer(serializers.ModelSerializer):
    contacted_by_id = serializers.PrimaryKeyRelatedField(
        source='contacted_by',
        queryset=Member.objects.all(),
        required=False,
        allow_null=True,
        write_only=False,
    )
    contacted_by_name = serializers.CharField(source='contacted_by.full_name', read_only=True)
    contacted_by_classification = serializers.CharField(source='contacted_by.classification', read_only=True)

    class Meta:
        model = GideonFriend
        fields = [
            'id',
            'full_name',
            'phone',
            'email',
            'address',
            'neighborhood',
            'city',
            'contacted_by_id',
            'contacted_by_name',
            'contacted_by_classification',
            'donation_amount',
            'became_friend_date',
            'observations',
            'status',
            'created_date',
            'updated_date',
            'created_by',
        ]

    def validate_contacted_by(self, value):
        if value and value.classification not in [Member.Classification.GIDEAO, Member.Classification.AUXILIAR]:
            raise serializers.ValidationError('O responsável pelo contato precisa ser Gideão ou Auxiliar.')

        return value


class ChurchScheduleSerializer(serializers.ModelSerializer):
    church_id = serializers.PrimaryKeyRelatedField(
        source='church',
        queryset=PartnerChurch.objects.all(),
        required=False,
        allow_null=True,
        write_only=False,
    )

    class Meta:
        model = ChurchSchedule
        fields = [
            'id',
            'church_id',
            'church_name',
            'pastor_name',
            'church_phone',
            'address',
            'neighborhood',
            'city',
            'date',
            'time',
            'commitment_type',
            'responsible',
            'observations',
            'status',
            'created_date',
            'updated_date',
            'created_by',
        ]


class BulkAttendanceItemSerializer(serializers.Serializer):
    member_id = serializers.PrimaryKeyRelatedField(source='member', queryset=Member.objects.all())
    status = serializers.ChoiceField(choices=Attendance.Status.choices, default=Attendance.Status.AUSENTE)
    arrival_time = serializers.CharField(required=False, allow_blank=True, max_length=10)
    observations = serializers.CharField(required=False, allow_blank=True)
