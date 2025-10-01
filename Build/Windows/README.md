# Build para Windows

Esta pasta contém os arquivos necessários para criar um executável Windows do Sistema de Gerenciamento de Salas.

## 📁 Arquivos

- **`build_windows.spec`** - Configuração do PyInstaller para build Windows
- **`BUILD_WINDOWS.md`** - Guia completo com instruções detalhadas
- **`build.sh`** - Script de build (para executar no Windows ou via PowerShell)

## 🚀 Como usar

**IMPORTANTE:** Você precisa executar o build em uma **máquina Windows**.

### Passo a passo rápido:

1. Copie todo o projeto para uma máquina Windows
2. Leia o arquivo **`BUILD_WINDOWS.md`** para instruções completas
3. Instale os pré-requisitos (Python, GTK4, Visual C++ Build Tools)
4. Execute os comandos de build no PowerShell
5. A pasta `Release` será criada com o executável

## ⚠️ Limitação

O PyInstaller **NÃO** pode criar executáveis Windows a partir do Linux.
Cross-compilation não é suportada.

Para mais detalhes, consulte: **BUILD_WINDOWS.md**
