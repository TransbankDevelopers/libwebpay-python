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
import cert_normal

from configuration import Configuration
from webpay import Webpay

certificate = cert_normal.certDictionary.dictionaryCert();

global configuration;
configuration = Configuration();
configuration.setEnvironment(certificate['environment'])
configuration.setCommerceCode(certificate['commerce_code']);
configuration.setPrivateKey(certificate['private_key']);
configuration.setPublicCert(certificate['public_cert']);
configuration.setWebpayCert(certificate['webpay_cert']);

global webpay; 
webpay = Webpay(configuration);

"""
Ejemplo de llamada a Libreria webpay_normal
"""

""" URL Final """
urlFinal = "http://127.0.0.1:8000/sample/tbk_normal/end";
	
""" URL Return """
urlReturn = "http://127.0.0.1:8000/sample/tbk_normal/result";

""" Monto de la Transaccion """
amount = '1500'

""" Identificador de la Orden """
buyOrder = '123'

""" (Opcional) Identificador de sesion, uso interno de comercio """ 
sessionId = "abc123"

client = webpay.getNormalTransaction().initTransaction(amount, buyOrder, sessionId, urlReturn, urlFinal);

print "Ejemplos Webpay - Transaccion Normal:"+str(client)

"""
Respuesta esperada debe ser similar a:

(wsInitTransactionOutput){
   token = "eb64463a0b655ed55fadd01fd3f6e67d7b8c0c376abfa6044b2d89e3753217f4"
   url = "https://tbk.orangepeople.cl/filtroUnificado/initTransaction"
}

"""
