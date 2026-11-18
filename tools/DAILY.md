# Rotina DIÁRIA - Virou Versos (@virouversos)
Roda todo dia de manhã e deixa agendado o post do dia às **20:00** (ver Horário único abaixo; America/Sao_Paulo, blogId 7921319), com um assunto novo em alta, transformado em mensagem que **inspira, encoraja, aumenta a autoconfiança e faz o mundo ser um lugar melhor**.
Leia também `tools/WEEKLY.md` (ética, voz editorial, playbook de crescimento, passos técnicos 6 a 9: artes, GitHub, Metricool, state.json). Em conflito, a ÉTICA vence.

## Regras do dia
1. Leia `tools/state.json`. Se a data de hoje estiver em `topical_done`, **não mexa**: já existe post do dia. Senão, faça o post de hoje e acrescente a data ao `topical_done`.
2. Se já existir post agendado para hoje no Metricool (getScheduledPosts) em data não protegida, **atualize-o** (updateScheduledPost) em vez de criar outro: no máximo 1 post por dia.
3. Formato (padrão **2 Reels : 1 carrossel**, sem relação com o dia da semana): olhe os 2 posts imediatamente anteriores a hoje no Metricool (publicados ou agendados). Se os dois foram Reel, hoje é **carrossel** (cover + 4 a 6 slides + slide final automático); caso contrário, hoje é **Reel** animado (build_reel, 25 a 35 s). Imagem única não entra mais na rotina. Horário: 20:00 (ver abaixo). Se já passou, use a próxima hora cheia futura (nunca no passado). Respeite a Cadência mensal abaixo.
4. Assunto: 1 por dia, **não é notícia**. É comportamento humano e vida real: ver "Pilares de conteúdo" abaixo. O gancho é um FATO real da semana sobre PESSOAS (celebridades, reality, viral, gente comum), anonimizado e filtrado, que vira lição de comportamento; nunca notícia dura (clima/COP, economia, política, cotação, números de decreto). Sem pessoa nomeada, sem marca, sem partido. Se o assunto for triste ou polêmico, use o ângulo de cuidado e esperança.

## Fórmula AIDA (obrigatória)
- **A**tenção (capa): título curto, simples e do dia a dia, no máximo 6 palavras, que prenda o olhar à primeira vista (ex.: "Seu valor não oscila", "Hoje você pode recomeçar"). Fale com "você". Sem jargão.
- **I**nteresse (slides 1-2): o fato do dia, verdadeiro e com fonte, ligado à vida real da pessoa.
- **D**esejo (slides 3-4): a imagem de como ela pode se sentir; mensagem fofa, acolhedora, positiva, que aumenta a autoconfiança ("Spoiler: você já é suficiente").
- **A**ção (último slide e legenda): uma "missão do dia" pequena e fácil (dizer algo a si mesma, mandar mensagem a alguém) + CTA: pergunta pessoal nos comentários + "Salve para ler nos dias difíceis e envie para quem precisa ouvir isso hoje".

## Gatilhos mentais (uso ético e honesto)
Identificação ("você que..."), pertencimento ("a gente"), reciprocidade (dar uma mensagem de presente), curiosidade honesta ("Spoiler:"), utilidade ("salve para reler"), altruísmo ("envie para quem precisa"), especificidade (número real da fonte), progresso (pequena missão). **Proibido:** falsa urgência, escassez inventada, prova social falsa, culpa, medo, clickbait.

## Tom
Fofo, caloroso, simples, no português do dia a dia. Frases curtas. Encoraje sem sermão e sem superioridade. Sem promessas milagrosas nem autoajuda vazia. Emojis só na legenda (1 a 3, corações e brilhos).

## Legenda
1ª linha: gancho com a palavra-chave + 1 emoji. Depois: fato do dia (com a fonte citada, ex. "segundo o Google Trends Brasil"), desejo, missão do dia, pergunta pessoal, "Salve... e envie...". No máximo 4 hashtags (1 do assunto, #poesiadoagora, #viroversos e uma de tema como #autoestima). Sempre mediaAltText. Saúde mental/sofrimento: linha do CVV 188.

## Fechamento
Commit/push (artes + state.json). Resumo curto: assunto, fonte (link), título/capa, horário, link do planner, "checagem ética feita".

## Horário único: 20:00 (America/Sao_Paulo)
Todos os posts saem às **20:00**, qualquer dia da semana (melhor média de audiência do Instagram deste perfil, segundo `getBestTimeToPostByNetwork`, e o mais estável entre os dias). Se 20:00 já passou, use a próxima hora cheia futura (nunca no passado).

## Cadência mensal (limite do plano gratuito: 20 posts publicados por mês, zera no dia 1)
- Dias 1 a 10 do mês: **1 post por dia**.
- Do dia 11 em diante: **dia sim, dia não**, em dias pares (12, 14, 16, ... 30), até completar os 20. Nunca deixe mais de 1 dia seguido sem post.
- Dezembro/2026: posts nos dias 1 a 10, 12, 14, 16, 18, 20, 22, 24, 26, 28 e 30 (dias 11, 25 e 31 sem post). Sextas com Reel: 4 e 18.
- Novembro/2026 (mês de transição, saldo ~14 posts em 13 dias): 1 post por dia até o dia 30.
- Antes de agendar, confira o saldo do mês (posts publicados + agendados no mês); se já chegou a 20, não agende.
- Em dia sem post pela cadência, não crie post nem marque `topical_done`.
A cada ~2 meses, reconsulte `getBestTimeToPostByNetwork` (instagram, blogId 7921319) e ajuste esta tabela.

## Personagens (Lume e Verso) e expressões

Todo post novo usa os mascotes (`tools/mascot.py`, `tools/stamp.py`; exemplo em `tools/apply_characters.py`). A expressão acompanha o conteúdo de cada slide:
- capa e conquistas/boas notícias: `happy`
- pergunta, curiosidade, dúvida no texto: `doubt`
- perda, saudade, preocupação leve (ex.: clima, "estou bem" que esconde): `sad`
- slide final (CTA) e ação/vitória: `celebrate` (Lume + Verso, usando `cta_final.png` como base)
- Posição: Verso embaixo à direita (700,850,440), Lume em cima à esquerda (-70,-70,400); conferir que não cobrem texto nem "@virouversos".
- Ética: tema pesado (tragédia, luto, violência) = nada de personagem alegre; usar `sad` discreto ou nenhum personagem.
- Alt text: descrever a expressão do personagem em cada slide.

## Gancho da capa (obrigatório)
Capa e primeira linha da legenda começam com PERGUNTA ou CURIOSIDADE que faça deslizar: "Você sabia que...?", "Qual é...?", "O que você ainda...?", um fato real surpreendente do assunto da semana. Evitar título só descritivo/poético ("Seu valor não oscila", "Balanço"). Ética: sem sensacionalismo, sem explorar tragédia, sem falsa urgência; o fato citado precisa ser verdadeiro e ter fonte. Script de referência: `tools/rehook.py` (arquivos h_slide_NN / h_post).

## Pilares de conteúdo (o que a página fala; alternar entre eles)
1. **Autoestima e confiança:** valor próprio, começar mesmo com medo, "você é capaz", não precisar de aprovação.
2. **Sucesso e notoriedade:** como pessoas comuns conquistam espaço, constância, humildade ao crescer, o que fica depois do aplauso, aparecer sem se perder.
3. **Esperança e fé:** recomeço, "vai passar", gratidão, acreditar no que ainda não se vê. Fé em sentido amplo e inclusivo (sem pregar religião específica nem criticar crença alguma).
4. **Bondade e gentileza:** gestos pequenos, quem ajuda sem plateia, ser a pessoa que faz diferença no dia de alguém.
5. **Reflexão sobre comportamentos ruins:** inveja, indiferença, julgamento, mentira, "falar mal por trás", quem some quando você precisa, humilhar para parecer grande, só aparecer na hora boa. Sempre no "a gente" ou no "quem", sem apontar pessoa, grupo ou caso real; termina com saída construtiva (como agir diferente, como se proteger, como ser quem não faz isso).
6. **Cenas do dia a dia:** ônibus, café, mensagem não respondida, família à mesa, segunda-feira, cansaço, o "estou bem" que não é.
7. **Gente que ganhou repercussão:** ver seção abaixo.

**Todo post parte de um FATO da semana sobre pessoas** (celebridade, reality, influenciador ou gente comum que viralizou) e vira lição de comportamento de um dos pilares acima. Fluxo:
1. **Buscar o que está sendo mais comentado esta semana** em portais de famosos e entretenimento (ex.: Quem, Contigo, Splash/UOL, Extra, O Povo Trends, Purepeople, Terra, Metrópoles) e no que viralizou nas redes (canaltech "virais da semana", G1 Pop). Leia a matéria, não só o título.
2. **Filtro de segurança do fato** (fofoca é a fonte menos confiável, então seja rígido): só use o que (a) foi dito ou publicado pela própria pessoa, ou (b) foi noticiado por 2 ou mais veículos, e dito como "foi noticiado". Rumor, "suposto", "teria", "fontes dizem" = descartar. Descartar também: saúde, morte, doença, luto, violência, processo judicial em andamento, vida íntima (traição, término com detalhes, sexo), menores de idade, humilhação de alguém.
3. **Nomes (regra combinada com o dono):** pode citar o nome de famoso muito comentado, inclusive em briga ou polêmica, SE o fato for comprovado (dito publicamente pela própria pessoa ou noticiado por 2 ou mais veículos, com a fonte lida no dia) e SE a mensagem do post for sempre positiva: aprendizado, crescimento, esperança, perdão, humildade, recomeço. Condições inegociáveis: (a) o nome aparece só na capa e/ou na legenda, em tom neutro de "segundo a imprensa"; o **poema** fala do comportamento e da lição, sem nome e sem tomar partido; (b) nunca dizer quem está certo ou errado, nunca ridicularizar, nunca insinuar; (c) nunca inventar frase ou intenção atribuída à pessoa; (d) nunca usar @, foto ou imagem; (e) fica de fora, SEM nome e sem tema: acusação grave ou crime, saúde, morte, luto, processo judicial em andamento, vida íntima (traição, término com detalhes), menores de idade, humilhação; (f) fato duvidoso, "suposto" ou de uma versão só = anonimizar ou descartar. Terminar sempre com a pergunta de aprendizado para o leitor ("e você, o que levaria disso?").
4. **Anonimizar (fato negativo ou duvidoso):** descrever o FENÔMENO, nunca a pessoa: "a indireta que viralizou", "o reality da semana", "a briga de duas famosas que dividiu a internet", "o término que parou a internet", "a apresentadora que se emocionou ao vivo". Sem nome, sem @, sem foto, sem marca. Quem conhece reconhece sozinho; quem não conhece entende igual.
5. **Escolher o pilar e a lição:** o fato é o gancho; o poema fala do COMPORTAMENTO por trás dele (indireta, inveja, vaidade, perdão em público, sucesso repentino, cancelamento, humildade, fé, recomeço) e termina com saída construtiva ("e você, o que faria diferente?"). Nunca tomar partido entre pessoas, nunca ridicularizar.
6. **Registrar a fonte** (link) no resumo do dia; a legenda cita "segundo a imprensa" quando houver fato noticiado. Sem fato que passe no filtro, use o pilar 6 (cenas do dia a dia).
Também sentir o clima do dia: data comemorativa, época do ano, semana do mês (cenário, não tema).
Evitar: notícia dura, números oficiais, política institucional, economia, cotação, clima/meio ambiente como pauta, jargão.
Regra de ouro (ética vence): fofoca/celebridade só como FENÔMENO anônimo, depois virar para o mundo real ("e o seu relacionamento? quem está do seu lado de verdade?"). Nunca repetir boato, acusação ou vida privada; nunca citar pessoas reais, marcas ou políticos pelo nome.

## Gente que ganhou repercussão (pilar 7)
Priorizar histórias de pessoas, sobretudo GENTE COMUM, que repercutiram e têm lado positivo ou lição (quem virou notícia por talento, constância, gentileza, superação, ou ganhou notoriedade de um jeito inesperado). Pode usar o fato como gancho e então tirar a lição de comportamento (por que isso tocou tanta gente? o que a gente faria?). Exemplos de pessoas: idosa que viralizou fazendo algo inesperado, gesto de gentileza filmado, superação, talento descoberto, vizinhança que se mobilizou, criança/pet fofo. Buscar em canaltech "virais da semana", G1 Fato ou Fake/Pop, UOL, Folha, portais regionais.
Como contar: descrever a cena sem nome e sem identificar (ex.: "uma senhora de 93 anos empinando pipa"), sem rosto/imagem da pessoa, só o fato noticiado. Virar para o leitor: "E você, o que ainda faria sem pedir licença?".
Nunca: expor, humilhar ou "cancelar" ninguém; pessoa privada identificável; vídeo de criança; pegadinha/constrangimento; boato; polêmica de influenciador. Se a história viral for de humilhação ou ataque a alguém, usar só o ângulo de acolhimento ao anônimo, sem repetir o caso, ou escolher outro.

## Padrão de qualidade do Reel (checar antes de agendar)
Baseado em guias de Reels 2026 (Metricool, AdaptlyPost, Agenciagram; são blogs de ferramentas, não fonte oficial do Instagram) e testado aqui: os números do perfil ainda são pequenos, então trate como hipótese e meça.
1. **Gancho no quadro 0:** o título em tela é PERGUNTA ou CURIOSIDADE de até 8 palavras (ex.: "Que boneca nasce de uma roupa rasgada?"), visível já no primeiro quadro, sem fade de entrada nem vinheta lenta. Título só descritivo ("Abayomi") reprova, e o gancho também não pode depender de um termo que o público não conhece ("Você conhece a Abayomi?" só atrai quem já conhece): abra com a curiosidade ou o benefício visível ("Que boneca nasce de uma roupa rasgada?") e revele o nome no meio do poema e na legenda.
2. **Duração 25 a 40 s** (30 a 60 s é a faixa recomendada), com 4 a 6 versos.
3. **Texto sempre na tela** (muita gente assiste sem som). Nada importante nos 250 px do topo e da base.
4. **Final em loop:** o fim volta ao título e emenda no início (já feito em `tools/reels2.py`, `T_LOOP`). Fechamento com PERGUNTA pessoal via `cta_lines` e `cta_title="Salve e envie"` (o padrão). **Nunca pedir curtida.**
5. **Legenda:** primeira linha repete o gancho (pergunta), pergunta pessoal, "Salve... e envie para...", máx. 4 hashtags, `mediaAltText`, `videoCoverMilliseconds` 1000 (a capa cai no título).
6. **Sinais que medimos:** envios, salvamentos, alcance e seguidores ganhos por post (`getAnalyticsDataByMetrics`). Compare Reel x carrossel após 2 semanas.
7. **Responder comentários** na primeira hora quando possível (isso é com o dono da conta).

## Gatilhos de legenda que já funcionam (usar sempre; não inventar fórmula nova)
Base: nosso melhor post até agora (poema do café, 11/11: maior alcance e único com salvamento) e o playbook do `WEEKLY.md` (pergunta pessoal +37% de comentários, pedir comentário +203%, pedir salvamento +92%; os números vêm de blogs de ferramentas e a amostra do perfil é pequena). Estrutura fixa da legenda:
1. **Primeira linha** = pergunta ou curiosidade que qualquer pessoa entende, igual à capa, com 1 emoji.
2. **Identificação:** uma frase "Se você já... / Se você anda..., esse poema é pra você." (a pessoa se vê no texto).
3. **Marque alguém:** "Marque quem anda precisando..." (foi o que o post do café usou).
4. **Pergunta pessoal** curta para comentar.
5. **"Salve para reler e envie para [pessoa específica]".** Nunca pedir curtida.
6. Máx. 4 hashtags, 1 delas de marca (#viroversos); sigla ou termo pouco conhecido só entre parênteses, nunca no gancho.
7. Fato de notícia só com fonte lida no dia; tradição ou lenda sempre dita como tal ("dizem que", "conta a tradição").
