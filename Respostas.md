# Quanto tempo demora a leitura de um arquivo?
As leituras de arquivos variam entre 12ms e 41ms

# Quanto tempo demora a aplicação da sua rotina de aplicação de contorno?
A rotina de aplicação do contorno levou em média 52ms para ser concluída para cada arquivo de previsão. Para o contorno, levou 3ms O programa por inteiro tem aproximadamente 700ms de média de tempo de execução. 

O programa corta os dados de todos os arquivos de dias de previsão e salva em outro arquivo no diretório `forecast_files_crop`

# Caso fossemos executar (em serial) a sua rotina no pior cenário (50 modelos, 45 dias de previsão, 1000 contornos), quanto tempo ela demoraria?
Para 50 modelos diferentes com 45 dias de previsão, com média de leitura de arquivo de 32ms, e 1000 contornos diferentes: $50\cdot45\cdot(0.052+0.0265)\cdot1000\cdot0.003 = 529.875 \text{ segundos}$ ou 8,83 minutos

# Comente sobre as melhorias que podem ser implementadas no seu código
Poderia ser minimizado o número de loops e criação de listas, visto que são processos lentos.