from django.shortcuts import render
from django.contrib.auth.models import User
from User.models import Userprofile
from django.db.utils import IntegrityError

def emigrate_db():

    for userprofile in Userprofile.objects.all().reverse():
        try:
            if userprofile.ltu_id and userprofile.ltu_id != '':
                ltu_id = userprofile.ltu_id.lower()
                ltu_id = ltu_id.replace('@student.ltu.se', '')

                userprofile.user.username = ltu_id
                userprofile.ltu_id = ''
                userprofile.user.save()
        except IntegrityError:
            print(f"IntegrityError on user {userprofile.user}")
            userprofile.user.delete()
        
    try:
        josef = User.objects.get(username="josutb-7")
        josef.is_superuser = True
        josef.save()
    except:
        pass

    # for user in User.objects.all():
        # print(user)

def home(request, lang=None):
    # emigrate_db()
    return render(request, 'home_en.html' if lang == 'en' else 'home_sv.html', {'lang': lang})

def notAMember(request, lang=None):
    return render(request, 'notAMember_en.html' if lang == 'en' else 'notAMember_sv.html', {'lang': lang})

def becomeAMember(request, lang=None):
    return render(request, 'becomeAMember_en.html' if lang == 'en' else 'becomeAMember_sv.html', {'lang': lang})
