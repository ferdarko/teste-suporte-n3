SELECT
    id,
    proposta_id,
    status,
    data_envio,
    mensagem_erro
FROM
    envios
WHERE
    status = 'erro'
    AND data_envio >= CURRENT_DATE - INTERVAL '7 days' -- Para PostgreSQL, MySQL
    -- OR data_envio >= DATE('now', '-7 days')          -- Para SQLite
    -- OR data_envio >= GETDATE() - 7                  -- Para SQL Server
    -- OR data_envio >= SYSDATE - 7                    -- Para Oracle
ORDER BY
    data_envio DESC;