from blog.models import IPAddress


class IPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            user_ip = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            user_ip = IPAddress.objects.create(ip_address=ip)

        request.user.ip_address = user_ip

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
