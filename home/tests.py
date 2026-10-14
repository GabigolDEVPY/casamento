import json

from django.test import Client, TestCase
from django.urls import reverse

from .models import Presente


class PresenteTests(TestCase):
	def setUp(self):
		self.presente = Presente.objects.create(
			name="Jogo de teste",
			image="items/jogo-de-teste.jpg",
		)

	def test_home_includes_image_url_for_gift(self):
		response = self.client.get(reverse("home:home"))

		presentes = json.loads(response.context["items_json"])
		presente = next(item for item in presentes if item["name"] == "Jogo de teste")

		self.assertEqual(presente["image"], "/media/items/jogo-de-teste.jpg")
		self.assertContains(response, "/media/items/jogo-de-teste.jpg")

	def test_last_unit_cannot_be_reserved_twice(self):
		dados = {
			"nome": "Convidado de teste",
			"telefone": "31999999999",
			"presente": self.presente.pk,
		}
		primeira_reserva = Client().post(reverse("home:confirmar_presente"), dados)
		segunda_reserva = Client().post(reverse("home:confirmar_presente"), dados)

		self.assertEqual(primeira_reserva.status_code, 200)
		self.assertEqual(segunda_reserva.status_code, 409)
		self.assertEqual(self.presente.reservations.count(), 1)

		response = self.client.get(reverse("home:home"))
		presentes = json.loads(response.context["items_json"])
		presente = next(item for item in presentes if item["name"] == "Jogo de teste")
		self.assertFalse(presente["available"])
