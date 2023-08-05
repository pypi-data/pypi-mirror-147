import random
import string


def gpass():
    tamanho = int(input('Qual o tamanho da senha que deseja? '))
    if tamanho <= 8:
        tamanho = int(input('Para a sua senha ser mais segura escolha acima de 8 caracteres: '))

    chars = string.ascii_letters + string.digits + '~!@#$%&*()_+'

    rnd = random.SystemRandom()

    passwd = (''.join(rnd.choice(chars) for _ in range(tamanho)))

    return print(passwd)


if __name__ == '__main__':
    gpass()
