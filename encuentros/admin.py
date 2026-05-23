from django.contrib import admin
from .models import (
    Meeting,
    Server,
    Participant,
    FamilyParticipantInfo,
    ChurchDataInfo,
    MeetingParticipant,
    FinanceMovements,
    Summary
)

# Register your models here.
admin.site.register(Meeting)
admin.site.register(Server)
admin.site.register(Participant)
admin.site.register(FamilyParticipantInfo)
admin.site.register(ChurchDataInfo)
admin.site.register(MeetingParticipant)
admin.site.register(FinanceMovements)
admin.site.register(Summary)
