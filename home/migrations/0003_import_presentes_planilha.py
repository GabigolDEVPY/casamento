from django.db import migrations


def importar_presentes(apps, schema_editor):
    Presente = apps.get_model("home", "Presente")
    presentes = [
        "JOGO DE PANELA",
        "TALHERES",
        "POTES",
        "ESCORREDOR DE VASILHAS",
        "FILTRO DE ÁGUA",
        "CAMA",
        "GUARDA-ROUPA",
        "CORTINAS",
        "ROUPAS DE CAMA",
        "TRAVESSEIROS",
        "SOFA",
        "CORTINA",
        "LIXO",
    ]

    for nome in presentes:
        Presente.objects.update_or_create(
            name=nome,
            defaults={"quantity": 1, "active": True},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0002_seed_presentes"),
    ]

    operations = [
        migrations.RunPython(importar_presentes, migrations.RunPython.noop),
    ]