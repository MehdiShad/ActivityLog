from typing import Optional
from django.db.models import QuerySet
from activity_log.activity.models import Item
from activity_log.activity.filters.item import ItemsFiter


def get_item(item_id: int) -> Optional[Item]:
    try:
        return Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return None


def get_filtered_items(*, filters=None) -> QuerySet[Item]:
    filters = filters or {}
    qs = Item.objects.filter().order_by('-id')
    return ItemsFiter(filters, qs).qs
