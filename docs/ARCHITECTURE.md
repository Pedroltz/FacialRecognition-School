# Arquitetura do Sistema

## Visão Geral

Sistema de reconhecimento facial para controle de presença em salas de aula, desenvolvido em Python com GTK4 seguindo o padrão MVC (Model-View-Controller).

## Estrutura do Projeto

```
FacialRecognition-School/
├── main.py                 # Ponto de entrada da aplicação
├── data/                   # Dados persistentes
│   ├── classroom.db        # Banco de dados SQLite
│   └── faces/              # Fotos dos professores
├── src/
│   ├── controllers/        # Lógica de negócio
│   │   └── room_controller.py
│   ├── models/             # Acesso a dados
│   │   └── database.py
│   ├── utils/              # Utilitários
│   │   └── face_recognition.py
│   └── views/              # Interface gráfica
│       ├── main_window.py
│       ├── manage_window.py
│       ├── register_class_window.py
│       └── register_room_window.py
└── docs/                   # Documentação
```

## Padrão MVC

### Model (Modelo)
- **Localização:** [src/models/database.py](../src/models/database.py)
- **Responsabilidade:** Gerenciamento de dados e persistência no SQLite
- **Tabelas:**
  - `teachers` - Professores cadastrados
  - `rooms` - Salas físicas
  - `classes` - Aulas agendadas (recorrentes)
  - `access_logs` - Registro de acessos

### View (Visão)
- **Localização:** `src/views/`
- **Responsabilidade:** Interface gráfica com GTK4
- **Componentes:**
  - `main_window.py` - Tela principal com câmera e seleção de sala
  - `manage_window.py` - Gerenciamento de professores, salas e aulas
  - `register_class_window.py` - Cadastro de aulas
  - `register_room_window.py` - Cadastro de salas

### Controller (Controlador)
- **Localização:** [src/controllers/room_controller.py](../src/controllers/room_controller.py)
- **Responsabilidade:** Lógica de negócio e coordenação entre Model e View
- **Principais métodos:**
  - `register_teacher()` - Cadastra professor com encoding facial
  - `create_room()` - Cria nova sala
  - `create_class()` - Agenda aula recorrente
  - `authenticate_teacher_in_room()` - Autentica professor via face

## Fluxo de Autenticação

```
1. Usuário seleciona sala → View
2. View captura frame da câmera → Controller
3. Controller detecta face → FaceRecognizer
4. FaceRecognizer gera encoding facial
5. Controller compara com professores cadastrados → Database
6. Controller verifica se há aula agendada no momento
7. Controller registra acesso → Database
8. Controller retorna resultado → View
9. View exibe mensagem de autorizado/negado
```

## Componentes Principais

### FaceRecognizer
- **Localização:** [src/utils/face_recognition.py](../src/utils/face_recognition.py)
- **Biblioteca:** face_recognition (baseada em dlib)
- **Tolerância padrão:** 0.6 (quanto menor, mais rigoroso)
- **Métodos principais:**
  - `encode_face()` - Gera encoding de imagem
  - `encode_face_from_frame()` - Gera encoding de frame de vídeo
  - `find_match()` - Busca correspondência em lista de encodings

### Database
- **Tecnologia:** SQLite3
- **Localização:** `data/classroom.db`
- **Características:**
  - Banco embutido, sem servidor externo
  - Criação automática de tabelas
  - Relacionamentos com foreign keys
  - Face encodings armazenados como BLOB (pickle)

### RoomController
- **Lógica de validação de aulas:**
  - Verifica dia da semana atual
  - Permite acesso 10 minutos antes do início até o fim da aula
  - Nega acesso se não houver aula agendada
  - Nega acesso se professor não for o responsável pela aula

## Tecnologias Utilizadas

- **Python 3.13+** - Linguagem principal
- **GTK4** - Framework de interface gráfica nativa
- **OpenCV** - Captura de vídeo da câmera
- **face_recognition** - Detecção e reconhecimento facial
- **dlib** - Algoritmos de machine learning (backend do face_recognition)
- **SQLite3** - Banco de dados relacional
- **NumPy** - Operações com arrays numéricos
- **Pillow** - Processamento de imagens

## Segurança

- Encodings faciais armazenados como binário (não reversível para imagem original)
- Fotos armazenadas localmente em `data/faces/`
- Validação de horários para evitar acessos não autorizados
- Logs de acesso com timestamp para auditoria
