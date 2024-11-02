import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configurações da tela e cores
LARGURA, ALTURA = 400, 500  # Aumentamos a altura para espaço dos botões
TAMANHO_CELULA = LARGURA // 4
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Caça ao Tesouro")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
CINZA = (200, 200, 200)

# Configurações do jogo
tentativas = 10
tesouro_x, tesouro_y = random.randint(0, 3), random.randint(0, 3)
matriz = [["" for _ in range(4)] for _ in range(4)]
fonte = pygame.font.SysFont(None, 40)
fonte_pequena = pygame.font.SysFont(None, 30)

# Função para desenhar o tabuleiro
def desenhar_tabuleiro():
    TELA.fill(BRANCO)
    # Desenhar células
    for linha in range(4):
        for coluna in range(4):
            x = coluna * TAMANHO_CELULA
            y = linha * TAMANHO_CELULA
            pygame.draw.rect(TELA, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)
            # Desenhar 'X' ou 'T' nas células cavadas
            if matriz[linha][coluna] == "X":
                texto = fonte.render("X", True, VERMELHO)
                TELA.blit(texto, (x + TAMANHO_CELULA // 2 - 10, y + TAMANHO_CELULA // 2 - 20))
            elif matriz[linha][coluna] == "T":
                texto = fonte.render("T", True, VERDE)
                TELA.blit(texto, (x + TAMANHO_CELULA // 2 - 10, y + TAMANHO_CELULA // 2 - 20))

# Função para exibir os botões
def desenhar_botoes():
    # Botão de Tentativas
    pygame.draw.rect(TELA, CINZA, (10, ALTURA - 90, 150, 50))
    texto_tentativas = fonte_pequena.render(f"Tentativas: {tentativas}", True, PRETO)
    TELA.blit(texto_tentativas, (20, ALTURA - 80))

    # Botão de Reiniciar
    pygame.draw.rect(TELA, CINZA, (LARGURA - 160, ALTURA - 90, 150, 50))
    texto_reiniciar = fonte_pequena.render("Reiniciar (R)", True, PRETO)
    TELA.blit(texto_reiniciar, (LARGURA - 150, ALTURA - 80))

def mostrar_mensagem(mensagem, cor):
    texto = fonte.render(mensagem, True, cor)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def main():
    global tentativas, tesouro_x, tesouro_y, matriz
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

                # Verificar se clicou na matriz
                if y < TAMANHO_CELULA * 4:
                    # Verificar se encontrou o tesouro
                    if (linha, coluna) == (tesouro_x, tesouro_y):
                        matriz[linha][coluna] = "T"
                        desenhar_tabuleiro()
                        mostrar_mensagem("Tesouro Encontrado!", VERDE)
                        rodando = False
                        break
                    else:
                        if matriz[linha][coluna] == "":
                            matriz[linha][coluna] = "X"
                            tentativas -= 1

                # Verificar se clicou no botão de reiniciar
                if LARGURA - 160 <= x <= LARGURA - 10 and ALTURA - 90 <= y <= ALTURA - 40:
                    # Reiniciar o jogo
                    tentativas = 10
                    matriz = [["" for _ in range(4)] for _ in range(4)]
                    tesouro_x, tesouro_y = random.randint(0, 3), random.randint(0, 3)
                    main()

                # Verificar se as tentativas acabaram
                if tentativas == 0 and matriz[tesouro_x][tesouro_y] != "T":
                    mostrar_mensagem("Não encontrou o tesouro!", VERMELHO)
                    rodando = False
                    break

        desenhar_tabuleiro()
        desenhar_botoes()
        pygame.display.flip()

    # Opção de reiniciar o jogo após o término
    while True:
        mostrar_mensagem("Pressione R para reiniciar", PRETO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    # Reiniciar o jogo
                    tentativas = 10
                    matriz = [["" for _ in range(4)] for _ in range(4)]
                    tesouro_x, tesouro_y = random.randint(0, 3), random.randint(0, 3)
                    main()

if __name__ == "_main_":
    main()