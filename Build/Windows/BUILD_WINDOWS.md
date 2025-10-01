# Como Criar Build para Windows

## ⚠️ Importante: Cross-compilation não é possível

O PyInstaller **NÃO** pode criar executáveis Windows a partir do Linux.
Você precisa compilar o projeto **EM UMA MÁQUINA WINDOWS**.

## 📋 Opções para criar o Build Windows

### Opção 1: Usar uma Máquina Windows Real (RECOMENDADO)

1. **Copie o projeto para uma máquina Windows**
   - Use pendrive, cloud storage, ou git

2. **Instale os pré-requisitos no Windows:**

   a) **Python 3.13+**
      - Download: https://www.python.org/downloads/
      - Marque "Add Python to PATH" durante instalação

   b) **GTK4 para Windows**
      - Download: https://github.com/wingtk/gvsbuild/releases
      - Instale o GTK4 Runtime

   c) **Microsoft Visual C++ Build Tools** (para dlib)
      - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
      - Selecione "Desktop development with C++"

   d) **CMake**
      - Download: https://cmake.org/download/
      - Adicione ao PATH

3. **Execute os seguintes comandos no PowerShell/CMD:**

```powershell
# Navegar até a pasta do projeto
cd C:\caminho\para\ProjetoImagens

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Atualizar pip
python -m pip install --upgrade pip setuptools wheel

# Instalar dependências
pip install cmake dlib
pip install face-recognition
pip install git+https://github.com/ageitgey/face_recognition_models
pip install opencv-python PyGObject
pip install pyinstaller

# Compilar com PyInstaller
pyinstaller build_windows.spec --clean

# Criar pasta Release
mkdir Release
xcopy /E /I dist\GerenciamentoSalas Release

# Copiar README
copy CLAUDE.MD Release\
```

4. **Resultado:**
   - Pasta `Release` conterá o executável e todos os arquivos necessários
   - Distribua a pasta completa (não apenas o .exe)

---

### Opção 2: Usar Máquina Virtual Windows

1. **Instale VirtualBox ou VMware**
   - VirtualBox: https://www.virtualbox.org/

2. **Baixe uma ISO do Windows**
   - Windows 10/11 Evaluation: https://www.microsoft.com/en-us/evalcenter/

3. **Crie uma VM Windows**
   - Pelo menos 4GB RAM
   - 50GB de disco

4. **Siga os passos da Opção 1 dentro da VM**

---

### Opção 3: Usar Wine no Linux (NÃO RECOMENDADO)

Wine pode tentar executar o Python Windows no Linux, mas:
- ❌ Muito instável
- ❌ Difícil configurar dependências (dlib, GTK4)
- ❌ Alta chance de falhar
- ⚠️ Não recomendamos esta opção

---

## 📦 Arquivo .spec Já Criado

O arquivo `build_windows.spec` já está configurado com:
- ✅ Todos os imports necessários
- ✅ Inclusão da pasta `data`
- ✅ Configurações otimizadas para Windows
- ✅ Nome do executável: `GerenciamentoSalas.exe`

## 📝 Após o Build

A pasta `Release` conterá:
```
Release/
├── GerenciamentoSalas.exe    # Executável principal
├── _internal/                # Dependências Python
├── data/                     # Banco de dados e fotos (criados em runtime)
├── README.txt               # Instruções para usuários Windows
└── CLAUDE.MD                # Documentação completa
```

## ⚙️ Requisitos no Windows do Usuário Final

Para rodar o executável, o usuário final precisa:
1. **GTK4 Runtime** instalado
2. **Webcam** funcional
3. **Windows 10+** (64-bit)

O GTK4 Runtime pode ser distribuído junto, mas aumenta muito o tamanho.

## 🎯 Distribuição

### Opção A: ZIP Simples
```bash
# Comprimir a pasta Release
zip -r GerenciamentoSalas-v4.0-Windows.zip Release/
```

### Opção B: Instalador (Mais profissional)

Use **Inno Setup** para criar um instalador `.exe`:
1. Download: https://jrsoftware.org/isdl.php
2. Crie script .iss apontando para a pasta Release
3. Compile o instalador

---

## 🐛 Problemas Comuns

### "Não foi possível abrir a câmera"
- Verificar se outra aplicação está usando a webcam
- Verificar permissões no Windows

### "GTK not found"
- Instalar GTK4 Runtime
- Adicionar GTK ao PATH do Windows

### "DLL load failed"
- Instalar Microsoft Visual C++ Redistributable
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Executável muito grande (>500MB)
- Normal devido a dependências (dlib, face_recognition, GTK)
- Considere usar UPX para comprimir (já configurado no .spec)

---

## 📚 Referências

- [PyInstaller Documentation](https://pyinstaller.org/)
- [GTK for Windows](https://www.gtk.org/docs/installations/windows)
- [face_recognition on Windows](https://github.com/ageitgey/face_recognition#installation-on-windows)

---

## ✅ Checklist Final

Antes de distribuir, teste em uma máquina Windows limpa:
- [ ] Executável inicia sem erros
- [ ] Câmera é detectada e funciona
- [ ] Cadastro de professor funciona
- [ ] Reconhecimento facial funciona
- [ ] Banco de dados é criado corretamente
- [ ] Interface GTK renderiza corretamente

---

**Última atualização:** 2025-10-01
**Versão do Projeto:** 4.0
