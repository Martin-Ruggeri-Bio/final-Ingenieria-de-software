from django.views.generic import View
from django.shortcuts import render

#pagina de inicio
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, 'pages/index.html', context)
