print()
print("Carregando bibliotecas......")
import random
import time
import ftfy
import nltk
from fuzzywuzzy import fuzz
import os

try:
    nltk.data.find('corpora/words.zip')
except LookupError:
    nltk.download('words')

os.system('cls' if os.name == 'nt' else 'clear')

print("\n")
print("Bibliotecas carregadas com sucesso!\n")

conversas_file_path = [
    'conversas_Artes.txt',
    'conversas_Astronomia.txt',
    'conversas_Biologia.txt',
    'conversas_Chatbot_Duvidas.txt',
    'conversas_Despedidas.txt',
    'conversas_Dia_a_Dia.txt',
    'conversas_Filmes.txt',
    'conversas_Filosofia.txt',
    'conversas_Fisica.txt',
    'conversas_Geografia.txt',
    'conversas_Geral.txt',
    'conversas_Historia.txt',
    'conversas_Livros.txt',
    'conversas_Matematica.txt',
    'conversas_Pessoas_Famosas.txt',
    'conversas_Quimica.txt',
    'conversas_Saudacoes.txt',
    'conversas_Tecnologia.txt',
]

MAX_CHARS_PER_LINE = 120

# Verifica se o arquivo de conversas já existe, se não, cria um novo
for file_path in conversas_file_path:
    if not os.path.exists(file_path):
        open(file_path, 'w', encoding='utf-8').close()

print()

# Carrega as perguntas e respostas salvas anteriormente
conversas = {}
encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
for file_path in conversas_file_path:
    print(f"Lendo arquivo {file_path}")
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                for line_num, line in enumerate(file):
                    line = line.strip()
                    if not line or '=' not in line or line.count('=') > 1:
                        continue
                    user_input, bot_response = line.strip().split('=')
                    if user_input in conversas:
                        conversas[user_input].append(bot_response)
                    else:
                        conversas[user_input] = [bot_response]
                    print(f"Lendo linha {line_num + 1} do arquivo {file_path}\r", end="")
                else:
                    print(f'Leitura do arquivo {file_path} finalizada !!')
                break  # encerra o loop quando a codificação correta for encontrada
        except UnicodeDecodeError:
            continue
print()

# Função para verificar similaridade entre duas strings
def is_similar(str1, str2):
    return fuzz.ratio(str1.lower(), str2.lower()) > 70

user_feedback_asked = False
while True:
    print()
    user_input = input('Você: ').capitalize()

    # Verifica se o input está vazio ou se não contém nenhuma palavra reconhecida
    if not user_input or not any(word in user_input.lower() for word in nltk.corpus.words.words()):
        print('Chatbot: Nenhuma mensagem encontrada.')
        continue

    # Verifica se a pergunta já foi feita antes em qualquer arquivo
    found_similar_question = False
    for file_path in conversas_file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '=' not in line:
                    continue
                saved_question, _ = line.split('=', 1)
                if is_similar(user_input, saved_question):
                    found_similar_question = True
                    bot_response = line.split('=', 1)[1]
                    if not user_feedback_asked:
                        print('Chatbot: ', end='')
                        line_chars = 0
                        for char in ftfy.fix_text(bot_response):
                            print(ftfy.fix_text(char), end='', flush=True)
                            line_chars += 1
                            if char == '.' and line_chars > 100:
                                print('\n')
                                line_chars = 0
                            elif char == '.':
                                line_chars = 0
                            elif char == ':':
                                line_chars = 0
                            time.sleep(0.005 if ftfy.fix_text(char).isalnum() else 0.005)
                        print()

                        # Pergunta ao usuário se a resposta está correta apenas na primeira vez
                        user_feedback = input('Chatbot: Está correto? (sim/não) ').lower()
                        while user_feedback not in ['sim', 'não', 's', 'n']:
                            user_feedback = input('Chatbot: Por favor, responda "sim/s" ou "não/n": ').lower()

                        # Se a resposta estiver errada, adiciona a pergunta na lista perguntas_erradas
                        if "não" in user_feedback or "n" in user_feedback:
                            # Pede a resposta correta
                            bot_response = input('Chatbot: Qual é a resposta correta? ')
                            # Adiciona a nova conversa ao arquivo usando o caractere '=' para separar pergunta e resposta
                            with open(file_path, 'a', encoding='utf-8') as file:
                                file.write(f'{ftfy.fix_text(user_input)}={ftfy.fix_text(bot_response)}\n')
                            print('Chatbot: Ok, agora eu sei a resposta.')
                        user_feedback_asked = True

                    break

    # Se não encontrou uma pergunta parecida em nenhum arquivo, pede para o usuário digitar a resposta
    if not found_similar_question:
        print('Desculpe, não sei responder.')
        bot_response = input('Por favor, diga-me a resposta para a sua pergunta: ')
        # Adiciona a nova conversa ao arquivo usando o caractere '=' para separar pergunta e resposta
        with open(conversas_file_path[0], 'a', encoding='utf-8') as file:
            file.write(f'{ftfy.fix_text(user_input)}={ftfy.fix_text(bot_response)}\n')
        print('Chatbot: Ok, agora eu sei a resposta.')

    # Redefine a variável para a próxima iteração
    user_feedback_asked = False

    print()