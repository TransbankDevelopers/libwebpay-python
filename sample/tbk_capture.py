"""
@brief      Ecommerce SDK for chilean Webpay
@category   Plugins/SDK
@author     Allware Ltda. (http://www.allware.cl)
@copyright  2015 Transbank S.A. (http://www.tranbank.cl)
@date       Jan 2016
@license    GNU LGPL
@version    2.0.1
@link       http://transbankdevelopers.cl/

This software was created for easy integration of ecommerce
portals with Transbank Webpay solution.

Required:
  - Linux 
  - Python 2.7+
  - Django 1.9.5
  
See documentation and how to install at link site
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 

from sample import *

from suds.client import Client
from suds.wsse import Security, Timestamp
from wsse.suds import WssePlugin

from suds.transport.https import HttpTransport
from random import randrange

from certificates import cert_capture
from configuration import Configuration
from webpay import Webpay

configuration = None;
webpay = None;

def pageLoad():

	certificate = cert_capture.certDictionary.dictionaryCert()

        global configuration;
        configuration = Configuration();
        configuration.setEnvironment(certificate['environment']);
        configuration.setCommerceCode(certificate['commerce_code']);
        configuration.setPrivateKey(certificate['private_key']);
        configuration.setPublicCert(certificate['public_cert']);
        configuration.setWebpayCert(certificate['webpay_cert']);
        
        global webpay; 
        webpay = Webpay(configuration);

"""
Llamada a pagina init (inicio de transaccion)
"""

def init(request):
	
	pageLoad();
	
	step = "<h2>Step: Init</h2>"
	title   = '<h1>Ejemplos Webpay - Captura Diferida</h1>'

        next_page = "http://127.0.0.1:8000/sample/tbk_capture/capture";

        html = "<p style='font-weight: bold; font-size: 150%;'>" + step + "</p>";
        html = html + "<form id='formulario' action="+next_page+" method='post'>";
        html = html + "<fieldset>";
        html = html + "<legend>Formulario de Captura</legend><br/><br/>";
        html = html + "<label>authorizationCode:</label>&nbsp;&nbsp;";
        html = html + "<input id='authorizationCode' name='authorizationCode' type='text' />&nbsp;&nbsp;&nbsp;";
        html = html + "<label>captureAmount:</label>&nbsp;&nbsp;";
        html = html + "<input id='captureAmount' name='captureAmount' type='text' />&nbsp;&nbsp;&nbsp;&nbsp;";
        html = html + "<label>buyOrder:</label>&nbsp;&nbsp;";
        html = html + "<input id='buyOrder' name='buyOrder' type='text' />&nbsp;&nbsp;&nbsp;&nbsp;<br/><br/><br/>";
        html = html + "<input id='campo3' name='enviar' type='submit' value='Enviar' />";
        html = html + "</fieldset>";
        html = html + "</form>";
        
        link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+html+link)

"""
Permite solicitar a Webpay la captura diferida de una transaccion con autorizacion y sin captura simultanea.
"""

@csrf_exempt
def capture(request):

	pageLoad();
	
	step    = '<h2>Step: capture</h2>'
	title   = '<h1>Ejemplos Webpay - Captura Diferida</h1>'

	try :

		""" Codigo de autorizacion de la transaccion que se requiere capturar """
		authorizationCode = request.POST.get('authorizationCode');

		""" Monto autorizado de la transaccion que se requiere capturar """
		captureAmount = request.POST.get('captureAmount');

		""" Orden de compra de la transaccion que se requiere capturar """
		buyOrder = request.POST.get('buyOrder');

		request_dict = dict()
		request_dict['authorizationCode'] = str(authorizationCode);
		request_dict['captureAmount'] = str(captureAmount);
		request_dict['buyOrder'] = str(buyOrder);

		client = webpay.getCaptureTransaction().capture(authorizationCode, captureAmount, buyOrder);
		
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
