from django.contrib import admin
from .models import Presente, PresenteReservado, Convidado


@admin.register(Presente)
class PresenteAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "active")
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(PresenteReservado)
class PresenteReservadoAdmin(admin.ModelAdmin):
    list_display = ("presente", "guest_name", "guest_phone", "created_at")
    list_filter = ("presente", "created_at")
    search_fields = ("guest_name", "guest_phone")


@admin.register(Convidado)
class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "confirmado_em")
    list_filter = ("confirmado_em",)
    search_fields = ("nome", "telefone")
