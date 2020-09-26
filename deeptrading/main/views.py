from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout


# Create your views here.

#MAIN PAGE:
def MainView(request):
	#si estamos identificados devolvemos la portada
	u=True
#	if request.user.is_authenticated:
	if u:
		context={"caca":"shit","2":"lil madafuka","hhh":"iii"}
#		tokers={1: {'Time':'2020-09-16 00:00:00','High': 116.0, 'Close': 112.12999725341797, 'Volume': 154679000, 'Open': 115.2300033569336, 'Low': 112.04000091552734}, 2: {'Time':'2020-09-14 00:00:00','High': 115.93000030517578, 'Close': 115.36000061035156, 'Volume': 140150100, 'Open': 114.72000122070312, 'Low': 112.80000305175781}, 3: {'Time':'2020-09-17 00:00:00','High': 112.19999694824219, 'Close': 110.33999633789062, 'Volume': 178011000, 'Open': 109.72000122070312, 'Low': 108.70999908447266}, 4: {'Time':'2020-09-10 00:00:00','High': 120.5, 'Close': 113.48999786376953, 'Volume': 182274400, 'Open': 120.36000061035156, 'Low': 112.5}, 5: {'Time':'2020-09-15 00:00:00','High': 118.83000183105469, 'Close': 115.54000091552734, 'Volume': 184642000, 'Open': 118.33000183105469, 'Low': 113.61000061035156}, 6: {'Time':'2020-09-18 00:00:00','High': 110.87999725341797, 'Close': 106.83999633789062, 'Volume': 286693600, 'Open': 110.4000015258789, 'Low': 106.08999633789062}, 7: {'Time':'2020-09-11 00:00:00','High': 115.2300033569336, 'Close': 112.0, 'Volume': 180860300, 'Open': 114.56999969482422, 'Low': 110.0}}
#		posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
		return render(request, 'main.html', context)
	else:
		return redirect('users:login')


#REGISTER PAGE
def RegView(request):
	#creamos el formulario de autenticacion vacio
	form = UserCreationForm()
	if request.method == 'POST':
		#añadimos los datos recibidos al formulario
		form = UserCreationForm(data=request.POST)
		#si el formulario es valido...
		if form.is_valid():
			#creamos la nueva cuenta de usuario
			user = form.save()
			#si el usuario se crea correctamente
			if user is not None:
				#hacemos login
				do_login(request, user)
				#y redireccionamos a la portada
				return redirect('MainView')
	#borrar campos de ayuda de formulario
	form.fields['username'].help_text = None
	form.fields['password1'].help_text = None
	form.fields['password2'].help_text = None
	return render(request, 'registration/signup.html',{'form':form})

#LOGIN PAGE
def LoginView(request):
	#Creamos el formulario de autenticación vacío
	form = AuthenticationForm()
	if request.method == 'POST':
		#Añadimos los datos recibidos al formulario
		form = AuthenticationForm(data=request.POST)
		#Si el formulario es valido...
		if form.is_valid():
			#Recuperamo las credenciales validadas
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			#Verificamos las credenciales
			user = authenticate(username=username, password=password)
			#si existe el usuario
			if user is not None:
				#hacemos login
				do_login(request, user)
				#Redireccionamos a la portada
				return redirect('MainView')
	#Si llegamos al final renderizamos el formulario
	return render(request, 'registration/login.html', {'form':form})

#LOGOUT PAGE
def LogoutView(request):
	#Finalizamos la sesion
	do_logout(request)
	return render(request, 'registration/logout.html')
