import os
import shutil
import sys

import yaml
from git import Repo

UMBREL_APPS_REPO = 'https://github.com/getumbrel/umbrel-apps.git'
UMBREL_APPS_PATH = './umbrel-apps'


def clone_repository(repo_url, clone_to_path):
    if os.path.exists(clone_to_path):
        if os.path.isdir(clone_to_path):
            shutil.rmtree(clone_to_path)

    try:
        Repo.clone_from(repo_url, clone_to_path)
    except Exception:
        print('Error cloning repository')


if os.path.exists(UMBREL_APPS_PATH):
    if os.path.isdir(UMBREL_APPS_PATH):
        shutil.rmtree(UMBREL_APPS_PATH)

try:
    Repo.clone_from(UMBREL_APPS_REPO, UMBREL_APPS_PATH)
except Exception:
    print('Error cloning repository')
    sys.exit(1)

ports = set()  # Usando um conjunto para garantir unicidade
for root, _, files in os.walk(UMBREL_APPS_PATH):
    for file in files:
        if file == 'umbrel-app.yml':
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as yml_file:
                try:
                    data = yaml.safe_load(yml_file)
                    if 'port' in data:
                        ports.add(data['port'])
                except yaml.YAMLError as e:
                    print(f'Erro ao processar {file_path}: {e}')

# Cria a pasta utils se não existir
os.makedirs('utils', exist_ok=True)

# Grava o conjunto de portas no arquivo ports.py
with open('cutp/utils/ports.py', 'w', encoding='utf-8') as py_file:
    py_file.write('# Arquivo gerado automaticamente com as portas extraídas\n')
    py_file.write(
        f'PORTS = {sorted(ports)}\n'
    )  # Lista ordenada para consistência

print('As portas foram salvas no arquivo: ports.py')
