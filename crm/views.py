from django.shortcuts import render


def test(request):
    return render(request, 'crm/layout/base.html')
