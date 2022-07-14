from django.shortcuts import render

def home(request, lang=None):
    print(lang)
    return render(request, 'home_en.html' if lang == 'en' else 'home_sv.html', {'lang': lang})

def notAMember(request, lang=None):
    return render(request, 'notAMember.html', {lang: lang})

