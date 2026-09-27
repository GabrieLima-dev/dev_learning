# Revisão sob demanda

Registre o início sem mudar a trilha principal:

```bash
python3 scripts/learning.py revision-start --topic "tema pedido"
```

Faça uma recapitulação curta e uma pergunta ou microatividade opcional. Se criar código, use package `dev.learning.revision` e não altere o exercício ativo nem registre a revisão como aula concluída.

Ao terminar:

```bash
python3 scripts/learning.py revision-end --summary "resultado curto"
```

Depois execute `python3 scripts/learning.py continue` para confirmar que módulo, aula, exercício e status principais foram preservados.
