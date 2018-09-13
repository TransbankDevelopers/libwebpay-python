"""
@author     Allware Ltda. (http://www.allware.cl)
@copyright  2016 Transbank S.A. (http://www.tranbank.cl)
@date       Jan 2015
@license    GNU LGPL
@version    2.0.1
"""

from django.conf.urls import url

from . import tbk_normal
from . import tbk_mall_normal
from . import tbk_nullify_normal
from . import tbk_nullify_mall_normal
from . import tbk_nullify_complete
from . import tbk_complete
from . import tbk_capture
from . import tbk_normal_capture
from . import tbk_oneclick
from . import default

""" Contiene las vistas creadas para webpay """
urlpatterns = [
	url(r'^default/index', default.index, name='index'),
	url(r'^tbk_normal/init', tbk_normal.init, name='init'),
	url(r'^tbk_normal/result', tbk_normal.result, name='result'),
	url(r'^tbk_normal/end', tbk_normal.end, name='end'),
	url(r'^tbk_normal/nullify', tbk_normal.nullify, name='nullify'),
	url(r'^tbk_nullify_normal/init', tbk_nullify_normal.init, name='init'),
	url(r'^tbk_nullify_normal/nullify', tbk_nullify_normal.nullify, name='nullify'),
	url(r'^tbk_nullify_mall_normal/init', tbk_nullify_mall_normal.init, name='init'),
	url(r'^tbk_nullify_mall_normal/nullify', tbk_nullify_mall_normal.nullify, name='nullify'),
	url(r'^tbk_mall_normal/init', tbk_mall_normal.init, name='init'),
	url(r'^tbk_mall_normal/result', tbk_mall_normal.result, name='result'),
	url(r'^tbk_mall_normal/end', tbk_mall_normal.end, name='end'),
	url(r'^tbk_mall_normal/nullify', tbk_mall_normal.nullify, name='nullify'),
	url(r'^tbk_complete/init', tbk_complete.init, name='init'),
	url(r'^tbk_complete/queryshare', tbk_complete.queryshare, name='queryshare'),
	url(r'^tbk_complete/authorize', tbk_complete.authorize, name='authorize'),
	url(r'^tbk_complete/end', tbk_complete.end, name='end'),
	url(r'^tbk_complete/nullify', tbk_complete.nullify, name='nullify'),
	url(r'^tbk_nullify_complete/init', tbk_nullify_complete.init, name='init'),
	url(r'^tbk_nullify_complete/nullify', tbk_nullify_complete.nullify, name='nullify'),
	url(r'^tbk_capture/init', tbk_capture.init, name='init'),
	url(r'^tbk_capture/capture', tbk_capture.capture, name='capture'),
	url(r'^tbk_normal_capture/init', tbk_normal_capture.init, name='init'),
	url(r'^tbk_normal_capture/result', tbk_normal_capture.result, name='result'),
	url(r'^tbk_normal_capture/end', tbk_normal_capture.end, name='end'),
	url(r'^tbk_normal_capture/capture', tbk_normal_capture.capture, name='capture'),
	url(r'^tbk_oneclick/init', tbk_oneclick.init, name='init'),
	url(r'^tbk_oneclick/OneClickFinishInscription', tbk_oneclick.OneClickFinishInscription, name='OneClickFinishInscription'),
	url(r'^tbk_oneclick/OneClickAuthorize', tbk_oneclick.OneClickAuthorize, name='OneClickAuthorize'),
	url(r'^tbk_oneclick/OneClickReverse', tbk_oneclick.OneClickReverse, name='OneClickReverse'),
	url(r'^tbk_oneclick/OneClickFinal', tbk_oneclick.OneClickFinal, name='OneClickFinal'),
]
