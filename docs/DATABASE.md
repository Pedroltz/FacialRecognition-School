# Estrutura do Banco de Dados

## Tecnologia

- **Sistema:** SQLite3
- **Localização:** `data/classroom.db`
- **Criação:** Automática na primeira execução

## Diagrama de Relacionamentos

```
┌──────────────┐         ┌──────────────┐
│   teachers   │         │    rooms     │
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ name         │         │ name         │
│ age          │         │ description  │
│ phone        │         │ created_at   │
│ email (UK)   │         └──────────────┘
│ face_encoding│                 │
│ photo_path   │                 │
│ created_at   │                 │
└──────────────┘                 │
       │                         │
       │         ┌───────────────┴────────────────┐
       │         │                                │
       └────────►│           classes              │
                 ├────────────────────────────────┤
                 │ id (PK)                        │
                 │ room_id (FK → rooms.id)        │
                 │ teacher_id (FK → teachers.id)  │
                 │ day_of_week                    │
                 │ start_time                     │
                 │ end_time                       │
                 │ subject                        │
                 │ created_at                     │
                 └────────────────────────────────┘
                                │
                                │
                ┌───────────────┴─────────────────┐
                │                                 │
                │         access_logs             │
                ├─────────────────────────────────┤
                │ id (PK)                         │
                │ room_id (FK → rooms.id)         │
                │ class_id (FK → classes.id, NULL)│
                │ teacher_id (FK → teachers.id)   │
                │ access_time                     │
                │ status                          │
                └─────────────────────────────────┘
```

## Tabelas

### teachers
Armazena informações dos professores cadastrados.

| Campo         | Tipo      | Restrições         | Descrição                        |
|---------------|-----------|-------------------|----------------------------------|
| id            | INTEGER   | PRIMARY KEY       | Identificador único              |
| name          | TEXT      | NOT NULL          | Nome completo                    |
| age           | INTEGER   | NOT NULL          | Idade                            |
| phone         | TEXT      | NOT NULL          | Telefone de contato              |
| email         | TEXT      | NOT NULL, UNIQUE  | Email (usado como identificador) |
| face_encoding | BLOB      | NOT NULL          | Encoding facial (pickle)         |
| photo_path    | TEXT      | NOT NULL          | Caminho da foto no filesystem    |
| created_at    | TIMESTAMP | DEFAULT NOW       | Data de cadastro                 |

**Índices:**
- PRIMARY KEY em `id`
- UNIQUE em `email`

---

### rooms
Representa as salas físicas.

| Campo       | Tipo      | Restrições         | Descrição                    |
|-------------|-----------|-------------------|------------------------------|
| id          | INTEGER   | PRIMARY KEY       | Identificador único          |
| name        | TEXT      | NOT NULL, UNIQUE  | Nome da sala (ex: "Sala A")  |
| description | TEXT      |                   | Descrição opcional           |
| created_at  | TIMESTAMP | DEFAULT NOW       | Data de criação              |

**Índices:**
- PRIMARY KEY em `id`
- UNIQUE em `name`

---

### classes
Representa aulas agendadas (recorrentes semanalmente).

| Campo       | Tipo      | Restrições            | Descrição                           |
|-------------|-----------|----------------------|-------------------------------------|
| id          | INTEGER   | PRIMARY KEY          | Identificador único                 |
| room_id     | INTEGER   | NOT NULL, FK         | Sala onde ocorre a aula             |
| teacher_id  | INTEGER   | NOT NULL, FK         | Professor responsável               |
| day_of_week | TEXT      | NOT NULL             | Dia da semana (Segunda, Terça, ...) |
| start_time  | TEXT      | NOT NULL             | Horário de início (HH:MM)           |
| end_time    | TEXT      | NOT NULL             | Horário de término (HH:MM)          |
| subject     | TEXT      |                      | Nome da disciplina (opcional)       |
| created_at  | TIMESTAMP | DEFAULT NOW          | Data de cadastro                    |

**Foreign Keys:**
- `room_id` → `rooms(id)`
- `teacher_id` → `teachers(id)`

**Valores válidos para day_of_week:**
- "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"

---

### access_logs
Registra todos os acessos (autorizados e negados) às salas.

| Campo       | Tipo      | Restrições            | Descrição                            |
|-------------|-----------|----------------------|--------------------------------------|
| id          | INTEGER   | PRIMARY KEY          | Identificador único                  |
| room_id     | INTEGER   | NOT NULL, FK         | Sala acessada                        |
| class_id    | INTEGER   | FK, NULL             | Aula relacionada (se houver)         |
| teacher_id  | INTEGER   | NOT NULL, FK         | Professor que tentou acesso          |
| access_time | TIMESTAMP | DEFAULT NOW          | Data/hora do acesso                  |
| status      | TEXT      | NOT NULL             | Status do acesso                     |

**Foreign Keys:**
- `room_id` → `rooms(id)`
- `class_id` → `classes(id)` (pode ser NULL)
- `teacher_id` → `teachers(id)`

**Exemplos de status:**
- `"AUTORIZADO - Matemática"`
- `"NEGADO - Sem aula agendada"`
- `"NEGADO - Sala reservada para João Silva"`

---

## Queries Comuns

### Listar aulas de uma sala ordenadas
```sql
SELECT c.*, r.name as room_name, t.name as teacher_name
FROM classes c
JOIN rooms r ON c.room_id = r.id
JOIN teachers t ON c.teacher_id = t.id
WHERE c.room_id = ?
ORDER BY
    CASE c.day_of_week
        WHEN 'Segunda' THEN 1
        WHEN 'Terça' THEN 2
        WHEN 'Quarta' THEN 3
        WHEN 'Quinta' THEN 4
        WHEN 'Sexta' THEN 5
        WHEN 'Sábado' THEN 6
    END,
    c.start_time
```

### Logs de acesso de uma sala
```sql
SELECT al.*, t.name as teacher_name
FROM access_logs al
JOIN teachers t ON al.teacher_id = t.id
WHERE al.room_id = ?
ORDER BY al.access_time DESC
```

### Aulas de um professor em um dia específico
```sql
SELECT c.*, r.name as room_name
FROM classes c
JOIN rooms r ON c.room_id = r.id
WHERE c.teacher_id = ? AND c.day_of_week = ?
ORDER BY c.start_time
```

---

## Manutenção

### Backup do banco
```bash
cp data/classroom.db data/classroom.db.backup
```

### Verificar integridade
```bash
sqlite3 data/classroom.db "PRAGMA integrity_check;"
```

### Resetar banco (ATENÇÃO: perde todos os dados)
```bash
rm data/classroom.db
python main.py  # Recria automaticamente
```

### Consultar banco via CLI
```bash
sqlite3 data/classroom.db

# Listar tabelas
.tables

# Ver estrutura de uma tabela
.schema teachers

# Query de exemplo
SELECT name, email FROM teachers;

# Sair
.quit
```
