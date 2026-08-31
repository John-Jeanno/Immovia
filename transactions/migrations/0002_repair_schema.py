import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('clients', '0001_initial'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "ALTER TABLE transactions_dossiertransaction ADD COLUMN titre varchar(200) NOT NULL DEFAULT ''",
                "ALTER TABLE transactions_dossiertransaction ADD COLUMN montant decimal NOT NULL DEFAULT 0",
                "ALTER TABLE transactions_dossiertransaction ADD COLUMN client_id bigint NULL REFERENCES clients_client(id)",
            ],
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='dossiertransaction',
                    name='titre',
                    field=models.CharField(default='', max_length=200),
                ),
                migrations.AddField(
                    model_name='dossiertransaction',
                    name='montant',
                    field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                migrations.AddField(
                    model_name='dossiertransaction',
                    name='client',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='clients.client',
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]