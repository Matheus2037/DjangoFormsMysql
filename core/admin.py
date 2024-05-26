from django.contrib import admin

from .models import Produto, Venda, ItemVenda

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'slug', 'criado', 'modificado', 'ativo')

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'ativo', 'criado', 'modificado')
    search_fields = ('nome',)
    list_filter = ('ativo', 'criado', 'modificado')
    ordering = ('nome',)
    readonly_fields = ('preco', 'subtotal')

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'data', 'ativo', 'criado', 'modificado')
    search_fields = ('cliente',)
    list_filter = ('data', 'criado', 'modificado')
    ordering = ('-data',)
    inlines = [ItemVendaInline]
    readonly_fields = ('total',)

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'produto', 'quantidade', 'preco', 'subtotal', 'ativo', 'criado', 'modificado')
    search_fields = ('venda__cliente', 'produto__nome')
    list_filter = ('venda__data', 'criado', 'modificado')
    ordering = ('venda',)
