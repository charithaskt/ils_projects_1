from datetime import datetime, timedelta
from collections import Counter

from django.shortcuts import get_object_or_404

from intranet.models import Holidays, Borrowers
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
import json
import re
from datetime import tzinfo, timedelta, datetime

def dates_between(start, end):
    while start <= end:
        yield start
        start += timedelta(1)


def count_weekday(start, end):
    counter = Counter()
    for date in dates_between(start, end):
        counter[date.strftime('%a')] += 1
    return counter


def count_weekendhdays(start, end, hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%a') in [hday.strftime('%a') for hday in hdays]:
            counter += 1
    return counter


def count_yrlyhdays(start, end, hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%m%d') in [hday.strftime('%m%d') for hday in hdays]:
            counter += 1
    return counter


def count_adhochdays(start, end, hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%Y%m%d') in [hday.strftime('%Y%m%d') for hday in hdays]:
            counter += 1
    return counter


def get_holidays():
    yearly = []
    weekend = []
    adhoc = []
    hqs = Holidays.objects.all()
    if hqs:
        i = 0
        while i < hqs.count():
            if hqs[i].isexception:
                if hqs[i].holiday_type == 'WEEKEND':
                    weekend.append(hqs[i].date)
                elif hqs[i].holiday_type == 'YEARLY':
                    yearly.append(hqs[i].date)
                elif hqs[i].holiday_type == 'ADHOC':
                    adhoc.append(hqs[i].date)
            i += 1
    return {'yearly': yearly, 'adhoc': adhoc, 'weekend': weekend}
