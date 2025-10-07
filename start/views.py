import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


def _has_install_payload(request) -> bool:
    """Определяем, что это первичный install-пост с токенами."""
    if request.method != "POST":
        return False
    f = request.POST
    if any(k in f for k in ("AUTH_ID", "auth[access_token]", "access_token")):
        return True

    try:
        if request.content_type and "application/json" in request.content_type:
            data = json.loads(request.body.decode("utf-8") or "{}")
            if any(k in data for k in ("AUTH_ID", "auth[access_token]", "access_token")):
                return True
    except Exception:
        pass
    return False


# Внутренний обработчик ТОЛЬКО для первого входа
@main_auth(on_start=True, set_cookie=True)
def _index_install(request):
    return render(request, "start/index.html", locals())


# Внутренний обработчик для обычных заходов
@main_auth(on_cookies=True)
def _index_cookies(request):
    return render(request, "start/index.html", locals())


@csrf_exempt
def index(request):
    if _has_install_payload(request):
        return _index_install(request)
    return _index_cookies(request)
