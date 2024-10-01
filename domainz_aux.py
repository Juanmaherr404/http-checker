import requests
import argparse

def iterar_sobre_archivo(path, funcion):
    with open(path, 'r') as f:
        for linea in f:
            elemento = linea.strip()  # Elimina espacios en blanco y saltos de línea
            funcion(elemento)

def add_http(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def comprobar_enlace(url, file="enlaces_accesibles.txt", timeout=5, ignore_errors=False):
    url = add_http(url)
    try:
        response = requests.get(url, timeout=timeout)
        print(f"[{response.status_code}] - {url}")
        write_file(response.status_code, url, file)
    except requests.exceptions.RequestException as e:
        if not ignore_errors:
            print(f"[Error] - {url}")
        write_file("Error", url, file)

def write_file(code, url, file="enlaces_accesibles.txt"):
    with open(file, 'a') as f:
        f.write(f"{code} - {url}\n")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Comprueba el estado de los enlaces en un archivo, guardando los resultados en un archivo de salida.",
        epilog="Ejemplo de uso: python script.py urls.txt -o resultados.txt --timeout 10 --ignore-errors"
    )
    
    # Argumentos principales
    parser.add_argument("input_file", help="Ruta al archivo que contiene los enlaces (uno por línea).")
    parser.add_argument("-o", "--output_file", default="enlaces_accesibles.txt", 
                        help="Archivo de salida donde se guardarán los resultados (por defecto 'enlaces_accesibles.txt').")
    
    # Argumentos opcionales adicionales
    parser.add_argument("-t", "--timeout", type=int, default=5, 
                        help="Tiempo de espera máximo en segundos para cada solicitud (por defecto 5 segundos).")
    parser.add_argument("-i", "--ignore_errors", action="store_true", 
                        help="Si se establece, ignora los errores y no muestra mensajes de error en pantalla.")
    
    return parser.parse_args()

def domainz(input_file, output_file, timeout, ignore_errors):
    iterar_sobre_archivo(input_file, lambda url: comprobar_enlace(url, output_file, timeout, ignore_errors))
    print("Proceso finalizado.")

if __name__ == "__main__":
    args = parse_args()
    domainz(args.input_file, args.output_file, args.timeout, args.ignore_errors)
