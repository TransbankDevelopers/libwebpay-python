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

from certificates import cert_oneclick
from webpay_oneclick import WebpayOneClick
from configuration import Configuration
from webpay import Webpay

configuration = None;
webpay = None;

"""Nombre de usuario o cliente en el sistema del comercio"""
username = "usuario";

"""Direcci&oacute;n de correo electr&oacute;nico registrada por el comercio"""
email = "usuario@transbank.cl";

def pageLoad():
	
	certificate = cert_oneclick.certDictionary.dictionaryCert();

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
	
	step = '<h2>Step: Init</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion OneClick</h1>'
	
	try :
	
		""" URL """
		urlReturn = "http://127.0.0.1:8000/sample/tbk_oneclick/OneClickFinishInscription";
	
		request_dict = dict()
		request_dict['username'] = str(username);
		request_dict['email'] = str(email);
		request_dict['urlReturn'] = str(urlReturn);
		
		""" Ejecucion de metodo initTransaction """
		client = webpay.getOneClickTransaction().initInscription(username, email, urlReturn);
		
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
	button  = "</br></br><form action="+client["urlWebpay"]+" method='post'><input type='hidden' name='TBK_TOKEN' value="+client["token"]+"><input type='submit' value='Continuar'></form>"
	link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+message+button+link)


"""
Permite finalizar el proceso de inscripcion del tarjetahabiente en Oneclick. Entre otras cosas, retorna el identificador del usuario en Oneclick,
el cual sera utilizado para realizar las transacciones de pago
"""

@csrf_exempt
def OneClickFinishInscription(request):
	
	pageLoad();
	
	step    = '<h2>Step: Get FinishInscription</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion OneClick</h1>'

	next_page = "http://127.0.0.1:8000/sample/tbk_oneclick/OneClickAuthorize";

	""" Obtenemos token desde initTransaction recibido por metodo POST """
	if request.POST.get("token_ws", "") is None :
        
		text    = "Ocurri&oacute un error en la transacci&oacuten"
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>[token_ws]=>0</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+request+"</p>"
        
        	""" Retorna HTML que se mostrara por navegador """
        	return HttpResponse(title+step+request+result+text)
    
	else:
		
		try :
			
			""" Token de la transaccion """
			token  = request.POST.get("TBK_TOKEN", "");

			request_dict = dict()
			request_dict['token'] = str(token);
			
			client = webpay.getOneClickTransaction().finishInscription(token);
			
			if (client.responseCode == 0):
				message = "Sesion iniciada con exito en webpay";
			else:
				message = "Webpay no disponible";
			
		except Exception as e:
		
			text    = "Ocurri&oacute un error en la transacci&oacuten (Validar correcta configuraci&oacuten de parametros)"
			link    = "<a href='../default/index'>&laquo; volver a index</a>";
			result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+text+". "+str(e)+"</p>";
			return HttpResponse(title+step+result+link)

		""" Crea HTML que se mostrara por navegador """
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+str(request_dict)+"</p>";
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>";
		button  = "</br></br><form action="+next_page+" method='post'><input type='hidden' name='tbkUser' value="+client.tbkUser+"><input type='submit' value='Continuar'></form>"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		
		""" Retorna HTML que se mostrara por navegador """
		return HttpResponse(title+step+request+result+message+button+link);

"""
Permite realizar transacciones de pago.
Retorna el resultado de la autorizacion. Este metodo que debe ser ejecutado, cada vez que el usuario selecciona pagar con Oneclick
"""

@csrf_exempt
def OneClickAuthorize(request):
	
	pageLoad();
	
	step    = '<h2>Step: Get Authorize</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion OneClick</h1>'
	
	next_page = "http://127.0.0.1:8000/sample/tbk_oneclick/OneClickReverse";

	if request.POST.get("token_ws", "") is None :
        
		text    = "Ocurri&oacute un error en la transacci&oacuten"
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>[token_ws]=>0</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+request+"</p>"
        
        	""" Retorna HTML que se mostrara por navegador """
        	return HttpResponse(title+step+request+result+text)
    
	else:
		
		try :
			
			""" Usuario Transbank de la transaccion """
			tbkUser  = request.POST.get("tbkUser", "");
			
			""" Monto del pago en pesos """
			amount = 9200;

			"""Identificador unico de la compra generado por el comercio"""
			buyOrder = randrange(999);
			
			request_dict = dict()
			request_dict['tbkUser'] = str(tbkUser);
			request_dict['amount'] = str(amount);
			request_dict['buyOrder'] = str(buyOrder);
			
			client = webpay.getOneClickTransaction().authorize(buyOrder, tbkUser, username, amount);

			if (client.responseCode == 0):
				
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
		button  = "</br></br><form action="+next_page+" method='post'><input type='hidden' name='buyOrder' value="+ str(buyOrder) +"><input type='hidden' name='tbkUser' value="+ str(tbkUser) +"><input type='submit' value='Continuar'></form>"
		link    = "<a href='../default/index'>&laquo; volver a index</a>";
		
		""" Retorna HTML que se mostrara por navegador """
		return HttpResponse(title+step+request+result+message+button+link);
	

"""
Permite reversar una transaccion de venta autorizada con anterioridad. Este metodo retorna como respuesta un identificador unico de la transaccion de reversa.
"""
	
@csrf_exempt
def OneClickReverse(request):
	
	pageLoad();
	
	step    = '<h2>Step: OneClickReverse</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion OneClick</h1>'
	
	next_page = "http://127.0.0.1:8000/sample/tbk_oneclick/OneClickFinal";
	
	tbkUser = request.POST.get("tbkUser", "");

	if (request.POST.get("buyOrder", "") is None):
		
		text    = "Ocurri&oacute un error en la transacci&oacuten"
		request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>[token_ws]=>0</p>"
		result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+request+"</p>"
        
        	""" Retorna HTML que se mostrara por navegador """
        	return HttpResponse(title+step+request+result+text)

	else:

		""" Identificador unico de la compra generado por el comercio """
		buyOrder = request.POST.get("buyOrder", "");
		
		request_dict = dict()
		request_dict['buyOrder'] = str(buyOrder);
		
		client = webpay.getOneClickTransaction().reverseTransaction(buyOrder);
		
	if (client.reversed == 0):		
		message = "Transacci&oacuten realizada con exito en Webpay";	
	else: 
		message = "Webpay no disponible";

	request = "<p style='font-size: 100%; background-color:lightyellow;'><strong>request</strong><br><br><br/>"+str(request_dict)+"</p>";
	result  = "<p style='font-size: 100%; background-color:lightgrey;'><strong>result</strong><br><br><br/>"+str(client)+"</p>";
	
	button  = "</br></br><form action="+next_page+" method='post'><input type='hidden' name='buyOrder' value="+buyOrder+"><input type='hidden' name='tbkUser' value="+tbkUser+"><input type='submit' value='Continuar'></form>"
	link    = "<a href='../default/index'>&laquo; volver a index</a>";

	""" Retorna HTML que se mostrara por navegador """
	return HttpResponse(title+step+request+result+message+button+link)


"""
Permite eliminar la inscripcion de un usuario en Webpay OneClick ya sea por la eliminacion de un cliente en su sistema o por la solicitud de este para no operar con esta forma de pago.
"""

@csrf_exempt
def OneClickFinal(request):

	pageLoad();
	
	step    = '<h2>Step: Get removeUser</h2>'
	title   = '<h1>Ejemplos Webpay - Transaccion OneClick</h1>'

	try :
	
		""" Usuario Transbank de la transaccion """
		tbkUser  = request.POST.get("tbkUser", "");
	
		request_dict = dict()
		request_dict['tbkUser'] = str(tbkUser);
	
		""" Ejecucion de metodo initTransaction """
		client = webpay.getOneClickTransaction().removeUser(tbkUser, username);
		
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