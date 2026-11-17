# Rotina DIÁRIA - Virou Versos (@virouversos)
Roda todo dia de manhã e deixa agendado o post do dia no **melhor horário do dia da semana** (tabela abaixo; America/Sao_Paulo, blogId 7921319), com um assunto novo em alta, transformado em mensagem que **inspira, encoraja, aumenta a autoconfiança e faz o mundo ser um lugar melhor**.
Leia também `tools/WEEKLY.md` (ética, voz editorial, playbook de crescimento, passos técnicos 6 a 9: artes, GitHub, Metricool, state.json). Em conflito, a ÉTICA vence.

## Regras do dia
1. Leia `tools/state.json`. Se a data de hoje estiver em `topical_done`, **não mexa**: já existe post do dia. Senão, faça o post de hoje e acrescente a data ao `topical_done`.
2. Se já existir post agendado para hoje no Metricool (getScheduledPosts) em data não protegida, **atualize-o** (updateScheduledPost) em vez de criar outro: no máximo 1 post por dia.
3. Formato: segunda a quinta, sábado e domingo = **carrossel** (cover + 4 a 6 slides + slide final automático). **Sexta = Reel** animado (build_reel, 25 a 35 s). Horário pela tabela abaixo. Se o horário do dia já passou, use a próxima hora cheia futura (nunca no passado).
4. Assunto: 1 assunto novo por dia, em alta HOJE (Google Trends BR: trends.google.com/trending?geo=BR, manchetes do dia). Pegue o que está em alta e vire **incentivo para o dia a dia**: autoestima, gentileza, coragem, recomeço, gratidão, união. Nada de citar pessoas, marcas ou partidos; o assunto só é o ponto de partida (ex.: "dólar hoje" vira "seu valor não oscila"). Se o assunto for triste ou polêmico, escolha outro ou o ângulo de cuidado e esperança.

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

## Horários (dados do Metricool para este perfil, Instagram)
Segunda 18:00 | Terça 17:00 | Quarta 18:00 | Quinta 20:00 | Sexta 17:00 (Reel) | Sábado 18:00 | Domingo 20:00.
A cada ~2 meses, reconsulte `getBestTimeToPostByNetwork` (instagram, blogId 7921319) e ajuste esta tabela.
