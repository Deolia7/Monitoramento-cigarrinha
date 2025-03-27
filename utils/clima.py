
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def obter_previsao_clima(media_adultos, media_ninfas):
    """
    Gera uma previsão populacional para os próximos 30 dias com base nas médias de adultos e ninfas.
    Considera uma taxa de crescimento simples para exemplificação.
    """
    dias = 30
    crescimento_adultos = 1.05  # crescimento diário de 5%
    crescimento_ninfas = 1.03   # crescimento diário de 3%

    datas = [datetime.today() + timedelta(days=i) for i in range(dias)]
    adultos = [media_adultos * (crescimento_adultos ** i) for i in range(dias)]
    ninfas = [media_ninfas * (crescimento_ninfas ** i) for i in range(dias)]
    pop_total = [a + n for a, n in zip(adultos, ninfas)]

    df = pd.DataFrame({
        'data': datas,
        'adultos': adultos,
        'ninfas': ninfas,
        'pop_total': pop_total
    })

    return df
