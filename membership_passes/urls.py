from django.urls import path

from membership_passes.views import (EntryCreateView, PassListCreateView,
                                     PassRetrieveUpdateDeleteView)

urlpatterns = [
    path('pass/<int:section_id>/pass/', PassListCreateView.as_view(), name='pass_list_add'),
    path('pass/<int:pk>/', PassRetrieveUpdateDeleteView.as_view(), name='pass_retrieve_update_delete'),
    path('pass/checkin/', EntryCreateView.as_view(), name='pass_checkin')
]
