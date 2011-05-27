from webob import Response

def file_view(context, request):
    
    fp = open(context.path(), 'rb')
    
    response = Response(fp.read())
    response.content_type =  context.content_type.encode('utf-8')
    fp.close()
    return response