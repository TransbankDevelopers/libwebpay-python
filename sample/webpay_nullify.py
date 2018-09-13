"""
@author     Allware Ltda. (http://www.allware.cl)
@copyright  2016 Transbank S.A. (http://www.tranbank.cl)
@date       Jan 2015
@license    GNU LGPL
@version    2.0.1
"""

from django.http import HttpResponse
import socket

from certificates import cert_normal

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
		config['INTEGRACION'] = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSCommerceIntegrationService?wsdl'
		
		""" Llave Privada Certificacion """
		config['CERTIFICACION'] = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSCommerceIntegrationService?wsdl'
		
		""" Llave Privada Produccion"""
		config['PRODUCCION'] = 'https://webpay3g.transbank.cl/WSWebpayTransaction/cxf/WSCommerceIntegrationService?wsdl'
		
		return config

class WebpayNullify():
		
	def __init__(self, configuration):
		
		global config;
		config = configuration;
		self.__config = config
		
		dictWsdl = Dictionaries.dictionaryConfig();
		
		global url;
		url = dictWsdl[self.__config.getEnvironment()];
		self.__url = url;

        """
        Permite solicitar a Webpay la anulacion de una transaccion
        realizada previamente y que se encuentra vigente.
        """

        @staticmethod
        def nullify(authorizationCode, authorizedAmount, buyOrder, nullifyAmount, commercecode):
        
            client = WebpayNullify.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());

            client.options.cache.clear();

            nullificationInput = client.factory.create('nullificationInput');

            """ Codigo de autorizacion de la transaccion que se requiere anular """
            nullificationInput.authorizationCode = authorizationCode;
            
            """ Monto autorizado de la transaccion que se requiere anular """
            nullificationInput.authorizedAmount = authorizedAmount;
            
            """ Orden de Compra """
            nullificationInput.buyOrder = buyOrder;
            
            """ Codigo de Comercio """
            if(commercecode == None):
                nullificationInput.commerceId = config.getCommerceCode();
            else:
                nullificationInput.commerceId = commercecode;
                
            nullificationInput.nullifyAmount = nullifyAmount;

            try :
                nullificationOutput = client.service.nullify(nullificationInput);
            except Exception as e:
                print str(e)

            return nullificationOutput;
        
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