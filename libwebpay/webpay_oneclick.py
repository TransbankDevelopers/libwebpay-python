"""
@author     Allware Ltda. (http://www.allware.cl)
@copyright  2016 Transbank S.A. (http://www.tranbank.cl)
@date       Jan 2015
@license    GNU LGPL
@version    2.0.1
"""

import sys
sys.path.append('../sample/certificates')

from suds.client import Client
from suds.wsse import Security, Timestamp
from wsse.suds import WssePlugin

from suds.transport.https import HttpTransport
import logging

logging.basicConfig()

config = None
url = None;

class Dictionaries():

		"""
		Configuracion de WSDL segun ambiente
		"""

		@staticmethod
		def dictionaryConfig():

				config = dict()

				""" Llave Privada Integracion """
				config['INTEGRACION'] = 'https://webpay3gint.transbank.cl/webpayserver/wswebpay/OneClickPaymentService?wsdl'
		
				""" Llave Privada Certificacion """
				config['CERTIFICACION'] = 'https://webpay3gint.transbank.cl/webpayserver/wswebpay/OneClickPaymentService?wsdl'
		
				""" Llave Privada Produccion"""
				config['PRODUCCION'] = 'https://webpay3g.transbank.cl/webpayserver/wswebpay/OneClickPaymentService?wsdl'
		
				return config

class WebpayOneClick():
		
		def __init__(self, configuration):
		
				global config;
				config = configuration;
				self.__config = config
		
				dictWsdl = Dictionaries.dictionaryConfig();
		
				global url;
				url = dictWsdl[self.__config.getEnvironment()];
				self.__url = url;
				
		"""
		Permite realizar la inscripcion del tarjetahabiente e informacion de su 
		tarjeta de crdito. Retorna como respuesta un token que representa la transaccion de inscripcion
		y una URL (UrlWebpay),que corresponde a la URL de inscripcion de One Click
		"""

		@staticmethod
		def initInscription(username, email, urlReturn):
        
				client = WebpayOneClick.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
				client.options.cache.clear();
				

				oneClickInscriptionInput = client.factory.create('oneClickInscriptionInput');
	    
				""" nombre de usuario """
				oneClickInscriptionInput.username = username;

				""" email """
				oneClickInscriptionInput.email = email;

				""" url de respuesta """
				oneClickInscriptionInput.responseURL = urlReturn;

				try :
						oneClickInscriptionOutput = client.service.initInscription(oneClickInscriptionInput);
				except Exception as e:
						print str(e);

				return oneClickInscriptionOutput;

		"""
		Permite finalizar el proceso de inscripcion del tarjetahabiente en Oneclick. Entre otras cosas, retorna el identificador del usuario en Oneclick,
		el cual sera utilizado para realizar las transacciones de pago
		"""

		@staticmethod
		def finishInscription(token):
        
				client = WebpayOneClick.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
            
				client.options.cache.clear();

				oneClickFinishInscriptionInput = client.factory.create('oneClickFinishInscriptionInput');
				
				"""token obtenido en initInscription """
				oneClickFinishInscriptionInput.token = token;

				try :
						oneClickFinishInscriptionOutput = client.service.finishInscription(oneClickFinishInscriptionInput);
				except Exception as e:
						print str(e)
            
				return oneClickFinishInscriptionOutput;

		"""
		Permite realizar transacciones de pago. Retorna el resultado de la autorizacion. Este metodo que debe ser ejecutado, cada vez que el usuario
		selecciona pagar con Oneclick
        """

		@staticmethod
		def authorize(buyOrder, tbkUser, username, amount):
        
				client = WebpayOneClick.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
            
				client.options.cache.clear();

				oneClickPayInput = client.factory.create('oneClickPayInput');

				""" Orden de Compra """
				oneClickPayInput.buyOrder = buyOrder;
				
				""" Usuario TRansbank """
				oneClickPayInput.tbkUser = tbkUser;
				
				""" Nombre de usuario """
				oneClickPayInput.username = username;
				
				""" Monto de Compra"""
				oneClickPayInput.amount = amount;

				try :
						oneClickPayOutput = client.service.authorize(oneClickPayInput);
				except Exception as e:
						print str(e)
            
				return oneClickPayOutput;
		
		"""
		Permite reversar una transaccion de venta autorizada con anterioridad. Este metodo retorna como respuesta un identificador unico de la transaccion de reversa.
		"""
		
		@staticmethod
		def reverseTransaction(buyOrder):

				client = WebpayOneClick.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());

				client.options.cache.clear();

				oneClickReverseInput = client.factory.create('oneClickReverseInput');
				
				oneClickReverseInput.buyorder = buyOrder;

				try :
						oneClickReverseOutput = client.service.codeReverseOneClick(oneClickReverseInput);
				except Exception as e:
						print str(e)
            
				return oneClickReverseOutput;
		
		
		"""
		Permite eliminar la inscripcion de un usuario en Webpay OneClick ya sea por la eliminacion de un cliente en su sistema o por la solicitud de este para no operar con esta forma de pago.
		"""
		
		@staticmethod
		def removeUser(tbkUser, username):
        
				client = WebpayOneClick.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
            
				client.options.cache.clear();

				oneClickRemoveUserInput = client.factory.create('oneClickRemoveUserInput');
				
				""" Usuario Transbank """
				oneClickRemoveUserInput.tbkUser = tbkUser;
				
				""" Nombre de Usuario """
				oneClickRemoveUserInput.username = username;

				try :
						return client.service.removeUser(oneClickRemoveUserInput);
				except Exception as e:
						print str(e);

		@staticmethod
		def get_client(wsdl_url, our_keyfile_path, our_certfile_path, their_certfile_path):
            
				transport=HttpTransport()
				wsse = Security()
            
				return Client(
        wsdl_url,
        transport=transport,
        wsse=wsse,
        plugins=[
            WssePlugin(
                keyfile=our_keyfile_path,
                certfile=our_certfile_path,
                their_certfile=their_certfile_path,
            ),
        ],
    )