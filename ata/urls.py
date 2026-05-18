from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceViewSet,
    ChurchScheduleViewSet,
    MeetingViewSet,
    MemberViewSet,
    MinutesViewSet,
    PartnerChurchViewSet,
    dashboard_summary,
    GideonFriendViewSet,
)

router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')
router.register(r'meetings', MeetingViewSet, basename='meeting')
router.register(r'minutes', MinutesViewSet, basename='minutes')
router.register(r'attendances', AttendanceViewSet, basename='attendance')
router.register(r'partner-churches', PartnerChurchViewSet, basename='partner-church')
router.register(r'gideon-friends', GideonFriendViewSet, basename='gideon-friend')
router.register(r'church-schedules', ChurchScheduleViewSet, basename='church-schedule')

urlpatterns = [
    path('dashboard/', dashboard_summary, name='dashboard-summary'),
    path('', include(router.urls)),
]
