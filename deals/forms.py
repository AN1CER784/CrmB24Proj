from django import forms

BITRIX_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

CURRENCY_CHOICES = [
    ("RUB", "Рубль"),
    ("USD", "Доллар США"),
    ("EUR", "Евро"),
]
DEAL_TYPE_CHOICES = (
    ("SALE", "Продажа"),
    ("REPEAT", "Повторная продажа"),
    ("SERVICES", "Услуги"),
    ("GOODS", "Товары"),
    ("PARTNER", "Партнёрская"),
)


class DealCreateForm(forms.Form):
    TITLE = forms.CharField(label="Наименование", max_length=255)

    CURRENCY_ID = forms.ChoiceField(
        label="Валюта",
        choices=CURRENCY_CHOICES,
        initial="RUB",
    )

    OPPORTUNITY = forms.DecimalField(
        label="Сумма",
        max_digits=14,
        decimal_places=2,
        min_value=0,
        required=False,
    )

    BEGINDATE = forms.DateTimeField(
        label="Начало",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        required=False,
    )

    CLOSEDATE = forms.DateTimeField(
        label="Конец",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        required=False,
    )

    TYPE_ID = forms.ChoiceField(
        label="Тип сделки (TYPE_ID)",
        choices=DEAL_TYPE_CHOICES,
        required=False,
        initial="SALE",
    )

    COMMENTS = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(),
        required=False,
    )

    UF_CRM_1759862274 = forms.CharField(
        label="Адрес компании",
        required=False,
    )
