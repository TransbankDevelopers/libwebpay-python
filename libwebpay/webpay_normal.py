"""
@author     Allware Ltda. (http://www.allware.cl)
@copyright  2016 Transbank S.A. (http://www.tranbank.cl)
@date       Jan 2015
@license    GNU LGPL
@version    2.0.1
"""

from django.http import HttpResponse
import socket

#from certificates import cert_normal
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
		config['INTEGRACION'] = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSWebpayService?wsdl'
		
		""" Llave Privada Certificacion """
		config['CERTIFICACION'] = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSWebpayService?wsdl'
		
		""" Llave Privada Produccion"""
		config['PRODUCCION'] = 'https://webpay3g.transbank.cl/WSWebpayTransaction/cxf/WSWebpayService?wsdl'
		
		return config


class WebpayNormal():
		
	def __init__(self, configuration):
		
		global config;
		config = configuration;
		self.__config = config
		
		dictWsdl = Dictionaries.dictionaryConfig();
		
		global url;
		url = dictWsdl[self.__config.getEnvironment()];
		self.__url = url;


	"""
	initTransaction
	
	Permite inicializar una transaccion en Webpay. 
	Como respuesta a la invocacion se genera un token que representa en forma unica una transaccion.
	"""
	
	@staticmethod
	def initTransaction(amount, buyOrder, sessionId, urlReturn, urlFinal):

		client = WebpayNormal.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert())
		client.options.cache.clear();
		init = client.factory.create('wsInitTransactionInput')
		
		init.wSTransactionType = client.factory.create('wsTransactionType').TR_NORMAL_WS
		
		init.commerceId = config.getCommerceCode();
		
		init.buyOrder = buyOrder;
		init.sessionId = sessionId;
		init.returnURL = urlReturn;
		init.finalURL = urlFinal;
		
		detail = client.factory.create('wsTransactionDetail');
		detail.amount = amount;
		
		detail.commerceCode = config.getCommerceCode();
		detail.buyOrder = buyOrder;
		
		init.transactionDetails.append(detail);
		init.wPMDetail=client.factory.create('wpmDetailInput');
		
		wsInitTransactionOutput = client.service.initTransaction(init);

		return wsInitTransactionOutput;
	
	"""
	getTransaction
	
	Permite obtener el resultado de la transaccion una vez que 
	Webpay ha resuelto su autorizacion financiera.
	"""
	
     	@staticmethod
	def getTransaction(token):

		client = WebpayNormal.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
		client.options.cache.clear();

        	transactionResultOutput = client.service.getTransactionResult(token);
        	acknowledge = WebpayNormal.acknowledgeTransaction(token);
		
		return transactionResultOutput;

	"""
	acknowledgeTransaction
	Indica  a Webpay que se ha recibido conforme el resultado de la transaccion
	"""
	
	@staticmethod
	def acknowledgeTransaction(token):
		
		client = WebpayNormal.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
		client.options.cache.clear();

		acknowledge = client.service.acknowledgeTransaction(token);
		
		return acknowledge;


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