from django.shortcuts import render, redirect
from openai import OpenAI
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import Registro, ReporteForm, UsernameForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import json
from django.urls import reverse
import re
from urllib.parse import urlencode
from .models import Reporte
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def index(request):
    user_name = request.user.username
    return render(request, 'home.html', {'user_name': user_name})

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
            return redirect('index')
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
        errores_usabilidad = request.POST.getlist('usability-errors')
        filtro = ""
        if errores_usabilidad:
            filtro = "quiero ver solo errores de usabilidad del tipo: "
        for i in errores_usabilidad:
            filtro = filtro + i+", "
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
            form.fileName = file.name
            form.save()

            ans = solicitud_ia(file_content,filtro)
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

def solicitud_ia(codigo,filtro):
    prompt = """
    Eres una IA experta en análisis de código HTML. Tu tarea es recibir código HTML, analizarlo y solamente devolver una cadena con errores en español detectados. Antes de poner la cadena poner 'output:'. La cadena tiene que listar los errores con su ubicacion en nro de linea separados por el delimitador '|', por ejemplo: Output: se detecto que falta un alt en la imagen x Linea 43 | no cumple con la estructura aria Linea 75
    respetame el output y los errores tienen que ser en español.Respeta solamente devolver una cadena con errores en español detectados. Antes de poner la cadena poner 'output:'. La cadena tiene que listar los errores con su ubicacion en nro de linea separados por el delimitador '|'y  ademas  """
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
    {"role": "system", "content": prompt + filtro},
    {"role": "user", "content": codigo}
    ] ,
    temperature=0.7,
    )
    # Extract the content from the message
    ans = completion.choices[0].message

    return ans

def merge_code_ai_request(input_html, error_description):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
    {"role": "system", "content": """
    Eres una IA experta en análisis de código HTML y te voy a dar un archivo HTML para analizar. De ese archivo HTML que te pase, analizalo y corregi el siguiente error de codigo: """ + error_description + """. En base a tu analis quiero que me muestren la linea de código con el error y la misma línea de código pero con el error corregido. Delimita tu respuesta usando ####original_line_start####, ####original_line_end####, ####fixed_line_start#### y ####fixed_line_end####. Un ejemplo sería: ####original_line_start####<title> </title> <!-- Missing Title -->####original_line_end########fixed_line_start####<title>Corrected Title</title>####fixed_line_end####"""},
    {"role": "user", "content": input_html}
    ] ,
    temperature=0.7,
    )
    # Extract the content from the message
    ans = completion.choices[0].message

    return ans

def merge_code_ai(input_html, error_description):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
    {"role": "system", "content": """
    Eres una IA experta en análisis de código HTML y te voy a dar un archivo HTML para analizar. De ese archivo HTML que te pase, analizalo y corregi el siguiente error de codigo: """ + error_description + """. En base a tu analis quiero que me devuelves el mismo código HTML pero con el error corregido."""},
    {"role": "user", "content": input_html}
    ] ,
    temperature=0.7,
    )
    # Extract the content from the message
    ans = completion.choices[0].message

    print("CODIGO CORREGIDO:\n", ans)

    return ans

def update_html(request, file_name, error_to_correct):
    if request.method == 'POST':
        try:
            # Recuperar el reporte por fileName
            reporte = Reporte.objects.get(fileName=file_name, usuario=request.user)

                # Acceder al archivo y leer su contenido
            with open(reporte.codigo.path, 'r') as archivo:
                file_content = archivo.read()

        except ObjectDoesNotExist:
            return HttpResponse(f'El reporte del archivo {file_name} no existe.')
        except FileNotFoundError:
            return HttpResponse(f'El archivo {file_name} no se encuentra en la ruta especificada.')

        fixed_code = str(merge_code_ai(file_content, error_to_correct))

        print('CODIGO ARREGLADO BEGIN\n', fixed_code, 'CODIGO ARREGLADO END\n')

        # Actualiza el campo aquí
        reporte.codigo = fixed_code
        reporte.save()
        
        # Deberia llamar devuelta al prompt con el nuevo archivo

        # Added the filename to the URL
        request.session['mi_dato'] = fixed_code
        url = reverse('results')
        query_params = urlencode({'file_name': file_name})
        full_url = f"{url}?{query_params}"
        return redirect(full_url)
    output = None
    return render(request, 'results/results.html', {'resultados': output, 'file_name': file_name})

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
    print("inicio dato: ", mi_dato, " fin dato.")
    # Expresión regular para extraer las frases específicas
    pattern = r'output:\s*(.*?)\.'
    matches = re.findall(pattern, mi_dato, re.DOTALL)
    output = []
    pattern2 = r'\*\*Error \d+\*\*:(.*?)\*\*Solución:\*\*(.*?)\n\n'
    patternLinea = r'(Linea \d+|línea \d+)'
    
    matches2 = re.findall(pattern2, mi_dato, re.DOTALL)

    if matches2:
        for match in matches:
            
            descripcion = match[1].strip().replace("\n","")
            linea = re.findall(patternLinea, descripcion, re.IGNORECASE)
            titulo = linea[0]
            # Agregar a la lista como un diccionario
            output.append({
                'titulo': titulo,
                'descripcion': descripcion
            })
    if matches:
        extracted_phrases = matches[0].strip()
        phrases_list = [phrase.strip() for phrase in extracted_phrases.split('|')]
        

        for index, phrase in enumerate(phrases_list, start=1):
            linea = re.findall(patternLinea, phrase, re.IGNORECASE)
            z=""
            if linea:

                z = linea[0]
            else:
                z = "Observacion"
            output.append({
                'titulo': z,
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
def error_result(request, file_name, detected_error):

    #file_name = request.GET.get('file_name')

    print("The filename is ", file_name)


    try:
        # Recuperar el reporte por fileName
        reporte = Reporte.objects.get(fileName=file_name)
        
        # Acceder al archivo y leer su contenido
        with open(reporte.codigo.path, 'r') as archivo:
            file_content = archivo.read()

    except ObjectDoesNotExist:
        return HttpResponse(f'El reporte del archivo {file_name} no existe.')
    except FileNotFoundError:
        return HttpResponse(f'El archivo {file_name} no se encuentra en la ruta especificada.')

    print("Error " + detected_error + " of file ", "file_name")

    #find file name
    ans = merge_code_ai_request(file_content, detected_error)

    #request.session['error_detectado_01E'] = str(ans)
    #url = reverse('results') 
    #return redirect(url)
    print(str(ans))
    (original_code, fixed_code) = extract_lines(str(ans))
    # Pasar las variables al contexto de la plantilla
    context = {
        "detected_error" : detected_error,
        "file_name" : "str(ans)",
        "original_code" : original_code,
        "fixed_code" : fixed_code
    }

    return render(request, 'results/error_result.html', context)

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
        

        return redirect('resultados')
    
    return render(request, 'tu_template.html', {'resultado': resultado})


def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Mantiene la sesión después del cambio
            messages.success(request, 'Su contraseña ha sido cambiada exitosamente.')
            return redirect('cambioContraDone')  # Redirige a la página de confirmación
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/change_pass.html', {'form': form})

def cambiar_contraseña_hecho(request):
    return render(request, 'registration/change_pass_done.html')

# Vista para ingresar el nombre de usuario
def password_reset_request(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                request.session['user_id'] = user.id  # Guardamos el ID de usuario en la sesión
                return redirect('set_new_password')
            except User.DoesNotExist:
                messages.error(request, "El nombre de usuario no existe.")
    else:
        form = UsernameForm()
    
    return render(request, 'registration/password_reset_request.html', {'form': form})

# Vista para establecer una nueva contraseña
def set_new_password(request):
    if 'user_id' not in request.session:
        return redirect('password_reset_request')

    user = get_object_or_404(User, id=request.session['user_id'])

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)  # Mantiene la sesión activa después del cambio
                messages.success(request, "Tu contraseña ha sido cambiada exitosamente.")
                del request.session['user_id']  # Elimina el user_id de la sesión
                return redirect('login')
            else:
                messages.error(request, "Las contraseñas no coinciden.")
    else:
        form = PasswordResetForm()

    return render(request, 'registration/set_new_password.html', {'form': form})