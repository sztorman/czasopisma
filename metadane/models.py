import os
from django.db import models
# Create your models here.
import re

def filterDateFromText(str):
    dateList = re.findall(r'\d{4}', str)
    result = ''
    if len(dateList) >= 1:
        result = dateList[0]
    return result

class Czasopismo(models.Model):
    id = models.IntegerField(primary_key=True)
    lp = models.CharField(max_length=3L, blank=True)
    tytul = models.CharField(max_length=767L, blank=True)
    nazwa_wydawcy = models.CharField(max_length=109L, blank=True)
    data_wydania = models.DateField(blank=True)
    miejsce_wydania = models.CharField(max_length=22L, blank=True)
    temat_i_slowa = models.CharField(max_length=144L, blank=True)
    kod_jezyka = models.CharField(max_length=11L, blank=True)
    sygnatura = models.CharField(max_length=64L, blank=True)
    prawa = models.CharField(max_length=29L, blank=True)

    @property
    def date_normalized(self):
        return filterDateFromText(self.data_druku)

    @property
    def title_page_path_s(self):
        key = 'nr' + unicode(self.lp)
        return 'czasopisma/' + key + '/' + key + '_Ss.Tyt/0001_S.jpg'

    @property
    def title_page_path_m(self):
        key = 'nr' + unicode(self.lp)
        return 'czasopisma/' + key + '/' + key + '_Ss.Tyt/0001_M.jpg'

    @property
    def get_thumbs(self):
        import czasWeb
        key = 'nr' + unicode(self.lp)
        thumbs = sorted(os.listdir (czasWeb.__path__[0] + '/static/czasopisma/' + key + '/' + key + '_T/'))
        return thumbs

    @property
    def get_thumbs_paths(self):
        import czasWeb
        key = 'nr' + unicode(self.lp)
        thumbs = sorted(os.listdir (czasWeb.__path__[0] + '/static/czasopisma/' + key + '/' + key + '_T/'))
        resultPaths = []
        for t in thumbs:
            resultPaths += ['czasopisma/' + key + '/' + key + '_T/' + t]
        return resultPaths

    @property
    def get_small_paths(self):
        import czasWeb
        key = 'nr' + unicode(self.lp)
        thumbs = sorted(os.listdir (czasWeb.__path__[0] + '/static/czasopisma/' + key + '/' + key + '_S/'))
        resultPaths = []
        for t in thumbs:
            resultPaths += ['czasopisma/' + key + '/' + key + '_S/' + t]
        return resultPaths

    @property
    def get_medium_paths(self):
        import czasWeb
        key = 'nr' + unicode(self.lp)
        thumbs = sorted(os.listdir (czasWeb.__path__[0] + '/static/czasopisma/' + key + '/' + key + '_M/'))
        resultPaths = []
        for t in thumbs:
            resultPaths += ['czasopisma/' + key + '/' + key + '_M/' + t]
        return resultPaths

    @property
    def get_large_paths(self):
        import czasWeb
        key = 'nr' + unicode(self.lp)
        thumbs = sorted(os.listdir (czasWeb.__path__[0] + '/static/czasopisma/' + key + '/' + key + '_L/'))
        resultPaths = []
        for t in thumbs:
            resultPaths += ['czasopisma/' + key + '/' + key + '_L/' + t]
        return resultPaths

    @property
    def get_pdf(self):
        import czasWeb
        key = 'nr' + unicode(self.lp)
        pdf = czasWeb.__path__[0] + '/static/czasopisma/' + key + '/' + key + '.PDF'
        return pdf

    @property
    def get_txt_page_path(self):
        import czasWeb
        key = 'nr' + unicode(self.lp)
        txt = czasWeb.__path__[0] + '/static/czasopisma/' + key + '/TXT/'

    class Meta:
        db_table = 'czasopismo'