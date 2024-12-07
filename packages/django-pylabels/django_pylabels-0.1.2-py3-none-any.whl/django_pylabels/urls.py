from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

app_name = "django_pylabels"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
    # path("print_labels/", PrintLabelsView.as_view(), name="print-barcode"),
    # path("", HomeView.as_view(), name="home"),
]
