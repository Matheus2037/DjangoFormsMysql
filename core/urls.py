from django.urls import path
from .views import index, contato, produto, deletar_produto, editar_produto, venda, criar_venda

urlpatterns = [
    path('', index, name='index'),
    path('contato/', contato, name='contato'),
    path('produto/', produto, name='produto'),
    path('deletar_produto/<int:product_id>/', deletar_produto, name='deletar_produto'),
    path('editar_produto/<int:produto_id>/', editar_produto, name='editar_produto'),
    path('venda/', venda, name='venda'),
    path('venda/nova/', criar_venda, name='criar_venda'),
]
