from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.core.files.uploadedfile import InMemoryUploadedFile
from transacao.models import Loja, Movimento

from transacao.funcoes_extras import calcula_saldo_total_existente


class TransacaoController(View):
    template_name = 'transacao-create.html'

    def get(self, request, *args, **kwargs):
        if 'error_message' in request.session:
            error_message = request.session['error_message']
            del request.session['error_message']
        else:
            error_message = False

        if 'success_message' in request.session:
            success_message = request.session['success_message']
            del request.session['success_message']
        else:
            success_message = False

        context = {
            'error_msg': error_message,
            'success_message': success_message
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            file_cnab = request.FILES['file_cnab']
            if not isinstance(file_cnab, InMemoryUploadedFile) or not file_cnab.name.endswith(
                    '.txt') or file_cnab.content_type != 'text/plain':
                request.session['error_message'] = 'Deve adicionar um ficheiro CNAB válido...'
                return HttpResponseBadRequest('Deve adicionar um ficheiro CNAB válido... <a href="/">clique aqui</a>')

            # Movimento.objects.all().delete()
            # Loja.objects.all().delete()
            if self.salvar_dados(self.normaliza_dados(file_cnab)):
                request.session['success_message'] = 'ficheiro carregado e parseado com sucesso...'
            else:
                request.session['error_message'] = 'Deve adicionar um ficheiro CNAB válido...'

        return HttpResponseRedirect('/transacao')

    def normaliza_dados(self, ficheiro):
        """ Este metódo normaliza os dados recebidos de um ficheiro CNAB,
        organiza-os em um formato de fácil entendimento e retorna uma lista dessses dados
        """
        dados = []
        if isinstance(ficheiro, InMemoryUploadedFile):
            for linha in ficheiro.readlines():
                texto = linha.decode('utf-8')
                dados.append({
                    'tipo': texto[0:1],
                    'data': texto[1:9][0:4] + "-" + texto[1:9][4:6] + "-" + texto[1:9][6:8],
                    'valor': texto[9:19],
                    'cpf': texto[19:30],
                    'cartao': texto[30:42],
                    'hora': texto[42:48][0:2] + ":" + texto[42:48][2:4] + ":" + texto[42:48][4:6],
                    'dono_loja': texto[48:62],
                    'loja': texto[62:81],
                })
        return dados

    def salvar_dados(self, dados):
        """Este metódo salva os movimentos no banco de dados a quando a importação de um ficheiro CNAB
             dados = {
                'tipo': '1',
                'data': '2021-06-19',
                'valor': 123.45,
                'cpf': 12394320548,
                'cartao': '32023***2333',
                'hora': '12:30:00',
                'dono_loja': 'exemplo daniel u ac',
                'loja': 'Exemplo U AC',
            }
        """
        for dado in dados:
            loja_id = None
            try:
                loja_id = Loja.objects.get(cpf=dado['cpf'])
            except:
                pass
            if not loja_id:
                loja = Loja()
                loja.representante = dado['dono_loja']
                loja.cpf = dado['cpf']
                loja.nome = dado['loja']
                loja.save()
                loja_id = Loja.objects.get(cpf=dado['cpf'])

            try:
                saldo = format((float(dado['valor']) / 100.00), '.2f')
                movimento = Movimento()
                movimento.valor = saldo
                movimento.saldo_actual = format(movimento.calcula_saldo_importado(loja_id.id, saldo, dado['tipo']),
                                                '.2f')
                movimento.loja_id = loja_id
                movimento.cartao = dado['cartao']
                movimento.tipo = movimento.get_tipo(dado['tipo'])
                movimento.data_transacao = dado['data']
                movimento.hora_transacao = dado['hora']
                movimento.save()
            except ValueError:
                return False
        return True



def lista_movimentosCtrl(request):
    """ permite listar movimento de loja por loja e de todas as lojas"""
    if 'loja_id' in request.GET and request.GET['loja_id'] != 'ALL':
        movimentos = Movimento.objects.filter(loja_id=request.GET['loja_id'])
        total = calcula_saldo_total_existente(movimentos)
    else:
        movimentos = Movimento.objects.all()
        total = False

    context = {
        'movimentos': movimentos,
        'lojas': Loja.objects.all(),
        'total': format(total, '.2f') if total is not False else False,
        "default_loja_id": 'All' if not 'loja_id' in request.GET or ('loja_id' in request.GET and request.GET['loja_id'] == 'ALL') else int(request.GET['loja_id'])
    }
    return render(request, "transacao-lista.html", context)
