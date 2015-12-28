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
    if a == 'A4':
        size = 40
    else:
        size = 60
    url = fetch_resources(r'/reim_pdf/static/')
    return render_to_pdf(
            'test.html',
            {
                'pagesize': a,
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
