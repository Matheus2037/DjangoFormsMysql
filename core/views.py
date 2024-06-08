from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .forms import ContatoForm, ProdutoModelForm, VendaModelForm, ItemVendaFormSet
from django.contrib import messages
from django.http import JsonResponse
from .models import Produto, Venda, ItemVenda
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum, F, ExpressionWrapper, DecimalField
import pandas as pd
import xlsxwriter
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template



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

def venda(request):
    return render(request, 'venda.html')

def criar_venda(request):
    if request.method == 'POST':
        venda_form = VendaModelForm(request.POST)
        item_venda_formset = ItemVendaFormSet(request.POST, instance=Venda())

        if venda_form.is_valid() and item_venda_formset.is_valid():
            venda = venda_form.save()
            itens_venda = item_venda_formset.save(commit=False)
            for item in itens_venda:
                item.venda = venda
                item.save()
            messages.success(request, 'Venda criada com sucesso!')
            return redirect('criar_venda')  # Redireciona para a mesma página para novo cadastro

    else:
        venda_form = VendaModelForm()
        item_venda_formset = ItemVendaFormSet()

    context = {
        'venda_form': venda_form,
        'item_venda_formset': item_venda_formset,
    }
    return render(request, 'venda/criar_venda.html', context)

def venda(request):
    vendas = Venda.objects.all()

    # Converter os dados das vendas em um DataFrame pandas
    vendas_df = pd.DataFrame(list(vendas.values()))

    if 'data' in vendas_df.columns:
        vendas_df = vendas_df.drop(columns=['data'])

    # Renderizar o DataFrame pandas como uma tabela HTML
    tabela_html = vendas_df.to_html(index=False, classes='table table-striped')

    return render(request, 'venda.html', {'tabela_html': tabela_html})



def relatorio(request):
    return render(request, 'relatorio.html')

def get_relatorio_cliente(request):
    # Agrupar vendas por cliente e calcular a quantidade de vendas e valor total
    vendas_agrupadas = Venda.objects.values('cliente').annotate(
        quantidade_vendas=Count('id'),
        valor_total=Sum('total'),
    )

    # Converter os dados para um DataFrame pandas
    df_clientes = pd.DataFrame(list(vendas_agrupadas))

    # Renderizar o DataFrame pandas como uma tabela HTML
    tabela_html = df_clientes.to_html(index=False, classes='table table-striped')

    return JsonResponse({'tabela_html': tabela_html})

def get_relatorio_produto(request):
    # Agrupar itens de venda por produto e calcular a quantidade total e valor total
    itens_agrupados = ItemVenda.objects.values('produto__nome').annotate(
        quantidade_total=Sum('quantidade'),
        valor_total=Sum(ExpressionWrapper(F('quantidade') * F('preco'), output_field=DecimalField(max_digits=10, decimal_places=2)))
    )

    # Converter os dados para um DataFrame pandas
    df_produtos = pd.DataFrame(list(itens_agrupados))

    # Renderizar o DataFrame pandas como uma tabela HTML
    tabela_html = df_produtos.to_html(index=False, classes='table table-striped')

    return JsonResponse({'tabela_html': tabela_html})


def exportar_relatorio_excel(request, tipo):
    if tipo == 'cliente':
        vendas_agrupadas = Venda.objects.values('cliente').annotate(
            quantidade_vendas=Count('id'),
            valor_total=Sum('total'),
        )
        df = pd.DataFrame(list(vendas_agrupadas))
    elif tipo == 'produto':
        itens_agrupados = ItemVenda.objects.values('produto__nome').annotate(
            quantidade_total=Sum('quantidade'),
            valor_total=Sum(ExpressionWrapper(F('quantidade') * F('preco'), output_field=DecimalField(max_digits=10, decimal_places=2)))
        )
        df = pd.DataFrame(list(itens_agrupados))

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Relatorio')
    writer.close()  # Feche o ExcelWriter para salvar o arquivo no buffer
    output.seek(0)  # Mova o cursor para o início do buffer

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=relatorio_{tipo}.xlsx'
    return response

def exportar_relatorio_pdf(request, tipo):
    if tipo == 'cliente':
        vendas_agrupadas = Venda.objects.values('cliente').annotate(
            quantidade_vendas=Count('id'),
            valor_total=Sum('total'),
        )
        df = pd.DataFrame(list(vendas_agrupadas))
    elif tipo == 'produto':
        itens_agrupados = ItemVenda.objects.values('produto__nome').annotate(
            quantidade_total=Sum('quantidade'),
            valor_total=Sum(ExpressionWrapper(F('quantidade') * F('preco'), output_field=DecimalField(max_digits=10, decimal_places=2)))
        )
        df = pd.DataFrame(list(itens_agrupados))

    template_path = 'relatorio_pdf.html'
    context = {'data': df.to_dict(orient='records')}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=relatorio_{tipo}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
