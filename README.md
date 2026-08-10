# 📚 Descargador Universal DEMRE (PAES / PDT / PSU)

Un script en Python rápido y automatizado para buscar, organizar y descargar pruebas oficiales, clavijeros, temarios y soluciones alojados en los servidores del DEMRE (2020 - 2026).

> **CREDITOS:** Elias BISAGRA + Gemini AI XD

---

## 🌟 Características
- **Velocidad Optimizada:** Filtra y consulta únicamente las URLs relevantes (~120 peticiones en lugar de +400).
- **Soporte Histórico:** Compatibilidad total con servidores antiguos (`historico.demre.cl`) para años 2020 a 2022.
- **Modos de Descarga:**
  - `--all` (`-A`): Descarga todo el material del año seleccionado.
  - `--everything` (`-E`): **Modo Acaparador.** Descarga toda la base histórica disponible (2020 a 2026).
- **Organización Automática:** Clasifica archivos por Año, Materia y Tipo de Documento.
- **Interfaz Limpia:** Barra de progreso dinámica, colores en terminal y salida sin errores al cancelar (`Ctrl + C`).

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/demre-downloader.git](https://github.com/TU_USUARIO/demre-downloader.git)
cd demre-downloader
