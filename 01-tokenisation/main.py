import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I am Aksh Khurana"
tokens = enc.encode(text)

print("Tokens : ", tokens)

decoded = enc.decode(tokens)

print("Decoded Text : ", decoded)