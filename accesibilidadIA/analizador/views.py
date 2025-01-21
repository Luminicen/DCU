from django.shortcuts import render, redirect
from openai import OpenAI
# Create your views here.
from django.http import HttpResponse, Http404
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
import os
from django.conf import settings as project_settings
from django.utils.encoding import iri_to_uri

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

@login_required
def eliminar_reporte(request, reporte_id):
    if request.method == "GET":
        print("aca entro AFAF")
        reporte = get_object_or_404(Reporte, id=reporte_id)
        file_path = reporte.codigo.path
        print(file_path)
        # Elimina el archivo si existe
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                messages.success(request, f"Archivo '{file_path}' eliminado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al eliminar el archivo: {e}")
        else:
            messages.warning(request, "El archivo no existe en el sistema.")
        reporte.delete()
        messages.success(request, f"El reporte '{reporte.nombre}' ha sido eliminado con éxito.")
        return redirect('user_analysis_history')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('user_analysis_history')

#analysis fun
@login_required
def analysis(request):
    print("entre", request.method )
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
            analysis_id = form.id
            print('ID', analysis_id)

            ans = solicitud_ia(file_content,filtro)
            request.session['mi_dato'] = str(ans)

            # Added the filename to the URL
            file_name = file.name
            url = reverse('results')
            query_params = urlencode({'file_name': file_name, 'analysis_id': analysis_id})
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
    print(completion)
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
    Eres una IA experta en análisis de código HTML y te voy a dar un archivo HTML para analizar. De ese archivo HTML que te pase, analizalo y corregi el siguiente error de codigo: """ + error_description + """. En base a tu analis quiero que me devuelves el mismo código HTML pero con el error corregido. Quiero que tu respuesta sea solo el código HTML, no agregues ningún tipo de información adicional."""},
    {"role": "user", "content": input_html}
    ] ,
    temperature=0.7,
    )
    # Extract the content from the message
    ans = completion.choices[0].message

    print("CODIGO CORREGIDO:\n", ans)

    return ans

def update_html(request, analysis_id, detected_error):
    #analysis_id = request.POST.get('analysis_id')
    #error_to_correct = request.POST.get('error_to_correct')
    error_to_correct = detected_error
    print("\n\n\nUPDATE HTML RENDER\n\n\n")
    print(f"\n\n analysis_id = {analysis_id} \n\n")
    print(f"\n\n detected_error = {detected_error} \n\n")
    if request.method == 'GET':
        try:
            # Recuperar el reporte por ID
            reporte = Reporte.objects.get(id=analysis_id)

            # Acceder al archivo y leer su contenido
            with open(reporte.codigo.path, 'r') as archivo:
                file_content = archivo.read()

        except ObjectDoesNotExist:
            return HttpResponse(f'El archivo del reporte no existe.')
        except FileNotFoundError:
            return HttpResponse(f'El archivo del reporte no se encuentra en la ruta especificada.')

        fixed_code = str(merge_code_ai(file_content, error_to_correct))

        print('CODIGO ARREGLADO BEGIN\n', fixed_code, 'CODIGO ARREGLADO END\n')

        # Actualizo el contenido del archivo con el codigo corregido
        with open(reporte.codigo.path, 'w') as file:
            file.write(fixed_code)
        
        # Debe llamar devuelta al prompt con el nuevo archivo

        # Actualizo el codigo con el nuevo codigo corregido
        request.session['mi_dato'] = fixed_code

        # Vuelvo a la pantalla de resultados
        url = reverse('results')
        #query_params = urlencode({'file_name': file_name})
        #full_url = f"{url}?{query_params}"
        return redirect(url)
    output = None
    return render(request, 'results/results.html', {'resultados': output})

def descargar_html(request, path):
    print("aca taba yo, en descarga")
    # Construir la ruta completa del archivo
    file_path = os.path.join(project_settings.MEDIA_ROOT, path)

    print("PATH:", str(file_path))
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            # Preparar la respuesta HTTP para un archivo HTML
            response = HttpResponse(
                fh.read(),
                content_type="text/html"  # Tipo MIME para HTML
            )
            # Forzar descarga con un nombre seguro
            response['Content-Disposition'] = f'attachment; filename="{iri_to_uri(os.path.basename(file_path))}"'
            return response
    
    # Lanzar una excepción si el archivo no existe
    raise Http404("El archivo HTML no existe.")

#result fun
def results(request):

    file_name = request.GET.get('file_name')
    analysis_id = request.GET.get('analysis_id')

    print("The filename is ", file_name)
    print("The ID is ", analysis_id)

    mi_dato = request.session.get('mi_dato')
    print("LISTO")
    print("inicio dato:\n", mi_dato, "\nfin dato.")
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
    return render(request, 'results/results.html', {'resultados': output, 'analysis_id': analysis_id, 'file_name': file_name})

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
def error_result(request, analysis_id, file_name, detected_error):

    print("Error result RENDER")
    #print("The id is ", analysis_id)
    #print("The filename is ", file_name)

    try:
        # Recuperar el reporte por ID
        reporte = Reporte.objects.get(id=analysis_id)

        # Acceder al archivo y leer su contenido
        with open(reporte.codigo.path, 'r') as archivo:
            file_content = archivo.read()

    except ObjectDoesNotExist:
        return HttpResponse(f'El reporte del archivo {file_name} no existe.')
    except FileNotFoundError:
        return HttpResponse(f'El archivo {file_name} no se encuentra en la ruta especificada.')

    print("Error " + detected_error + " of file ", file_name)

    #find file name
    ans = merge_code_ai_request(file_content, detected_error)

    #request.session['error_detectado_01E'] = str(ans)
    #url = reverse('results') 
    #return redirect(url)
    print(str(ans))
    (original_code, fixed_code) = extract_lines(str(ans))

    # Pasar las variables al contexto de la plantilla
    context = {
        "analysis_id" : analysis_id,
        "error_name" : detected_error,
        "file_name" : "str(ans)",
        "original_code" : original_code,
        "fixed_code" : fixed_code
    }

    return render(request, 'results/error_result.html', context)

#settings fun
def settings(request):
    return render(request, 'settings/settings.html')

def account(request):
    return render(request, 'account/account.html')

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

@login_required
def user_analysis_history(request):
    # Obtener los análisis del usuario logueado
    analyses = Reporte.objects.filter(usuario=request.user).order_by('analysisTime')
    return render(request, 'results/user_analysis_history.html', {'analyses': analyses})

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