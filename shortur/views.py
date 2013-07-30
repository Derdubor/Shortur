from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPNotFound
import re

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    ShortURL,
    ShortURLHits,
    )


@view_config(route_name='home', renderer='templates/shortur.pt', accept='text/html')
@view_config(route_name='home', renderer='json', accept='application/json')
def shortur_front(request):
    response = {}

    if 'url' in request.POST and request.POST['url'].strip():
        url = request.POST['url'].strip()
        
        if not re.match('[a-z0-9]+://', url):
            if url.startswith('//'):
                url = 'http:' + url
            elif url.startswith('/'):
                url = 'http:/' + url
            else:
                url = 'http://' + url
        
        surl = DBSession.query(ShortURL).filter(ShortURL.url == url).first()
        
        if not surl:
            key = ShortURL.generate_available_key()
            surl = ShortURL(url=url, key=key)
            DBSession.add(surl)
        else:
            key = surl.key
        
        response['url'] = url
        response['key'] = key

    return response

@view_config(route_name='lookup', renderer='templates/notfound.pt')    
def shortur_resolve(request):
    surl = DBSession.query(ShortURL).filter(
        ShortURL.key == request.matchdict['key']
    ).first()
    
    if surl:
        surl.got_hit()
        return HTTPMovedPermanently(location=surl.url)
        
    return {'key': request.matchdict['key']}
    
@view_config(route_name='statistics', renderer='templates/statistics.pt', accept='text/html')
@view_config(route_name='statistics', renderer='json', accept='application/json')
def shortur_statistics(request):
    response = {}

    surl = DBSession.query(ShortURL).filter(
        ShortURL.key == request.matchdict['key']
    ).first()
    
    if not surl:
        return HTTPNotFound()
    
    response['shorturl'] = {
        'key': surl.key,
        'url': surl.url,
        'hits': [],
        'hits_total': surl.hits_total,
    }
    
    for hit in surl.hits:
        response['shorturl']['hits'].append({
            'date': str(hit.date),
            'hits': hit.hits,
        })
        
    return response
