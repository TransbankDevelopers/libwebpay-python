"""
@author     Allware Ltda. (http://www.allware.cl)
@copyright  2016 Transbank S.A. (http://www.tranbank.cl)
@date       Jan 2015
@license    GNU LGPL
@version    2.0.1
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 

from sample import *

from suds.client import Client
from suds.wsse import Security, Timestamp
from wsse.suds import WssePlugin

from suds.transport.https import HttpTransport
from random import randrange

from certificates import cert_normal_mall
from webpay_nullify import WebpayNullify
from configuration import Configuration
from webpay import Webpay

configuration = None;
webpay = None;

def pageLoad():

	certificate = cert_normal_mall.certDictionary.dictionaryCert();
    
        global configuration;
        configuration = Configuration();
	
	print certificate['commerce_code']
	
	configuration.setEnvironment(certificate['environment'])
        configuration.setCommerceCode(certificate['commerce_code']);
        configuration.setPrivateKey(certificate['private_key']);
        configuration.setPublicCert(certificate['public_cert']);
        configuration.setWebpayCert(certificate['webpay_cert']);
        
        global webpay; 
        webpay = Webpay(configuration);

def init(request):
	
	pageLoad();
	
	step = "<h2>Step: Init</h2>"
	title   = '<h1>Ejemplos Webpay - Transaccion Mall Normal Anulacion</h1>'

        next_page = "http://127.0.0.1:8000/sample/tbk_nullify_mall_normal/nullify";

        html = "<p style='font-weight: bold; font-size: 150%;'>" + step + "</p>";
        html = html + "<form id='formulario' action="+next_page+" method='post'>";
        html = html + "<fieldset>";
        html = html + "<legend>Formulario de Anulaci&oacute;n</legend><br/><br/>";
	html = html + "<label>commercecode:</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
        html = html + "<input id='commercecode' name='commercecode' type='text' />&nbsp;&nbsp;&nbsp;<br/><br/>";
        html = html + "<label>authorizationCode:</label>&nbsp;&nbsp;";
        html = html + "<input id='authorizationCode' name='authorizationCode' type='text' />&nbsp;&nbsp;&nbsp;";
        html = html + "<label>authorizedAmount:</label>&nbsp;&nbsp;";
        html = html + "<input id='authorizedAmount' name='authorizedAmount' type='text' />&nbsp;&nbsp;&nbsp;&nbsp;";
        html = html + "<label>buyOrder:</label>&nbsp;&nbsp;";
        html = html + "<input id='buyOrder' name='buyOrder' type='text' />&nbsp;&nbsp;&nbsp;&nbsp;";
        html = html + "<label>nullifyAmount:</label>&nbsp;&nbsp;";
        html = html + "<input id='nullifyAmount' name='nullifyAmount' type='text' /><br/><br/><br/>";
        html = html + "<input id='campo3' name='enviar' type='submit' value='Enviar' />";
        html = html + "</fieldset>";
        html = html + "</form>";
        
        link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+html+link)


@csrf_exempt
def nullify(request):

	pageLoad();
	
	step    = '<h2>Step: nullify</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion Mall Normal Anulacion</h1>'

	try :
	
		""" Codigo de Comercio """
		commercecode = request.POST.get('commercecode');

		""" Codigo de autorizacion de la transaccion que se requiere anular """
		authorizationCode = request.POST.get('authorizationCode');

		""" Monto autorizado de la transaccion que se requiere anular """
		authorizedAmount = request.POST.get('authorizedAmount');

		""" Orden de compra de la transaccion que se requiere anular """
		buyOrder = request.POST.get('buyOrder');

		""" Monto que se desea anular de la transaccion """
		nullifyAmount = request.POST.get('nullifyAmount');

		request_dict = dict()
		request_dict['commercecode'] = str(commercecode);
		request_dict['authorizationCode'] = str(authorizationCode);
		request_dict['authorizedAmount'] = str(authorizedAmount);
		request_dict['buyOrder'] = str(buyOrder);
		request_dict['nullifyAmount'] = str(nullifyAmount);
	
		""" Ejecucion de metodo initTransaction """
		client = webpay.getNullifyTransaction().nullify(authorizationCode, authorizedAmount, buyOrder, nullifyAmount, commercecode);
		
		message = "Transacci&oacute;n Finalizada";
		
	except Exception as e:
		
		text    = "Ocurri&oacute un error en la transacci&oacuten (Validar correcta configuraci&oacuten de parametros)"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+text+". "+str(e)+"</p>"
		return HttpResponse(title+step+result+link)
	
	""" Crea HTML que se mostrara por navegador """
	request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+str(request_dict)+"</p>"
	result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>"

	link    = "<br/><br/><a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+message+link);
