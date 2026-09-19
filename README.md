# 📚 Descargador  de Pruebas Publicadas por el DEMRE (PAES / PDT / PSU)

Herramienta en Python para buscar, verificar y descargar automáticamente modelos de prueba y resoluciones oficiales publicadas por el DEMRE desde el proceso de admisión **2015 hasta 2027**.

## 🚀 Características
- **Amplio rango histórico:** Soporte desde el proceso de Admisión 2015 hasta 2027 (PAES Regular, PAES Invierno, PDT y PSU).
- **Mapeo inteligente de materias:** Normaliza búsquedas globales como `ciencias` (descarga Química, Física y Biología por separado) o `matematicas` (M1 y M2).
- **Verificación en tiempo real:** Comprueba que los archivos PDF existan en los servidores del DEMRE antes de descargar.
- **Organización automática:** Clasifica las descargas en subcarpetas estructuradas por Año y Materia (`DESCARGADOR DEMRE/AÑO/MATERIA/`).

  ACTUALIZACION: AGREGUE FORMATOS NUEVOS PARA DESCARGAR CONTENIDOS
  COMANDOS MASIVOS:
  --todo-el-ano         Descarga todas las materias y clavijeros de un año (jaja ke chistosooooo dice ano rianse)
                         Ejemplo: -a 2024 --todo-el-ano

  --toda-la-materia      Descarga una materia de TODOS los años (2015-2027).
                         Ejemplo: -m ciencias --toda-la-materia

--todos-los-clavijeros# Descarga sólo los clavijeros/pautas de todos los años.
                         Ejemplo: --todos-los-clavijeros

  --descargar-todo3       Descarga TODO el archivo histórico del DEMRE (2015-2027).
                         Ejemplo: --descargar-todo
                         Filtros opcionales:
                           --descargar-todo --solo-pruebas
                           --descargar-todo --solo-clavijeros




  
---

## 🛠️ Requisitos
- Python 3.6 o superior.
- Conexión a Internet (no requiere librerías externas, utiliza bibliotecas nativas de Python).

---

## 💻 Modo de Uso

Ejecuta el script interactivo desde tu terminal o consola:


python paes-tracker.py

Una vez iniciado el programa (PAES>), puedes ingresar comandos con la siguiente estructura:
Bash

-a [AÑO] -m [MATERIA] -t [TIPO]

Parámetros

    -a: Año del proceso de admisión (2015 a 2027).
    
    -m: Materia o módulo a buscar:

        lectura / lenguaje / competencia lectora / comprension lectora

        matematica / matematicas / m1 / m2

        historia

        ciencias (descarga Química, Física y Biología)

        quimica / fisica / biologia

        ciencias-tp / tp

    -t: Tipo de archivo a buscar:

        prueba (Modelos de prueba oficiales, incluye Regular e Invierno)

        clavijero (Pautas, claves o resoluciones explicadas)

📋 Ejemplos de Comandos

PAES> -a 2025 -m m1 -t prueba
PAES> -a 2022 -m ciencias -t prueba
PAES> -a 2019 -m historia -t clavijero
PAES> -a 2016 -m lenguaje -t prueba
PAES> --help

📂 Estructura de Salida

Las descargas se guardan automáticamente respetando este esquema:
Plaintext

DESCARGADOR DEMRE/
├── 2025/
│   ├── M1/
│   └── QUIMICA/
└── 2018/
    └── HISTORIA/

Desarrollado para facilitar el acceso al material de estudio oficial del DEMRE.
