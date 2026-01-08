import pandas as pd
import numpy as np

class DPError(Exception):
    pass


def validate_privacy_config(df, privacy_cfg):
    """
    - verifica se colunas existem
    - verifica bounds
    - garante tipos numéricos
    """
    if "sensitive_attributes" not in privacy_cfg:
        raise DPError("Configuração de privacidade sem 'sensitive_attribute'")
    
    if "mechanisms" not in privacy_cfg:
        raise DPError("Configuração de privacidade sem 'mechanisms'")
    
    for attr, bounds in privacy_cfg['sensitive_attributes'].items():

        if attr not in df.columns:
            raise DPError(f"Atributo sensível ausente no dataset: {attr}")

        if not pd.api.types.is_numeric_dtype(df[attr]):
            raise DPError(f"Atributo não numérico: {attr}")

        if "min" not in bounds or "max" not in bounds:
            raise DPError(f"Bounds incompletos para {attr}")

        if bounds["min"] >= bounds["max"]:
            raise DPError(f"Bound inválido para {attr}")

    mech = privacy_cfg["mechanisms"]
    
    for eps in mech["epsilons"]:
        if eps <= 0:
            raise DPError(f"Epsilon inválido: {eps}")
            


def clip_series(series, min_val, max_val):
    """
    Hard clipping obrigatório
    """
    return series.clip(lower=min_val, upper=max_val)


def laplace_mechanism(series, epsilon, sensitivity, rng):
    """
    Aplica ruído Laplace
    """
    scale = sensitivity / epsilon
    noise = rng.laplace(loc=0.0, scale=scale, size=len(series))
    return series + noise


def apply_dp(df, privacy_cfg):
    """
    Retorna:
    {
    epsilon: df_dp
    },
    metadata
    """
    validate_privacy_config(df, privacy_cfg)

    results = {}
    metadata = {
        "mechanisms": "laplace",
        "attributes": {},
    }

    sensitive_attrs = privacy_cfg["sensitive_attributes"]

    mech = privacy_cfg["mechanisms"]

    

    if mech['name'] != 'laplace':
        raise DPError(f"Mecanismo não suportado: {mech['name']}")

    seed = mech.get("seed", 42)
    rng = np.random.default_rng(seed)


    sensitivity_map = {
        "salario": 1000,
        "nota_media": 1.0,
        "idade": 1,
        "tempo_na_empresa": 1,
    }


    for eps in sorted(mech["epsilons"]):

        df_dp = df.copy()

        for attr in sorted(sensitive_attrs):

            bounds = sensitive_attrs[attr]

            clipped = clip_series(
                df_dp[attr],
                bounds["min"],
                bounds["max"]
            )

            noisy = laplace_mechanism(
                clipped,
                epsilon=eps,
                sensitivity=sensitivity_map[attr],
                rng=rng
            )

            df_dp[attr] = clip_series(
                noisy,
                bounds["min"],
                bounds["max"]
            )

            metadata["attributes"][attr] = {
                "min": bounds["min"],
                "max": bounds["max"],
                "sensitivity": sensitivity_map[attr]
            }

        results[eps] = df_dp

    metadata["epsilons"] = list(results.keys())

    return results, metadata