# Generated by Django 4.1 on 2024-05-18 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Data de criação')),
                ('modificado', models.DateField(auto_now_add=True, verbose_name='Data de modificação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo: ')),
                ('cliente', models.CharField(max_length=100, verbose_name='Cliente')),
                ('total', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, verbose_name='Total')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da venda')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Data de criação')),
                ('modificado', models.DateField(auto_now_add=True, verbose_name='Data de modificação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo: ')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.produto')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='core.venda')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
