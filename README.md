# DENOX TEST

Esse projeto toma como pressuposto de que os dados foram importados corretamente para o banco de dados.

Obs.: Realizei o tratamento dos dados exportados, visto que todos estavam como STRING.


### Instruções

Para executar o app, entre na pasta src, crie o venv e instale as dependencias:

```shell
cd src/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Obs.: Caso não consiga instalar o scikit-learn, instale utilizando o seguinte comando:

```shell
pip install -U scikit-learn
```

Para iniciar o app, execute o seguinte comando:

```shell
python app.py
```

A API será executada na porta 4000.

### API

POST /api/calcula_metricas

Obtem os dados pesquisados e insere os mesmos no banco de dados.

Payload:

```json
{
    "serial": "ac8251468654944f2abedb9dbfe3b700",
    "datahora_inicio": "10/04/2019 10:30:51",
    "datahora_fim": "24/04/2019 11:30:51"
}
```

GET /api/retorna_metricas

Obtem os resultados.

Exemplo de resposta:

```json
[
    {
        "serial": "ac8251468654944f2abedb9dbfe3b700",
        "distancia_percorrida": 25.314,
        "tempo_parado": 177,
        "tempo_em_movimento": 3356,
        "centroides_paradas": [
            [
                -12.902777,
                -38.336407
            ],
            [
                -12.903254,
                -38.337242
            ]
        ]
    },
    {
        "serial": "ac8251468654944f2abedb9dbfe3b700",
        "distancia_percorrida": 25.314,
        "tempo_parado": 177,
        "tempo_em_movimento": 3356,
        "centroides_paradas": [
            [
                -12.902777,
                -38.336407
            ],
            [
                -12.903254,
                -38.337242
            ]
        ]
    },
]
```
