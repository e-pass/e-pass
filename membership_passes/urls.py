from django.urls import path

from membership_passes.views import PassListCreateView, PassRetrieveUpdateDeleteView


urlpatterns = [
    path('pass/<int:section_id>/pass/', PassListCreateView.as_view(), name='list_or_add_pass'),
    path('pass/<int:pk>/', PassRetrieveUpdateDeleteView.as_view(), name='pass_retrieve_update_delete')
]
