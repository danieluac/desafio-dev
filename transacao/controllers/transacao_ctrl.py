from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

class TransacaoController(View):
    template_name = 'transacao-create.html'

    def get (self, request, *args, **kwargs):
        context = {

        }
        return render(request, self.template_name, context)

    def post (self, request, *args, **kwargs):
        return HttpResponseRedirect('/')


