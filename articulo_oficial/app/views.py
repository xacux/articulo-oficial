from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Articulo
from .serializers import ArticuloSerializer
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from selenium import webdriver
import json,re

class ArticuloViewSet(viewsets.ModelViewSet):
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()
    google_key = ''#API SEARCH
    nombre = ''
    descripcion=''
    caracteristicas=''
    codigo_ean = None
    def is_par(self, n):
        n = int(n)
        if n % 2 == 0:
            return True
        else:
            return False

    def calcula_digito(self):
        par = 0
        imp = 0
        c = 0
        for v in list(self.codigo_ean):
            if self.is_par(c):
                par = par + int(v)
            else:
                imp = imp + int(v)
            c = c + 1
            if c ==11:
                break
        resultado = imp * 3 + par
        return 10 - int(list(str(resultado))[len(list(str(resultado)))-1])

    def create(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            articulo = serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def extraccion(self):
        browser = webdriver.Chrome()
        #Por alguna razon no puedo encontrar productos con el codigo EAN desde la API Search de google.
        try:
            browser.get("https://www.google.com/search?client=ubuntu&channel=fs&q="+str(self.codigo_ean)+"&ie=utf-8&oe=utf-8")
        except HTTPError as e:
            print(e)
        except URLError:
            print("Servidor caido o dominio incorrecto")
        else:
            page = BeautifulSoup(browser.page_source,"html5lib")
            browser.close()
            links = page.findAll("h3")
            r = re.compile('\d+')
            r2 = re.compile('\W+')
            for a in links:
                tmp = ''
                for t in str(a.text).split():
                    if len(re.findall(r,t))==0 and len(re.findall(r2,t))==0:
                        tmp+= (t.rstrip('\n'))+' '
                    else:
                        break
                if len(self.nombre) < len(tmp):
                    self.nombre = tmp
            url_google = 'https://www.googleapis.com/customsearch/v1?key='+self.google_key+'&cx=013036536707430787589:_pqjad5hr1a&gl=es&cr=es&googlehost=google.es&q='+(self.nombre.replace(' ','+'))+'&alt=json'
            try:
                response = urlopen(url_google)
            except HTTPError as e:
                print(e)
            else:
                data = json.loads(response.read())
                try:
                    self.descripcion = data['items'][0]['snippet']
                except:
                    pass
                else:
                    articulo = Articulo(codigo_ean = str(self.codigo_ean),nombre = self.nombre, descripcion = self.descripcion)
                    articulo.save()
                    return True
        return False

    def get_queryset(self):
        queryset = Articulo.objects.all()
        self.codigo_ean = self.request.query_params.get('ean', None)
        if self.codigo_ean is not None:
            #Valida el codigo con el ultimo dígito
            if len(str(self.codigo_ean)) == 13 and int(self.calcula_digito()) == int(float(self.codigo_ean[12])):
                if queryset.filter(codigo_ean=self.codigo_ean).exists():
                    queryset = queryset.filter(codigo_ean=self.codigo_ean)
                else:
                    if self.extraccion():
                        print('Articulo creado '+self.nombre+' ('+self.codigo_ean+').')
                        queryset = queryset.filter(codigo_ean=self.codigo_ean)
                    else:
                        print('No se creo la wea')
            else:
                print('Codigo erroneo: '+self.codigo_ean)
        return queryset