#coding:utf-8
from django.shortcuts import render
 
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
def index(request, a, b):
    #Retrieve data or whatever you need
    results = str(int(a)+int(b))
    return render_to_pdf(
            'test.html',
            {
                'pagesize':'A4',
                'results': results,
            }
        )
def html(request, a, b):
    #Retrieve data or whatever you need
    results = a+b
    return render(request, 'test.html',
            {
                'pagesize':'A4',
                'results': results,
            })
