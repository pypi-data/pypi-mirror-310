from danbi.database import setPsql

setPsql(
    user="realquant",
    password="realquant",
    host="rsnet2",
    port=5432,
    database="realquant",
    pool_min=1,
    pool_max=20,
    base_package="grafana_fastapi",
    mappers=[
        "price.yaml",
    ],
    namespace="realquant",
    tag=1.0
)