from typing import Callable
from django.http import HttpRequest, HttpResponse


class ThrottlingMiddleware:
    """
    Ограничивает обработку запросов пользователя, если он делает обращения слишком часто
    """

    def __init__(self, get_respose: Callable):
        self.get_respose = get_respose
        self.ip_dict = dict()

    def __call__(self, request: HttpRequest) -> HttpResponse:
        import datetime

        ip = request.META['REMOTE_ADDR']
        time_req = datetime.datetime.now()
        last_time_req = self.ip_dict.get(ip)

        if last_time_req is None or (time_req - last_time_req).total_seconds() >= 5:
            self.ip_dict[ip] = time_req
            response = self.get_respose(request)
        else:
            response = HttpResponse('Частая отправка запросов!!!')

        return response
