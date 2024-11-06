# Maquina de Encriptacion

```python

class TuringEncryption:
    def __init__(self):
        self.key_array = [7, 13, 17, 23, 29, 31, 37, 41, 43, 47]
        self.chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        self.substitution_map = {
            self.chars[i]: self.chars[(i + 7) % len(self.chars)] 
            for i in range(len(self.chars))
        }
    def is_valid_input(self, text):
        return all(char in self.chars for char in text)

    def apply_transformation(self, char, position):
        if char in self.chars:
            idx = self.chars.index(char)
            key = self.key_array[position % 10]
            new_idx = (idx + key) % len(self.chars)
            return self.chars[new_idx]
        return char

    def reverse_transformation(self, char, position):
        if char in self.chars:
            idx = self.chars.index(char)
            key = self.key_array[position % 10]
            new_idx = (idx - key) % len(self.chars)
            return self.chars[new_idx]
        return char

    def encrypt(self, text):
        if not text or not self.is_valid_input(text):
            raise ValueError("El texto solo debe contener letras y números")
        transformed = ""
        for i, char in enumerate(text):
            transformed += self.apply_transformation(char, i)
        encrypted = ""
        for char in transformed:
            encrypted += self.substitution_map.get(char, char)
        final = "E#" + encrypted + "#E"
        return final

    def decrypt(self, encrypted):
        if not encrypted or len(encrypted) < 4:
            raise ValueError("Texto encriptado inválido")
        if not (encrypted.startswith("E#") and encrypted.endswith("#E")):
            raise ValueError("Formato de encriptación inválido")
        encrypted = encrypted[2:-2]
        reverse_sub_map = {v: k for k, v in self.substitution_map.items()}
        unsubstituted = ""
        for char in encrypted:
            unsubstituted += reverse_sub_map.get(char, char)
        final = ""
        for i, char in enumerate(unsubstituted):
            final += self.reverse_transformation(char, i)

        return final    
        
```

### Para ver mas codiog abrir el archivo de encrypt.py dentro de este repositorio