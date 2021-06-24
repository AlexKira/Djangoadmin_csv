import csv
import pandas
import django
import datetime as d
from django.conf import settings
from django.contrib import admin
from 'my_project'.models import 'my_model'
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse, HttpResponseForbidden

# pip install django-admin-rangefilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# Register your models here.

'my_model' = get_user_model()

class 'my_model'Admin(UserAdmin):
    model = 'my_model'
    list_display = ['my_filds_model']
    list_editable = ['my_filds_model']
    list_display_links = ('my_filds_model')
    search_fields = ('my_filds_model',)
    ordering = ('-my_filds_date_model',)
    csv_fields = ['my_filds_model']
    list_filter = ('my_filds_model', ('my_filds_date_model', DateRangeFilter),)

# CSV module

    def export_as_csv(self, request, queryset):
        # everyone has perms to export as csv unless explicitly defined
        if getattr(settings, 'DJANGO_EXPORTS_REQUIRE_PERM', None):
            admin_opts = self
            has_csv_permission = request.user.objects_name.all("%s" % (admin_opts))
        else:
            has_csv_permission = self.has_csv_permission(request) \
                if (hasattr(self, 'has_csv_permission') and callable(getattr(self, 'has_csv_permission'))) \
                else True
        if has_csv_permission:
            start_date = request.GET.get("date_joined__range__gte", None)
            end_date = request.GET.get("date_joined__range__lte", None)
            list_editable = request.GET.get('email_confirm__exact', "all")
            if request.GET.get('email_confirm__exact' ) == '1':
                list_editable = "yes"
            if request.GET.get('email_confirm__exact' ) == '0':
                list_editable = "not"
            if getattr(self, 'csv_fields', None):
                field_names = self.csv_fields
            if django.VERSION[0] == 1 and django.VERSION[1] <= 5:
                response = HttpResponse(mimetype='text/csv')
            else:
                response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=emails_{}_{}_confirm_{}.csv'.format(start_date, end_date, list_editable)
            queryset = queryset.values_list(*field_names)
            pandas.DataFrame(list(queryset), columns=field_names).to_csv(response, index=False, encoding='utf-8')
            return response
        return HttpResponseForbidden()
    export_as_csv.short_description = "Сохранить в .csv"
    actions = [export_as_csv]

admin.site.register('my_model', 'my_model'Admin)
