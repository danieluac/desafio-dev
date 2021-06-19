from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.core.files.uploadedfile import InMemoryUploadedFile
from transacao.models import Loja, Movimento


class TransacaoController(View):
    template_name = 'transacao-create.html'

    def get(self, request, *args, **kwargs):
        context = {
            'datas': []
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            file_cnab = request.FILES['file_cnab']
            if not isinstance(file_cnab, InMemoryUploadedFile) or not file_cnab.name.endswith(
                    '.txt') or file_cnab.content_type != 'text/plain':
                raise Exception("faça correctamente o carregamento do ficheiro CNAB.txt")
            transacao_data = self.normaliza_dados(file_cnab)
            Movimento.objects.all().delete()
            Loja.objects.all().delete()
            self.salvar_dados(transacao_data)

        context = {
            'movimentos': Movimento.objects.all(),
            'lojas': Loja.objects.all(),
            'self_ctrl': self
        }
        return render(request, self.template_name, context)

    def normaliza_dados(self, ficheiro):
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
                loja_id = Loja.objects.last()

            movimento = Movimento()
            # normaliza o valor recebido
            saldo = (float(dado['valor']) / 100.00)
            movimento.valor = saldo
            movimento.saldo_actual = movimento.calcula_saldo(saldo, dado['tipo'])
            movimento.loja_id = loja_id
            movimento.cartao = dado['cartao']
            movimento.tipo = movimento.get_tipo(dado['tipo'])
            movimento.data_transacao = dado['data']
            movimento.hora_transacao = dado['hora']
            movimento.save()

