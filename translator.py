from googletrans import Translator

translator = Translator()

def translate(prompt, src='ko'):
    prompt_en = translator.translate(prompt, src=src, dest='en').text
    print("Original prompt:", prompt)
    print("Translated prompt:", prompt_en)
    return prompt