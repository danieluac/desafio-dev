from django.urls import path
from django.views.generic.base import RedirectView
from .controllers.transacao_ctrl import TransacaoController, lista_movimentosCtrl

urlpatterns = [
    path('transacao/',TransacaoController.as_view()),
    path('', RedirectView.as_view(url ='transacao/')),
    path('transacao/index', lista_movimentosCtrl)
]