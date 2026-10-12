from django.db import models


class Presente(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade total")
    active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Presente"
        verbose_name_plural = "Presentes"

    def __str__(self):
        return self.name


class PresenteReservado(models.Model):
    presente = models.ForeignKey(
        Presente, on_delete=models.CASCADE, related_name="reservations"
    )
    guest_name = models.CharField(max_length=200, verbose_name="Nome do convidado")
    guest_phone = models.CharField(max_length=20, verbose_name="Telefone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    class Meta:
        verbose_name = "Presente reservado"
        verbose_name_plural = "Presentes reservados"

    def __str__(self):
        return f"{self.guest_name} reservou {self.presente.name}"


class Convidado(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    confirmado_em = models.DateTimeField(auto_now_add=True, verbose_name="Confirmado em")

    class Meta:
        verbose_name = "Convidado"
        verbose_name_plural = "Convidados"

    def __str__(self):
        return self.nome
