from graph_of_thoughts.drawer import Tokenizer, Drawer
if __name__ == '__main__':
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    sequence = [START_TOKEN, 2, 18, 10, 28,END_TOKEN]
    result = drawer.decode(sequence)
    print(result)