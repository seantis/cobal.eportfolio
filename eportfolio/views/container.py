from webob import Response
from webob.exc import HTTPUnauthorized, HTTPBadRequest

from repoze.bfg.security import has_permission

def remove_item(context, request):
    """
    View to remove an item from a container. 
    
    The view checks for the 'remove' permission on the *item*.
    """
    
    item_id = request.POST.get('item', None)
    try:
        if has_permission('remove', context[item_id], request):
            del context[item_id]
        else:
            return HTTPUnauthorized()
    except (KeyError, TypeError):
        return HTTPBadRequest()
        
    return Response('success')
    

def reorder_items(context, request):
    
    for index, indicator_id in enumerate(request.POST['items'].split(',')):
        indicator = context[indicator_id]
        if indicator and hasattr(indicator, 'sort_order'):
            indicator.sort_order = index
    
    return Response()