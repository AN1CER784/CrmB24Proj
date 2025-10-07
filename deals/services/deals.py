from typing import Any, Dict, List

# Какие поля берём у сделки из Bitrix
_SELECT_FIELDS = [
    "ID", "TITLE", "CURRENCY_ID", "OPPORTUNITY", "STAGE_ID",
    "TYPE_ID", "BEGINDATE", "CLOSEDATE", "LAST_ACTIVITY_TIME", "UF_CRM_1759862274"
]

# Человеческие заголовки столбцов для шаблона
_LABELS = {
    "ID": "ID",
    "TITLE": "Наименование",
    "CURRENCY_ID": "Валюта",
    "OPPORTUNITY": "Сумма",
    "STAGE_ID": "Статус",
    "TYPE_ID": "Тип сделки",
    "BEGINDATE": "Начало",
    "CLOSEDATE": "Конец",
    "UF_CRM_1759862274": "Адрес компании"
}


def _label_order() -> List[str]:
    # Порядок вывода в таблицу (без тех. поля сортировки)
    return [k for k in _SELECT_FIELDS if k != "LAST_ACTIVITY_TIME"]


def list_last_deals(
        token: Any,
        *,
        limit: int = 10,
        only_active: bool = True,
        assigned_to_me: bool = True,
) -> Dict[str, Any]:
    """
    Возвращает последнии сделки табличкой:
    {
      "fields": ["ID","Наименование",...],
      "rows": [ [..значения..], ... ]
    }
    """
    _filter: Dict[str, Any] = {}
    if only_active:
        _filter["CLOSED"] = "N"

    if assigned_to_me:
        me = token.call_api_method("user.current")["result"]
        _filter["ASSIGNED_BY_ID"] = me["ID"]

    payload = {
        "filter": _filter,
        "order": {"LAST_ACTIVITY_TIME": "DESC"},
        "select": _SELECT_FIELDS,
        "start": 0,
    }
    res = token.call_api_method("crm.deal.list", params=payload)
    items: List[Dict[str, Any]] = res.get("result", [])

    items = items[:limit]
    # Готовим табличку для шаблона
    header_keys = _label_order()
    fields = [_LABELS[k] for k in header_keys]
    rows: List[List[Any]] = [[deal.get(k) for k in header_keys] for deal in items]

    return {"fields": fields, "rows": rows}
