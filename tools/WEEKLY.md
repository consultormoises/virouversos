> ORIENTAÇÃO VIGENTE DE ASSUNTO: a página NÃO é de notícia. Os temas seguem os "Pilares de conteúdo" de `tools/DAILY.md` (autoestima, sucesso e notoriedade, esperança e fé, bondade, reflexão sobre comportamentos ruins, cenas do dia a dia, gente que ganhou repercussão). Onde este arquivo mandar pesquisar manchetes, use-as só para sentir o clima das pessoas. Em conflito, vale o DAILY.md e a ética.

# Rotina semanal – Virou Versos (@virouversos)

A página transforma os **assuntos em alta da semana** em versos **reflexivos e humanos**.
Esta rotina roda **toda segunda-feira de manhã** e prepara os 4 posts da semana (segunda a domingo).

## Pré-requisitos (confira antes de começar)
- Metricool conectado (marca "Virou Versos", `blogId` **7921319**, fuso `America/Sao_Paulo`).
- Repositório `moisessebrae-source/virouversos` com acesso de escrita (`add_repo` com `access: "push"`), clonado.
- `python3` com numpy, Pillow, openpyxl; `ffmpeg`; fontes Lora e Inter instaladas no sistema. Sem rede para pip: use só o que existe.
- Ferramentas deste diretório: `tools/viz.py`, `tools/feed.py`, `tools/reels2.py`.

## Slots da semana
> Atenção: horário e cadência vigentes estão em `tools/DAILY.md` (20:00 em todos os posts; 1 por dia até o dia 10, depois dia sim, dia não). A tabela abaixo é histórica.

| Dia | Horário | Formato | Tema visual sugerido |
|---|---|---|---|
| Segunda | 19:00 | Carrossel | conforme o assunto (veja abaixo) |
| Quarta | 19:00 | Imagem única | idem |
| Sexta | 19:00 | Reel animado | idem |
| Domingo | 10:00 | Carrossel (mais sentimental) | idem |

Temas visuais (nomes exatos usados no código): `"1. Ruídos do Agora"` (ondas de luz: tecnologia, notícias, ritmo acelerado),
`"2. Cidade em Verso"` (cidade ao entardecer: cotidiano, sociedade, cultura), `"3. O que a gente não diz"` (lua e névoa: emoções, silêncio, meio ambiente),
`"4. Fecha o Ano em Verso"` (nascer do sol: esperança, gratidão, balanço).

## Voz editorial da página (definida pelo dono)
A página não é de esquerda nem de direita. Os versos defendem, sem apontar partido, governo ou pessoa:
- **Senso crítico:** pensar por conta própria vale mais do que torcer. É um erro defender político ou ideia a qualquer custo, sem questionar. Escrever sobre dúvida, escuta, perguntar "e se eu estiver errado?", sem dizer em quem votar nem quem está certo.
- **Agir certo sem plateia:** valorizar quem faz a coisa correta fora do padrão, sem buscar aprovação nem aplauso (gestos anônimos, escolhas difíceis, coragem silenciosa).
- **Mundo real acima do mundo dos famosos:** convidar a olhar para o que está perto (vizinho, família, rua, o próprio dia) em vez de viver a vida alheia das celebridades. Falar do fenômeno, nunca citar celebridade ou marca.
- A crítica é sempre a um **comportamento humano comum** (fanatismo, vaidade, distração), nunca a um grupo, partido, religião ou pessoa. Tom de convite à reflexão, sem sermão e sem superioridade moral.
- Ao escolher assuntos da semana, prefira os que permitam esse olhar.

## Playbook de crescimento (viralização com ética)
Base: dados do Metricool 2026 (metricool.com/pt/algoritmo-instagram e /tendencias-instagram).
- **Sinais que mais pesam:** salvamentos, compartilhamentos (envio por DM), tempo de visualização e comentários longos. Carrossel recebe cerca de 9x mais salvamentos; Reel tem o maior tempo de visualização. Imagem única é o formato mais fraco: prefira carrossel e Reel.
- **CTA que funciona:** pedir comentário (+203%), pedir salvamento (+92%), fazer uma pergunta pessoal na legenda (+37% de comentários). **Nunca pedir curtida** (reduz). Fórmula: pergunta pessoal + "Salve para reler e envie para [alguém específico]".
- **Hashtags:** no máximo 4 (posts com muitas hashtags tiveram cerca de 31% menos visualizações). O Instagram indexa palavras da legenda e posts públicos aparecem no Google: ponha a palavra-chave do assunto na primeira linha (ex.: "Poema sobre o Enem", "Abayomi", "COP31").
- **Gancho:** capa do carrossel e primeiros 2 segundos do Reel com a frase mais forte do poema. Último slide/verso deve dar vontade de enviar a alguém.
- **72 horas:** cerca de 70% das visualizações vêm nos 3 primeiros dias. Postar às 19h (maior engajamento médio), 10h aos domingos.
- **Séries assinatura (reconhecimento):** segunda = "Verso da Semana" (carrossel); quarta = "O Avesso da Trend" (imagem ou carrossel curto: pega o que está mais buscado e mostra o lado humano, sem citar nomes e sem tomar lado); sexta = Reel curto com gancho; domingo = "Carta de Domingo" (carrossel sentimental para salvar).
- **Inspiração de assuntos:** além das manchetes, olhe Google Trends BR (trends.google.com/trending?geo=BR) e datas da semana. Itens de política, celebridades e esporte entram só pelo ângulo humano e comum (ex.: o preço das coisas que não têm preço, o aplauso que ninguém vê), conforme a voz editorial e a ética. Em dezembro: campanha "Retrospectiva em Verso" (2026 em versos, Carta ao eu de janeiro).
- Viral nunca justifica quebrar a ética: nada de clickbait, falsa urgência, polêmica vazia ou exploração de dor.

## Ética e cuidados (inegociáveis, valem para TODO post)
**Respeito e não discriminação**
- Nenhum conteúdo preconceituoso: nada que discrimine, estereotipe, ridicularize ou diminua pessoas por raça, cor, etnia, origem, região (ex.: nordestinos, nortistas), gênero, orientação sexual, identidade de gênero, religião, idade, deficiência, aparência, classe social ou profissão.
- Sem piadas, ironias ou metáforas que usem grupos como alvo. Linguagem inclusiva e digna; evitar termos pejorativos, capacitistas ou que naturalizem violência.
- Falar **sobre** temas e comunidades com respeito, nunca "em nome" de um grupo nem apropriando a voz de quem viveu a experiência. Em datas como Consciência Negra, Dia do Orgulho, Dia da Mulher e similares: tom de reconhecimento e escuta, sem folclorizar, sem clichês e sem transformar dor em estética.
- Pobreza, seca, doença, luto e violência: tratar pessoas com dignidade, como sujeitos, nunca como cenário nem como "inspiração" para os outros.

**Verdade e transparência**
- Só afirmar fatos que constem em fonte lida, com data desta semana. Não inventar números, falas, nomes ou causas. Se a fonte for incerta ou houver versões conflitantes, escolher outro assunto.
- Versos **originais**: nunca copiar ou parafrasear de perto poemas, letras ou textos existentes, e não imitar o estilo reconhecível de um autor vivo.
- Não sugerir que a página tem opinião oficial de governo, empresa ou instituição. Não usar nomes de marcas, empresas ou celebridades.

**Política e assuntos sensíveis**
- Neutralidade partidária total: sem apoio ou ataque a candidatos, partidos, governos ou movimentos; sem fazer eleição, impeachment ou polarização de matéria-prima. Se o assunto é político, escolher o ângulo humano e comum a todos (ex.: esperar, cuidar, a conta do mês) ou escolher outro assunto.
- Evitar saúde com orientação (diagnóstico, tratamento, vacina), religião como disputa, e tragédias recentes com mortos como matéria-prima.
- **Saúde mental:** não romantizar tristeza, automutilação ou suicídio, nem usar o tema como efeito poético. Se um poema tocar em sofrimento emocional, acrescentar à legenda uma linha de acolhimento ("Se estiver difícil, procure alguém de confiança. No Brasil, o CVV atende 24 horas pelo 188.") e evitar imagens de desesperança sem saída.
- Crianças e adolescentes: nada que os exponha, sexualize ou cite individualmente.

**Privacidade e imagem**
- Não citar nem retratar pessoas reais identificáveis (nome, rosto, voz). Nas artes só ilustrações próprias; não usar fotos de terceiros.
- Não expor dados pessoais de seguidores. Se responder a comentários algum dia, nunca expor o autor.

**Acessibilidade e boa-fé com o público**
- Sempre preencher `mediaAltText` descrevendo a arte e transcrevendo o poema.
- Evitar clickbait, manipulação emocional, falsas urgências e "marque 3 amigos ou terá azar". Chamadas para ação só convidam a refletir, salvar ou compartilhar.
- Se houver erro, corrigir o post (atualizar legenda ou trocar a mídia no Metricool) e registrar no resumo.

**Antes de agendar, faça esta checagem final** (e registre "checagem ética feita" no resumo):
1. Algum verso ofende, estereotipa ou ironiza algum grupo? 2. Todo fato está na fonte, com data da semana? 3. Há pessoa real, marca ou partido citado? 4. O assunto explora uma dor recente? 5. Há alt text? Se qualquer resposta indicar risco, reescreva ou troque o assunto.

## Passo a passo
1. **Estado.** Leia `tools/state.json`. Datas em `topical_done` já têm post baseado em assunto em alta: **não sobrescreva** esses posts.
   Liste os posts agendados da semana com `getScheduledPosts` (segunda 00:00 a domingo 23:59, fuso `America/Sao_Paulo`). Guarde `id` e `uuid` de cada um (o `id` muda após cada atualização).
2. **Pesquisa dos assuntos (obrigatória, com fontes reais).** Use WebSearch/WebFetch para ler páginas **desta semana**: Repórter Brasil (TV Brasil, tvbrasil.ebc.com.br), manchetes do dia de portais, Google Trends Brasil (`https://trends.google.com/trends/trendingsearches/daily?geo=BR&hl=pt-BR`), cultura, esporte, clima, tecnologia, educação.
   Confirme a data da fonte: notícia antiga não é "em alta". Escolha 4 assuntos, um por post.
3. **Critérios de seleção.**
   - Preferir assuntos humanos: educação, cultura, clima, esporte, tecnologia, cotidiano, datas comemorativas, saudade, esperança.
   - **Evitar:** tragédias com mortes como matéria-prima, boatos não confirmados, disputa partidária, ataque ou elogio a políticos/partidos, saúde com orientação médica, conteúdo que alimente ódio.
   - **Não citar pessoas reais nos versos** (nem mortos recentes). Falar do tema, não do nome.
   - Só afirmar fatos que estejam na fonte lida. Se houver número ou data, confira.
   - Se uma data comemorativa cair na semana (ex.: 20/11 Consciência Negra), priorize com respeito.
4. **Escrever os versos.** Português do Brasil, tom reflexivo, humano e acolhedor, sem moralismo, sem panfleto. Verso livre, 6 a 9 linhas (imagem única), 5 a 8 slides curtos (carrossel), 3 a 4 estrofes de 2 a 3 versos (Reel). Originais, nunca copiados de poemas existentes.
5. **Legenda** (siga o "Playbook de crescimento" abaixo). Primeira linha: palavra-chave do assunto + gancho + 1 emoji. Depois 1 a 2 parágrafos curtos (contexto honesto + convite à reflexão), uma pergunta pessoal para comentários e a chamada "Salve e envie para...".
   Hashtags no fim: no máximo 4, sendo 1 ou 2 do assunto + `#poesiadoagora #viroversos`.
6. **Artes e vídeo** (rodar a partir da pasta `tools`):
```python
import sys; sys.path.insert(0, "tools")
from feed import render_single, render_carousel
from reels2 import build_reel
render_single(tema, "Título", "verso 1\nverso 2\n...", "v2/AAAA-MM-DD_slug/post.png", seed=123)
n = render_carousel(tema, "Título", ["slide 1 (pode ter \n)", "slide 2", ...], "v2/AAAA-MM-DD_slug", seed=123)  # gera capa + slides + slide final; máx. 10 no total
build_reel(tema, "Título", [["verso", "verso"], ["verso", "verso"], ...], "v2/AAAA-MM-DD_slug/reel.mp4", label="ROTULO DO ASSUNTO", seed=123)
```
   Confira o resultado: abra 1 ou 2 PNGs (Read) e valide o vídeo com `ffprobe` (1080x1920, ~25 a 40 s, com áudio). Textos longos encolhem sozinhos; se algo ficar cortado, reescreva mais curto.
   Mantenha o nome da pasta ASCII (sem acentos), `v2/AAAA-MM-DD_slug/`.
7. **Subir mídias.** `git add`, `commit`, `git push` no repositório. URL pública: `https://raw.githubusercontent.com/moisessebrae-source/virouversos/main/v2/<pasta>/<arquivo>`.
8. **Metricool.**
   - Post já agendado no slot e data **não** listada em `topical_done`: `updateScheduledPost` (use `id` e `uuid` atuais), trocando `media`, `text`, `mediaAltText`.
   - Slot sem post: `createScheduledPost`.
   - Estrutura de `info`: `{"autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "", "hasNotReadNotes": false, "media": [urls], "mediaAltText": [], "providers": [{"network": "instagram"}], "publicationDate": {"dateTime": "AAAA-MM-DDTHH:MM:SS", "timezone": "America/Sao_Paulo"}, "shortener": false, "smartLinkData": {"ids": []}, "text": "...", "instagramData": {"type": "POST"}}`.
   - Reel: `"instagramData": {"type": "REEL", "showReelOnFeed": true}` e `"videoCoverMilliseconds": 1500` no `info`.
   - Nunca agende no passado: se o horário do slot da semana já passou, pule esse slot.
9. **Fechamento.** Atualize `tools/state.json` (acrescente as datas feitas a `topical_done`) e faça commit/push.
   Termine com um resumo curto: assunto de cada post, fonte (link), data/hora, link do planner do Metricool. Se algo falhar ou não houver assunto adequado, **mantenha o post existente** e avise no resumo.

## Padrões
- Instagram: `blogId` 7921319. Usuário prefere publicação automática (`autoPublish: true`).
- Nada de emojis dentro das artes. Emojis só na legenda.
- Não publicar informação não verificada. Em dúvida, escolha outro assunto.
