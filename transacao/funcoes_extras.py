
def calcula_saldo_total_existente(movimentos):
    """ Este método calcula o saldo currente total existente em movimento, de todas as lojas ou por loja """
    saldo_actual = 0
    if movimentos:
        for movimento in movimentos:
            if movimento.tipo in ('D', 'C', 'RE', 'V', 'RT', 'RD'):
                saldo_actual = saldo_actual + float(movimento.valor)
            elif movimento.tipo in ('B', 'F', 'A'):
                saldo_actual = saldo_actual - float(movimento.valor)

    return saldo_actual
