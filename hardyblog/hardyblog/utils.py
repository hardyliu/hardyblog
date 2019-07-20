try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    print('ref_url',ref_url)
    test_url = urlparse(urljoin(request.host_url, target))
    print('test_url',test_url)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    print('redirect_back->next',request.args.get('next'))
    print('redirect_back->referrer',request.referrer)
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
