from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import Registro

from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = Registro(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = Registro()
    return render(request, 'registration/registerForm.html', {'form': form})

#analysis fun
def analysis(request):
    return render(request, "analysis/analysis.html")

def upload_html(request):
    return render(request, "analysis/upload_html.html")

def preferences(request):
    return render(request, "analysis/preferences.html")

def preview(request):
    return render(request, "analysis/preview.html")

#result fun
def results(request):
    resultados_lista = [
        {
            'titulo': 'Linea 11: Falta de descripción en el botón de envío',
            'descripcion': 'El botón de envío en la línea 11 no tiene un atributo `aria-label` o `title` que describa su propósito, lo que puede dificultar la navegación para los usuarios que dependen de lectores de pantalla.'
        },
        {
            'titulo': 'Linea 34: Falta de descripción en el icono de búsqueda',
            'descripcion': 'El icono de búsqueda en la línea 34 carece de un `alt` o `aria-label`, impidiendo que los usuarios con discapacidades visuales comprendan su función. Es esencial para la accesibilidad.'
        },
        {
            'titulo': 'Linea 121: Falta de descripción en la imagen del encabezado',
            'descripcion': 'La imagen en la línea 121, que forma parte del encabezado del sitio, no tiene un atributo `alt` que describa la imagen. Esto puede resultar en una pérdida de contexto importante para los usuarios de lectores de pantalla.'
        },
        {
            'titulo': 'Linea 134: Falta de descripción en el enlace de pie de página',
            'descripcion': 'El enlace en la línea 134 del pie de página no tiene un texto descriptivo. Los enlaces deberían proporcionar información suficiente para que los usuarios comprendan su destino sin necesidad de contexto adicional.'
        },
        {
            'titulo': 'Linea 211: Falta de descripción en el botón de navegación',
            'descripcion': 'El botón de navegación en la línea 211 no incluye un `aria-label` o `title`, lo que puede ser problemático para los usuarios que utilizan tecnologías asistivas para navegar por el sitio.'
        }
    ]
    return render(request, 'results/results.html', {'resultados': resultados_lista})

#settings fun
def settings(request):
    return render(request, 'settings/settings.html')

def procesar_resultado(request, resultado_id):
    resultado = get_object_or_404(Resultado, id=resultado_id)
    
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')
        
        resultado.descripcion = descripcion
        resultado.estado = estado
        resultado.save()
        
        # Redirigir a una página de confirmación o de nuevo a la lista de resultados
        return redirect('resultados')  # Cambia 'resultados' por el nombre de tu vista de resultados
    
    return render(request, 'tu_template.html', {'resultado': resultado})