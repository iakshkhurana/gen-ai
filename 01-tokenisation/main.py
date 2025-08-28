import tiktoken
# tiktoken -> enc = tiktoken.get_encoding / tiktoken.encoding_for_model
# enc.encode / enc.decode

enc = tiktoken.encoding_for_model("gpt-4o")

tokens = enc.encode("My name is Aksh")

print(tokens)

decoded = enc.decode(tokens)

print(decoded)