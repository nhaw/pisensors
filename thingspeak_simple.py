
import urllib
import urllib2


def log(api_key, fields):
    args = {'api_key':api_key}
    for (name, value) in fields:
        args[name] = str(value) 

    params = urllib.urlencode(args)
    url = 'https://api.thingspeak.com/update?' + params
    ret = urllib2.urlopen(url)
    code = ret.getcode()
    if code != 200:
        print 'Code for field {} value {} wass not OK: {}'.format(field_name, value, code)
    return code
