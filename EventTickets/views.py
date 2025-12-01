from django.shortcuts import render, redirect
from django.db import connections
from django.conf import settings


def select_database(request):
    if request.method == "POST":
        selected = request.POST.get("db_choice")

        db_configs = {
                'relational': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'tickets',
                    'USER': 'inez',
                    'PASSWORD': 'inez',
                    'HOST': 'localhost',
                    'PORT': '5432',
            },
                # 'nosql': {
                    # 'ENGINE': 'djongo',
                    # 'NAME': '',
                    # 'ENFORCE_SCHEMA': False,
                    # 'CLIENT': {
                    #     'host': 'mongodb://localhost:27017',
                    # },
                # },
            'objective_relational': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'db_obj_rel',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'db',
                'PORT': '5432',
            },
        }

        settings.DATABASES['default'] = db_configs.get(selected, {})
            
        connections.close_all()

        return redirect('home')

    return render(request, 'select_database.html')

def home(request):
    return render(request, "home.html")

