# -*- coding: utf-8 -*-
from django.db.models import Count

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.core.paginator import Paginator

from math import ceil
from pyPdf import PdfFileWriter, PdfFileReader

from czasWeb.util import *
from metadane.models import *

appName = 'czasWeb'

templates = {
    'base': appName + '/base.html',
    'base_browse': appName + '/base_browse.html',
    'main': appName + '/main.html',
    'index': appName + '/index.html',
    'about': appName + '/about.html',
    'resource': appName + '/resource.html',
    'searchAdv': appName + '/searchAdv.html',
    'searchResultsGrid': appName + '/searchResultsGrid.html',
    'searchResultsList': appName + '/searchResultsList.html',
    'single': appName + '/single.html',
    'thumbnails': appName + '/thumbnails.html',
    'zoom': appName + '/zoom.html',
    'double': appName + '/double.html',
    'social': appName + '/social.html',
    'share': appName + '/share.html',
    'listNames': appName + '/listNames.html',
    'browse': appName + '/browse.html',
    }
    
def main(request):
    context = {}
    return render_to_response(templates['index'], context)

def about(request):
    context = {
        'title': 'stare druki BIH UW - O projekcie',
        'templates': templates,
        'highlight': [],
        }
    return render_to_response(templates['about'], context)

def resource(request):
    context = {
        'title': 'stare druki BIH UW - O zasobie',
        'templates': templates,
        'highlight': [],
        }
    return render_to_response(templates['resource'], context)
    
def searchAdv(request):
    context = {
        'title': 'stare druki BIH UW - Wyszukiwanie zaawansowane',
        'templates': templates,
        'highlight': ['searchAdv'],
    }
    return render_to_response(templates['searchAdv'], context)

def searchResults(request):
    if 'query' in request.GET:
        if request.GET['query'] == '':
            return redirect('czasWeb.views.searchAdv')
    qs = processQuery(request)
    view = request.GET.get('view', 'grid')
    currPage = 0
    pageNo = 0
    pages = None
    objPerPage = None
    p = None
    if qs.exists():
        p = Paginator(qs, 12)
        pageNo = int(request.GET.get('pageNo', 1))
        currPage = p.page(pageNo)
        objPerPage = currPage.object_list
        
        if currPage.has_other_pages():
            pages = []
            if pageNo < 4:
                for i in range(7):
                    if (i+1) <= p.num_pages:
                        pages += [p.page(i+1)]
            elif pageNo > p.num_pages - 3:
                for i in range(p.num_pages-7, p.num_pages):
                    pages += [p.page(i+1)]
            else:
                for i in range(pageNo-3, pageNo+4):
                    pages += [p.page(i)]
    
    type = request.GET.get('type', 'all')
    highlight = ['grid']
    ordering = request.GET.get('order', '')
    highlight += [ordering.replace("-","")]

    ordDir = request.GET.get('ordDir', '')
    if ordDir == 'asc':
        ordDir = 'desc'
    else:
        ordDir = 'asc'
    
    if type == 'all':
        highlight += ['browse']
    elif type == 'simple':
        pass
    else:
        highlight += ['searchAdv']
    
    context = {
        'type': request.GET.get('type', 'all'),
        'ordDir': ordDir,
        'view': view,
        'qs': objPerPage,
        'page': pageNo,
        'curPage': currPage,
        'p': p,
        'pages': pages,
        'viewUrl': request.get_full_path().replace('view=grid', '').replace('view=list', ''),
        'criteria': searchDescription(request),
        'title': 'stare druki BIH UW - Wynik wyszukiwania',
        'templates': templates,
        'pageUrl': re.sub('&pageNo=\d+', '', request.get_full_path()),
        'highlight': highlight,
    }
    templ = templates['searchResultsGrid']
     
    return render_to_response(templ, context)     
    
def single(request, id):
    context = {
        'obj': Czasopismo.objects.get(id=id),
        'title': 'Czasopismoi',
        'request': request,
        'templates': templates,
        'highlight': [],
        }
    return render_to_response(templates['single'], context)

def showThumbnails(request, id, pageNo):
    parent = Czasopismo.objects.get(id=id)
    thumbs = parent.get_thumbs_paths
    p = Paginator(thumbs, 36)
    page = p.page(pageNo)
    pageTranslate = {
        'thumbnail': int(ceil(page.start_index()/36.0)),
        'double': int(ceil(page.start_index()/2.0)),
        'zoom': page.start_index(),
        }
    context = {
        'qs': page.object_list,
        'parent': parent,
        'page': page,
        'paginator': p,
        'pageLink': re.sub('pageNo=\d+', '', request.get_full_path()),
        'obj': Czasopismo.objects.get(id=id),
        'title': 'stare druki BIH UW - przeglądaj miniatury',
        'request': request,
        'templates': templates,
        'chnagePageLink': 'czasWeb.views.showThumbnails',
        'pt': pageTranslate,
        }
    return render_to_response(templates['thumbnails'], context)

def zoom(request, id, pageNo):
    parent = Czasopismo.objects.get(id=id)
    thumbs = parent.get_large_paths
    txt = parent.get_txt_page_path
    p = Paginator(thumbs, 1)
    page = p.page(pageNo)
    pageTranslate = {
        'thumbnail': int(ceil(page.start_index()/36.0)),
        'double': int(ceil(page.start_index()/2.0)),
        'zoom': page.start_index(),
        }
    context = {
        'qs': page.object_list,
        'parent': parent,
        'page': page,
        'paginator': p,
        'pageLink': re.sub('pageNo=\d+', '', request.get_full_path()),
        'obj': Czasopismo.objects.get(id=id),
        'title': 'stare druki BIH UW - pojedyncza strona',
        'request': request,
        'templates': templates,
        'sharebox': 1,
        'chnagePageLink': 'czasWeb.views.zoom',
        'pt': pageTranslate,
        }
    return render_to_response(templates['zoom'], context)
    
def double(request, id, pageNo):
    parent = Czasopismo.objects.get(id=id)
    thumbs = [''] + parent.get_medium_paths
    p = Paginator(thumbs, 2)
    page = p.page(pageNo)
    pageTranslate = {
        'thumbnail': int(ceil(page.start_index()/36.0)),
        'double': int(ceil(page.start_index()/2.0)),
        'zoom': page.start_index(),
        }
    context = {
        'qs': page.object_list,
        'parent': parent,
        'page': page,
        'paginator': p,
        'pageLink': re.sub('pageNo=\d+', '', request.get_full_path()),
        'obj': Czasopismo.objects.get(id=id),
        'title': 'stare druki BIH UW - widok książki',
        'request': request,
        'templates': templates,
        'sharebox': 1,
        'chnagePageLink': 'czasWeb.views.double',
        'pt': pageTranslate,
        }
    return render_to_response(templates['double'], context)


def listMagazines(request, letter, pageNo):
    magazines=Czasopismo.objects.filter()
    years = list(set([entry.data_wydania.year for entry in magazines]))
    #years = Czasopismo.objects.extra(select={"year": "EXTRACT(YEAR FROM data_wydania)"}).distinct().values_list("year", flat=True)
    if letter != '#':
        if letter=='0':
            qs = Czasopismo.objects.filter(data_wydania__year=years[0])
        else:
            qs = Czasopismo.objects.filter(data_wydania__year=letter)
    qs = sorted(qs)
    p = None
    currPage = None
    actQuery = []
    alphabet = map(chr, range(65, 91))
    pages = []
    if len(qs) > 0:
        p = Paginator(qs, 63)
        pageNo = int(request.GET.get('pageNo', 1))
        currPage = p.page(pageNo)
        objPerPage = currPage.object_list

        if currPage.has_other_pages():
            if pageNo < 4:
                for i in range(7):
                    pages += [p.page(i+1)]
            elif pageNo > p.num_pages - 3:
                for i in range(p.num_pages-7, p.num_pages):
                    pages += [p.page(i+1)]
            else:
                for i in range(pageNo-3, pageNo+4):
                    pages += [p.page(i)]
    if currPage:
        actQuery = currPage.object_list
    context = {
        'years': years,
        'actLet': letter,
        'qs': actQuery,
        'page': currPage,
        'pages': pages,
        'p': p,
        'title': 'stare druki BIH UW - indeks autorów',
        'request': request,
        'templates': templates,
        'pageUrl': re.sub('&pageNo=\d+', '', request.get_full_path()),
        'highlight': ['listNames'],
        }
    return render_to_response(templates['listNames'], context)

def browse(request):
    context = {
        'title': 'stare druki BIH UW - widok książki',
        'request': request,
        'templates': templates,
        }
    return render_to_response(templates['base'], context)    
    
def download(request):
    import os.path
    import mimetypes
    mimetypes.init()
    files = request.GET.getlist('file')
    type = request.GET.get('exportType', '')
    objId = request.GET.get('obId', '')
    
    
#     if len(files) == 0:
#         return HttpResponseNotFound()
        
    try:
        if type == 'full':
            obj = Czasopismo.objects.get(id=objId)        
            file_path = obj.get_pdf
            fsock = open(file_path,"r")
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            print "file size is: " + str(file_size)
            mime_type_guess = mimetypes.guess_type(file_name)
            if mime_type_guess is not None:
                response = HttpResponse(fsock, mimetype=mime_type_guess[0])
            downloadedFileName = truncate_string(obj.wariant_tytulu, 3)
            if downloadedFileName == '':
                downloadedFileName = truncate_string(obj.tytul, 3)
                if downloadedFileName == '':
                    downloadedFileName = file_name
            response['Content-Disposition'] = 'attachment; filename=' + downloadedFileName + '.pdf'
        elif type == 'pages':
            obj = Czasopismo.objects.get(id=objId)        
            file_path = obj.get_pdf
            dataOd = request.GET.get('stronyOd','1')
            dataDo = request.GET.get('stronyDo', '1')
            output = PdfFileWriter()
            inputpdf = PdfFileReader(file(file_path, "rb"))
            lastPage = int(dataDo) 
            if lastPage > inputpdf.getNumPages():
                lastPage = inputpdf.getNumPages()
            
            for i in range(int(dataOd), lastPage+1):
                output.addPage(inputpdf.getPage(i-1))
            outfile_path = '/tmp/Czasopismoi/'
            if not os.path.exists(outfile_path):
                os.makedirs(outfile_path)
            import random
            outFileSeed = str(random.randint(1, 650000)) + '.pdf'
            if 'sessionid' in request.COOKIES:
                outFileSeed = request.COOKIES['sessionid'] + '.pdf'
            outfile_path += outFileSeed             
            outputStream = file(outfile_path, "wb")
            output.write(outputStream)
            outputStream.close()
            
            fsock = open(outfile_path,"r")
            file_name = os.path.basename(outfile_path)
            file_size = os.path.getsize(outfile_path)
            print "file size is: " + str(file_size)
            mime_type_guess = mimetypes.guess_type(file_name)
            if mime_type_guess is not None:
                response = HttpResponse(fsock, mimetype=mime_type_guess[0])
            downloadedFileName = truncate_string(obj.wariant_tytulu, 3)
            if downloadedFileName == '':
                downloadedFileName = truncate_string(obj.tytul, 3)
                if downloadedFileName == '':
                    downloadedFileName = file_name
            response['Content-Disposition'] = 'attachment; filename=' + downloadedFileName + '.pdf'
        else:
            obj = Czasopismo.objects.get(id=objId)
            system_path = '/srv/www/python/django-1.5-env/www/Czasopismoi/czasWeb/static/'
            file_path = system_path + files[0]
            if not os.path.exists(file_path):
                file_path = system_path + (Czasopismo.objects.get(id=files[0])).title_page_path_m
            fsock = open(file_path,"r")
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            print "file size is: " + str(file_size)
            mime_type_guess = mimetypes.guess_type(file_name)
            if mime_type_guess is not None:
                response = HttpResponse(fsock, mimetype=mime_type_guess[0])
            downloadedFileName = truncate_string(obj.wariant_tytulu, 3)
            if downloadedFileName == '':
                downloadedFileName = truncate_string(obj.tytul, 3)
                if downloadedFileName == '':
                    downloadedFileName = file_name
            response['Content-Disposition'] = 'attachment; filename=' + downloadedFileName + '.jpg'
#         else:
#             response = HttpResponseNotFound()            
    except IOError:
        response = HttpResponseNotFound()
    return response