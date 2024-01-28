from django.shortcuts import render
from .forms import ContatoForm, ProdutoModelForm
from django.contrib import messages
from .models import Produto
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def index(request):
    search_query = request.GET.get('q')

    if search_query:
        produtos = Produto.objects.filter(Q(id__icontains=search_query) | Q(nome__icontains=search_query)).order_by('id')

    else:
        produto_list = Produto.objects.order_by('id')
        paginator = Paginator(produto_list, 10)  # Dividir a lista em páginas de 10 produtos cada

        page = request.GET.get('page')
        try:
            produtos = paginator.page(page)
        except PageNotAnInteger:
            # Se 'page' não for um número inteiro, exibir a primeira página
            produtos = paginator.page(1)
        except EmptyPage:
            # Se 'page' estiver fora do intervalo, exibir a última página de resultados
            produtos = paginator.page(paginator.num_pages)

    form = ProdutoModelForm()

    context = {
        'produtos': produtos,
        'form': form,
        'search_query': search_query,
    }
    return render(request, 'index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_email()

            messages.success(request, 'Email enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')

    context = {
        'form': form
    }
    return render(request, 'contato.html', context)


def produto(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto salvo com sucesso!')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar produto!')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form
        }
        return render(request, 'produto.html', context)

    else:
        return redirect('index')

def deletar_produto(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Produto, pk=product_id)
        product.delete()
        return redirect('index')
    else:
        return HttpResponse("Método não permitido")

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == 'POST':
        form = ProdutoModelForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProdutoModelForm(instance=produto)
    return render(request, 'index', {'form': form, 'produto': produto})