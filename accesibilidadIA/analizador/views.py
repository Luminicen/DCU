from django.shortcuts import render, redirect
from openai import OpenAI
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import Registro, ReporteForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import json
from django.urls import reverse
import re
from urllib.parse import urlencode

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
@login_required
def analysis(request):
    if request.method == 'POST':
        analysis_name = request.POST.get('analysis-name')
        description = request.POST.get('description')
        file = request.FILES.get('file-input')

        if file:
            from .models import Reporte
            print(file)
            print(analysis_name)
            print(description)
            file_content = file.read().decode('utf-8')
            
            form = Reporte()
            form.usuario = request.user
            form.nombre = analysis_name
            form.codigo = file
            form.save()
            ans = solicitud_ia(file_content)
            request.session['mi_dato'] = str(ans)

            # Added the filename to the URL
            file_name = file.name
            url = reverse('results')
            query_params = urlencode({'file_name': file_name})
            full_url = f"{url}?{query_params}"
            return redirect(full_url)

        else:
            return HttpResponse('No se ha subido ningún archivo')

    return render(request, "analysis/analysis.html")

def upload_html(request):
    return render(request, "analysis/upload_html.html")

def preferences(request):
    return render(request, "analysis/preferences.html")

def preview(request):
    return render(request, "analysis/preview.html")

def solicitud_ia(codigo):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
    {"role": "system", "content": """
    Eres una IA experta en análisis de código HTML. Tu tarea es recibir código HTML, analizarlo y solamente devolver una cadena con errores en español detectados. Antes de poner la cadena poner 'output:'. La cadena tiene que listar los errores con su ubicacion en nro de linea separados por el delimitador '|', por ejemplo: Output: se detecto que falta un alt en la imagen x Linea 43 | no cumple con la estructura aria Linea 75
    respetame el output y los errores tienen que ser en español"""},
    {"role": "user", "content": codigo}
    ] ,
    temperature=0.7,
    )
    # Extract the content from the message
    ans = completion.choices[0].message

    return ans

def merge_code_ai_request():
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
    {"role": "system", "content": """
    Recuerda que eres una IA experta en análisis de código HTML y te pase un archivo HTML para analizar. De ese archivo HTML que te pase analizalo y corregi el siguiente error de codigo. En base a tu analis quiero que me muestren la linea de código con el error y la misma línea de código pero con el error corregido. Delimita tu respuesta usando ####original_line_start####, ####original_line_end####, ####fixed_line_start#### y ####fixed_line_end####. Un ejemplo sería: ####original_line_start####<title> </title> <!-- Missing Title -->####original_line_end########fixed_line_start####<title>Corrected Title</title>####fixed_line_end####"""},
    {"role": "user", "content": "Se detectó que falta un title en la línea 7"}
    ] ,
    temperature=0.7,
    )
    # Extract the content from the message
    ans = completion.choices[0].message

    return ans

#result fun
def results(request):

    file_name = request.GET.get('file_name')

    print("The filename is ", file_name)

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
    mi_dato = request.session.get('mi_dato')
    print("LISTO")
    print(mi_dato)
    # Expresión regular para extraer las frases específicas
    pattern = r'output:\s*(.*?)\.'
    matches = re.findall(pattern, mi_dato, re.DOTALL)
    output = []
    pattern2 = r'\*\*Error \d+\*\*:(.*?)\*\*Solución:\*\*(.*?)\n\n'

    matches2 = re.findall(pattern2, mi_dato, re.DOTALL)

    if matches2:
        for match in matches:
            titulo = "ERROR " + match[0].strip()
            descripcion = match[1].strip().replace("\n","")

            # Agregar a la lista como un diccionario
            output.append({
                'titulo': titulo,
                'descripcion': descripcion
            })
    if matches:
        extracted_phrases = matches[0].strip()
        phrases_list = [phrase.strip() for phrase in extracted_phrases.split('|')]
        

        for index, phrase in enumerate(phrases_list, start=1):
            output.append({
                'titulo': str(index),
                'descripcion': phrase
            })

        print(output)
    else:
        print("No se encontraron frases específicas.")
    return render(request, 'results/results.html', {'resultados': output, 'file_name': file_name})

def extract_lines(response):
    # Define regex patterns for the original and fixed lines
    original_pattern = r'####original_line_start####(.*?)####original_line_end####'
    fixed_pattern = r'####fixed_line_start####(.*?)####fixed_line_end####'
    
    # Search for the patterns in the response
    original_match = re.search(original_pattern, response, re.DOTALL)
    fixed_match = re.search(fixed_pattern, response, re.DOTALL)
    
    # Extract the lines if found
    original_line = original_match.group(1).strip() if original_match else None
    fixed_line = fixed_match.group(1).strip() if fixed_match else None

    print("\nOriginal code: ", original_line, ". Fixed code: ",  fixed_line, "\n")
    
    return original_line, fixed_line

#result fun
def error_result(request):
    #find file name
    ans = merge_code_ai_request()

    #request.session['error_detectado_01E'] = str(ans)
    #url = reverse('results') 
    #return redirect(url)
    print(str(ans))
    extract_lines(str(ans))
    return render(request, 'results/error_result.html')

#settings fun
def settings(request):
    return render(request, 'settings/settings.html')

def procesar_resultado(request, resultado_id):
    Resultado = None
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