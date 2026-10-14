from django.db import migrations, models


def associar_fotos(apps, schema_editor):
    Presente = apps.get_model("home", "Presente")
    fotos = {
        "JOGO DE PANELA": "items/jogo_de_panelas.jpg",
        "TALHERES": "items/talheres.jpeg",
        "POTES": "items/potes.jpg",
        "ROUPAS DE CAMA": "items/jogo_de_cama.jpeg",
        "TRAVESSEIROS": "items/travesseiros.jpeg",
        "SOFA": "itens/sofa.jpeg",
        "LIXO": "items/lixo_de_banheiro.jpeg",
        "Sanduicheira / Grill": "items/misteira.jpeg",
    }

    for nome, caminho in fotos.items():
        Presente.objects.filter(name=nome).update(image=caminho)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0003_import_presentes_planilha"),
    ]

    operations = [
        migrations.AddField(
            model_name="presente",
            name="image",
            field=models.ImageField(
                blank=True,
                default="",
                upload_to="items/",
                verbose_name="Foto",
            ),
        ),
        migrations.RunPython(associar_fotos, migrations.RunPython.noop),
    ]