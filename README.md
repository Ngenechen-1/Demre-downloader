# 📚 Descargador Oficial PAES/PDT/PSU DEMRE

Una herramienta CLI en Python para buscar, verificar y descargar de forma automatizada ensayos, modelos de prueba y clavijeros/resoluciones oficiales del DEMRE desde el año 2020 hasta el 2027.

---

## 🚀 Características

* **Descargas unificadas:** Obtén archivos de Admisión Regular e Invierno.
* **Soporte multivariable:** Procesa solicitudes agrupadas o asignaturas independientes.
* **Organización automática:** Estructura los PDF descargados en carpetas por Año y Asignatura.
* **Modo interactivo CLI:** Ejecución continua mediante línea de comandos personalizada.

---

## 🛠️ Modos de Uso

El programa acepta los siguientes parámetros:

* `-a` **Año de Proceso de Admisión:** `2020` a `2027`
* `-m` **Materia / Asignatura:**
  * `m1` | `m2` | `matematica` (Soporta sintaxis de PDT y PAES)
  * `lectura` | `lenguaje` | `competencia lectora`
  * `historia`
  * `ciencias` *(Generalizador para Química, Física y Biología)*
  * `quimica` | `fisica` | `biologia` *(Búsqueda independiente)*
  * `ciencias-tp` | `tp` *(Módulo Técnico Profesional)*
* `-t` **Tipo de Archivo:**
  * `prueba` *(Modelos y ensayos completos)*
  * `clavijero` *(Pautas de respuestas y resoluciones)*

---

## 💻 Ejemplos de Comandos

```bash
PAES> -a 2025 -m m1 -t prueba
PAES> -a 2023 -m ciencias -t prueba
PAES> -a 2022 -m ciencias-tp -t prueba
PAES> -a 2020 -m lenguaje -t clavijero
