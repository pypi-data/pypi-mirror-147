from urllib import request
from http.cookiejar import CookieJar

def GetServerTime(URL: str):
    try:
        assert 'http://' in URL or 'https://' in URL, 'Invalid scheme from url %r'%URL
        jar = CookieJar()
        requester = request.Request(URL, headers={'Pragma': 'no-cache'})
        opener = request.build_opener(request.HTTPCookieProcessor(jar))
        response = opener.open(requester)
        date = response.headers.get('Date')
        assert date is not None, 'Date is missing from response headers'
        response.close()
        return date
    except:
        raise ConnectionError('Connection aborted from %r'%URL)