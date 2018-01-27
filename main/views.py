# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.views.generic import TemplateView
from django.conf import settings
import os
from .models import Registration, Duration
from datetime import datetime
from django.db.models import Count, Case, When, Sum, Value, IntegerField
from django.db.models.functions import TruncMonth
import cv2


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        q = Registration.objects.filter(card__group__isnull=False).values('group__label')\
            .annotate(accepted=Sum(Case(When(action="Accept", then=Value(1)), default=Value(0), output_field=IntegerField())),
                      declined=Sum(Case(When(action="Decline", then=Value(1)), default=Value(0), output_field=IntegerField())),
                      month=TruncMonth('datetime')).order_by('month','group__label')

        stat = [(x['month'], x['group__label'], x['accepted'], x['declined']) for x in q]
        context['stat'] = stat

        return context




class ViewAjax(TemplateView):
    template_name = 'ajax.html'

    def get_context_data(self, **kwargs):
        context = super(ViewAjax, self).get_context_data(**kwargs)

        s_card = ""

        f = open(os.path.join(settings.BASE_DIR,"rfid0"))
        l = f.readline()
        if l:
            s_datetime = l[:26]
            s_dev = l[27:28]
            s_card = l[29:]

            o_datetime = datetime.strptime(s_datetime, "%Y-%m-%d %H:%M:%S.%f")

            filename = "r" + o_datetime.strftime("%Y%m%d%H%M%S%f") + ".jpg"
            filepath = os.path.join(settings.MEDIA_ROOT, "photoes", filename)

            o_card, dir, max_cnt, action, avaible, mkph = Registration.objects.register(o_datetime, s_dev, s_card, filename)

            if mkph:
	        cap = cv2.VideoCapture(0)
	        ret, frame = cap.read()
	        cv2.imwrite(filepath, frame)
	        cap.release()
	        cv2.destroyAllWindows()

        q = Duration.objects.filter(registration_out__isnull=True).values('card__group', 'card__group__label').annotate(cnt=Count('card__group'))
        stat = [(x["card__group__label"], x["cnt"]) for x in q]

        context['ajax_card'] = s_card
        context['ajax_card_obj'] = o_card
        context['ajax_card_meta'] = o_card._meta
        context['ajax_dir'] = dir
        context['ajax_grp'] = o_card.group
        context['ajax_max_cnt'] = max_cnt
        context['ajax_avaible'] = avaible
        context['ajax_datetime'] = o_datetime
        context['ajax_action'] = action
        context['ajax_stat'] = stat
        context['is_ajax'] = self.request.is_ajax()
        return context
