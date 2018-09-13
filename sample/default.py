from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 

from sample import *

from suds.client import Client
from suds.wsse import Security, Timestamp
from wsse.suds import WssePlugin

from suds.transport.https import HttpTransport
from random import randrange

from certificates import cert_normal
from webpay_normal import WebpayNormal
from webpay_nullify import WebpayNullify
from configuration import Configuration
from webpay import Webpay

def index(request):

        html = '<h1>Ejemplos Webpay</h1>'
        
        html = html +'<table border="0" style="width:70%">'
        html = html +'<tr>'
        html = html +'<td><h3>Transacci&oacute;n Normal</h3></td>'
        html = html +'<td><h3><a href="../tbk_normal/init">Webpay Normal</a></h3></td>'
        html = html +'<td><h3><a href="../tbk_nullify_normal/init">Webpay Normal Anulaci&oacute;n </a></h3></td>'
        html = html +'</tr>'
        html = html +'<tr>'
        html = html +'<td><h3>Transacci&oacute;n Mall Normal</h3></td>'
        html = html +'<td><h3><a href="../tbk_mall_normal/init">Webpay Mall Normal</a></h3></td>'
        html = html +'<td><h3><a href="../tbk_nullify_mall_normal/init">Webpay Mall Normal Anulaci&oacute;n </a></h3></td>'
        html = html +'</tr>'
        html = html +'<tr>'
        html = html +'<td><h3>Transacci&oacute;n Completa</h3></td>'
        html = html +'<td><h3><a href="../tbk_complete/init">Webpay Completa</a></h3></td>'
        html = html +'<td><h3><a href="../tbk_nullify_complete/init">Webpay Completa Anulaci&oacute;n </a></h3></td>'
        html = html +'</tr>'
        html = html +'<tr>'
        html = html +'<td><h3>Transacci&oacute;n Captura Diferida</h3></td>'
        html = html +'<td><h3><a href="../tbk_normal_capture/init">Webpay Normal Captura Diferida</a></h3></td>'
        html = html +'<td><h3><a href="../tbk_capture/init">Webpay Captura Diferida</a></h3></td>'
        html = html +'</tr>'
        html = html +'<tr>'
        html = html +'<td><h3>Transacci&oacute;n OneClick</h3></td>'
        html = html +'<td><h3><a href="../tbk_oneclick/init">Webpay OneClick</a></h3></td>'
        html = html +'<td><h3> - </h3></td>'
        html = html +'</tr>'
        html = html +'</table>'
        
        return HttpResponse(html)