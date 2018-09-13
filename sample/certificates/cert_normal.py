"""
  @author     Allware Ltda. (http://www.allware.cl)
  @copyright  2015 Transbank S.A. (http://www.tranbank.cl)
  @date       Jan 2015
  @license    GNU LGPL
  @version    2.0.1
"""

import os

class certDictionary():

	@staticmethod
	def dictionaryCert():
		
		certificate = dict()
		
		dir = os.path.dirname(__file__)
		
		""" ATENCION: Configurar modo de uso (INTEGRACION, CERTIFICACION o PRODUCCION) """
		certificate['environment'] = 'INTEGRACION'
		
		""" Llave Privada: Configura tu ruta absoluta """
		certificate['private_key'] = dir+'/integracion_normal/597020000541.key'
		
		""" Certificado Publico: Configura tu ruta absoluta """
		certificate['public_cert'] = dir+'/integracion_normal/597020000541.crt'
		
		""" Certificado Privado: COnfigura tu ruta absoluta """
		certificate['webpay_cert'] = dir+'/integracion_normal/tbk.pem'
		
		""" Codigo Comercio """
		certificate['commerce_code'] = '597020000541'
			
		return certificate