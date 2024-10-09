import pathlib
import string
import sys
import os
import shutil
import subprocess
import tempfile
import random


def generate_unique_file_path(directory = tempfile.gettempdir(), base_file_name = '', extension = '', length=10):
    """
    Gera o caminho de um arquivo único, garantindo que não exista arquivo que tenha esse caminho.
    :param directory: Diretório onde será criado esse arquivo. Por padrão é o diretório temporário
    :param base_file_name: Nome base do arquivo. Por padrão é uma string vazia.
    :param extension: Extensão do arquivo. Por padrão é uma string vazia.
    :param length: Tamanho da string aleatória gerada para garantir unicidade. Por padrão é 10.
    :return: Caminho de um arquivo que não existe no diretório escolhido com a extensão desejada.
    """
    file_path = ""
    characters = string.ascii_letters + string.digits
    file_is_unique = False

    # Definindo o nome do arquivo inicial
    file_name = ''
    if len(extension) > 0 and len(base_file_name) > 0:
        file_name = '{}.{}'.format(base_file_name, extension)
    elif len(base_file_name) > 0:
        file_name = '{}'.format(base_file_name, extension)

    while not file_is_unique:

        # Obtendo o caminho do arquivo
        file_path = os.path.join(directory, file_name)

        # Verificando se o arquivo eh unico
        if (not os.path.isfile(file_path)) and (not os.path.isdir(file_path)):
            file_is_unique = True

        # Gerando novo nome de arquivo
        if len(extension) > 0 and len(base_file_name) > 0 :
            file_name = '{}_{}.{}'.format(base_file_name, ''.join(random.choices(characters, k=length)), extension)
        elif len(base_file_name) > 0 :
            file_name = '{}_{}'.format(base_file_name, ''.join(random.choices(characters, k=length)))
        elif len(extension) > 0:
            file_name = '{}.{}'.format(''.join(random.choices(characters, k=length)), extension)
        else:
            file_name = ''.join(random.choices(characters, k=length))

    return file_path

if __name__ == '__main__':

    # Obtendo o caminho do clang
    clang_path = shutil.which('clang')
    print('clang_path = {}'.format(clang_path))

    # Obtendo o caminho do programa
    source_file_path = os.path.realpath(sys.argv[1])
    print('programa = {}'.format(source_file_path))

    # Definindo o caminho do arquivo de bytecodes
    bytecodes_file_path = generate_unique_file_path(os.path.dirname(source_file_path), pathlib.Path(os.path.basename(source_file_path)).stem, 'bc')
    print('bytecodes_file_path = {}'.format(bytecodes_file_path))

    # Obtendo a representação intermediária
    args = [clang_path, '-emit-llvm', '-c', source_file_path, '-o', bytecodes_file_path]
    print('args = {}'.format(args))
    subprocess.run(args)

