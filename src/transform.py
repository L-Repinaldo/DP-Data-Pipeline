import pandas as pd

class TransformError(Exception):
    pass


def calcula_tempo(date_input):

    from datetime import date
    from dateutil.relativedelta import relativedelta

    today = date.today()
    delta = relativedelta(today, date_input)
    return delta.years


def transform(dataframes: dict) -> tuple[pd.DataFrame, dict]:

    try:
        df_funcionario = dataframes["funcionarios"].copy()
        df_avaliacoes = dataframes["avaliacoes"].copy()
        df_beneficio_funcionario = dataframes["beneficio_funcionario"].copy()
        df_beneficios = dataframes["beneficios"].copy()
        df_setores = dataframes["setores"].copy()
        df_cargos = dataframes["cargos"].copy()

    except KeyError as e:
        raise TransformError(f"Tabela ausente na extração: {e}")


    df_funcionario["idade"] = df_funcionario["data_nascimento"].apply(calcula_tempo)
    df_funcionario["tempo_na_empresa"] = df_funcionario["data_admissao"].apply(calcula_tempo)


    df_funcionario = df_funcionario[
        [
            "id",
            "id_setor",
            "id_cargo",
            "salario",
            "idade",
            "tempo_na_empresa",
        ]
    ]

    df_avaliacoes = df_avaliacoes[["id_funcionario", "nota"]]

    df_avaliacoes_agg = (
        df_avaliacoes
        .groupby("id_funcionario", as_index=False)
        .agg(nota_media=("nota", "mean"))
    )

    df_beneficio_funcionario = df_beneficio_funcionario.merge(
        df_beneficios[["id"]],
        left_on="id_beneficio",
        right_on="id",
        how="left"
    )

    df_beneficio_count = (
        df_beneficio_funcionario
        .groupby("id_funcionario", as_index=False)
        .size()
        .rename(columns={"size": "qtd_beneficios"})
    )

    df_setores = df_setores[["id", "nome"]].rename(columns={"nome": "setor"})
    df_cargos = df_cargos[["id", "nome"]].rename(columns={"nome": "cargo"})

    df = (
        df_funcionario
        .merge(df_avaliacoes_agg, left_on="id", right_on="id_funcionario", how="left")
        .merge(df_beneficio_count, left_on="id", right_on="id_funcionario", how="left")
        .merge(df_cargos, left_on="id_cargo", right_on="id", how="left")
        .merge(df_setores, left_on="id_setor", right_on="id", how="left")
    )

    df = df.drop(columns=["id_funcionario_x", "id_funcionario_y", "id_funcionario_y", "id_x", "id_y", "id_cargo", "id_setor", "id"])


    df["idade"] = df["idade"].fillna(0)
    df["tempo_na_empresa"] = df["tempo_na_empresa"].fillna(0)
    df["salario"] = df["salario"].fillna(0)
    df["nota_media"] = df["nota_media"].fillna(0)
    df["qtd_beneficios"] = df["qtd_beneficios"].fillna(0)


    df["idade"] = df["idade"].astype(int)
    df["tempo_na_empresa"] = df["tempo_na_empresa"].astype(int)
    df["salario"] = df["salario"].astype(float)
    df["nota_media"] = df["nota_media"].astype(float)
    df["qtd_beneficios"] = df["qtd_beneficios"].astype(int)
    df["setor"] = df["setor"].astype("category")
    df["cargo"] = df["cargo"].astype("category")

    sensitive_attributes = [
        "idade",
        "salario",
        "nota_media",
        "tempo_na_empresa"
    ]

    schema_info = {
        "columns": list(df.columns),
        "sensitive_attributes": sensitive_attributes,
        "non_sensitive_attributes": [c for c in df.columns if c not in sensitive_attributes],
        "row_count": len(df),
    }

    return df, schema_info
