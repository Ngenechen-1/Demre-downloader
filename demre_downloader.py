import argparse
import os
import re
import sys
import time
import requests

# Habilitar colores en Windows
if os.name == 'nt':
    try:
        import colorama
        colorama.init()
    except ImportError:
        os.system('')

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SUBJECT_KEYWORDS = {
    "m1": ["matematica-1", "matematica1", "matematica_1", "m1", "matematica", "mate"],
    "m2": ["matematica-2", "matematica2", "matematica_2", "m2", "matematica", "mate"],
    "lectora": ["lectora", "lenguaje", "comp-lectora", "comp_lectora", "lengua"],
    "historia": ["historia", "sociales", "hist", "cs-sociales", "historia-ciencias-sociales"],
    "ciencias": ["ciencias", "biologia", "fisica", "quimica", "modulo-tp", "tecnico-profesional"]
}

SUBJECT_FOLDERS = {
    "m1": "Matematica_1",
    "m2": "Matematica_2",
    "lectora": "Competencia_Lectora",
    "historia": "Historia",
    "ciencias": "Ciencias"
}

DATES_DB = {
    "2026": {
        "regular_pruebas": ["2026-25-11-25", "2026-25-12-04"],
        "regular_clavijeros": ["2026-25-12-28", "2026-25-01-06"],
        "regular_temarios": ["2026-25-03-20"],
        "invierno_pruebas": ["2026-25-06-18"],
        "invierno_clavijeros": ["2026-25-07-18"],
        "invierno_temarios": ["2026-25-01-24"]
    },
    "2025": {
        "regular_pruebas": ["2025-24-12-02", "2025-24-12-03", "2025-24-12-04"],
        "regular_clavijeros": ["2025-25-01-06", "2025-24-12-28"],
        "regular_temarios": ["2025-24-03-20", "2025-24-01-24"],
        "invierno_pruebas": ["2025-24-06-19", "2025-24-06-20"],
        "invierno_clavijeros": ["2025-24-07-05"],
        "invierno_temarios": ["2025-24-01-20"]
    },
    "2024": {
        "regular_pruebas": ["2024-23-11-27", "2024-23-11-28", "2024-23-11-29"],
        "regular_clavijeros": ["2024-23-12-28"],
        "regular_temarios": ["2024-23-03-23"],
        "invierno_pruebas": ["2024-23-06-19", "2024-23-06-20", "2024-23-06-21", "2024-23-06-22"],
        "invierno_clavijeros": ["2024-23-07-05"],
        "invierno_temarios": ["2024-23-01-23"]
    },
    "2023": {
        "regular_pruebas": ["2023-22-11-28", "2023-22-11-29", "2023-22-11-30"],
        "regular_clavijeros": ["2023-22-12-29"],
        "regular_temarios": ["2023-22-01-26"],
        "invierno_pruebas": ["2023-23-06-19", "2023-22-04-07"],
        "invierno_clavijeros": ["2023-22-08-03"],
        "invierno_temarios": ["2023-22-02-26"]
    },
    "2022": {
        "regular_pruebas": ["2022-21-07-19", "2022-21-06-24", "2022-21-03-31"],
        "regular_clavijeros": ["2022-21-08-05", "2022-21-06-24"],
        "regular_temarios": ["2022-21-04-26"]
    },
    "2021": {
        "regular_pruebas": ["2021-20-06-11", "2021-20-07-29", "2021-20-04-23", "2021-20-03-12"],
        "regular_clavijeros": ["2021-20-06-11", "2021-20-07-29"],
        "regular_temarios": ["2021-20-04-23", "2021-20-03-12"]
    },
    "2020": {
        "regular_pruebas": ["2020-19-08-01", "2020-19-01-06", "2020-19-04-11", "2019-19-08-01"],
        "regular_clavijeros": ["2020-19-08-01", "2020-19-01-06"],
        "regular_temarios": ["2020-19-04-11", "2019-19-04-11"]
    }
}

PATTERNS_SUFFIXES = [
    "paes-regular-{subj}-p{yr}.pdf",
    "paes-regular-oficial-{subj}-p{yr}.pdf",
    "clavijero-paes-regular-{subj}.pdf",
    "temario-paes-regular-{subj}.pdf",
    "pdt-regular-{subj}-p{yr}.pdf",
    "pdt-invierno-{subj}-p{yr}.pdf",
    "clavijero-pdt-{subj}.pdf",
    "temario-pdt-{subj}.pdf",
    "modelo-{subj}.pdf",
    "modelo-{subj}-p{yr}.pdf",
    "modelo-prueba-{subj}.pdf",
    "resolucion-modelo-{subj}.pdf",
    "resolucion-modelo-prueba-{subj}.pdf",
    "claves-modelo-{subj}.pdf",
    "significado-claves-modelo-{subj}.pdf",
    "temario-{subj}-p{yr}.pdf",
    "temario-{subj}.pdf",
    "temario-psu-{subj}.pdf"
]

SUBJECT_SLUGS = {
    "m1": ["matematica", "matematica1", "competencia-matematica1"],
    "m2": ["matematica2", "competencia-matematica2", "matematica"],
    "lectora": ["competencia-lectora", "lenguaje", "lenguaje-y-comunicacion"],
    "historia": ["historia", "historia-ciencias-sociales", "historia-geografia-y-ciencias-sociales"],
    "ciencias": [
        "ciencias", "ciencias-biologia", "ciencias-fisica", "ciencias-quimica", 
        "ciencias-tp", "biologia", "quimica", "fisica", "modulo-tp"
    ]
}

def get_desktop_path():
    home = os.path.expanduser("~")
    for name in ["Escritorio", "Desktop"]:
        path = os.path.join(home, name)
        if os.path.exists(path):
            return path
    return home

def classify_document(url_or_name):
    txt = url_or_name.lower()
    
    if "temario" in txt:
        doc_type = "Temarios"
    elif "resolucion" in txt:
        doc_type = "Resolucion_Modulos"
    elif any(k in txt for k in ["clavijero", "solucionario", "clave", "claves", "respuestas"]):
        doc_type = "Clavijeros"
    elif any(k in txt for k in ["modulo", "modelo"]):
        doc_type = "Modulos_de_Prueba"
    else:
        doc_type = "Pruebas_Oficiales"

    modality = "Invierno" if "invierno" in txt else "Regular"
    return f"{doc_type}_{modality}"

def generate_urls_for_year(year):
    if year not in DATES_DB:
        return []

    urls = set()
    dates_entry = DATES_DB[year]
    all_dates = []
    for category in dates_entry.values():
        all_dates.extend(category)

    bases = [
        "https://demre.cl/publicaciones/pdf/",
        "https://historico.demre.cl/publicaciones/pdf/"
    ]

    for base in bases:
        for prefix_date in all_dates:
            for subj_key, slugs in SUBJECT_SLUGS.items():
                for slug in slugs:
                    for pat in PATTERNS_SUFFIXES:
                        filename = pat.format(subj=slug, yr=year)
                        urls.add(f"{base}{prefix_date}-{filename}")
                        urls.add(f"{base}{prefix_date}-{slug}.pdf")

    return list(urls)

def download_file_with_progress(url, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    filename = os.path.basename(filepath)

    if os.path.exists(filepath):
        print(f"  {YELLOW}[–] Ya existe en disco:{RESET} {filename}")
        return True

    try:
        res = requests.get(url, headers=HEADERS, stream=True, timeout=15)
        if res.status_code != 200:
            return False

        total_size = int(res.headers.get('content-length', 0))
        print(f"  {CYAN}[↓] Descargando:{RESET} {filename}")
        
        with open(filepath, "wb") as f:
            downloaded = 0
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        mb = downloaded / (1024 * 1024)
                        sys.stdout.write(f"\r      Progreso: {percent}% ({mb:.2f} MB)")
                        sys.stdout.flush()
        print(f"\n  {GREEN}[✓] Guardado con éxito.{RESET}\n")
        return True
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"\n  {RED}[✗] Error descargando {filename}: {e}{RESET}\n")
        return False

def process_year(year, materia_req, tipo_filter, output_dir):
    if year in ["2020", "2021", "2022"] and materia_req == "m2":
        print(f"\n{YELLOW}{BOLD}[!] AVISO:{RESET} {YELLOW}Es posible que te equivocaste al poner el comando, probablemente por que un prefijo no existia historicamente en el contexto de la prueba en aquel año en concreto jeje o_o{RESET}")
        print(f"{CYAN}    (Buscando la prueba general de matemática disponible para el año {year}...){RESET}\n")
        materia_req = "m1"

    candidate_urls = generate_urls_for_year(year)
    if not candidate_urls:
        return []

    filtered_candidates = []
    for url in candidate_urls:
        url_lower = url.lower()

        matched_subject = None
        if materia_req:
            keywords = SUBJECT_KEYWORDS.get(materia_req, [])
            if any(kw in url_lower for kw in keywords):
                matched_subject = SUBJECT_FOLDERS[materia_req]
            else:
                continue
        else:
            for s_key, keywords in SUBJECT_KEYWORDS.items():
                if any(kw in url_lower for kw in keywords):
                    matched_subject = SUBJECT_FOLDERS[s_key]
                    break

        if not matched_subject:
            continue

        category = classify_document(url_lower)

        if tipo_filter:
            if tipo_filter == "temarios" and "Temarios" not in category:
                continue
            elif tipo_filter == "clavijeros" and not any(k in category for k in ["Clavijeros", "Resolucion"]):
                continue
            elif tipo_filter == "modulos" and "Modulos" not in category:
                continue
            elif tipo_filter == "resoluciones" and "Resolucion" not in category:
                continue
            elif tipo_filter == "pruebas" and not any(k in category for k in ["Pruebas", "Modulos"]):
                continue

        filtered_candidates.append((url, matched_subject, category))

    output_year_dir = os.path.join(output_dir, year)
    found_files = []
    total_to_check = len(filtered_candidates)

    print(f"Comprobando {total_to_check} enlaces en servidores DEMRE (Año {BOLD}{year}{RESET})...\n")
    start_time = time.time()

    for idx, (url, matched_subject, category) in enumerate(filtered_candidates, 1):
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        time_str = f"{mins:02d}:{secs:02d}"

        sys.stdout.write(f"\r{CYAN}[⚙] [{time_str}] Verificando enlace {idx}/{total_to_check}...{RESET}")
        sys.stdout.flush()
        
        try:
            res = requests.head(url, headers=HEADERS, timeout=3.5)
            if res.status_code == 200:
                filename = os.path.basename(url)
                target_folder = os.path.join(output_year_dir, matched_subject, category)
                filepath = os.path.join(target_folder, filename)
                found_files.append((url, filepath, matched_subject, category, filename))
        except KeyboardInterrupt:
            raise
        except Exception:
            pass

    sys.stdout.write("\r" + " " * 75 + "\r")
    sys.stdout.flush()

    return list({f[0]: f for f in found_files}.values())

def print_header():
    print(f"\n{BOLD}{CYAN}===================================================={RESET}")
    print(f"{BOLD}{CYAN}Hola, bienvenido al descargador del demre!!!1 :DD{RESET}")
    print(f"{CYAN}Puedes descargar desde 2025 hasta 2020, para obtener ayuda, escribe el comando \"paes --help\" o hablame jeje :v{RESET}")
    print(f"{BOLD}{YELLOW}CREDITOS: Elias BISAGRA + Gemini AI XD{RESET}")
    print(f"{BOLD}{CYAN}===================================================={RESET}\n")

def main():
    try:
        # Mostrar cabecera SIEMPRE antes de procesar cualquier argumento
        print_header()

        parser = argparse.ArgumentParser(description="Descargador Universal PAES / PDT / PSU DEMRE.")
        parser.add_argument("-a", "--ano", type=str, default="2025", help="Año específico (2020 a 2026)")
        parser.add_argument("-m", "--materia", choices=["m1", "m2", "lectora", "historia", "ciencias"], help="Materia específica")
        parser.add_argument("-t", "--tipo", choices=["pruebas", "clavijeros", "temarios", "modulos", "resoluciones"], help="Filtrar por tipo de documento")
        parser.add_argument("-A", "--all", action="store_true", help="Descargar TODO el material disponible para el año seleccionado")
        parser.add_argument("-E", "--everything", action="store_true", help="Descargar TODO el registro histórico (2020 a 2026)")
        
        desktop = get_desktop_path()
        default_out = os.path.join(desktop, "PAES_Descargas")
        parser.add_argument("-o", "--output", type=str, default=default_out, help="Ruta de destino")

        if len(sys.argv) == 1:
            parser.print_help()
            return

        args = parser.parse_args()

        all_unique_files = []

        if args.everything:
            print(f"{BOLD}{YELLOW}[!] Modo EVERYTHING activado: Se buscarán todos los documentos disponibles entre 2020 y 2026.{RESET}\n")
            years_to_process = sorted(list(DATES_DB.keys()), reverse=True)
            for y in years_to_process:
                files = process_year(y, None, None, args.output)
                all_unique_files.extend(files)
        elif args.all:
            year = args.ano if args.ano else "2025"
            print(f"{BOLD}{YELLOW}[!] Modo ALL activado para el año {year}: Se buscarán todos las materias y tipos del año.{RESET}\n")
            files = process_year(year, None, None, args.output)
            all_unique_files.extend(files)
        else:
            files = process_year(args.ano, args.materia, args.tipo, args.output)
            all_unique_files.extend(files)

        if not all_unique_files:
            print(f"{RED}Oh... Hubo un error o no pude encontrarlo :\"v{RESET}\n")
            return

        print(f"{BOLD}Archivos encontrados en total ({len(all_unique_files)}):{RESET}")
        for idx, (_, _, subj, cat, fname) in enumerate(all_unique_files, 1):
            print(f" {CYAN}{idx:2d}.{RESET} [{subj} / {cat}] {fname}")

        print(f"\nRuta de destino: {BOLD}{args.output}{RESET}\n")

        confirm = input(f"{BOLD}{YELLOW}¿Deseas proceder con la descarga? [S/n]: {RESET}").strip().lower()
        if confirm not in ["", "s", "si", "sí", "y", "yes"]:
            print(f"\n{RED}Operación cancelada por el usuario.{RESET}\n")
            return

        print(f"\n{BOLD}Iniciando descargas...{RESET}\n")
        downloaded_count = 0
        for url, path, _, _, _ in all_unique_files:
            if download_file_with_progress(url, path):
                downloaded_count += 1

        if downloaded_count > 0:
            print(f"\n{BOLD}{GREEN}===================================================={RESET}")
            print(f"{BOLD}{GREEN}Lo lograste, disfruta y... Estudia!!! <3{RESET}")
            print(f"{BOLD}{GREEN}===================================================={RESET}\n")
        else:
            print(f"{RED}Oh... Hubo un error o no pude encontrarlo :\"v{RESET}\n")

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Operación cancelada por el usuario (Ctrl + C). ¡Hasta luego!{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
