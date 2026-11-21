"""LFSR 8 bits + filtre non lineaire g + chiffrement quasi-Vernam (d'apres le tableau)."""

TAPS_FILTRE = (2, 5, 7)          # cases utilisees pour x1, x2, x3

COEFS = {
    1: [1, 1, 0, 1, 1, 0, 0, 0],
    2: [1, 0, 1, 1, 1, 0, 0, 0],
    3: [1, 0, 0, 1, 1, 0, 0, 0],
}


def g(x1, x2, x3):
    return x1 ^ x2 ^ (x2 & x3) ^ (x1 & x2 & x3)


def step(state, coefs):
    """Un pas : retourne (nouvel_etat, z_t). z_t est calcule sur l'etat courant."""
    z = g(*(state[i] for i in TAPS_FILTRE))
    fb = 0
    for c, x in zip(coefs, state):
        fb ^= c & x
    return state[1:] + [fb], z          # decalage a gauche, bit ajoute a droite


def keystream(state, coefs):
    state = list(state)
    while True:
        state, z = step(state, coefs)
        yield z


def periode(state, coefs, limite=1000):
    s0 = list(state)
    s = list(state)
    for t in range(1, limite + 1):
        s, _ = step(s, coefs)
        if s == s0:
            return t
    return None


def bits_de_octets(data):
    return [(b >> (7 - i)) & 1 for b in data for i in range(8)]


def octets_de_bits(bits):
    return bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))


def quasi_vernam(data, etat_initial, coefs):
    ks = keystream(etat_initial, coefs)
    return octets_de_bits([p ^ next(ks) for p in bits_de_octets(data)])


if __name__ == "__main__":
    X0 = [0, 1, 1, 1, 0, 1, 1, 0]       # etat t:0 du tableau

    # Verification avec le tableau (jeu 1)
    s = X0
    for t in range(4):
        print(f"t:{t}", "".join(map(str, s)))
        s, _ = step(s, COEFS[1])
    print("z0..z3 =", [z for z, _ in zip(keystream(X0, COEFS[1]), range(4))])

    # Experimentations
    for n, c in COEFS.items():
        print(f"Jeu ({n}) {c} : periode = {periode(X0, c)}")

    # Chiffrement / dechiffrement
    msg = "Bonjour !".encode()
    chiffre = quasi_vernam(msg, X0, COEFS[1])
    print("Chiffre :", chiffre.hex())
    print("Clair   :", quasi_vernam(chiffre, X0, COEFS[1]).decode())
