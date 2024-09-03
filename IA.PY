import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import os

sns.set(style="whitegrid")

# Definições e carregamento de dados
cursos_validos = [
    "Engenharia",
    "Direito",
    "Psicologia",
    "Adm",
    "CC",
    "Medicina",
    "Historia",
    "Biologia",
    "Matematica",
    "Letras",
    "Filosofia",
    "EdFisica",
    "ArtesVisuais",
    "Musica",
    "Geografia",
    "Sociologia",
    "Economia",
    "EngCivil",
    "Quimica",
    "Fisica",
]

generos_validos = [
    "M",
    "F",
    "NB",
]

# df = DataFrame, uma variável criada para ler o arquivo CSV.
df = pd.read_csv("tabela.csv")

# Identifica e remove valores ausentes
df = df.dropna()

# Remove IDs duplicados
df = df.drop_duplicates(subset=["id_estudante"])

# Aqui definimos que a idade não pode ser menor que 0
# embaixo que a media_geral tem que ser entre 0 e 10
# o id_estudante tem que ser diferente de 0
df = df[df["idade"] >= 0]
df = df[(df["media_geral"] >= 0) & (df["media_geral"] <= 10)]
df = df[df["id_estudante"] != 0]

# Depois de todo o processo de verificação de valores ausentes, remoção de valores que não existem ou exclusão de dado duplicado, ele salva e corrige a tabela.
df.to_csv("dados_corrigidos.csv", index=False)

# Aqui eu pego a variável df (DataFrame), menciono a coluna idade e digo que ela recebe a "idade" como int, faço a mesma coisa pra horas estudo
# mas mudo na media geral pra float devido às notas nem sempre serem arredondadas.
# Eu coloquei o genero como category ao invés de object porque pelo que foi pesquisado, colunas que têm um valor fixo mais limitado, no caso como genero
# só tem apenas 3 valores, e participa_atividades_extra tem apenas 2, é mais eficiente o uso do category pela eficiência da memória, desempenho e
# a integridade de dados.
df["idade"] = df["idade"].astype(int)
df["horas_estudo_semana"] = df["horas_estudo_semana"].astype(int)
df["media_geral"] = df["media_geral"].astype(float)
df["genero"] = df["genero"].astype("category")
df["participa_atividades_extra"] = df["participa_atividades_extra"].astype("category")


def adicionar_informacoes():
    # Aqui gera automaticamente o ID, impossibilitando o usuário de colocar o ID por conta própria pra evitar conflitos e erros.
    novo_id = df["id_estudante"].max() + 1 if not df.empty else 1
    # Aqui é um loop pra fazer a validação. (tem varios desses)
    while True:
        curso = input("Informe o curso: ")
        if curso in cursos_validos:
            break
        else:
            print("Curso inválido. Por favor, escolha um curso da lista válida.")

    while True:
        genero = input("Informe o gênero: ")
        if genero in generos_validos:
            break
        else:
            print("Gênero não reconhecido. Por favor, escolha um gênero válido.")

    while True:
        horas_estudo = int(input("Informe as horas de estudo por semana: "))
        if 0 <= horas_estudo <= 24:
            break
        else:
            print("O Dia só tem 24 horas.")

    idade = int(input("Informe a idade: "))

    while True:
        media_geral = float(input("Informe a média geral: "))
        if 0 <= media_geral <= 10:
            break
        else:
            print("A média geral deve estar entre 0 e 10.")

    # Adiciona as novas informações ao DataFrame
    novo_registro = {
        "id_estudante": novo_id,
        "curso": curso,
        "genero": genero,
        "horas_estudo_semana": horas_estudo,
        "idade": idade,
        "media_geral": media_geral,
    }
    df.loc[len(df)] = novo_registro
    df.to_csv("dados_corrigidos.csv", index=False)
    print("Informações adicionadas com sucesso!")


def exibir_tabelas_por_genero():
    estatisticas_por_genero = df.groupby("genero").agg(
        {
            "media_geral": ["mean", "median", lambda x: x.mode()[0], "std"],
            "horas_estudo_semana": ["mean", "median", lambda x: x.mode()[0], "std"],
        }
    )

    # aqui eu só to mudando ao inves de aparecer como mean, median ele aparece do jeitinho que tá escrito ali em baixo, facilita a leitura!

    estatisticas_por_genero.columns = [
        "Média Média Geral",
        "Mediana Média Geral",
        "Moda Média Geral",
        "Desvio Padrão Média Geral",
        "Média Horas Estudo",
        "Mediana Horas Estudo",
        "Moda Horas Estudo",
        "Desvio Padrão Horas Estudo",
    ]
    distribuicao_genero = df["genero"].value_counts(normalize=True) * 100

    fig, axs = plt.subplots(2, 1, figsize=(16, 10), tight_layout=True)

    # esse código abaixo está gerando e estilizando o gráfico pra ele ficar legivel e bonito (ou quase bonito.)

    sns.barplot(
        data=estatisticas_por_genero.reset_index(),
        x="genero",
        y="Média Média Geral",
        ax=axs[0],
        palette="viridis",
    )
    axs[0].set_title("Média da Média Geral por Gênero")
    axs[0].set_ylabel("Média Média Geral")
    axs[0].set_xlabel("Gênero")

    sns.barplot(
        x=distribuicao_genero.index,
        y=distribuicao_genero.values,
        ax=axs[1],
        palette="coolwarm",
    )
    axs[1].set_title("Distribuição Percentual por Gênero")
    axs[1].set_ylabel("Percentual (%)")
    axs[1].set_xlabel("Gênero")

    for ax in axs.flat:
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 9),
                textcoords="offset points",
            )

    plt.show()

    media_geral_por_genero = estatisticas_por_genero["Média Média Geral"]
    print(
        f"Insight: A média geral dos estudantes varia por gênero. A análise indica que, em média, o desempenho acadêmico pode diferir entre gêneros, com algumas diferenças observadas na média geral e nas horas de estudo. A distribuição percentual de gênero mostra a proporção de cada gênero no total dos estudantes."
    )


# auto explicativo
def exibir_tabelas_por_curso():
    estatisticas_por_curso = df.groupby("curso").agg(
        {
            "media_geral": ["mean", "median", lambda x: x.mode()[0], "std"],
            "horas_estudo_semana": ["mean", "median", lambda x: x.mode()[0], "std"],
        }
    )
    estatisticas_por_curso.columns = [
        "Média Média Geral",
        "Mediana Média Geral",
        "Moda Média Geral",
        "Desvio Padrão Média Geral",
        "Média Horas Estudo",
        "Mediana Horas Estudo",
        "Moda Horas Estudo",
        "Desvio Padrão Horas Estudo",
    ]
    distribuicao_curso = df["curso"].value_counts(normalize=True) * 100

    fig, axs = plt.subplots(2, 1, figsize=(16, 10), tight_layout=True)

    sns.barplot(
        data=estatisticas_por_curso.reset_index(),
        x="curso",
        y="Média Média Geral",
        ax=axs[0],
        palette="viridis",
    )
    axs[0].set_title("Média da Média Geral por Curso")
    axs[0].set_ylabel("Média Média Geral")
    axs[0].set_xlabel("Curso")

    sns.barplot(
        x=distribuicao_curso.index,
        y=distribuicao_curso.values,
        ax=axs[1],
        palette="coolwarm",
    )
    axs[1].set_title("Distribuição Percentual por Curso")
    axs[1].set_ylabel("Percentual (%)")
    axs[1].set_xlabel("Curso")

    for ax in axs.flat:
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 9),
                textcoords="offset points",
            )

    plt.show()

    media_geral_por_curso = estatisticas_por_curso["Média Média Geral"]
    print(
        f"Insight: As estatísticas mostram variações nas médias gerais entre cursos. Cursos com médias gerais mais altas podem refletir uma maior carga de estudo ou diferentes padrões de avaliação. A distribuição percentual por curso revela quais cursos têm mais ou menos estudantes, podendo indicar a popularidade e a densidade de cada curso."
    )


# aqui é pra visualizar o grafico histograma.


def visualizar_histograma():
    plt.figure(figsize=(10, 6))
    plt.hist(df["media_geral"], bins=10, color="skyblue", edgecolor="black")
    plt.title("Histograma da Distribuição da Média Geral")
    plt.xlabel("Média Geral")
    plt.ylabel("Frequência")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()

    media_geral = df["media_geral"].describe()
    print(
        f"Insight: O histograma mostra a distribuição das médias gerais dos estudantes. A análise revela se a maioria dos estudantes tem notas próximas à média ou se há uma ampla gama de notas. A média geral dos estudantes é {media_geral['mean']:.2f}, e a dispersão das notas pode indicar a concentração de desempenho acadêmico."
    )


# aqui é pra visualizar o grafico boxplot.


def visualizar_boxplot():
    plt.figure(figsize=(14, 8))
    sns.boxplot(x="curso", y="media_geral", data=df, palette="pastel", width=0.8)
    plt.title("Boxplot da Média Geral por Curso", fontsize=16)
    plt.xlabel("Curso", fontsize=14)
    plt.ylabel("Média Geral", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    # eu salvo o arquivo em temporario e exibo pra eu poder conseguir mostrar o insight quando ele for excluido.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        file_path = temp_file.name
        plt.savefig(file_path)

    plt.close()  # aqui fecha o plot.

    # aqui exibe o abençoado do grafico.
    img = plt.imread(file_path)
    plt.imshow(img)
    plt.axis("off")
    plt.show()

    # aqui ele remove o arquivo pra poder dar a permissão pra exibir o insight (em outras palavras, deu um bug e só funciona assim.)
    os.remove(file_path)

    print(
        "Insight: O boxplot mostra a variação das médias gerais entre cursos. Cursos com caixas mais longas e outliers indicam maior variação nas notas. Cursos com caixas mais curtas e menos outliers sugerem uma distribuição de notas mais uniforme."
    )


#  função que vai visualizar o gráfico em dispersão (foi bem mais facil que o heatmap, meu Deus.)


def visualizar_dispersao():
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x="horas_estudo_semana",
        y="media_geral",
        hue="curso",
        data=df,
        palette="viridis",
        s=100,
    )
    plt.title("Gráfico de Dispersão entre Horas de Estudo e Média Geral")
    plt.xlabel("Horas de Estudo por Semana")
    plt.ylabel("Média Geral")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()

    correlacao = df["horas_estudo_semana"].corr(df["media_geral"])
    print(
        f"Insight: O gráfico de dispersão mostra a relação entre horas de estudo e média geral. Há uma correlação positiva entre horas de estudo e média geral (correlação: {correlacao:.2f}). Estudantes que dedicam mais horas de estudo tendem a ter médias gerais mais altas."
    )


# função que vai visualizar o heatmap (Sim, eu sofri pra pesquisar e entender o que é isso, nem sabia o que era heatmap.)


def visualizar_heatmap():
    plt.figure(figsize=(10, 8))
    correlacao = df[["idade", "horas_estudo_semana", "media_geral"]].corr()
    sns.heatmap(correlacao, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Heatmap da Correlação entre Variáveis")
    plt.show()

    print(
        f"Insight: O heatmap da correlação mostra as relações entre idade, horas de estudo e média geral. A correlação positiva entre horas de estudo e média geral (correlação: {correlacao.loc['horas_estudo_semana', 'media_geral']:.2f}) indica que mais horas de estudo estão associadas a notas mais altas."
    )


def menu_visualizacao():
    while True:
        print("\nEscolha uma das opções de visualização:")
        print("1. Tabelas por gênero")
        print("2. Tabelas por curso")
        print("3. Adicionar informações")
        print("4. Histograma da distribuição da média geral")
        print("5. Boxplot da média geral por curso")
        print("6. Gráfico de dispersão entre horas de estudo e média geral")
        print("7. Heatmap da correlação entre variáveis")
        print("8. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            exibir_tabelas_por_genero()
        elif escolha == "2":
            exibir_tabelas_por_curso()
        elif escolha == "3":
            adicionar_informacoes()
        elif escolha == "4":
            visualizar_histograma()
        elif escolha == "5":
            visualizar_boxplot()
        elif escolha == "6":
            visualizar_dispersao()
        elif escolha == "7":
            visualizar_heatmap()
        elif escolha == "8":
            print("Saindo do menu de visualização.")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


menu_visualizacao()
