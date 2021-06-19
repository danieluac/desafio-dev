from django.db import models
# Create your models here.


class Beneficiario(models.Model):
    cpf = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)

class Loja(models.Model):
    nome = models.CharField(max_length=100)
    representante_id = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)

class Movimento(models.Model):
    valor = models.FloatField()
    loja_id = models.ForeignKey(Loja, on_delete=models.CASCADE)
    data_transacao = models.DateField()
    hora_transacao = models.TimeField()
    cartao = models.CharField(max_length=50)
    TIPO = (
        ('D', 'Debito'),
        ('C', 'Credito'),
        ('B', 'Boleto'),
        ('F', 'Financiamento'),
        ('RE', 'Recebimento Empréstimo'),
        ('V', 'Vendas'),
        ('RT', 'Recebimento TED'),
        ('RD', 'Recebimento DOC'),
        ('A', 'Aluguel'),
    )
    tipo = models.CharField(choices=TIPO, max_length=2)

    def get_tipo(self, tipo, e_numero=True, indice='value'):
        tipos = []
        tipos.append({'nome': 'Debito', 'value': 'D'})
        tipos.append({'nome': 'Credito', 'value': 'C'})
        tipos.append({'nome': 'Boleto', 'value': 'B'})
        tipos.append({'nome': 'Financiamento', 'value': 'F'})
        tipos.append({'nome': 'Recebimento Empréstimo', 'value': 'RE'})
        tipos.append({'nome': 'Vendas', 'value': 'V'})
        tipos.append({'nome': 'Recebimento TED', 'value': 'RT'})
        tipos.append({'nome': 'Recebimento DOC', 'value': 'RD'})
        tipos.append({'nome': 'Aluguel', 'value': 'A'})

        if e_numero:
            return tipos[int(tipo) - 1][indice]
        elif not e_numero and type(e_numero) is str:
            valor = None
            for dado in tipos:
                if dado['value'] == tipo:
                    valor = dado[indice]
                    break
            return valor
