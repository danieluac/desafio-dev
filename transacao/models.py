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
