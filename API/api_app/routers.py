from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'study_subjects', StudySubjectViewSet)
router.register(r'researchers', ResearcherViewSet)
router.register(r'posts', AnnouncementPostViewSet)
router.register(r'ratings', RatingViewSet)
