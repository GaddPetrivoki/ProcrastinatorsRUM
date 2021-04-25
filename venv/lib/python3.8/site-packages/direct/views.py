from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from gdc.get_direct_certificate import DCert
import json
from utils import get_cert_highlights
from forms import DiscoverPEMForm, DiscoverPublicForm



def  walk_chain_with_pem(request):
    name = "Verify Certificate and Chain from a PEM x509 Certificate" 
    if request.method == 'POST':
        form = DiscoverPEMForm(request.POST)
        if form.is_valid():
            c = form.save()
            output_format = form.cleaned_data.get('output_format', "html")
            if output_format == "json":
               return HttpResponse(json.dumps(c, indent=4),
                                 content_type="application/json")
            #else its HTML
            highlights = get_cert_highlights(c)
            summary = highlights['Summary']
            details = highlights['Details']
            del highlights['Summary']
            del highlights['Details']
            
            for d in details:
                messages.warning(request, _(d))
            if not details:
                messages.success(request, _("Certificate looks good!"))
            print details
                
            return render_to_response('direct/discovery.html',
                                      {'name': name,
                                       'highlights': [highlights, ],
                                       'summary': summary},
                                            RequestContext(request))
        else:
            #The form is invalid
             return render_to_response('direct/generic/bootstrapform.html',
                                            {'form': form,
                                             'name': name},
                                            RequestContext(request))
   #this is a GET
    context= {'name':name, 'form': DiscoverPEMForm() }
    return render_to_response('direct/generic/bootstrapform.html',
                              RequestContext(request, context,))


def  walk_chain_with_discovery(request):
    number_of_certs =0
    certs =[]
    possible_ocsp = False
    is_good = False
    is_unsure = False
    summary="Bad"
    name = "Verify the Certificate Chain from DNS and/or LDAP" 
    if request.method == 'POST':
        form = DiscoverPublicForm(request.POST)
        if form.is_valid():
            c = form.save()
            output_format = form.cleaned_data.get('output_format', "html")
            if output_format == "json":
               return HttpResponse(json.dumps(c, indent=4),
                                 content_type="application/json")
            #else its HTML
            if not c['is_found']:
                messages.error(request, _("The certificate was not found in LDAP or DNS."))
                highlights = {}
                highlights['Summary'] = "Not Found"
                certs = [highlights,]
                return render_to_response('direct/discovery.html',
                                      {'name': name,
                                       'highlights': certs,
                                       'summary': "Not Found",                                       
                                       },
                                            RequestContext(request))
            if  c['dns']['status'] == 200:
                
                for i in c['dns']['cert_details']:
                    number_of_certs += 1
                    highlights = get_cert_highlights(i)
                    certs.append(highlights)
                    for d in highlights['Details']:
                        messages.warning(request, _(d))
                        if d.__contains__('CRLs missing'):
                            possible_ocsp = True
                        
                    if highlights['Summary'] == "Good":
                        is_good = True
                    if highlights['Summary'] == "Unsure":
                        is_unsure = True
            
            if  c['ldap']['status'] == 200:

                
                for i in c['ldap']['cert_details']:
                    number_of_certs += 1
                    highlights = get_cert_highlights(i)
                    certs.append(highlights)
                    for d in highlights['Details']:
                        messages.warning(request, _(d))
                        if d.__contains__('CRLs missing'):
                            possible_ocsp = True
                    if highlights['Summary'] == "Good":
                        is_good = True
                    if highlights['Summary'] == "Unsure":
                        is_unsure = True
            if possible_ocsp == True:
                messages.info(request, _("The revocation status may be able to be confirmed with OCSP. OCSP is not yet implemented in this tool."))
                
            if number_of_certs>1:
                messages.info(request, _("More than one certificate was discovered."))
            
            
            if is_unsure and not is_good:
                summary = "Unsure"
            if is_good:
                summary="Good"
                messages.success(request, _("Certificate looks good!"))
                
            
            return render_to_response('direct/discovery.html',
                                      {'highlights': certs,
                                      'summary': summary
                                      },
                                            RequestContext(request))
            
            return HttpResponse(json.dumps(c, indent=4),
                         content_type="application/json")
        

        else:
            #The form is invalid
             return render_to_response('direct/generic/bootstrapform.html',
                                            {'form': form,
                                             'name': name},
                                            RequestContext(request))
   #this is a GET
    context= {'name':name, 'form': DiscoverPublicForm() }
    return render_to_response('direct/generic/bootstrapform.html',
                              RequestContext(request, context,))



def validate_direct_endpoint(request, endpoint):

    d = DCert(endpoint, endpoint)    
    result = d.validate_certificate()
    return HttpResponse(json.dumps(result),
                content_type="application/json")
    

def get_direct_endpoint_certificate(request, endpoint, file_extension="pem"):
    d = DCert(endpoint, endpoint)
    result = d.get_certificate()    
    response = HttpResponse(result, content_type="text/plain; charset=us-ascii") 
    
    if request.path.endswith(".pem") and result.__contains__("-----BEGIN CERTIFICATE-----"):
        response = HttpResponse(result, content_type="application/x-pem-file") 
    return response


