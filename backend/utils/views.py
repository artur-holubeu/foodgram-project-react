from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _


def error_404(request, exception):
    message = _('Данного адреса не существует.')
    response = JsonResponse(data={'message': message, 'status_code': 404})
    response.status_code = 404
    return response


def error_500(request):
    message = _('Хьюстон у нас проблемы, сервер прилег!')
    response = JsonResponse(data={'message': message, 'status_code': 500})
    response.status_code = 500
    return response
