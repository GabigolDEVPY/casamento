import json

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count

from .models import Presente, PresenteReservado, Convidado


class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = Presente.objects.filter(active=True).annotate(
            reservations_count=Count("reservations")
        )

        for item in items:
            item.available_quantity = item.quantity - item.reservations_count
            item.is_available = item.available_quantity > 0

        context["items"] = items
        context["items_json"] = json.dumps([
            {
                "id": item.id,
                "name": item.name,
                "image": item.image.url if item.image else "",
                "quantity": item.quantity,
                "reserved": item.reservations_count,
                "available": item.is_available,
            }
            for item in items
        ])

        # Sessão — presente
        context["presente_confirmado"] = self.request.session.get("presente_confirmado", False)
        context["presente_nome"] = self.request.session.get("presente_nome", "")

        return context


class ConfirmarPresenca(TemplateView):
    template_name = "home/confirmar_presenca.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["presenca_confirmada"] = self.request.session.get("presenca_confirmada", False)
        context["convidado_nome"] = self.request.session.get("convidado_nome", "")
        return context


def confirmar_presenca(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Método não permitido."},
            status=405,
        )

    if request.session.get("presenca_confirmada"):
        return JsonResponse({
            "success": True,
            "already_confirmed": True,
            "message": "Você já confirmou sua presença!",
            "guest_name": request.session.get("convidado_nome", ""),
        })

    nome = request.POST.get("nome", "").strip()
    telefone = request.POST.get("telefone", "").strip()

    if not nome or not telefone:
        return JsonResponse(
            {"success": False, "message": "Preencha seu nome e telefone."},
            status=400,
        )

    Convidado.objects.create(nome=nome, telefone=telefone)

    request.session["presenca_confirmada"] = True
    request.session["convidado_nome"] = nome
    request.session.set_expiry(200 * 24 * 60 * 60)  # ~200 dias

    return JsonResponse({
        "success": True,
        "already_confirmed": False,
        "message": "Presença confirmada!",
        "guest_name": nome,
    })


def confirmar_presente(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Método não permitido."},
            status=405,
        )

    if request.session.get("presente_confirmado"):
        return JsonResponse({
            "success": True,
            "already_confirmed": True,
            "message": "Você já confirmou um presente. Muito obrigado!",
            "guest_name": request.session.get("convidado_nome", ""),
            "gift_name": request.session.get("presente_nome", ""),
        })

    nome = request.POST.get("nome", "").strip()
    telefone = request.POST.get("telefone", "").strip()
    item_id = request.POST.get("presente")

    if not nome or not telefone or not item_id:
        return JsonResponse(
            {"success": False, "message": "Preencha seu nome, telefone e escolha um presente."},
            status=400,
        )

    item = Presente.objects.filter(id=item_id).first()
    if item is None:
        return JsonResponse(
            {"success": False, "message": "Presente não encontrado."},
            status=404,
        )

    current_reservations = item.reservations.count()

    if current_reservations >= item.quantity or not item.active:
        return JsonResponse(
            {"success": False, "message": "Desculpe, este presente já foi escolhido por todas as pessoas possíveis."},
            status=409,
        )

    PresenteReservado.objects.create(
        presente=item,
        guest_name=nome,
        guest_phone=telefone,
    )

    request.session["presente_confirmado"] = True
    request.session["presente_nome"] = item.name
    request.session["convidado_nome"] = nome
    request.session.set_expiry(200 * 24 * 60 * 60)

    return JsonResponse({
        "success": True,
        "already_confirmed": False,
        "message": "Presente confirmado!",
        "guest_name": nome,
        "gift_name": item.name,
    })
