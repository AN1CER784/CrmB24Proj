from django.shortcuts import render, redirect

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .forms import DealCreateForm
from .services.deals import list_last_deals


@main_auth(on_cookies=True)
def last_deals(request):
    token = request.bitrix_user_token
    try:
        table = list_last_deals(
            token,
            limit=10,
            only_active=True,
            assigned_to_me=True,
        )
        context = {"fields": table["fields"], "deals": table["rows"]}
    except Exception as e:
        context = {"fields": [], "deals": [], "error": str(e)}
    return render(request, "deals/last_deals.html", context)


@main_auth(on_cookies=True)
def add_deal(request):
    token = request.bitrix_user_token
    form = DealCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            token.call_api_method('crm.deal.add', {"fields": form.cleaned_data})
            return redirect("deals:last_deals")
    return render(request, 'deals/add_deal.html', context={"form": form})
