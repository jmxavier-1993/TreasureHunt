import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configurações da tela e cores
LARGURA, ALTURA = 400, 500  # Aumentamos a altura para espaço dos botões
TAMANHO_CELULA = LARGURA // 7  # Ajustado para 7 células na largura
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Caça ao Tesouro")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (200, 200, 200)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)

# Configurações do jogo
tentativas = 10
tesouro_x, tesouro_y = random.randint(0, 6), random.randint(0, 6)
matriz = [["" for _ in range(7)] for _ in range(7)]
fonte = pygame.font.SysFont(None, 40)
fonte_pequena = pygame.font.SysFont(None, 30)

# Carregar a imagem do tesouro e redimensioná-la
icone_tesouro = pygame.image.load('C:/Caça ao Tesouro/tesouro-icone/tesouro.png')
icone_tesouro = pygame.transform.scale(icone_tesouro, (TAMANHO_CELULA, TAMANHO_CELULA))

# Distribuir os bônus e penalidades
bonus_posicoes = []


def distribuir_beneficios():
    global bonus_posicoes
    while len(bonus_posicoes) < 14:  # 3 "+1", 4 "+5", 5 "-1", 2 "-3"
        posicao = (random.randint(0, 6), random.randint(0, 6))
        if posicao != (tesouro_x, tesouro_y) and posicao not in bonus_posicoes:
            if len([x for x in bonus_posicoes if x[1] == "+1"]) < 3:
                bonus_posicoes.append((posicao, "+1"))
            elif len([x for x in bonus_posicoes if x[1] == "+5"]) < 4:
                bonus_posicoes.append((posicao, "+5"))
            elif len([x for x in bonus_posicoes if x[1] == "-1"]) < 5:
                bonus_posicoes.append((posicao, "-1"))
            elif len([x for x in bonus_posicoes if x[1] == "-3"]) < 2:
                bonus_posicoes.append((posicao, "-3"))


distribuir_beneficios()


# Função para desenhar o tabuleiro
def desenhar_tabuleiro():
    TELA.fill(BRANCO)
    for linha in range(7):
        for coluna in range(7):
            x = coluna * TAMANHO_CELULA
            y = linha * TAMANHO_CELULA
            pygame.draw.rect(TELA, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)

            if matriz[linha][coluna] == "X":
                cor = definir_cor_proximidade(linha, coluna)
                texto = fonte.render("X", True, cor)
                TELA.blit(texto, (x + TAMANHO_CELULA // 2 - 10, y + TAMANHO_CELULA // 2 - 20))
            elif matriz[linha][coluna] == "T":
                TELA.blit(icone_tesouro, (x, y))
            elif matriz[linha][coluna] in {"+1", "+5", "-1", "-3"}:
                texto = fonte.render(matriz[linha][coluna], True,
                                     AZUL if matriz[linha][coluna].startswith("+") else VERMELHO)
                TELA.blit(texto, (x + TAMANHO_CELULA // 2 - 15, y + TAMANHO_CELULA // 2 - 20))


# Função para definir cor com base na proximidade do tesouro
def definir_cor_proximidade(linha, coluna):
    distancia = abs(tesouro_x - linha) + abs(tesouro_y - coluna)
    if distancia == 0:
        return VERDE
    elif distancia <= 2:
        return AMARELO
    elif distancia <= 4:
        return LARANJA
    else:
        return VERMELHO


# Função para exibir os botões
def desenhar_botoes():
    pygame.draw.rect(TELA, CINZA, (10, ALTURA - 90, 150, 50))
    texto_tentativas = fonte_pequena.render(f"Tentativas: {tentativas}", True, PRETO)
    TELA.blit(texto_tentativas, (20, ALTURA - 80))

    pygame.draw.rect(TELA, CINZA, (LARGURA - 160, ALTURA - 90, 150, 50))
    texto_reiniciar = fonte_pequena.render("Reiniciar (R)", True, PRETO)
    TELA.blit(texto_reiniciar, (LARGURA - 150, ALTURA - 80))


def mostrar_mensagem(mensagem, cor):
    texto = fonte.render(mensagem, True, cor)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)


def main():
    global tentativas, matriz, tesouro_x, tesouro_y
    rodando = True

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

                if y < TAMANHO_CELULA * 7:
                    if (linha, coluna) == (tesouro_x, tesouro_y):
                        matriz[linha][coluna] = "T"
                        desenhar_tabuleiro()
                        mostrar_mensagem("Tesouro Encontrado!", VERDE)
                        rodando = False
                    elif matriz[linha][coluna] == "":
                        matriz[linha][coluna] = "X"
                        tentativas -= 1
                        for posicao, valor in bonus_posicoes:
                            if posicao == (linha, coluna):
                                matriz[linha][coluna] = valor
                                if valor == "+1":
                                    tentativas += 1
                                elif valor == "+5":
                                    tentativas += 5
                                elif valor == "-1":
                                    tentativas -= 1
                                elif valor == "-3":
                                    tentativas -= 3

                                # Verificar imediatamente se as tentativas são <= 0
                                if tentativas <= 0:
                                    desenhar_tabuleiro()
                                    mostrar_mensagem("GAME OVER", VERMELHO)
                                    rodando = False
                                break

                if LARGURA - 160 <= x <= LARGURA - 10 and ALTURA - 90 <= y <= ALTURA - 40:
                    tentativas = 10
                    matriz = [["" for _ in range(7)] for _ in range(7)]
                    tesouro_x, tesouro_y = random.randint(0, 6), random.randint(0, 6)
                    bonus_posicoes.clear()
                    distribuir_beneficios()
                    main()

                if tentativas == 0 and matriz[tesouro_x][tesouro_y] != "T":
                    matriz[tesouro_x][tesouro_y] = "T"
                    desenhar_tabuleiro()
                    pygame.display.flip()
                    mostrar_mensagem("GAME OVER", AMARELO)
                    rodando = False

        desenhar_tabuleiro()
        desenhar_botoes()
        pygame.display.flip()

    while True:
        mostrar_mensagem("Pressione R para reiniciar", AZUL)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    tentativas = 10
                    matriz = [["" for _ in range(7)] for _ in range(7)]
                    tesouro_x, tesouro_y = random.randint(0, 6), random.randint(0, 6)
                    bonus_posicoes.clear()
                    distribuir_beneficios()
                    main()


if __name__ == "__main__":
    main()
