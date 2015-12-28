#!/bin/env python
#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.shortcuts import render
 
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
import os

def fetch_resources(uri):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + uri
    return path

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
def index(request, a):
    #Retrieve data or whatever you need
    if a == 'B5':
        size = {'content_width':649, 'content_height':314,'content_top':135,'footer_top':462,'form_left':392}
        page_size = a + ' landscape'
    elif a == 'A5':
        size = {'content_width':537, 'content_height':235,'content_top':135,'footer_top':366,'form_left':281}
        page_size = a + ' landscape'
    else :
        page_size = a + ' portrait'
        size = {'content_width':537, 'content_height':637,'content_top':155,'footer_top':802,'form_left':281}
    url = fetch_resources(r'/reim_pdf/static/')
    return render_to_pdf(
            'test.html',
            {
                'pagesize': page_size,
                'url':url,
                'size':size
            }
        )
def html(request, a, b):
    #Retrieve data or whatever you need
    results = str(int(a)+int(b))
    url = fetch_resources(r'/reim_pdf/static/')
    return render(request, 'test.html',
            {
                'pagesize':'A4',
                'results': results,
                'url':url,
            })
