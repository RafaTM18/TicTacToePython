from math import inf
from random import choice

class Jogo(object):
    
    def __init__(self, primeiroJogador, alg):
        self.tabuleiro = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        if(primeiroJogador == 'USU'):
            self.usu = 'X'
            self.comp = 'O'
            self.jogadorAtual = self.usu
            print('O usuário começara jogando!')
        elif(primeiroJogador == 'COMP'):
            self.usu = 'O'
            self.comp = 'X'
            self.jogadorAtual = self.comp
            print('O computador começara jogando!')
        self.alg = alg

    def desenhaTabuleiro(self):
        print('   1   2   3')
        print('1 ', self.tabuleiro[0][0], '|', self.tabuleiro[0][1], '|', self.tabuleiro[0][2])
        print('  ---+---+---')
        print('2 ', self.tabuleiro[1][0], '|', self.tabuleiro[1][1], '|', self.tabuleiro[1][2])
        print('  ---+---+---')
        print('3 ', self.tabuleiro[2][0], '|', self.tabuleiro[2][1], '|', self.tabuleiro[2][2])

    # Retorna uma lista de posições vazias no tabuleiro
    def tabuleiroVazio(self):
        casaVazia = []
        for i in range(3):
            for j in range(3):
                if (self.tabuleiro[i][j] == '-'):
                    casaVazia.append([i, j])
        return casaVazia
    
    def confereVencedor(self):
        resultado = None
        # Confere se alguém ganhou na horizontal
        for i in range(3):
            if((self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2]) and self.tabuleiro[i][0] != '-'):
                resultado = self.tabuleiro[i][0]
        
        # Confere se alguém ganhou na vertical
        for i in range(3):
            if((self.tabuleiro[0][i] == self.tabuleiro[1][i] == self.tabuleiro[2][i]) and self.tabuleiro[0][i] != '-'):
                resultado = self.tabuleiro[0][i]

        # Confere se alguém ganhou na diagonal primária
        if((self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2]) and self.tabuleiro[0][0] != '-'):
            resultado = self.tabuleiro[0][0]

        # Confere se alguém ganhou na diagonal secundária
        if((self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0]) and self.tabuleiro[0][2] != '-'):
            resultado = self.tabuleiro[0][2]

        # Confere se ninguém ganhou ainda e se não há casas sobrando no tabuleiro
        # Isso então, significa um empate
        if(resultado == None and len(self.tabuleiroVazio()) == 0):
            resultado = 'Empate'
        return resultado

    def confereFimJogo(self):
        return self.confereVencedor() != None

    def confereValido(self, x, y):
        return self.tabuleiro[x][y] == '-'

    def jogar(self):
        # Função principal da classe, continua jogando enquanto não tiver um resultado
        while(not self.confereFimJogo()):
            self.desenhaTabuleiro()
            if(self.jogadorAtual == self.usu):
                self.turnUsu()
            else:
                print('Vez do computador')
                self.turnComp()

        self.desenhaTabuleiro()
        resultado = self.confereVencedor()
        if(resultado == self.usu):
            print('O vencedor do jogo é o usuário')
        elif(resultado == self.comp):
            print('O vencedor do jogo é o computador')
        else:
            print('O jogo terminou em um empate')

    def turnUsu(self):
        # Pede a casa desejada pro usuário
        pos = input(f'Digite a casa que você deseja colocar seu {self.jogadorAtual} (<linha> <coluna>): ').split()
        x = int(pos[0])
        y = int(pos[1])
        x -= 1
        y -= 1
        if(self.confereValido(x, y)):
            # Insere a operação no tabuleiro se ela for válida
            self.tabuleiro[x][y] = self.jogadorAtual
        else:
            print('Casa já ocupada!')
            self.turnUsu()
        self.jogadorAtual = self.comp

    def turnComp(self):
        melhorMov = {'Linha': -1, 'Coluna': -1, 'Valor': -inf}

        if(len(self.tabuleiroVazio()) == 9):
            # Essa parte é especifica pra versão do MiniMax
            # Como o programa demorava muito para escolher uma casa no inicio do jogo
            # Preferimos escolher uma posição aleatória, que além de mais rápido
            # torna o jogo mais dinamico, pois o MiniMax sempre retorna a casa 1,1 como melhor
            melhorMov['Linha'] = choice([0, 1, 2])
            melhorMov['Coluna'] = choice([0, 1, 2])
        else:
            for esp in self.tabuleiroVazio():
                x, y = esp[0], esp[1]
                self.tabuleiro[x][y] = self.comp
                melhorValor = self.alg.avaliaPos(self,0,False)
                self.tabuleiro[x][y] = '-'
                if(melhorValor > melhorMov['Valor']):
                    melhorMov['Valor'] = melhorValor
                    melhorMov['Linha'] = x
                    melhorMov['Coluna'] = y
        
        #Insere a melhor opção no tabuleiro
        self.tabuleiro[melhorMov['Linha']][melhorMov['Coluna']] = self.comp
        self.jogadorAtual = self.usu


class MiniMax(object):
    def __init__(self, primeiroJogador):
        if(primeiroJogador == 'USU'):
            self.usu = 'X'
            self.comp = 'O'
        elif(primeiroJogador == 'COMP'):
            self.usu = 'O'
            self.comp = 'X'

    def avaliaPos(self, jogo, profund, jogMax):
        # Confere se a arvore chegou num estado terminal e retorna o valor apropriado
        if(jogo.confereFimJogo()):
            result = jogo.confereVencedor()
            if(result == self.comp):
                return 1
            elif(result == self.usu):
                return -1
            else: 
                return 0
        
        if(jogMax):
            # Percorre o tabuleiro por casas vazias e dá um valor para aquela posição, retornando o maior valor
            melhorVal = -inf
            for esp in jogo.tabuleiroVazio():
                x, y = esp[0], esp[1]
                jogo.tabuleiro[x][y] = self.comp
                val = self.avaliaPos(jogo, profund + 1, False)
                jogo.tabuleiro[x][y] = '-'
                melhorVal = max(melhorVal, val)

        else:
            # Percorre o tabuleiro por casas vazias e dá um valor para aquela posição, retornando o menor valor
            melhorVal = inf
            for esp in jogo.tabuleiroVazio():
                x, y = esp[0], esp[1]
                jogo.tabuleiro[x][y] = self.usu
                val = self.avaliaPos(jogo, profund + 1, True)
                jogo.tabuleiro[x][y] = '-'
                melhorVal = min(melhorVal, val)
                
        return melhorVal


def main():
    primeiroJogador = 'COMP'
    minimax = MiniMax(primeiroJogador)
    jogo = Jogo(primeiroJogador, minimax)
    jogo.jogar()

if __name__ == '__main__':
    main()