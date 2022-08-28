from django.shortcuts import render

def home(request, lang=None):
    print(lang)
    return render(request, 'home_en.html' if lang == 'en' else 'home_sv.html', {'lang': lang})

def notAMember(request, lang=None):
    return render(request, 'notAMember_en.html' if lang == 'en' else 'notAMember_sv.html', {'lang': lang})

def becomeAMember(request, lang=None):
    return render(request, 'becomeAMember_en.html' if lang == 'en' else 'becomeAMember_sv.html', {'lang': lang})
