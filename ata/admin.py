from django.contrib import admin

from .models import Attendance, ChurchSchedule, Meeting, Member, Minutes, PartnerChurch

admin.site.register(Member)
admin.site.register(Meeting)
admin.site.register(Minutes)
admin.site.register(Attendance)
admin.site.register(PartnerChurch)
admin.site.register(ChurchSchedule)
