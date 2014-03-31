import GeoIP

def geolocate(request):
    # Find the user
    g = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    ip = request.META['REMOTE_ADDR']
    if ((not ip) or ip == '127.0.0.1') and request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']

    # Get country
    country = g.country_code_by_addr(ip)

    return HttpResponse("I know where you live! " + str(country))