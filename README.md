# Car Race Pico W

Um jogo de corrida simples desenvolvido para o **Raspberry Pi Pico W** utilizando o display **Pimoroni Pico Display 2**. O jogador controla um carro que deve desviar de obstáculos em movimento e acumular pontos.  

---

## 🔹 Funcionalidades

- Controle do carro usando **botões físicos** (substituindo joystick).  
- Obstáculos gerados aleatoriamente, com aumento gradual da velocidade.  
- Pontuação baseada na sobrevivência do jogador.  
- Rankings locais com os 5 melhores scores.  
- Estrada com faixa central animada e bordas visíveis.  

---

## 🔹 Requisitos

- **Hardware**:  
  - Raspberry Pi Pico W  
  - Pimoroni Pico Display 2  
  - Dois botões físicos conectados aos pinos GPIO 5 e 6  

- **Software**:  
  - MicroPython para Raspberry Pi Pico W  
  - Biblioteca `picographics` da Pimoroni  
  - Biblioteca `pimoroni_bus`  

> ⚠️ **ATENÇÃO**: Antes de fazer upload do código para a placa, **é necessário instalar o firmware da Pimoroni** no Raspberry Pi Pico W. Caso contrário, a biblioteca `picographics` e o display não funcionarão corretamente.

---

## 🔹 Como Jogar

1. Conecte os botões físicos aos pinos GPIO 5 (esquerda) e 6 (direita).  
2. Faça o upload do código para o Pico W via **Thonny** ou outro editor compatível com MicroPython.  
3. O carro se move automaticamente para frente; use os botões para desviar dos obstáculos.  
4. O jogo termina se houver colisão e a pontuação será registrada no ranking.  

---

## 🔹 Estrutura do Código

- `draw_road()` → Desenha estrada, faixas e bordas.  
- `draw_car()` → Desenha o carro com luzes frontais.  
- `draw_obstacles()` → Desenha obstáculos com bordas.  
- `update_obstacles()` → Atualiza posição e adiciona novos obstáculos.  
- `check_collision()` → Verifica colisão do carro com obstáculos.  
- `game_tick()` → Loop principal do jogo, atualizando pontuação, obstáculos e desenho.  

---

## 🔹 Melhorias Futuras

- Adicionar sons usando buzzer ou speaker.  
- Implementar múltiplos níveis de dificuldade.  
- Persistência do ranking entre reinicializações da placa.  
- Suporte a joystick ou touchscreen.  

---

## 🔹 Referências

- [Pimoroni Pico Display 2](https://shop.pimoroni.com/products/pico-display)  
- [Picographics Library](https://github.com/pimoroni/picographics)  

---

**Divirta-se jogando! 🚗💨**
