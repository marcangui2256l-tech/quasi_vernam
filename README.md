# LFSR 8 bits et chiffrement quasi-Vernam

Projet réalisé en cours de cryptographie (Bachelor BSI Cyber, ISEN Ouest). Il implémente en Python :

- un **registre à décalage à rétroaction linéaire (LFSR)** de 8 bits ;
- un **filtre non linéaire** `g` qui produit les bits de la suite chiffrante ;
- un **chiffrement par flot de type quasi-Vernam** : chaque bit du message est combiné par XOR avec un bit de la suite chiffrante ;
- le **calcul de la période** du registre pour plusieurs jeux de coefficients.

## Fonctionnement

1. **LFSR** : l'état est une liste de 8 bits. À chaque pas, le bit de rétroaction est le XOR des cases sélectionnées par les coefficients. L'état se décale d'un cran vers la gauche et le nouveau bit est ajouté à droite.
2. **Filtre non linéaire** : trois cases de l'état (positions 2, 5 et 7) donnent `x1`, `x2`, `x3`. Le bit de sortie est :
   `g(x1, x2, x3) = x1 ⊕ x2 ⊕ (x2 · x3) ⊕ (x1 · x2 · x3)`
3. **Chiffrement** : le message est converti en bits, puis chaque bit est combiné par XOR avec le bit suivant de la suite chiffrante. Comme le XOR est son propre inverse, la **même fonction** chiffre et déchiffre, avec le même état initial et les mêmes coefficients.

## Jeux de coefficients testés

| Jeu | Coefficients | Période obtenue |
|---|---|---|
| 1 | `[1, 1, 0, 1, 1, 0, 0, 0]` | 51 |
| 2 | `[1, 0, 1, 1, 1, 0, 0, 0]` | 255 |
| 3 | `[1, 0, 0, 1, 1, 0, 0, 0]` | 127 |

Avec l'état initial `[0, 1, 1, 1, 0, 1, 1, 0]`. Le jeu 2 atteint la période maximale d'un registre de 8 bits (2⁸ − 1 = 255).

## Exemple

```
Chiffré : 52d8ac084b63d036d9
Clair   : Bonjour !
```

## Lancer le programme

```bash
python3 lfsr_quasi_vernam.py
```
Prérequis : Python 3, aucune bibliothèque externe.

Le programme affiche les premiers états du registre (vérification avec le tableau du cours), les périodes des trois jeux de coefficients, puis un exemple de chiffrement et de déchiffrement.

## Limites

Ce chiffrement est un **exercice pédagogique**. Un vrai chiffrement de Vernam (masque jetable) demande une clé aléatoire, aussi longue que le message et utilisée une seule fois. Ici, la suite chiffrante est générée par un registre de 8 bits : elle est déterministe et se répète au bout de la période. Il ne doit pas être utilisé pour protéger de vraies données.

## Auteur
Koffi Marc-Aurel Angui, étudiant en Bachelor BSI Cyber à l'ISEN Ouest (Nantes).
