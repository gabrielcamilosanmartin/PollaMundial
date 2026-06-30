from django.db import migrations

COUNTRIES = [
    ("Mexico", "México"),
    ("South Korea", "Corea del Sur"),
    ("Czech Republic", "República Checa"),
    ("South Africa", "Sudáfrica"),
    ("Canada", "Canadá"),
    ("Qatar", "Catar"),
    ("Switzerland", "Suiza"),
    ("Bosnia & Herzegovina", "Bosnia y Herzegovina"),
    ("Brazil", "Brasil"),
    ("Haiti", "Haití"),
    ("Scotland", "Escocia"),
    ("Morocco", "Marruecos"),
    ("USA", "Estados Unidos"),
    ("Australia", "Australia"),
    ("Turkey", "Turquía"),
    ("Paraguay", "Paraguay"),
    ("Germany", "Alemania"),
    ("Ivory Coast", "Costa de Marfil"),
    ("Ecuador", "Ecuador"),
    ("Curaçao", "Curaçao"),
    ("Netherlands", "Países Bajos"),
    ("Sweden", "Suecia"),
    ("Tunisia", "Túnez"),
    ("Japan", "Japón"),
    ("Belgium", "Bélgica"),
    ("Iran", "Irán"),
    ("New Zealand", "Nueva Zelanda"),
    ("Egypt", "Egipto"),
    ("Spain", "España"),
    ("Saudi Arabia", "Arabia Saudita"),
    ("Uruguay", "Uruguay"),
    ("Cape Verde", "Cabo Verde"),
    ("France", "Francia"),
    ("Iraq", "Irak"),
    ("Norway", "Noruega"),
    ("Senegal", "Senegal"),
    ("Argentina", "Argentina"),
    ("Austria", "Austria"),
    ("Jordan", "Jordania"),
    ("Algeria", "Argelia"),
    ("Portugal", "Portugal"),
    ("Uzbekistan", "Uzbekistán"),
    ("Colombia", "Colombia"),
    ("DR Congo", "República Democrática del Congo"),
    ("England", "Inglaterra"),
    ("Ghana", "Ghana"),
    ("Panama", "Panamá"),
    ("Croatia", "Croacia"),
]


def add_countries(apps, schema_editor):
    Country = apps.get_model("countries", "Country")
    for code, name in COUNTRIES:
        Country.objects.update_or_create(code=code, defaults={"name": name})


def remove_countries(apps, schema_editor):
    Country = apps.get_model("countries", "Country")
    Country.objects.filter(code__in=[code for code, _ in COUNTRIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("countries", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_countries, remove_countries),
    ]
