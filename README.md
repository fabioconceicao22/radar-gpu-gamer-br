# Radar GPU Gamer BR

Dashboard em Streamlit para comparar placas de vídeo por preço, desempenho e custo-benefício.

## Automação de preços

Os produtos e links monitorados ficam em `data/links.csv`. O coletor:

- valida e remove links duplicados;
- identifica a loja pelo domínio;
- pesquisa novamente o produto na loja e avalia links compatíveis com o modelo;
- compara o link cadastrado com os candidatos encontrados e seleciona a menor oferta válida;
- tenta obter o preço via JSON-LD, seletor específico da loja e texto da página;
- repete tentativas em falhas temporárias;
- grava URL final, status, erro e data da coleta em `data/precos_coletados.csv`.

O workflow `Atualizar preços das GPUs` roda duas vezes por dia e também pode ser iniciado manualmente na aba **Actions**. Quando há mudanças, o próprio workflow atualiza o CSV.

O dashboard diferencia valores automáticos de valores de referência, mostra o horário da última coleta e recomenda confirmar preço, estoque e frete na loja antes da compra.

## Recursos do dashboard

- temas claro e escuro;
- pesquisa por GPU ou modelo;
- filtros combináveis por marca, loja, VRAM, preço e origem;
- ordenação por custo, desempenho, desconto ou score;
- acesso direto à oferta selecionada.

## Executar localmente

```bash
python -m pip install -r requirements.txt
playwright install chromium
python coletar_precos.py
streamlit run Radar.py
```

## Formato de `data/links.csv`

Use CSV separado por ponto e vírgula com as colunas:

```text
produto;link;loja
GeForce RTX 4060 8GB;https://exemplo.com/produto;Loja
```

As colunas antigas extras continuam sendo aceitas.

