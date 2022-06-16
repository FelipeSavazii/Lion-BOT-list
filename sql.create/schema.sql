DROP TABLE IF EXISTS bots;
DROP TABLE IF EXISTS config;

CREATE TABLE bots (
    guild_id INTEGER NOT NULL,
    developer_id INTEGER NOT NULL,
    app INTEGER NOT NULL,
    lang TEXT NOT NULL,
    desc TEXT NOT NULL,
    prefix TEXT NOT NULL
);

CREATE TABLE config (
    guild_id INTEGER NOT NULL,
    correio_id INTEGER NOT NULL,
    logs_id INTEGER NOT NULL,
    cargo_analise_id INTEGER NOT NULL,
    cargo_aprovado_id INTEGER NOT NULL,
    cargo_dev_id INTEGER NOT NULL,
    cargo_verificador_id INTEGER NOT NULL
);
