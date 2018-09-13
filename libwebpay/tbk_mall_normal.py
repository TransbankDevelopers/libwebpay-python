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
import cert_normal_mall

from configuration import Configuration
from webpay import Webpay
	
certificate = cert_normal_mall.certDictionary.dictionaryCert();
store_codes = cert_normal_mall.certDictionary.store_codes();

global configuration;
configuration = Configuration();
configuration.setEnvironment(certificate['environment'])
configuration.setCommerceCode(certificate['commerce_code']);
configuration.setPrivateKey(certificate['private_key']);
configuration.setPublicCert(certificate['public_cert']);
configuration.setWebpayCert(certificate['webpay_cert']);
configuration.setStoreCodes(store_codes);
	
global webpay; 
webpay = Webpay(configuration);

step = "<h2>Step: Init</h2>"
title   = '<h1></h1>'
	
""" Monto de la Transaccion """
amount = '1500'

""" Identificador de la Orden """
buyOrder = randrange(999)

""" (Opcional) Identificador de sesion, uso interno de comercio """ 
sessionId = "abc123"

""" URL Final """
urlFinal = "http://127.0.0.1:8000/sample/tbk_mall_normal/end";

""" URL Return """
urlReturn = "http://127.0.0.1:8000/sample/tbk_mall_normal/result";

""" Agregamos las tiendas existentes en configuracion """
w, h = 3, 2
i = 0;
stores = [[0 for x in range(w)] for y in range(h)] 
		
for k, v in configuration.getStoreCodes().items():
	stores[i][0] = v;
	stores[i][1] = randrange(9999);
	stores[i][2] = randrange(9999);
	i = i + 1;
		
client = webpay.getMallNormalTransaction().initTransaction(amount, buyOrder, sessionId, urlReturn, urlFinal, stores);

print "Ejemplos Webpay - Transaccion Mall Normal:"+str(client)

"""
(wsInitTransactionOutput){
   token = "ec645ae0bad3c1b53f431f3668a3405f2da064b948d606a6f97e056bb0f3f950"
   url = "https://tbk.orangepeople.cl/filtroUnificado/initTransaction"
 }
"""
