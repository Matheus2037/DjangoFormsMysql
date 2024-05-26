from django import forms
from django.core.mail.message import EmailMessage
from .models import Produto, Venda, ItemVenda
from django.forms import inlineformset_factory


class ContatoForm(forms.Form):
    nome = forms.CharField(label='nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    assunto = forms.CharField(label='Assunto', max_length=120)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_email(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}'

        mail = EmailMessage(
            subject='E-mail enviado pelo sistema djangoM',
            body=conteudo,
            from_email='matheusdasilvagastaldi@gmail.com',
            to = ['contato@seudominio.com.br',],
            headers={'Reply-To': email}
        )
        mail.send()

class ProdutoModelForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'estoque', 'image']


class VendaModelForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

ItemVendaFormSet = inlineformset_factory(Venda, ItemVenda, form=ItemVendaForm, extra=1, can_delete=True)
