"""
@author     Allware Ltda. (http://www.allware.cl)
@copyright  2016 Transbank S.A. (http://www.tranbank.cl)
@date       Jan 2015
@license    GNU LGPL
@version    2.0.1
"""

#from certificates import cert_normal
import sys
sys.path.append('../sample/certificates')

from suds.client import Client
from suds.wsse import Security, Timestamp
from wsse.suds import WssePlugin

from suds.transport.https import HttpTransport
import logging

logging.basicConfig()

from decimal import *
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
		config['INTEGRACION'] = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSCompleteWebpayService?wsdl'
		
		""" Llave Privada Certificacion """
		config['CERTIFICACION'] = 'https://webpay3gint.transbank.cl/WSWebpayTransaction/cxf/WSCompleteWebpayService?wsdl'
		
		""" Llave Privada Produccion"""
		config['PRODUCCION'] = 'https://webpay3g.transbank.cl/WSWebpayTransaction/cxf/WSCompleteWebpayService?wsdl'
		
		return config

class WebpayComplete():
		
	def __init__(self, configuration):
		
		global config;
		config = configuration;
		self.__config = config
		
		dictWsdl = Dictionaries.dictionaryConfig();
		
		global url;
		url = dictWsdl[self.__config.getEnvironment()];
		self.__url = url;

        """
        Permite solicitar a Webpay la anulacion de una transaccion realizada previamente y que se encuentra vigente.
        """

        @staticmethod
        def initCompleteTransaction(amount, buyOrder, sessionId, cardExpirationdate, cvv, cardNumber):
        
            client = WebpayComplete.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
            client.options.cache.clear();

            wsCompleteInitTransactionInput = client.factory.create('wsCompleteInitTransactionInput');
	    
	    wsCompleteTransactionDetail = client.factory.create('wsCompleteTransactionDetail');
	    
	    completeCardDetail = client.factory.create('completeCardDetail');
	    
	    wsCompleteInitTransactionInput.transactionType = client.factory.create('wsCompleteTransactionType').TR_COMPLETA_WS;
	    wsCompleteInitTransactionInput.sessionId = sessionId;
	    
	    wsCompleteTransactionDetail.amount = amount;
            wsCompleteTransactionDetail.buyOrder = buyOrder;
	    wsCompleteTransactionDetail.commerceCode = config.getCommerceCode();
	    
	    completeCardDetail.cardExpirationDate = cardExpirationdate;
	    completeCardDetail.cvv = cvv;
	    completeCardDetail.cardNumber = cardNumber;
	    
	    wsCompleteInitTransactionInput.cardDetail = completeCardDetail;
	    
	    wsCompleteInitTransactionInput.transactionDetails = wsCompleteTransactionDetail;

            try :
                wsCompleteInitTransactionOutput = client.service.initCompleteTransaction(wsCompleteInitTransactionInput);
            except Exception as e:
                print str(e)
            
            return wsCompleteInitTransactionOutput;

        """
	Permite realizar consultas del valor de cuotas (producto nuevas cuotas)
	"""

        @staticmethod
        def queryshare(token, buyOrder, shareNumber):
        
            client = WebpayComplete.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
            client.options.cache.clear();

            wsCompleteQueryShareInput = client.factory.create('wsCompleteQueryShareInput');

            try :
                wsCompleteQuerySharesOutput = client.service.queryShare(token, buyOrder, int(shareNumber));
            except Exception as e:
                print str(e)
            
            return wsCompleteQuerySharesOutput;

        """
	Ejecuta la solicitud de autorizacion, esta puede ser realizada con o sin cuotas. La respuesta entrega el resultado de la transaccion.
	"""

        @staticmethod
        def authorize(token, buyOrder, gracePeriod, idQueryShare, deferredPeriodIndex):
        
            client = WebpayComplete.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
            client.options.cache.clear();

            authorize = client.factory.create('authorize');
	    
	    wsCompletePaymentTypeInput = client.factory.create('wsCompletePaymentTypeInput');
	    
	    wsCompleteQueryShareInput  = client.factory.create('wsCompleteQueryShareInput');

	    authorize.token = token;

	    wsCompletePaymentTypeInput.buyOrder = buyOrder;
	    wsCompletePaymentTypeInput.commerceCode = config.getCommerceCode();
	    wsCompletePaymentTypeInput.gracePeriod = gracePeriod;
	    
	    wsCompleteQueryShareInput.idQueryShare = idQueryShare; 
	    wsCompleteQueryShareInput.deferredPeriodIndex = deferredPeriodIndex;

	    wsCompletePaymentTypeInput.queryShareInput = wsCompleteQueryShareInput;

	    authorize.paymentTypeList = wsCompletePaymentTypeInput;

            try :
                wsCompleteAuthorizeOutput = client.service.authorize(token, wsCompletePaymentTypeInput);
		acknowledge = WebpayComplete.acknowledgeTransaction(token);
            except Exception as e:
                print str(e)
            
            return wsCompleteAuthorizeOutput;

	"""
	acknowledgeTransaction
	Indica a Webpay que se ha recibido conforme el resultado de la transaccion
	"""
	
	@staticmethod
	def acknowledgeTransaction(token):
		
		client = WebpayComplete.get_client(url, config.getPrivateKey(), config.getPublicCert(), config.getWebPayCert());
		client.options.cache.clear();
		
		acknowledge = client.service.acknowledgeCompleteTransaction(token);
		
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