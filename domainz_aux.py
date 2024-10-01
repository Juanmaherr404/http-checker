import requests
import sys

def iterar_sobre_archivo(path, funcion):
    with open(path, 'r') as f:
        for linea in f:
            elemento = linea.strip()  # Elimina espacios en blanco y saltos de línea
            funcion(elemento)

def add_http(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def comprobar_enlace(url, file="enlaces_accesibles.txt"):
    url = add_http(url)
    try:
        response = requests.get(url, timeout=5)
        print(f"[{response.status_code}] - {url}")
        write_file(response.status_code, url, file)
    except requests.exceptions.RequestException as e:
        print(f"[Error] - {url}")
        write_file("Error", url, file)

def write_file(code, url, file="enlaces_accesibles.txt"):
    with open(file, 'a') as f:
        f.write(f"{code} - {url}\n")

def all_argvs():
    return sys.argv[1:]

def domainz(inputs):
    iterar_sobre_archivo(inputs[0], comprobar_enlace)
    print("Proceso finalizado.")

if __name__ == "__main__":
    inputs = all_argvs()
    domainz(inputs)