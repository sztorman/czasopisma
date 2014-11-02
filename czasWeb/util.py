# -*- coding: utf-8 -*-
import glob
import os

from metadane.models import Czasopismo
import re
from django.db.models import Q

def truncate_string(mystring, numberofwords): 
    return ' '.join(mystring.split()[:numberofwords])

def filterDateFromText(str):
    dateList = re.findall(r'\d{4}', str)
    result = ''
    if len(dateList) >= 1:
        result = dateList[0]
    return result

def processQuery(request):
    type = request.GET.get('type', '')
#     query = request.GET.get('query', '')
    qs = Czasopismo.objects.all()
    if type == 'simple':
        query = request.GET.get('query', '')
        #cięcie stringa na kawałki
        #znalezc wszysskiet ANDy i ORy, potem sprawdzic, czy nie ma cudzyslowow

        qObjs = Q(tytul__search=query) | Q(zawartosc_strony_tytulowej__search=query) | Q(autor_dok__search=query) | Q(autor_khw__search=query) 
        qs = qs.filter(qObjs)
    elif type == 'all':
        orderby = request.GET.get('order', 'data_wydania')
        if orderby == 'data_wydania' or orderby == '-data_wydania':
#             sql_normalize = "(CASE WHEN data_wydania REGEXP '[-]' THEN replace(replace(replace(replace(substr(data_wydania, 0, locate('-', data_wydania)), '[', ''), ']', ''), 'post', ''), ' ', '') ELSE replace(replace(replace(replace(data_wydania, '[', ''), ']', ''), 'post', ''), ' ', '') END)"            
#             qs = qs.extra(select={'data_normalized': sql_normalize}).extra(order_by=[orderby.replace('data_wydania', 'data_normalized')])
            qs = qs.extra(order_by=[orderby.replace('data_wydania','nazwa_wydawcy')])
        else:
            qs = qs.order_by(orderby)   
    elif type == 'adv':
        if 'rocznik' in request.GET:
            if request.GET['rocznik'] != '':
                qs = qs.filter(data_wydania__year=request.GET['rocznik'])
        if 'numer' in request.GET:
            if request.GET['numer'] != '':
                qs = qs.filter(lp=request.GET['numer'])
        if 'tresc' in request.GET:
            lp_list = []
            if request.GET['tresc'] != '':
                r=re.compile(request.GET['tresc'])
                for row in qs:
                    path = request.get_txt_page_path(row.lp)
                    for infile in glob.glob( os.path.join(path, '*.txt')):
                            text=open(infile).read()
                            if (re.findall(r,text)>0):
                                lp_list.append(row.lp)
                qs = qs.filter(lp__in=lp_list)
        if 'dataOd' in request.GET:
            if request.GET['dataOd'] != '':
#                 sql_normalize = "(CASE WHEN data_wydania REGEXP '[-]' THEN replace(replace(replace(replace(substr(data_wydania, 0, locate('-', data_wydania)), '[', ''), ']', ''), 'post', ''), ' ', '') ELSE replace(replace(replace(replace(data_wydania, '[', ''), ']', ''), 'post', ''), ' ', '') END)"
#                 qs = qs.extra(where=[sql_normalize + " >= " + request.GET['dataOd']])
                sql_normalize = '(data_wydania >= ' + request.GET['dataOd'] + ' OR data_wydania >= ' + request.GET['dataOd'] + ")"
                qs = qs.extra(where=[sql_normalize])
                # qs = qs.filter(date_normalized__gte=filterDateFromText(request.GET['dataOd']))
        if 'dataDo' in request.GET:
            if request.GET['dataDo'] != '':
#                 sql_normalize = "(CASE WHEN data_wydania REGEXP '[-]' THEN replace(replace(replace(replace(substr(data_wydania, 0, locate('-', data_wydania)), '[', ''), ']', ''), 'post', ''), ' ', '') ELSE replace(replace(replace(replace(data_wydania, '[', ''), ']', ''), 'post', ''), ' ', '') END)"
#                 qs = qs.extra(where=[sql_normalize + " <= " + request.GET['dataDo']])
                sql_normalize = '(data_wydania <= ' + request.GET['dataDo'] + ' OR data_wydania <= ' + request.GET['dataDo'] + ")"
                qs = qs.extra(where=[sql_normalize])
                # qs = qs.filter(date_normalized__lte=filterDataFromText(request.GET['dataDo']))
            
    return qs

def searchDescription(request):
    type = request.GET.get('type', '')
    opis = 'Wyniki wyszukiwania dla '
    if type == 'simple':
        opis += request.GET.get('query', '')
    elif type == 'adv':
        opis += ": "
        objList = []
        for k,v in request.GET.iteritems():
            objList += [(k,v)]
        objList.reverse()
        for k,v in objList:
            if k not in ['pageNo', 'type', 'view']:
                if v != '':
                    if opis[opis.__len__()-1:opis.__len__()] == ',':
                        opis += " "
                    if k == 'dataDo':
                        opis +=  u'data do: “' + v + u'”,'
                    elif k == 'dataOd':
                        opis +=  u'data od: “' + v + u'”,'
                    else:
                        opis += k + u': “' + v + u'”,'
        opis = opis[0:opis.__len__()-1]
    
    return opis