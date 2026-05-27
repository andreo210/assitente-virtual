# ============================================
# ASSISTENTE VIRTUAL COM PLN EM PYTHON
# ============================================
#
# Funcionalidades:
#
# 1. Text To Speech (Texto para voz)
# 2. Speech To Text (Voz para texto)
# 3. Comandos de voz:
#    - Abrir YouTube
#    - Pesquisar na Wikipedia
#    - Procurar farmácia próxima
#    - Abrir Google
#    - Encerrar assistente
#
# ============================================

import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import requests
import json
import os


# ============================================
# CONFIGURAÇÕES
# ============================================

wikipedia.set_lang("pt")

engine = pyttsx3.init()

voices = engine.getProperty('voices')

# Seleciona voz em português se disponível
for voice in voices:
    if "portuguese" in voice.name.lower():
        engine.setProperty('voice', voice.id)

engine.setProperty('rate', 180)


# ============================================
# TEXT TO SPEECH
# ============================================

def falar(texto):

    print(f"\nAssistente: {texto}")

    engine.say(texto)

    engine.runAndWait()


# ============================================
# SPEECH TO TEXT
# ============================================

def ouvir():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nOuvindo...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        comando = recognizer.recognize_google(
            audio,
            language='pt-BR'
        )

        print(f"\nVocê disse: {comando}")

        return comando.lower()

    except sr.UnknownValueError:

        falar("Não consegui entender.")

        return ""

    except sr.RequestError:

        falar("Erro ao conectar ao serviço.")

        return ""


# ============================================
# PESQUISAR WIKIPEDIA
# ============================================

def pesquisar_wikipedia(comando):

    termo = comando.replace(
        "pesquisar",
        ""
    ).replace(
        "wikipedia",
        ""
    ).strip()

    if termo == "":
        falar("Informe o termo da pesquisa.")
        return

    try:

        resultado = wikipedia.summary(
            termo,
            sentences=2
        )

        falar(resultado)

    except Exception:

        falar("Não encontrei resultados.")


# ============================================
# ABRIR YOUTUBE
# ============================================

def abrir_youtube():

    falar("Abrindo YouTube")

    webbrowser.open(
        "https://www.youtube.com"
    )


# ============================================
# ABRIR GOOGLE
# ============================================

def abrir_google():

    falar("Abrindo Google")

    webbrowser.open(
        "https://www.google.com"
    )


# ============================================
# FARMÁCIA MAIS PRÓXIMA
# ============================================

def abrir_farmacia():

    falar("Procurando farmácia próxima")

    webbrowser.open(
        "https://www.google.com/maps/search/farmacia+proxima"
    )


# ============================================
# PROCESSAR COMANDOS
# ============================================

def executar_comando(comando):

    if "youtube" in comando:

        abrir_youtube()

    elif "google" in comando:

        abrir_google()

    elif "farmácia" in comando or "farmacia" in comando:

        abrir_farmacia()

    elif "wikipedia" in comando or "pesquisar" in comando:

        pesquisar_wikipedia(comando)

    elif "encerrar" in comando or "sair" in comando:

        falar("Encerrando assistente virtual")

        return False

    else:

        falar("Comando não reconhecido")

    return True


# ============================================
# MAIN
# ============================================

def main():

    falar("Assistente virtual iniciada")

    ativo = True

    while ativo:

        comando = ouvir()

        if comando != "":

            ativo = executar_comando(comando)


# ============================================
# EXECUÇÃO
# ============================================

if __name__ == "__main__":

    main()