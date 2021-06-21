from django.db import models
# Create your models here.



class Loja(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, null=True)
    representante = models.CharField(max_length=100, null=True)

class Movimento(models.Model):
    valor = models.FloatField()
    saldo_actual = models.FloatField(null=True)
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
        """ Este método recupera o tipo da transação ao se efectuar um movimento ou consulta de movimento """
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
    def calcula_saldo_importado(self,loja_id, saldo, operacao):
        """ Este método calcula o saldo actual, ao cadastrar um movimento vindo de um ficheiro CNAB"""
        try:
            movimento = Movimento.objects.filter(loja_id=loja_id).order_by('-id')[0]
        except:
            movimento = None
        saldo_actual = 0
        if movimento:
            if self.get_tipo(operacao) in ('D', 'C', 'RE', 'V', 'RT', 'RD'):
                saldo_actual = movimento.saldo_actual + float(saldo)
            elif self.get_tipo(operacao) in ('B', 'F', 'A'):
                saldo_actual = movimento.saldo_actual - float(saldo)
        else:
            if self.get_tipo(operacao) in ('D', 'C', 'RE', 'V', 'RT', 'RD'):
                saldo_actual = float(saldo)
            elif self.get_tipo(operacao) in ('B', 'F', 'A'):
                saldo_actual = - float(saldo)

        return saldo_actual

    # def calcula_saldo_total_existente(self, loja = 'ALL'):
    #     """ Este método calcula o saldo currente total existente em movimento, de todas as lojas ou por loja """
    #     if loja is not 'ALL':
    #         movimentos = Movimento.objects.get(loja_id = loja)
    #     else:
    #         movimentos = Movimento.objects.all()
    #
    #     saldo_actual = 0
    #     if movimentos:
    #         for movimento in movimentos:
    #             if movimento.tipo in ('D', 'C', 'RE', 'V', 'RT', 'RD'):
    #                 saldo_actual = saldo_actual + float(movimento.valor)
    #             elif movimento.tipo in ('B', 'F', 'A'):
    #                 saldo_actual = saldo_actual - float(movimento.valor)
    #
    #     return saldo_actual
