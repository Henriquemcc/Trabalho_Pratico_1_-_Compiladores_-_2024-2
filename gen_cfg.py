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

    # Obtendo o caminho do opt
    opt_path = shutil.which('opt')
    print('opt_path = {}'.format(opt_path))

    # Obtendo o caminho do llc
    llc_path = shutil.which('llc')
    print('llc_path = {}'.format(llc_path))

    # Obtendo o caminho do programa
    source_file_path = os.path.realpath(sys.argv[1])
    print('programa = {}'.format(source_file_path))

    # Obtendo a representação intermediária
    code_generation_options = ['O0', 'O1', 'O2', 'O3']
    for code_generation_option in code_generation_options:

        # Definindo o caminho do arquivo de bytecodes
        bytecodes_file_path = "{}_{}".format(pathlib.Path(os.path.basename(source_file_path)).stem, code_generation_option)
        bytecodes_file_path = generate_unique_file_path(os.path.dirname(source_file_path), bytecodes_file_path, 'bc')
        print('bytecodes_file_path = {}'.format(bytecodes_file_path))

        # Definido os argumentos para executar o Clang
        args = [clang_path, '-emit-llvm', '-S', source_file_path, '-o', bytecodes_file_path]
        print('args = {}'.format(args))

        # Executando o Clang
        subprocess.run(args)

        # Substituindo o 'optnone' por nada
        with open(bytecodes_file_path, 'r') as bytecodes_file:
            bytecodes_file_data = bytecodes_file.read()
        bytecodes_file_data = bytecodes_file_data.replace('optnone', '')
        with open(bytecodes_file_path, 'w') as bytecodes_file:
            bytecodes_file.write(bytecodes_file_data)

        # Definindo o caminho do arquivo da linguagem intermediária
        intermediary_language_file_path = "{}_{}".format(pathlib.Path(os.path.basename(source_file_path)).stem, code_generation_option)
        intermediary_language_file_path = generate_unique_file_path(os.path.dirname(source_file_path), intermediary_language_file_path, 'dot')
        print('intermediary_language_file_path = {}'.format(intermediary_language_file_path))

        # Definindo os argumentos para executar o Opt
        args = [opt_path, '-passes=default<{}>,dot-cfg'.format(code_generation_option), bytecodes_file_path]
        print('args = {}'.format(args))

        # Executando o Opt
        subprocess.run(args)

        # Definindo o caminho do arquivo assembly
        assembly_file_path = "{}_{}".format(pathlib.Path(os.path.basename(intermediary_language_file_path)).stem, code_generation_option)
        assembly_file_path = generate_unique_file_path(os.path.dirname(source_file_path), assembly_file_path, 's')
        print('assembly_file_path = {}'.format(assembly_file_path))

        # Definindo os argumentos para executar o Llc
        args = [llc_path, intermediary_language_file_path, '-o', assembly_file_path]

        # Executando o Llc
        subprocess.run(args)
