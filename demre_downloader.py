#!/usr/bin/env python3
import os
import sys
import time
import argparse
import shlex
import urllib.request
import urllib.error
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS DE ALMACENAMIENTO (SIEMPRE EN EL ESCRITORIO) ---
desktop_path = Path.home() / "Escritorio"
if not desktop_path.exists():
    desktop_path = Path.home() / "Desktop"

BASE_DIR = desktop_path / "DESCARGADOR DEMRE"

# --- MENSAJES Y TEXTOS ESTÉTICOS ---
MSG_WELCOME = (
    "Holaaa, bienvenido al descargador de pruebas de la paes del demre :DD\n"
    "Escribe -- help si requieres ayuda o... Hablame po!!1\n"
    "-CREDITOS: ELIAS BISAGRA Y GEMINI AI XDDD\n"
)
MSG_SEARCHING = "Espera un poquito..."
MSG_SUCCESS = "Ke disfruti tu estudio... Supongo uwu"
MSG_CANCEL = "No se realizara ninguna descarga, dah..."
MSG_FAIL = "Oh... Tuvimos un problema parece, ve si el formato del comando esta bien puesta o hablame porfiiss..."

# --- BASE DE DATOS DE URLs SEGÚN EL AÑO Y MATERIA ---
URL_DATABASE = {
    "2027": {
        "invierno": {
            "m2": "2026-06-15",
            "historia": "2026-06-17",
            "ciencias-tp": "2026-06-17",
            "competencia-lectora": "2026-06-17",
            "biologia": "2026-06-16",
            "quimica": "2026-06-16",
            "fisica": "2026-06-16",
            "m1": "2026-06-17",
            "_clavijeros": "2026-06-17"
        }
    },
    "2026": {
        "invierno": {
            "m1": "2025-06-16",
            "competencia-lectora": "2025-06-17",
            "ciencias-tp": "2025-06-17",
            "historia": "2025-06-18",
            "m2": "2025-06-18",
            "fisica": "2025-06-17",
            "quimica": "2025-06-17",
            "biologia": "2025-06-17",
            "_clavijeros": "2025-07-18"
        },
        "regular": {
            "m2": "2025-12-01",
            "competencia-lectora": "2025-12-02",
            "ciencias-tp": "2025-12-02",
            "fisica": "2025-12-02",
            "quimica": "2025-12-02",
            "biologia": "2025-12-02",
            "historia": "2025-12-03",
            "m1": "2025-12-03",
            "_clavijeros": "2026-01-05"
        }
    },
    "2025": {
        "regular": {
            "m2": "2024-12-04",
            "competencia-lectora": "2024-12-03",
            "ciencias-tp": "2024-12-03",
            "fisica": "2024-12-03",
            "quimica": "2024-12-03",
            "biologia": "2024-12-03",
            "historia": "2024-12-04",
            "m1": "2024-12-04",
            "_clavijeros": "2025-01-06"
        },
        "invierno": {
            "m2": "2024-06-17",
            "competencia-lectora": "2024-06-18",
            "ciencias-tp": "2024-06-18",
            "fisica": "2024-06-18",
            "quimica": "2024-06-18",
            "biologia": "2024-06-18",
            "historia": "2024-06-19",
            "m1": "2024-06-19",
            "_clavijeros": "2024-07-19"
        }
    },
    "2024": {
        "regular": {
            "m2": "2023-11-27",
            "competencia-lectora": "2023-11-28",
            "ciencias-tp": "2023-11-28",
            "fisica": "2023-11-28",
            "quimica": "2023-11-28",
            "biologia": "2023-11-28",
            "historia": "2023-11-29",
            "m1": "2023-11-29",
            "_clavijeros": "2023-12-28"
        },
        "invierno": {
            "m2": "2023-06-19",
            "competencia-lectora": "2023-06-20",
            "ciencias-tp": "2023-06-20",
            "fisica": "2023-06-20",
            "quimica": "2023-06-20",
            "biologia": "2023-06-20",
            "historia": "2023-06-22",
            "m1": "2023-06-22",
            "_clavijeros": "2023-07-20"
        }
    },
    "2023": {
        "regular": {
            "m2": "2022-11-29",
            "competencia-lectora": "2022-11-29",
            "ciencias-tp": "2022-11-28",
            "fisica": "2022-11-28",
            "quimica": "2022-11-28",
            "biologia": "2022-11-28",
            "ciencias": "2022-11-28",
            "historia": "2022-11-30",
            "m1": "2022-11-30",
            "_clavijeros": "2022-12-29"
        },
        "invierno": {
            "competencia-lectora": "2022-07-04",
            "ciencias-tp": "2022-07-04",
            "fisica": "2022-07-04",
            "quimica": "2022-07-04",
            "biologia": "2022-07-04",
            "ciencias": "2022-07-04",
            "matematica": "2022-07-05",
            "historia": "2022-07-05",
            "_clavijeros": "2022-08-03"
        }
    },
    "2022": {
        "regular": {
            "matematica": "2021-06-24",
            "comprension-lectora": "2021-07-08",
            "ciencias-tp": "2021-07-15",
            "fisica": "2021-07-15",
            "quimica": "2021-07-15",
            "biologia": "2021-07-15",
            "historia": "2021-07-15",
            "_resoluciones": "2021-08-05"
        }
    },
    "2021": {
        "regular": {
            "quimica": "2020-06-11",
            "fisica": "2020-06-11",
            "biologia": "2020-06-11",
            "ciencias-tp": "2020-06-11",
            "comprension-lectora": "2020-06-11",
            "matematica": "2020-06-11",
            "historia": "2020-06-11",
            "_todas": "2020-06-11",
            "_resoluciones": "2020-07-29"
        }
    },
    "2020": {
        "regular": {
            "quimica": "2019-08-01",
            "fisica": "2019-08-01",
            "biologia": "2019-08-01",
            "ciencias-tp": "2019-08-01",
            "lenguaje": "2019-08-01",
            "matematica": "2019-08-01",
            "historia": "2019-08-01",
            "_todas": "2019-08-01",
            "_resoluciones": "2019-08-01"
        }
    },
    "2019": {
        "regular": {
            "_todas": "2018-07-19",
            "_resoluciones": "2018-08-02"
        }
    },
    "2018": {
        "regular": {
            "_todas": "2017-07-20",
            "_resoluciones": "2017-07-27"
        }
    },
    "2017": {
        "regular": {
            "_todas": "2016-07-14",
            "_resoluciones": "2016-09-05"
        }
    },
    "2016": {
        "regular": {
            "quimica": "2015-06-25",
            "fisica": "2015-06-25",
            "biologia": "2015-06-25",
            "ciencias-tp": "2015-06-25",
            "historia": "2015-06-18",
            "matematica": "2015-06-11",
            "lenguaje": "2015-06-04",
            "_res_quimica": "2015-08-13",
            "_res_fisica": "2015-08-13",
            "_res_biologia": "2015-08-13",
            "_res_ciencias-tp": "2015-08-13",
            "_res_historia": "2015-08-06",
            "_res_matematica": "2015-07-30",
            "_res_lenguaje": "2015-07-23"
        }
    },
    "2015": {
        "regular": {
            "_todas": "2014-08-21",
            "_resoluciones": "2014-09-01"
        }
    }
}

def print_help():
    help_text = """
GLOSARIO Y MODO DE USO:
  -a  Año de proceso de admisión (2015 a 2027)
  -m  Materia a buscar:
      - Lectura / Comprension Lectora / Lenguaje
      - M1 / M2 / Matematica / Matematicas (Generalizador)
      - Historia
      - Ciencias (Generalizador solo para Química, Física y Biología)
      - Quimica / Fisica / Biologia (Menciones independientes)
      - Ciencias-TP / TP / Cienciastp (Módulo Técnico Profesional independiente)
  -t  Tipo de archivo:
      - prueba (Busca la prueba completa, incluye Regular e Invierno)
      - clavijero (Busca pautas, claves o resoluciones de módulos)

EJEMPLOS DE USO:
  -a 2019 -m ciencias -t prueba      (Descarga Química, Física y Biología 2019)
  -a 2018 -m ciencias-tp -t clavijero(Descarga la resolución de Ciencias TP 2018)
  -a 2016 -m lenguaje -t prueba      (Descarga Modelo de Lenguaje 2016)
  -a 2015 -m matematica -t clavijero (Descarga Resolución de Matemática 2015)
"""
    print(help_text)

def normalizar_materia(materia_raw, ano):
    m = materia_raw.lower().strip()
    ano_int = int(ano)
    
    # Mapeo para Matemáticas
    if m in ["m1", "m2", "matematica", "matematicas"]:
        if ano_int <= 2023:
            return ["matematica"]
        elif m == "matematicas":
            return ["m1", "m2"]
        return [m]
        
    # Mapeo para Lenguaje / Lectura
    if m in ["lectura", "lenguaje", "competencia lectora", "comprension lectora"]:
        if ano_int <= 2020:
            return ["lenguaje"]
        elif ano_int in [2021, 2022, 2023]:
            return ["comprension-lectora"]
        else:
            return ["competencia-lectora"]
            
    # 'ciencias' NUNCA incluye ciencias-tp
    if m in ["ciencias", "ciencia"]:
        return ["quimica", "fisica", "biologia"]
        
    if m in ["quimica", "química"]: return ["quimica"]
    if m in ["fisica", "física"]: return ["fisica"]
    if m in ["biologia", "biología"]: return ["biologia"]
    if m in ["ciencias-tp", "tp", "cienciastp"]: return ["ciencias-tp"]
    if m in ["historia", "historia-csociales", "hycsoc"]: return ["historia"]
    
    return [m]

def obtener_codigos_materia(m, ano_int, tipo):
    codigos = []
    
    if m in ["quimica", "fisica", "biologia"]:
        if tipo == "prueba":
            if ano_int >= 2022:
                codigos = [f"ciencias-{m}", m]
            elif ano_int in [2018, 2019]:
                codigos = [f"ciencias-{m}", f"cs-{m}", m]
            elif ano_int == 2017:
                codigos = [m, f"cs-{m}", f"ciencias-{m}"]
            elif ano_int == 2016:
                short_m = "cquim" if m == "quimica" else ("cfis" if m == "fisica" else "cbio")
                codigos = [short_m]
            elif ano_int == 2015:
                codigos = [f"ciencias-{m}"]
            else:
                codigos = [m, f"ciencias-{m}"]
        elif tipo == "clavijero":
            if ano_int >= 2023:
                codigos = [f"ciencias-{m}", m]
            elif ano_int in [2017, 2018, 2019]:
                codigos = [f"cs-{m}", f"ciencias-{m}", m]
            elif ano_int == 2016:
                codigos = [f"cs-{m}"]
            elif ano_int == 2015:
                codigos = [f"ciencias-{m}"]
            else:
                codigos = [f"ciencias-{m}", m]

    elif m == "ciencias-tp":
        if ano_int == 2016:
            codigos = ["ctp"] if tipo == "prueba" else ["cs-tp"]
        elif ano_int == 2015:
            codigos = ["ciencias-tecnico-profesional"]
        else:
            codigos = ["ciencias-tp"]
            
    elif m == "lenguaje":
        if ano_int == 2017 and tipo == "prueba":
            codigos = ["lenguaje-comunicacion", "lenguaje"]
        elif ano_int == 2016:
            codigos = ["lyc"]
        else:
            codigos = ["lenguaje"]

    elif m == "historia":
        if ano_int == 2017 and tipo == "prueba":
            codigos = ["historia-csociales", "historia"]
        elif ano_int == 2016:
            codigos = ["hycsoc"]
        else:
            codigos = ["historia"]

    elif m == "m1":
        codigos = ["matematica1", "m1"]
    elif m == "m2":
        codigos = ["matematica2", "m2"]
    else:
        codigos = [m]

    return codigos

def generar_urls(ano, materias, tipo):
    urls = []
    ano_int = int(ano)
    domain = "https://historico.demre.cl" if ano_int <= 2024 else "https://demre.cl"

    if ano not in URL_DATABASE:
        return urls

    periodos = URL_DATABASE[ano]

    for m in materias:
        m_codes = obtener_codigos_materia(m, ano_int, tipo)

        for periodo, data in periodos.items():
            if ano_int == 2016 and tipo in ["clavijero", "respuestas"]:
                fecha = data.get(f"_res_{m}", None)
            else:
                fecha = data.get(m, data.get("_todas", None))
            
            for m_code in m_codes:
                if tipo == "prueba":
                    if ano_int >= 2024:
                        tag_tipo = f"paes-{periodo}-oficial" if "invierno" in periodo else "paes-regular"
                        if ano_int == 2024 and periodo == "regular": 
                            tag_tipo = "paes-regular-oficial"
                        if fecha:
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha[2:]}-{tag_tipo}-{m_code}-p{ano}.pdf"
                            urls.append((url, periodo, m))
                    elif ano_int == 2023:
                        if periodo == "invierno" and fecha:
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha[2:]}-pdt-oficial-{m_code}-p{ano}.pdf"
                            urls.append((url, periodo, m))
                        elif fecha:
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha[2:]}-paes-oficial-{m_code}-p{ano}.pdf"
                            urls.append((url, periodo, m))
                    elif ano_int in [2017, 2018, 2019, 2020, 2021, 2022]:
                        if fecha:
                            fecha_corta = fecha[2:]
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha_corta}-modelo-{m_code}.pdf"
                            urls.append((url, periodo, m))
                    elif ano_int == 2016:
                        if fecha:
                            if len(fecha) == 10 and fecha.startswith("2015-06-1"):
                                fecha_formateada = f"{fecha[:4]}-{fecha[5:]}"
                            else:
                                fecha_formateada = f"{fecha[:4]}-{fecha[2:4]}-{fecha[5:]}"
                            
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha_formateada}-demre-modelo-{m_code}.pdf"
                            urls.append((url, periodo, m))
                    elif ano_int == 2015:
                        url = f"{domain}/publicaciones/pdf/2015-demre-modelo-prueba-{m_code}.pdf"
                        urls.append((url, periodo, m))

                elif tipo in ["clavijero", "respuestas"]:
                    if ano_int == 2016:
                        fecha_clav = data.get(f"_res_{m}", None)
                    else:
                        fecha_clav = data.get("_clavijeros", data.get("_resoluciones", None))
                        
                    if fecha_clav or ano_int == 2015:
                        if ano_int >= 2024:
                            prefix = "clavijero-paes-invierno" if periodo == "invierno" else "clavijero-paes-regular"
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha_clav[2:]}-{prefix}-{m_code}.pdf"
                            urls.append((url, periodo, m))
                        elif ano_int == 2023:
                            if periodo == "invierno":
                                url = f"{domain}/publicaciones/pdf/{ano}-{fecha_clav[2:]}-clavijeropdt-{m_code}.pdf"
                            else:
                                url = f"{domain}/publicaciones/pdf/{ano}-{fecha_clav[2:]}-clavijero-paes-{m_code}.pdf"
                            urls.append((url, periodo, m))
                        elif ano_int in [2017, 2018, 2019, 2020, 2021, 2022]:
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha_clav[2:]}-resolucion-modelo-{m_code}.pdf"
                            urls.append((url, periodo, m))
                        elif ano_int == 2016:
                            doble_guion = "--" if m == "lenguaje" else "-"
                            url = f"{domain}/publicaciones/pdf/{ano}-{fecha_clav[2:]}{doble_guion}demre-resolucion-modelo-{m_code}.pdf"
                            urls.append((url, periodo, m))
                        elif ano_int == 2015:
                            num_res = {
                                "matematica": "01",
                                "lenguaje": "02",
                                "quimica": "03",
                                "fisica": "04",
                                "biologia": "05",
                                "ciencias-tecnico-profesional": "06",
                                "historia": "07"
                            }.get(m_code, "01")
                            url = f"{domain}/publicaciones/pdf/2015-demre-{num_res}-resolucion-{m_code}.pdf"
                            urls.append((url, periodo, m))
                        
    return urls

def verificar_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return True
    except Exception:
        return False
    return False

def descargar_archivo(url, destino_path):
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response, open(destino_path, 'wb') as out_file:
            out_file.write(response.read())
        return True
    except Exception:
        return False

def procesar_comando(args_list):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-a", type=str, required=True)
    parser.add_argument("-m", type=str, required=True)
    parser.add_argument("-t", type=str, required=True)

    try:
        args = parser.parse_args(args_list)
    except SystemExit:
        print(MSG_FAIL)
        return

    print(MSG_SEARCHING)
    time.sleep(1)

    tipo_normalizado = "clavijero" if args.t.lower() in ["clavijero", "clavijeros", "respuestas"] else "prueba"
    materias_normalizadas = normalizar_materia(args.m, args.a)
    candidatos = generar_urls(args.a, materias_normalizadas, tipo_normalizado)

    encontrados = []
    vistos = set()

    for url, periodo, mat in candidatos:
        if url not in vistos and verificar_url(url):
            vistos.add(url)
            encontrados.append((url, periodo, mat))

    if not encontrados:
        print(MSG_FAIL)
        return

    print(f"\nSe encontraron {len(encontrados)} archivo(s):")
    for url, periodo, mat in encontrados:
        print(f" - [{periodo.upper()}] {mat.upper()}: {url}")

    confirm = input("\n¿Desea descargarlos? (SI/NO): ").strip().upper()
    
    if confirm in ["SI", "S"]:
        exito = False
        for url, periodo, mat in encontrados:
            folder = BASE_DIR / args.a / mat.upper()
            file_name = f"{tipo_normalizado}_{periodo}_{url.split('/')[-1]}"
            target_file = folder / file_name

            if descargar_archivo(url, target_file):
                print(f" Guardado en: {target_file}")
                exito = True
        
        if exito:
            print(f"\n{MSG_SUCCESS}\n")
        else:
            print(MSG_FAIL)
    else:
        print(f"\n{MSG_CANCEL}\n")

def main():
    print(MSG_WELCOME)
    
    while True:
        try:
            user_input = input("PAES> ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "salir"]:
                break

            if "--help" in user_input or "help" in user_input:
                print_help()
                continue

            if user_input.lower().startswith("paes "):
                user_input = user_input[5:].strip()
            elif user_input.lower() == "paes":
                continue

            tokens = shlex.split(user_input)
            procesar_comando(tokens)

        except KeyboardInterrupt:
            print("\n¡Nos vemos!")
            break
        except Exception:
            print(MSG_FAIL)

if __name__ == "__main__":
    main()
