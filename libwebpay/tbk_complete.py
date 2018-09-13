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

from random import randrange

import sys
sys.path.append('../sample/certificates')
import cert_complete

from configuration import Configuration
from webpay import Webpay

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

""" Ejecucion de metodo initCompleteTransaction """
client = webpay.getCompleteTransaction().initCompleteTransaction(amount, buyOrder, sessionId, cardExpirationDate, cvv, cardNumber);

print "Ejemplos Webpay - Transaccion Complete:"+str(client)