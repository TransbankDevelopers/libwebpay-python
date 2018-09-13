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
import cert_oneclick

from configuration import Configuration
from webpay import Webpay

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

""" URL """
urlReturn = "http://127.0.0.1:8000/sample/tbk_oneclick/OneClickFinishInscription";

"""Nombre de usuario o cliente en el sistema del comercio"""
username = "usuario";

"""Direcci&oacute;n de correo electr&oacute;nico registrada por el comercio"""
email = "usuario@transbank.cl";
		
""" Ejecucion de metodo initTransaction """
client = webpay.getOneClickTransaction().initInscription(username, email, urlReturn);

print "Ejemplos Webpay - Transaccion OneClick: "+str(client)

