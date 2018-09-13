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

from certificates import cert_complete
from configuration import Configuration
from webpay import Webpay

configuration = None;
webpay = None;

def pageLoad():
	
	certificate = cert_complete.certDictionary.dictionaryCert();

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
	title   = '<h1>Ejemplos Webpay - Transaccion Complete</h1>'
	next_page = "http://127.0.0.1:8000/sample/tbk_complete/queryshare";

	""" Monto de la Transaccion """
	amount = '9990'

	""" Identificador de la Orden """
	buyOrder = randrange(999)

	""" (Opcional) Identificador de sesion, uso interno de comercio """ 
	sessionId = "abc123"
	
	""" Fecha de Expiracion de tarjeta, formato YY/MM """
	cardExpirationDate = "18/04"
	
	""" Codigo de verificacion de la tarjeta """
	cvv = 123
	
	""" Numero de la Tarjeta """
	cardNumber = "4051885600446623"
	
	try :
	
		request_dict = dict()
		request_dict['amount'] = str(amount);
		request_dict['buyOrder'] = str(buyOrder);
		request_dict['sessionId'] = str(sessionId);
		request_dict['cardExpirationDate'] = str(cardExpirationDate);
		request_dict['cvv'] = str(cvv);
		request_dict['cardNumber'] = str(cardNumber);
		
		""" Ejecucion de metodo initCompleteTransaction """
		client = webpay.getCompleteTransaction().initCompleteTransaction(amount, buyOrder, sessionId, cardExpirationDate, cvv, cardNumber);
		
		if (client["token"] != None and client["token"] != ""):
			message = "Sesion iniciada con exito en webpay";
		else:
			message = "Webpay no disponible";
		
	except Exception as e:
		
		text    = "Ocurri&oacute un error en la transacci&oacuten (Validar correcta configuraci&oacuten de parametros)"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+text+". "+str(e)+"</p>"
		return HttpResponse(title+step+result+link)

	request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+ str(request_dict) +"</p>"
	result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>"
	button  = "</br></br><form action="+next_page+" method='post'><input type='hidden' name='buyOrder' value="+str(buyOrder)+"><input type='hidden' name='token_ws' value="+client["token"]+"><input type='submit' value='Continuar'></form>"
	link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+message+button+link)

"""
Permite realizar consultas del valor de cuotas (producto nuevas cuotas)
"""

@csrf_exempt
def queryshare(request):
	
	pageLoad();
	
	step    = '<h2>Step: Queryshare</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion Complete</h1>'
	
	next_page = "http://127.0.0.1:8000/sample/tbk_complete/"+"authorize";

	""" Obtenemos token recibido por metodo POST """
	if request.POST.get("token_ws", "") is None :
        
		text    = "Ocurri&oacute un error en la transacci&oacuten"
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>[token_ws]=>0</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+request+"</p>"
        
        	""" Retorna HTML que se mostrara por navegador """
        	return HttpResponse(title+step+request+result+text)
    
	else:
		
		try :
			
			""" Token de la transaccion """
			token  = request.POST.get("token_ws", "");
			
			""" Identificador de la Orden """
			buyOrder  = request.POST.get("buyOrder", "");
			
			""" Numero de Cuotas """
			shareNumber = 2;
			
			request_dict = dict()
			request_dict['token'] = str(token);
			request_dict['buyOrder'] = str(buyOrder);
			request_dict['shareNumber'] = str(shareNumber);
			
			""" Ejecucion de metodo queryshare """
			client = webpay.getCompleteTransaction().queryshare(token, buyOrder, shareNumber);
			
			if (client["token"] != None or client["token"] != ""):
				message = "Sesion iniciada con exito en webpay";
			else:
				message = "Webpay no disponible";
			
		except Exception as e:
		
			text    = "Ocurri&oacute un error en la transacci&oacuten (Validar correcta configuraci&oacuten de parametros)"
			link    = "<a href='../default/index'>&laquo; volver a index</a>";
			result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+text+". "+str(e)+"</p>"
			return HttpResponse(title+step+result+link)

		""" Crea HTML que se mostrara por navegador """
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+str(request_dict)+"</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>"
		button  = "</br></br><form action="+next_page+" method='post'><input type='hidden' name='queryId' value="+str(client.queryId)+"><input type='hidden' name='buyOrder' value="+buyOrder+"><input type='hidden' name='token_ws' value="+token+"><input type='submit' value='Continuar'></form>"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		
		""" Retorna HTML que se mostrara por navegador """
		return HttpResponse(title+step+request+result+message+button+link);

"""
Ejecuta la solicitud de autorizacion, esta puede ser realizada con o sin cuotas. La respuesta entrega el resultado de la transaccion
"""

@csrf_exempt
def authorize(request):
	
	pageLoad();
	
	step    = '<h2>Step: Authorize</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion Complete</h1>'
	
	next_page = "http://127.0.0.1:8000/sample/tbk_complete/end";

	if request.POST.get("token_ws", "") is None :
        
		text    = "Ocurri&oacute un error en la transacci&oacuten"
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>[token_ws]=>0</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+request+"</p>"
        
        	""" Retorna HTML que se mostrara por navegador """
        	return HttpResponse(title+step+request+result+text)
    
	elif request.POST.get("token_ws", "") :
		
		try :
			
			""" Token de la transaccion """
			token  = request.POST.get("token_ws", "");
			
			""" Identificador de la Orden """
			buyOrder  = request.POST.get("buyOrder", "");

			""" (Opcional) Flag que indica si aplica o no periodo de gracia """
			gracePeriod = "false";
			
			""" (Opcional) Lista de contiene los meses en los cuales se puede diferir el pago, y el monto asociado a cada periodo (0 = No aplica) """
			deferredPeriodIndex = 0;
			
			""" Identificador de la consulta de cuota """
			idQueryShare  = request.POST.get("queryId", "");
			
			request_dict = dict()
			request_dict['token'] = str(token);
			request_dict['buyOrder'] = str(buyOrder);
			request_dict['gracePeriod'] = str(gracePeriod);
			request_dict['idQueryShare'] = str(idQueryShare);
			request_dict['deferredPeriodIndex'] = str(deferredPeriodIndex);
			
			""" Ejecucion de metodo authorize """
			client = webpay.getCompleteTransaction().authorize(token, buyOrder, gracePeriod, idQueryShare, deferredPeriodIndex);

			if (client.detailsOutput[0]['responseCode'] == 0):
				
				message = "Transacci&oacuten realizada con exito en Webpay";
				
			else: 
				message = "Webpay no disponible";
			
		except Exception as e:
		
			text    = "Ocurri&oacute un error en la transacci&oacuten (Validar correcta configuraci&oacuten de parametros)"
			link    = "<a href='../default/index'>&laquo; volver a index</a>";
			result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+text+". "+str(e)+"</p>"
			return HttpResponse(title+step+result+link)

		""" Crea HTML que se mostrara por navegador """
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+str(request_dict)+"</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>"
		button  = "</br></br><form action="+next_page+" method='post'><input type='hidden' name='authorizationCode' value="+client.detailsOutput[0]['authorizationCode']+"><input type='hidden' name='idQueryShare' value="+idQueryShare+"><input type='hidden' name='buyOrder' value="+buyOrder+"><input type='hidden' name='token_ws' value="+token+"><input type='submit' value='Continuar'></form>"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		
		""" Retorna HTML que se mostrara por navegador """
		return HttpResponse(title+step+request+result+message+button+link);

@csrf_exempt
def end(request):
	
	pageLoad();

	if (request.POST.get("token_ws", "") != None):
		
		next_page = "http://127.0.0.1:8000/sample/tbk_complete/nullify";
		
		message = request.POST.get("token_ws", "");
			
		buyOrder = request.POST.get("buyOrder", "");
			
		authorizationCode = request.POST.get("authorizationCode", "");

	else:

		message = "No Result"

	step    = '<h2>Step: End</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion Complete</h1>'
	request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>No Request</p>";
	result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+message+"</p>";
	
	text    = "Transaccion Finalizada";
	button  = "</br></br><form action="+next_page+" method='post'><input type='hidden' name='authorizationCode' value="+authorizationCode+"><input type='hidden' name='buyOrder' value="+buyOrder+"><input type='hidden' name='token_ws' value="+message+"><input type='submit' value='Anular transacci&oacute;n'></form>"
	link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+text+button+link)

@csrf_exempt
def nullify(request):

	pageLoad();
	
	step    = '<h2>Step: Nullify</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion Complete</h1>'

	try :
	
		""" Codigo de Comercio """
		commercecode = configuration.getCommerceCode();
		
		""" Codigo de autorizacion de la transaccion que se requiere anular """
		authorizationCode = request.POST.get('authorizationCode', "");

		""" Monto autorizado de la transaccion que se requiere anular """
		authorizedAmount = "9990";

		""" Orden de compra de la transaccion que se requiere anular """
		buyOrder = request.POST.get('buyOrder', "");

		""" Monto que se desea anular de la transaccion """
		nullifyAmount = authorizedAmount

		request_dict = dict()
		request_dict['commercecode'] = str(commercecode);
		request_dict['authorizationCode'] = str(authorizationCode);
		request_dict['authorizedAmount'] = str(authorizedAmount);
		request_dict['buyOrder'] = str(buyOrder);
		request_dict['nullifyAmount'] = str(nullifyAmount);
	
		""" Ejecucion de metodo nullify """
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
	link    = "<br><br/><a href='../default/index'>&laquo; volver a index</a>";
	
	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+message+link);