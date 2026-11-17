# Rotina semanal – Virou Versos (@virouversos)

A página transforma os **assuntos em alta da semana** em versos **reflexivos e humanos**.
Esta rotina roda **toda segunda-feira de manhã** e prepara os 4 posts da semana (segunda a domingo).

## Pré-requisitos (confira antes de começar)
- Metricool conectado (marca "Virou Versos", `blogId` **7921319**, fuso `America/Sao_Paulo`).
- Repositório `moisessebrae-source/virouversos` com acesso de escrita (`add_repo` com `access: "push"`), clonado.
- `python3` com numpy, Pillow, openpyxl; `ffmpeg`; fontes Lora e Inter instaladas no sistema. Sem rede para pip: use só o que existe.
- Ferramentas deste diretório: `tools/viz.py`, `tools/feed.py`, `tools/reels2.py`.

## Slots da semana
| Dia | Horário | Formato | Tema visual sugerido |
|---|---|---|---|
| Segunda | 19:00 | Carrossel | conforme o assunto (veja abaixo) |
| Quarta | 19:00 | Imagem única | idem |
| Sexta | 19:00 | Reel animado | idem |
| Domingo | 10:00 | Carrossel (mais sentimental) | idem |

Temas visuais (nomes exatos usados no código): `"1. Ruídos do Agora"` (ondas de luz: tecnologia, notícias, ritmo acelerado),
`"2. Cidade em Verso"` (cidade ao entardecer: cotidiano, sociedade, cultura), `"3. O que a gente não diz"` (lua e névoa: emoções, silêncio, meio ambiente),
`"4. Fecha o Ano em Verso"` (nascer do sol: esperança, gratidão, balanço).

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
5. **Legenda.** Primeira linha: gancho com o assunto + 1 emoji. Depois 2 parágrafos curtos (contexto honesto do assunto + convite à reflexão), uma pergunta para comentários e chamada para salvar/compartilhar.
   Hashtags no fim: 3 do assunto + `#poesiadoagora #poesia #poetasdoinstagram #viroversos`.
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
