import subprocess
import sys

def check_nmap_installed():
    """Check if nmap is installed."""
    try:
        subprocess.run(['nmap', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("nmap is already installed.")
        return True
    except subprocess.CalledProcessError:
        print("nmap is not installed.")
        return False

def install_nmap():
    """Install nmap using apt-get."""
    try:
        print("Attempting to install nmap...")
        subprocess.run(['apt-get', 'update'], check=True)
        subprocess.run(['apt-get', 'install', '-y', 'nmap'], check=True)
        print("nmap installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing nmap: {e}")
        sys.exit(1)

def main():
    """Main function."""
    if not check_nmap_installed():
        install_nmap()

if __name__ == "__main__":
    main()
