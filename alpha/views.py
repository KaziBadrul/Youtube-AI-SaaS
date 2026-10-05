from django.http import JsonResponse
from django.views.decorators.http import require_safe

@require_safe
def health(request):
    """Liveness only: no database, provider, media or production execution."""
    return JsonResponse({"status": "ok"})
