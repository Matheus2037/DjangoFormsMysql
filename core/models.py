from django.db import models
from stdimage.models import StdImageField

from django.db.models import  signals
from django.template.defaultfilters import slugify

class Base(models.Model):
    criado = models.DateField('Data de criação', auto_now_add=True)
    modificado = models.DateField('Data de modificação', auto_now_add=True)
    ativo = models.BooleanField('Ativo: ', default=True)

    class Meta:
        abstract = True


class Produto(Base):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')
    image = StdImageField('Imagem', upload_to='produtos', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.nome

def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

signals.pre_save.connect(produto_pre_save, sender=Produto)

class Venda(Base):
    cliente = models.CharField('Cliente', max_length=100)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0, blank=True, editable=False)
    data = models.DateTimeField('Data da venda', auto_now_add=True)

    def __str__(self):
        return f'Venda {self.id} - {self.cliente}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Salva a venda primeiro para obter o ID
        total = sum(item.subtotal() for item in self.itens.all())
        if self.total != total:
            self.total = total
            super().save(*args, **kwargs)


class ItemVenda(Base):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField('Quantidade')
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'

    def subtotal(self):
        return self.quantidade * self.preco

def itemvenda_pre_save(signal, instance, sender, **kwargs):
    instance.preco = instance.produto.preco

signals.pre_save.connect(itemvenda_pre_save, sender=ItemVenda)


def update_venda_total(instance, **kwargs):
    venda = instance.venda
    venda.total = sum(item.subtotal() for item in venda.itens.all())
    venda.save()

signals.post_save.connect(update_venda_total, sender=ItemVenda)
signals.post_delete.connect(update_venda_total, sender=ItemVenda)