from django.db import migrations


def seed_presentes(apps, schema_editor):
    Presente = apps.get_model('home', 'Presente')

    initial_gifts = [
        {"name": "Jogo de Panelas Antiaderente", "quantity": 3},
        {"name": "Liquidificador", "quantity": 2},
        {"name": "Jogo de Toalhas de Banho", "quantity": 5},
        {"name": "Aspirador de Pó", "quantity": 2},
        {"name": "Jogo de Lençol Casal", "quantity": 3},
        {"name": "Ferro de Passar a Vapor", "quantity": 2},
        {"name": "Jogo de Jantar 18 Peças", "quantity": 2},
        {"name": "Cafeteira Elétrica", "quantity": 2},
        {"name": "Sanduicheira / Grill", "quantity": 1},
        {"name": "Jogo de Copos (6 Peças)", "quantity": 4},
        {"name": "Air Fryer", "quantity": 2},
        {"name": "Mixer / Processador", "quantity": 2},
    ]

    for item in initial_gifts:
        Presente.objects.get_or_create(
            name=item["name"],
            defaults={"quantity": item["quantity"], "active": True}
        )


def unseed_presentes(apps, schema_editor):
    Presente = apps.get_model('home', 'Presente')
    Presente.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_presentes, unseed_presentes),
    ]
