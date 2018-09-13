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
from webpay_capture import WebpayCapture
from configuration import Configuration
from webpay import Webpay

request_dict = dict()

configuration = None;
webpay = None;

def pageLoad():
	
	certificate = cert_capture.certDictionary.dictionaryCert();

	global configuration;
	configuration = Configuration();
	configuration.setEnvironment(certificate['environment'])
	configuration.setCommerceCode(certificate['commerce_code']);
	configuration.setPrivateKey(certificate['private_key']);
	configuration.setPublicCert(certificate['public_cert']);
	configuration.setWebpayCert(certificate['webpay_cert']);
	
	global webpay; 
	webpay = Webpay(configuration);

""" Llamada a pagina init (inicio de transaccion) """

def init(request):
	
	pageLoad();
	
	step = "<h2>Step: Init</h2>"
	title   = '<h1>Ejemplos Webpay - Transaccion Normal Captura Diferida</h1>'

	""" Monto de la Transaccion """
	amount = '9990'

	""" Identificador de la Orden """
	buyOrder = randrange(999)

	""" (Opcional) Identificador de sesion, uso interno de comercio """ 
	sessionId = "abc123"
	
	""" URL Final """
	urlFinal = "http://127.0.0.1:8000/sample/tbk_normal_capture/end";
	
	""" URL Return """
	urlReturn = "http://127.0.0.1:8000/sample/tbk_normal_capture/result";
	
	try :

		request_dict['amount'] = amount;
		request_dict['buyOrder'] = buyOrder;
		request_dict['sessionId'] = sessionId;
		request_dict['urlFinal'] = urlReturn;
		request_dict['urlReturn'] = urlFinal;
	
		""" Ejecucion de metodo initTransaction """
		client = webpay.getNormalTransaction().initTransaction(amount, buyOrder, sessionId, urlReturn, urlFinal);
		text    = "Sesion iniciada con exito en Webpay";
		
		if (client["token"] != None and client["token"] != ""):
			message = "Sesion iniciada con exito en webpay";
		else:
			message = "Webpay no disponible";
		
	except Exception as e:
		
		text    = "Ocurri&oacute un error en la transacci&oacuten (Validar correcta configuraci&oacuten de parametros)"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+text+". "+str(e)+"</p>"
		return HttpResponse(title+step+result+link)

	request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+str(request_dict)+"</p>"
	result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>"
	button  = "</br></br><form action="+client["url"]+" method='post'><input type='hidden' name='token_ws' value="+client["token"]+"><input type='submit' value='Continuar'></form>"
	link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+message+button+link)

""" Llamada a pagina /result (resultado de transaccion) """

@csrf_exempt
def result(request):
	
	pageLoad();
	
	step    = '<h2>Step: Get Result</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion Normal Captura Diferida</h1>'

	""" Obtenemos token desde initTransaction recibido por metodo Post """
	if request.POST.get("token_ws", "") is None :
        
		text    = "Ocurri&oacute un error en la transacci&oacuten"
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>[token_ws]=>0</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+request+"</p>"
        
        	""" Retorna HTML que se mostrara por navegador """
        	return HttpResponse(title+step+request+result+text)
    
	elif request.POST.get("token_ws", "") :
		
		try :
			
			token  = request.POST.get("token_ws", "");
			
			request_dict['token'] = token;
			
			""" Ejecucion de metodo getTransaction """
			client = webpay.getNormalTransaction().getTransaction(token);
			
			if (client.detailOutput[0]['responseCode'] == 0):
				
				message = "Pago ACEPTADO por webpay (se deben guardar datos para mostrar voucher)"

				script = "<script>localStorage.setItem('authorizationCode', " + str(client.detailOutput[0]['authorizationCode']) + ")</script>";
				script = script + "<script>localStorage.setItem('commercecode', " + str(client.detailOutput[0]['commerceCode']) + ")</script>";
				script = script + "<script>localStorage.setItem('amount', " + str(client.detailOutput[0]['amount']) + ")</script>";
				script = script + "<script>localStorage.setItem('buyOrder', " + str(client.detailOutput[0]['buyOrder']) + ")</script>";
				
			else: 
				message = "Pago RECHAZADO por webpay [Codigo]=>"+client.detailOutput[0]['responseCode'];
			
		except Exception as e:
		
			text    = "Ocurri&oacute un error en la transacci&oacuten (Validar correcta configuraci&oacuten de parametros)"
			link    = "<a href='../default/index'>&laquo; volver a index</a>";
			result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+text+". "+str(e)+"</p>"
			return HttpResponse(title+step+result+link)

		""" Crea HTML que se mostrara por navegador """
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+str(request_dict)+"</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>"
		button  = "</br></br><form action="+client["urlRedirection"]+" method='post'><input type='hidden' name='token_ws' value="+token+"><input type='submit' value='Continuar'></form>"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		
		""" Retorna HTML que se mostrara por navegador """
		return HttpResponse(title+step+request+result+message+button+link+script);

""" Llamada a pagina /end (pagina final) """

@csrf_exempt
def end(request):
	
	pageLoad();

	nullify = "";

	if (request.POST.get('token_ws') != None):
		
		message = request.POST.get('token_ws')
		
		next_page = "http://127.0.0.1:8000/sample/tbk_normal_capture/"+"capture";
		
		nullify = "<form action=" + next_page + " method='post'>";
		nullify = nullify + "<input type='hidden' name='commercecode' id='commercecode' value=''>";
		nullify = nullify + "<input type='hidden' name='authorizationCode' id='authorizationCode' value=''>";
		nullify = nullify + "<input type='hidden' name='amount' id='amount' value=''>";
		nullify = nullify + "<input type='hidden' name='buyOrder' id='buyOrder' value=''>";
		nullify = nullify + "<input type='submit' value='Capturar Transacci&oacute;n &raquo;'></form>";
		nullify = nullify + "<script>var commercecode = localStorage.getItem('commercecode');document.getElementById('commercecode').value = commercecode;</script>";
		nullify = nullify + "<script>var authorizationCode = localStorage.getItem('authorizationCode');document.getElementById('authorizationCode').value = authorizationCode;</script>";
		nullify = nullify + "<script>var amount = localStorage.getItem('amount');document.getElementById('amount').value = amount;</script>";
		nullify = nullify + "<script>var buyOrder = localStorage.getItem('buyOrder');document.getElementById('buyOrder').value = buyOrder;</script>";
		
	else:

		message = "No Result"

	step    = '<h2>Step: End</h2>';
	title   = '<h1>Ejemplos Webpay - Transaccion Normal</h1>';
	request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>No Request</p>";
	result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+message+"</p>";
	
	text    = "Transaccion Finalizada<br><br><br/>";
	link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+text+nullify+link)

"""
Permite solicitar a Webpay la captura diferida de una transaccion con autorizacion y sin captura simultanea.
"""

@csrf_exempt
def capture(request):

	pageLoad();
	
	step    = '<h2>Step: Capture</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion Normal Captura Diferida</h1>'

	try :

		""" Codigo de autorizacion de la transaccion que se requiere anular """
		authorizationCode = request.POST.get('authorizationCode', '');

		""" Monto autorizado de la transaccion que se requiere anular """
		captureAmount = 200;

		""" Orden de compra de la transaccion que se requiere anular """
		buyOrder = request.POST.get('buyOrder', '');

		request_dict['authorizationCode'] = str(authorizationCode);
		request_dict['captureAmount'] = str(captureAmount);
		request_dict['buyOrder'] = str(buyOrder);

		""" Ejecucion de metodo capture """
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
	link    = "<br><br/><a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+message+link);