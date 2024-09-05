import subprocess
import socket
from colorama import Fore, Style, init
from pyfiglet import figlet_format
from datetime import datetime
import os
import random
import string

# Inicializar colorama
init()

def display_banner():
    banner = figlet_format("Nmap", font="small")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.GREEN + "Bienvenido al escáner de puertos y vulnerabilidades" + Style.RESET_ALL)

def scan_ports(ip):
    # Escanear solo puertos comunes para acelerar el proceso
    nmap_command = f"nmap -p 1-1024 -Pn {ip}"
    try:
        result = subprocess.run(nmap_command, shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"Error al escanear: {e}"

def scan_vulnerabilities(ip, port):
    nmap_command = f"nmap -p {port} -Pn --script vuln {ip}"
    try:
        result = subprocess.run(nmap_command, shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"Error al escanear: {e}"

def scan_vulnerabilities_no_port(ip):
    nmap_command = f"nmap -Pn --script vuln {ip}"
    try:
        result = subprocess.run(nmap_command, shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"Error al escanear: {e}"

def save_report(data, filename):
    with open(filename, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"\n\n{Fore.YELLOW}--- Reporte generado el {timestamp} ---{Style.RESET_ALL}\n")
        file.write(data)
        file.write(f"\n\n{Fore.YELLOW}--- Fin del Reporte ---{Style.RESET_ALL}\n")

def view_report(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            print(file.read())
    else:
        print(f"El archivo {filename} no existe.")

def generate_random_filename():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{random_string}.Rep.txt"

def get_ip_from_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.error as e:
        return f"Error al resolver el dominio: {e}"

def main():
    display_banner()
    while True:
        print(Fore.BLUE + "\n1] Escaneo de IP (dominio a IP y puertos existentes en la IP)" + Style.RESET_ALL)
        print(Fore.BLUE + "2] Escaneo de Vulnerabilidades en la IP y Puerto" + Style.RESET_ALL)
        print(Fore.BLUE + "3] Ver Rep.txt" + Style.RESET_ALL)
        print(Fore.BLUE + "4] Escaneo de Vulnerabilidades sin especificar Puerto" + Style.RESET_ALL)
        print(Fore.RED + "0] Salir" + Style.RESET_ALL)
        choice = input("Selecciona una opción: ")

        if choice == '1':
            domain = input("Dominio del Objetivo (ej. www.universocraft.com): ")
            target_ip = get_ip_from_domain(domain)
            if "Error" in target_ip:
                print(target_ip)
                continue
            print(f"IP del dominio {domain} es {target_ip}")
            print(f"Escaneando puertos en {target_ip}...")
            scan_result = scan_ports(target_ip)
            save_report(scan_result, 'Rep.txt')
            print("Escaneo de puertos completado y reporte guardado en Rep.txt.")
        elif choice == '2':
            target_ip = input("IP del Objetivo: ")
            target_port = input("Puerto del objetivo: ")
            print(f"Escaneando vulnerabilidades en {target_ip}:{target_port}...")
            scan_result = scan_vulnerabilities(target_ip, target_port)
            save_report(scan_result, 'Rep.txt')
            print("Escaneo de vulnerabilidades completado y reporte guardado en Rep.txt.")
        elif choice == '3':
            print("Mostrando contenido de Rep.txt...")
            view_report('Rep.txt')
        elif choice == '4':
            target_ip = input("IP del Objetivo: ")
            print(f"Escaneando vulnerabilidades en {target_ip} sin especificar puerto...")
            scan_result = scan_vulnerabilities_no_port(target_ip)
            save_report(scan_result, 'Rep.txt')
            print("Escaneo de vulnerabilidades sin especificar puerto completado y reporte guardado en Rep.txt.")
        elif choice == '0':
            new_filename = generate_random_filename()
            os.rename('Rep.txt', new_filename)
            print(f"El archivo Rep.txt ha sido renombrado a {new_filename}.")
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
