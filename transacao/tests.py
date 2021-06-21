from django.test import TestCase, Client
from transacao.models import Loja, Movimento
from django.conf import settings
from datetime import datetime
import os
# Create your tests here.

class MovimentoFinanceiroTestCase(TestCase):
    def setUp(self):
        Loja.objects.create(nome='Loja 1 test', cpf=12333291, representante='Daniel Garcia')
        Movimento.objects.create(
            loja_id=Loja.objects.last(),
            valor=123.20,
            saldo_actual=(0-123.20),
            tipo='B',
            cartao='12121****1212',
            data_transacao=datetime.now().date(),
            hora_transacao=datetime.now().time()
        )

    def test_cadastro_de_movimento(self):
        """Testa o cadastro de um movimento financeiro"""
        movimento = Movimento.objects.last()
        self.assertEqual(movimento.valor, 123.20)
        self.assertEqual(movimento.saldo_actual, -123.20)

class RequestTestCase(TestCase):
    resposta, reposta_upload_ficheiro = None, None
    def setUp(self):
        cliente = Client()
        self.resposta = cliente.get('/transacao/')

        with open(os.path.join(settings.BASE_DIR, 'CNAB.txt'), 'rb') as file_cnab:
            print(file_cnab)
            self.reposta_upload_ficheiro = cliente.post('/transacao/', {'file_cnab': file_cnab})

    def test_get_status_code(self):
        """Verifica o status code da resposta da requisição"""
        self.assertEqual(self.resposta.status_code, 200)

    def test_file_upload(self):
        """Verifica se o upload de ficheiro ocorreu com sucesso"""
        if self.reposta_upload_ficheiro.status_code == 400:
            self.assertEqual(self.reposta_upload_ficheiro.content, bytes('Deve adicionar um ficheiro CNAB válido... <a href="/">clique aqui</a>', 'utf-8'))
        else:
            self.assertEqual(self.reposta_upload_ficheiro.status_code, 302)


