
import datetime

from django.contrib.admin import FieldListFilter
from django.contrib.admin import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

class DateRangeFilter(DateFieldListFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # ############################################################
        # Below section is copied from DateFieldListFilter.__init__
        # ############################################################
        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:       # field is a models.DateField
            today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)
        # ############################################################
        # Above section is copied from DateFieldListFilter.__init__
        # ############################################################

        self.links = [
                ("----最近使用时间----", {}),
                ("2022-01-03 00:00:00 ~ 2022-01-03 23:59:59", {}),
                ("2021-01-01 00:00:00 ~ 2021-12-31 23:59:59", {}),
                ("2022-01-03 00:00:00 ~ 2022-01-10 23:59:59", {}),

                ("----常用过往时间----", {}),
                ("今天", {
                    self.lookup_kwarg_since: str(today),
                    self.lookup_kwarg_until: str(tomorrow),
                }),

                ("昨天", {
                    self.lookup_kwarg_since: str(today - datetime.timedelta(days=1)),
                    self.lookup_kwarg_until: str(today),
                }),

                ("明天", {
                    self.lookup_kwarg_since: str(tomorrow),
                    self.lookup_kwarg_until: str(tomorrow + datetime.timedelta(days=1)),
                }),

                ("本月", {
                    self.lookup_kwarg_since: str(today.replace(day=1)),
                    self.lookup_kwarg_until: str(next_month),
                }),
                ("上月", {
                    self.lookup_kwarg_since: str((today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)),
                    self.lookup_kwarg_until: str(today.replace(day=1)),
                }),
                ("今年", {
                    self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                    self.lookup_kwarg_until: str(next_year),
                }),
                ("去年", {
                    self.lookup_kwarg_since: str((today.replace(month=1, day=1) - datetime.timedelta(days=1)).replace(month=1, day=1)),
                    self.lookup_kwarg_until: str(today.replace(month=1, day=1)),
                }),
                ("最近7天", {
                    self.lookup_kwarg_since: str(today - datetime.timedelta(days=7)),
                    self.lookup_kwarg_until: str(tomorrow),
                }),
                ("最近30天", {}),

                ("截止本周", {}),
                ("截止本月", {}),
                ("截止下月", {}),
                ("截止今年", {}),
                ("截止来年", {}),


                ("具有日期", {}),
                ("没有日期", {}),
                ("自定义日期范围", {}),
                ("任意日期", {}),
        ]

    def expected_parameters(self):
        params = [self.lookup_kwarg_since, self.lookup_kwarg_until]
        if self.field.null:
            params.append(self.lookup_kwarg_isnull)
        return params

    def choices(self, changelist):


        for title, param_dict in self.links:
            yield {
                'selected': self.date_params == param_dict,
                'query_string': changelist.get_query_string(param_dict, [self.field_generic]),
                'display': title,
            }
