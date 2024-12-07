from argparse import ArgumentParser, Namespace
from subprocess import run
from os import name


def get_args() -> Namespace:
    parser = ArgumentParser(description='Actualice todas las dependencias instaladas con pip.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s v0.1.0', help='Mostrar el número de versión del programa y salir.')
    parser.add_argument('-V', '--verbose', action='store_true', default=False, help='Mostrar más información al ejecutar el programa.')
    
    return parser.parse_args()


def list_outdated_dependencies():
    args = get_args()
    
    result = run(f"pip list --outdated {"--verbose" if args.verbose else ""}", shell=True, capture_output=True, text=True)
    
    print(result.stdout)


def update_dependencies():
    args = get_args()
    
    result = run("pip list", shell=True, capture_output=True, text=True)

    output = result.stdout

    lines = output.splitlines()[2:]

    column = [line.split()[0] for line in lines]

    command = f"{"python" if name == "nt" else "python3"} -m pip install --upgrade "

    for package in column:
        command += f"{package} "

    print("Actualizando paquetes.")

    result = run(command, shell=True, capture_output=not args.verbose, text=True)

    print("Paquetes actualizados con éxito.")
    