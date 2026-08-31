from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('chantiers', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "ALTER TABLE chantiers_chantier ADD COLUMN adresse varchar(200) NOT NULL DEFAULT ''",
                "ALTER TABLE chantiers_chantier ADD COLUMN budget_depense decimal NOT NULL DEFAULT 0",
                "ALTER TABLE chantiers_chantier ADD COLUMN pourcentage_avancement integer NOT NULL DEFAULT 0",
                "ALTER TABLE chantiers_chantier ADD COLUMN etat_chantier varchar(20) NOT NULL DEFAULT 'planifie'",
                "ALTER TABLE chantiers_chantier ADD COLUMN date_creation datetime NOT NULL DEFAULT CURRENT_TIMESTAMP",
            ],
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='chantier',
                    name='adresse',
                    field=models.CharField(blank=True, default='', max_length=200),
                ),
                migrations.AddField(
                    model_name='chantier',
                    name='budget_depense',
                    field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                migrations.AddField(
                    model_name='chantier',
                    name='pourcentage_avancement',
                    field=models.IntegerField(default=0),
                ),
                migrations.AddField(
                    model_name='chantier',
                    name='etat_chantier',
                    field=models.CharField(
                        choices=[
                            ('planifie', 'Planifié'),
                            ('preparation', 'Préparation'),
                            ('en_cours', 'En cours'),
                            ('finition', 'Finition'),
                            ('termine', 'Terminé'),
                            ('livre', 'Livré'),
                            ('en_retard', 'En retard'),
                        ],
                        default='planifie',
                        max_length=20,
                    ),
                ),
                migrations.AddField(
                    model_name='chantier',
                    name='date_creation',
                    field=models.DateTimeField(auto_now_add=True),
                ),
            ],
            database_operations=[],
        ),
    ]