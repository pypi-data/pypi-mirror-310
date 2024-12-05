import subprocess


def install_package(command: str, package_name: str) -> bool:
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"{package_name} installed successfully.")
        return True
    except subprocess.CalledProcessError as error:
        print(f"Error installing {package_name}: {error}")
        return False
