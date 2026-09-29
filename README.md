# Chatbot multiagente de salud

## Descripción

Este proyecto contiene dos chatbots de consola construidos con **AG2 (AutoGen)** y modelos de lenguaje:

- **Orientación sanitaria:** analiza síntomas, presenta posibles causas sin emitir un diagnóstico definitivo, sugiere medidas generales y orienta sobre la urgencia de consultar a un profesional.
- **Bienestar y salud mental:** identifica las emociones expresadas por la persona y propone técnicas de relajación y autocuidado, recomendando buscar apoyo profesional cuando sea necesario.

Cada flujo divide la conversación entre agentes especializados coordinados mediante un `GroupChat`. La configuración del proveedor de IA se centraliza en `Config.py`, lo que permite utilizar Groq, Gemini u OpenAI y configurar proveedores de respaldo sin modificar los scripts principales.

> **Aviso importante:** este proyecto tiene fines educativos e informativos. No sustituye una evaluación, un diagnóstico ni un tratamiento profesional. Ante una emergencia médica o riesgo para la seguridad de una persona, contacta inmediatamente a los servicios de emergencia o a una línea de crisis local.

## Características principales

- Arquitectura multiagente con roles separados.
- Conversaciones con rondas limitadas para evitar ciclos infinitos.
- Respuestas en el mismo idioma que utiliza la persona.
- Configuración centralizada de modelos y proveedores.
- Soporte para proveedor principal y proveedores de respaldo.
- Carga de claves mediante variables de entorno.

## Requisitos

- Python 3.10 o posterior.
- Una API key de al menos uno de los proveedores compatibles:
  - [Groq](https://console.groq.com/)
  - [Google Gemini](https://aistudio.google.com/)
  - [OpenAI](https://platform.openai.com/)

## Instalación

1. Clona o descarga este proyecto y abre una terminal en su carpeta.
2. Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   ```

   En Windows:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias:

   ```bash
   pip install pyautogen python-dotenv
   ```

4. Crea un archivo `.env` en la raíz del proyecto. No compartas este archivo ni subas sus claves a un repositorio:

   ```env
   PROVIDER=groq
   GROQ_API_KEY=tu_clave_de_groq
   ```

   También puedes utilizar Gemini u OpenAI:

   ```env
   PROVIDER=gemini
   GEMINI_API_KEY=tu_clave_de_gemini
   ```

   ```env
   PROVIDER=openai
   OPENAI_API_KEY=tu_clave_de_openai
   ```

## Configuración de proveedores

La variable `PROVIDER` define el orden de uso. Para configurar un proveedor principal y uno de respaldo, sepáralos por comas:

```env
PROVIDER=groq,gemini
GROQ_API_KEY=tu_clave_de_groq
GEMINI_API_KEY=tu_clave_de_gemini
```

Los modelos predeterminados están definidos en `Config.py`. Se pueden sobrescribir desde `.env`:

```env
GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_MODEL=gemini-3.8-flash
OPENAI_MODEL=gpt-4.1-mini
```

Si el proveedor indicado no existe o no se encuentra ninguna API key válida, la aplicación detiene el inicio y muestra un error de configuración.

## Uso

### Chatbot de orientación sanitaria

Solicita síntomas y ejecuta el flujo de análisis, recomendaciones generales y nivel de urgencia:

```bash
python Healthcare_chatbot.py
```

### Chatbot de salud mental

Solicita cómo se siente la persona, analiza las emociones y ofrece sugerencias de autocuidado:

```bash
python Mental_health_chatbot.py
```

La respuesta se genera en la terminal y requiere conexión a Internet para comunicarse con el proveedor del modelo.

## Arquitectura

### `Healthcare_chatbot.py`

1. `patient`: inicia la conversación con los síntomas.
2. `diagnosis`: enumera posibles causas y aclara que no es un diagnóstico definitivo.
3. `pharmacy`: ofrece opciones generales de venta libre y precauciones, sin diagnosticar.
4. `consultation`: indica si conviene consultar a un médico y con qué urgencia.
5. `GroupChatManager`: coordina el orden de participación de los agentes.

### `Mental_health_chatbot.py`

1. `patient`: comunica las emociones o preocupaciones.
2. `emotion_analysis`: resume las emociones predominantes sin proporcionar tratamiento.
3. `therapy_recommendation`: propone relajación y autocuidado, e indica buscar ayuda profesional o de emergencia cuando corresponda.
4. `GroupChatManager`: coordina el análisis y las recomendaciones.

## Estructura del proyecto

```text
.
├── Config.py
├── Healthcare_chatbot.py
├── Mental_health_chatbot.py
└── README.md
```

## Solución de problemas

- **`No se encontró ninguna API key`**: revisa que `.env` esté en la raíz del proyecto, que el nombre de la variable coincida con el proveedor y que el archivo se cargue correctamente.
- **`Proveedor desconocido`**: utiliza únicamente `groq`, `gemini` u `openai` en `PROVIDER`.
- **Error de instalación de `autogen`**: confirma que el entorno virtual esté activo y reinstala `pyautogen` con `pip`.
- **Límites de cuota o disponibilidad**: configura más de un proveedor en `PROVIDER`, por ejemplo `groq,gemini`.

## Licencia

No se ha definido una licencia para este proyecto. Antes de distribuirlo, añade una licencia que especifique los permisos de uso, modificación y redistribución.
