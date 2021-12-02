from generate import Generate

prefix = "今天我放学回到家，看到爸爸阴沉的脸，我知道要遭殃了。我这次期末考得了28分。"
generated = Generate().generate(prefix)
print(generated)