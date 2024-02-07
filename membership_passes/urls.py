from django.urls import path

from membership_passes.views import PassListCreateView, PassRetrieveUpdateDeleteView, EntryCreateView


urlpatterns = [
    path('pass/<int:section_id>/pass/add/', PassListCreateView.as_view(), name='add_pass'),
    path('pass/<int:section_id>/pass/list/', PassListCreateView.as_view(), name='pass_list'),
    path('pass/<int:pk>/', PassRetrieveUpdateDeleteView.as_view(), name='pass_retrieve_update_delete'),
    path('pass/checkin/', EntryCreateView.as_view(), name='pass_checkin')
]
