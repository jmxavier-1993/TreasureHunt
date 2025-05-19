import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configurações gerais
LARGURA_INICIAL, ALTURA_INICIAL = 400, 500
TELA = pygame.display.set_mode((LARGURA_INICIAL, ALTURA_INICIAL))
pygame.display.set_caption("Caça ao Tesouro - Estágio 1")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (200, 200, 200)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)
ROXO = (128, 0, 128)

# Configurações por estágio
ESTAGIOS = [
    {"tamanho": 7, "tentativas": 10, "bonus": {"+1": 3, "+5": 4, "-1": 5, "-3": 2}},
    {
        "tamanho": 9,
        "tentativas": 12,
        "bonus": {"+1": 4, "+5": 5, "-1": 6, "-3": 3, "-5": 1},
    },
    {
        "tamanho": 11,
        "tentativas": 15,
        "bonus": {"+1": 5, "+5": 6, "-1": 7, "-3": 4, "-5": 2},
    },
    {
        "tamanho": 13,
        "tentativas": 18,
        "bonus": {"+1": 6, "+5": 7, "-1": 8, "-3": 5, "-5": 3, "+10": 1},
    },
    {
        "tamanho": 15,
        "tentativas": 20,
        "bonus": {"+1": 7, "+5": 8, "-1": 10, "-3": 6, "-5": 4, "+10": 2, "-10": 1},
    },
]

estagio_atual = 0
config = ESTAGIOS[estagio_atual]
TAMANHO_CELULA = LARGURA_INICIAL // config["tamanho"]
LARGURA, ALTURA = (
    config["tamanho"] * TAMANHO_CELULA,
    config["tamanho"] * TAMANHO_CELULA + 100,
)
TELA = pygame.display.set_mode((LARGURA, ALTURA))

# Variáveis do jogo
tentativas = config["tentativas"]
tesouro_x, tesouro_y = random.randint(0, config["tamanho"] - 1), random.randint(
    0, config["tamanho"] - 1
)
matriz = [["" for _ in range(config["tamanho"])] for _ in range(config["tamanho"])]
fonte = pygame.font.SysFont(None, 40)
fonte_pequena = pygame.font.SysFont(None, 30)
fonte_grande = pygame.font.SysFont(None, 60)

# Carregar a imagem do tesouro e redimensioná-la
try:
    icone_tesouro = pygame.image.load("tesouro.png")
    icone_tesouro = pygame.transform.scale(
        icone_tesouro, (TAMANHO_CELULA, TAMANHO_CELULA)
    )
except:
    # Caso a imagem não seja encontrada, usaremos um retângulo amarelo
    icone_tesouro = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA))
    icone_tesouro.fill(AMARELO)

bonus_posicoes = []


def distribuir_beneficios():
    global bonus_posicoes
    bonus_posicoes = []
    beneficios = []

    for tipo, quantidade in config["bonus"].items():
        beneficios.extend([tipo] * quantidade)

    random.shuffle(beneficios)

    while beneficios and len(bonus_posicoes) < len(beneficios):
        posicao = (
            random.randint(0, config["tamanho"] - 1),
            random.randint(0, config["tamanho"] - 1),
        )
        if posicao != (tesouro_x, tesouro_y) and posicao not in [
            x[0] for x in bonus_posicoes
        ]:
            bonus_posicoes.append((posicao, beneficios[len(bonus_posicoes)]))


def reiniciar_estagio():
    global tentativas, matriz, tesouro_x, tesouro_y, bonus_posicoes
    tentativas = config["tentativas"]
    matriz = [["" for _ in range(config["tamanho"])] for _ in range(config["tamanho"])]
    tesouro_x, tesouro_y = random.randint(0, config["tamanho"] - 1), random.randint(
        0, config["tamanho"] - 1
    )
    bonus_posicoes.clear()
    distribuir_beneficios()


def proximo_estagio():
    global estagio_atual, config, TAMANHO_CELULA, LARGURA, ALTURA, TELA
    estagio_atual += 1

    if estagio_atual >= len(ESTAGIOS):
        mostrar_mensagem("PARABÉNS! VOCÊ COMPLETOU TODOS OS ESTÁGIOS!", VERDE, 3000)
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    config = ESTAGIOS[estagio_atual]
    TAMANHO_CELULA = LARGURA_INICIAL // config["tamanho"]
    LARGURA, ALTURA = (
        config["tamanho"] * TAMANHO_CELULA,
        config["tamanho"] * TAMANHO_CELULA + 100,
    )
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(f"Caça ao Tesouro - Estágio {estagio_atual + 1}")
    reiniciar_estagio()


def desenhar_tabuleiro():
    TELA.fill(BRANCO)
    for linha in range(config["tamanho"]):
        for coluna in range(config["tamanho"]):
            x = coluna * TAMANHO_CELULA
            y = linha * TAMANHO_CELULA
            pygame.draw.rect(TELA, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)

            if matriz[linha][coluna] == "X":
                cor = definir_cor_proximidade(linha, coluna)
                texto = fonte.render("X", True, cor)
                TELA.blit(
                    texto, (x + TAMANHO_CELULA // 2 - 10, y + TAMANHO_CELULA // 2 - 20)
                )
            elif matriz[linha][coluna] == "T":
                TELA.blit(icone_tesouro, (x, y))
            elif matriz[linha][coluna] in config["bonus"].keys():
                texto = fonte.render(
                    matriz[linha][coluna],
                    True,
                    AZUL if matriz[linha][coluna].startswith("+") else VERMELHO,
                )
                TELA.blit(
                    texto, (x + TAMANHO_CELULA // 2 - 15, y + TAMANHO_CELULA // 2 - 20)
                )


def definir_cor_proximidade(linha, coluna):
    distancia = abs(tesouro_x - linha) + abs(tesouro_y - coluna)
    max_dist = (config["tamanho"] - 1) * 2
    if distancia == 0:
        return VERDE
    elif distancia <= max_dist * 0.2:
        return AMARELO
    elif distancia <= max_dist * 0.4:
        return LARANJA
    elif distancia <= max_dist * 0.6:
        return ROXO
    else:
        return VERMELHO


def desenhar_botoes():
    pygame.draw.rect(TELA, CINZA, (10, ALTURA - 90, 150, 50))
    texto_tentativas = fonte_pequena.render(f"Tentativas: {tentativas}", True, PRETO)
    TELA.blit(texto_tentativas, (20, ALTURA - 80))

    pygame.draw.rect(TELA, CINZA, (LARGURA - 160, ALTURA - 90, 150, 50))
    texto_reiniciar = fonte_pequena.render("Reiniciar (R)", True, PRETO)
    TELA.blit(texto_reiniciar, (LARGURA - 150, ALTURA - 80))

    # Mostrar estágio atual
    texto_estagio = fonte_pequena.render(f"Estágio: {estagio_atual + 1}/5", True, PRETO)
    TELA.blit(texto_estagio, (LARGURA // 2 - 50, ALTURA - 80))


def mostrar_mensagem(mensagem, cor, tempo=2000):
    texto = fonte_grande.render(mensagem, True, cor)
    pygame.draw.rect(
        TELA, BRANCO, (LARGURA // 4, ALTURA // 3, LARGURA // 2, ALTURA // 3)
    )
    TELA.blit(
        texto,
        (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2),
    )
    pygame.display.flip()
    pygame.time.delay(tempo)


def main():
    global tentativas, matriz, tesouro_x, tesouro_y, estagio_atual
    rodando = True

    reiniciar_estagio()

    while rodando:
        desenhar_tabuleiro()
        desenhar_botoes()
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN and tentativas > 0:
                x, y = evento.pos
                coluna = x // TAMANHO_CELULA
                linha = y // TAMANHO_CELULA

                if y < TAMANHO_CELULA * config["tamanho"]:
                    if (linha, coluna) == (tesouro_x, tesouro_y):
                        matriz[linha][coluna] = "T"
                        desenhar_tabuleiro()
                        mostrar_mensagem("Tesouro Encontrado!", VERDE)
                        pygame.time.delay(1500)
                        proximo_estagio()
                    elif matriz[linha][coluna] == "":
                        matriz[linha][coluna] = "X"
                        tentativas -= 1
                        for posicao, valor in bonus_posicoes:
                            if posicao == (linha, coluna):
                                matriz[linha][coluna] = valor
                                if valor.startswith("+"):
                                    tentativas += int(valor[1:])
                                else:
                                    tentativas -= int(valor[1:])

                                if tentativas <= 0:
                                    desenhar_tabuleiro()
                                    mostrar_mensagem("GAME OVER", VERMELHO)
                                    rodando = False
                                break

                if (
                    LARGURA - 160 <= x <= LARGURA - 10
                    and ALTURA - 90 <= y <= ALTURA - 40
                ):
                    reiniciar_estagio()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar_estagio()

        if tentativas == 0 and matriz[tesouro_x][tesouro_y] != "T":
            matriz[tesouro_x][tesouro_y] = "T"
            desenhar_tabuleiro()
            pygame.display.flip()
            mostrar_mensagem("GAME OVER", VERMELHO)
            rodando = False

    while True:
        mostrar_mensagem("Pressione R para reiniciar", AZUL, 1000)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar_estagio()
                    main()


if __name__ == "__main__":
    main()
