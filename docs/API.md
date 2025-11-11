# API do Sistema

## RoomController

Controller principal que coordena toda a lógica de negócio.

### Gerenciamento de Professores

#### `register_teacher(name, age, phone, email, photo_path)`
Registra um novo professor no sistema.

**Parâmetros:**
- `name` (str) - Nome completo do professor
- `age` (int) - Idade do professor
- `phone` (str) - Telefone de contato
- `email` (str) - Email (deve ser único)
- `photo_path` (str) - Caminho da foto capturada

**Retorno:** `(bool, str)` - (sucesso, mensagem)

**Exemplo:**
```python
controller = RoomController()
success, msg = controller.register_teacher(
    name="João Silva",
    age=35,
    phone="11999999999",
    email="joao@email.com",
    photo_path="/tmp/photo.jpg"
)
```

#### `get_all_teachers()`
Retorna todos os professores cadastrados.

**Retorno:** `List[Dict]` - Lista de professores

**Estrutura do dicionário:**
```python
{
    'id': int,
    'name': str,
    'age': int,
    'phone': str,
    'email': str,
    'face_encoding': bytes,
    'photo_path': str,
    'created_at': str
}
```

#### `delete_teacher(teacher_id)`
Remove um professor do sistema e sua foto.

**Parâmetros:**
- `teacher_id` (int) - ID do professor

**Retorno:** `bool` - True se removido com sucesso

---

### Gerenciamento de Salas

#### `create_room(name, description="")`
Cria uma nova sala física.

**Parâmetros:**
- `name` (str) - Nome da sala (ex: "Sala A", "Lab 01")
- `description` (str, opcional) - Descrição adicional

**Retorno:** `(bool, str)` - (sucesso, mensagem)

#### `get_all_rooms()`
Retorna todas as salas cadastradas.

**Retorno:** `List[Dict]`

**Estrutura:**
```python
{
    'id': int,
    'name': str,
    'description': str,
    'created_at': str
}
```

#### `delete_room(room_id)`
Remove uma sala do sistema.

**Parâmetros:**
- `room_id` (int) - ID da sala

**Retorno:** `bool`

---

### Gerenciamento de Aulas

#### `create_class(room_id, teacher_id, day_of_week, start_time, end_time, subject="")`
Cria uma nova aula recorrente.

**Parâmetros:**
- `room_id` (int) - ID da sala
- `teacher_id` (int) - ID do professor responsável
- `day_of_week` (str) - Dia da semana: "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"
- `start_time` (str) - Horário de início no formato "HH:MM"
- `end_time` (str) - Horário de término no formato "HH:MM"
- `subject` (str, opcional) - Nome da disciplina

**Retorno:** `(bool, str)` - (sucesso, mensagem)

**Exemplo:**
```python
success, msg = controller.create_class(
    room_id=1,
    teacher_id=5,
    day_of_week="Segunda",
    start_time="14:00",
    end_time="16:00",
    subject="Matemática"
)
```

#### `get_classes_by_room(room_id)`
Retorna todas as aulas de uma sala específica.

**Parâmetros:**
- `room_id` (int) - ID da sala

**Retorno:** `List[Dict]` - Aulas ordenadas por dia da semana e horário

#### `get_all_classes()`
Retorna todas as aulas cadastradas.

**Retorno:** `List[Dict]`

**Estrutura:**
```python
{
    'id': int,
    'room_id': int,
    'teacher_id': int,
    'day_of_week': str,
    'start_time': str,
    'end_time': str,
    'subject': str,
    'created_at': str,
    'room_name': str,
    'teacher_name': str,
    'teacher_email': str
}
```

#### `delete_class(class_id)`
Remove uma aula do sistema.

**Parâmetros:**
- `class_id` (int) - ID da aula

**Retorno:** `bool`

---

### Autenticação

#### `authenticate_teacher_in_room(frame, room_id)`
Autentica um professor através de reconhecimento facial.

**Parâmetros:**
- `frame` (np.ndarray) - Frame capturado da câmera (BGR format)
- `room_id` (int) - ID da sala onde ocorre a autenticação

**Retorno:** `(bool, Optional[Dict], str, Optional[Dict])`
- `bool` - Sucesso da autenticação
- `Dict | None` - Dados do professor reconhecido
- `str` - Mensagem de status
- `Dict | None` - Dados da aula atual (se houver)

**Lógica:**
1. Detecta face no frame
2. Identifica o professor
3. Verifica se há aula agendada no momento (10min antes até fim)
4. Valida se o professor reconhecido é o responsável pela aula
5. Registra acesso no log

**Exemplo:**
```python
success, teacher, message, current_class = controller.authenticate_teacher_in_room(
    frame=camera_frame,
    room_id=1
)

if success:
    print(f"Acesso autorizado: {teacher['name']}")
    print(f"Disciplina: {current_class['subject']}")
else:
    print(f"Acesso negado: {message}")
```

#### `get_room_logs(room_id)`
Retorna o histórico de acessos de uma sala.

**Parâmetros:**
- `room_id` (int) - ID da sala

**Retorno:** `List[Dict]` - Logs ordenados por data (mais recentes primeiro)

---

## Database

Classe de acesso direto ao banco de dados.

### Métodos Principais

#### `add_teacher(name, age, phone, email, face_encoding, photo_path)`
Insere novo professor no banco.

**Retorno:** `int` - ID do professor criado

#### `add_room(name, description)`
Insere nova sala no banco.

**Retorno:** `int` - ID da sala criada

#### `add_class(room_id, teacher_id, day_of_week, start_time, end_time, subject)`
Insere nova aula no banco.

**Retorno:** `int` - ID da aula criada

#### `add_access_log(room_id, teacher_id, status, class_id=None)`
Registra um acesso (autorizado ou negado) no log.

**Parâmetros:**
- `room_id` (int) - ID da sala
- `teacher_id` (int) - ID do professor
- `status` (str) - Descrição do status (ex: "AUTORIZADO - Matemática", "NEGADO - Sem aula agendada")
- `class_id` (int, opcional) - ID da aula relacionada

**Retorno:** `int` - ID do log criado

---

## FaceRecognizer

Utilitário para reconhecimento facial.

### Métodos

#### `encode_face(image_path)`
Gera encoding facial de uma imagem.

**Parâmetros:**
- `image_path` (str) - Caminho da imagem

**Retorno:** `np.ndarray | None` - Encoding da face ou None se não detectar face

#### `encode_face_from_frame(frame)`
Gera encoding facial de um frame de vídeo.

**Parâmetros:**
- `frame` (np.ndarray) - Frame BGR do OpenCV

**Retorno:** `np.ndarray | None`

#### `find_match(unknown_encoding, known_encodings)`
Busca correspondência em uma lista de encodings conhecidos.

**Parâmetros:**
- `unknown_encoding` (np.ndarray) - Encoding a ser identificado
- `known_encodings` (List[Tuple[int, np.ndarray]]) - Lista de tuplas (id, encoding)

**Retorno:** `int | None` - ID correspondente ou None

#### Métodos Estáticos

##### `encoding_to_bytes(encoding)`
Serializa encoding para armazenamento.

**Parâmetros:**
- `encoding` (np.ndarray) - Encoding facial

**Retorno:** `bytes` - Dados serializados (pickle)

##### `bytes_to_encoding(data)`
Desserializa encoding do banco de dados.

**Parâmetros:**
- `data` (bytes) - Dados serializados

**Retorno:** `np.ndarray` - Encoding facial
