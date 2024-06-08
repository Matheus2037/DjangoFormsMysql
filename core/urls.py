from django.urls import path
from .views import index, contato, produto, deletar_produto, editar_produto, venda, criar_venda, relatorio, get_relatorio_cliente, get_relatorio_produto

urlpatterns = [
    path('', index, name='index'),
    path('contato/', contato, name='contato'),
    path('produto/', produto, name='produto'),
    path('deletar_produto/<int:product_id>/', deletar_produto, name='deletar_produto'),
    path('editar_produto/<int:produto_id>/', editar_produto, name='editar_produto'),
    path('venda/', venda, name='venda'),
    path('venda/nova/', criar_venda, name='criar_venda'),
    path('relatorio/', relatorio, name='relatorio'),
    path('relatorio/cliente/', get_relatorio_cliente, name='get_relatorio_cliente'),
    path('relatorio/produto/', get_relatorio_produto, name='get_relatorio_produto'),
]
