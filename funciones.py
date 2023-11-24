def limpiar_input(input_text):
    # Convierte a mayúsculas, elimina espacios al inicio y al final, y quita tildes
    return input_text.upper().strip().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
