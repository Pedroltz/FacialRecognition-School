#!/bin/bash

echo "==================================="
echo "Build para Windows - Sistema de Gerenciamento de Salas"
echo "==================================="
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Limpar builds anteriores
echo "Limpando builds anteriores..."
rm -rf build dist Release

# Criar build com PyInstaller
echo ""
echo "Compilando aplicação..."
pyinstaller build_windows.spec --clean

# Verificar se build foi bem-sucedido
if [ -d "dist/GerenciamentoSalas" ]; then
    echo ""
    echo "Build concluído com sucesso!"

    # Criar pasta Release
    echo ""
    echo "Criando pasta Release..."
    mkdir -p Release

    # Mover arquivos para Release
    mv dist/GerenciamentoSalas/* Release/

    # Criar README para Windows
    cat > Release/README.txt << 'EOF'
Sistema de Gerenciamento de Salas com Reconhecimento Facial
=============================================================

REQUISITOS PARA WINDOWS:
-------------------------
1. GTK4 Runtime deve estar instalado
   Download: https://github.com/wingtk/gvsbuild/releases

2. Webcam funcional

3. Windows 10 ou superior (64-bit)

INSTALAÇÃO:
-----------
1. Descompacte todos os arquivos em uma pasta
2. Instale GTK4 Runtime (se ainda não tiver)
3. Execute GerenciamentoSalas.exe

PRIMEIRA EXECUÇÃO:
------------------
- O sistema criará automaticamente o banco de dados
- Uma pasta "data/faces" será criada para armazenar fotos

OBSERVAÇÕES:
------------
- Certifique-se de que a webcam não está sendo usada por outro programa
- O firewall pode solicitar permissão na primeira execução
- Para resetar o banco de dados, delete o arquivo data/classroom.db

SUPORTE:
--------
Documentação completa: Veja CLAUDE.MD no projeto original

Versão: 4.0
Data: 2025-10-01
EOF

    # Copiar documentação
    cp CLAUDE.MD Release/ 2>/dev/null || true

    # Limpar arquivos temporários
    rm -rf build dist

    echo ""
    echo "==================================="
    echo "Build finalizado!"
    echo "Pasta Release criada com sucesso!"
    echo "==================================="
    echo ""
    echo "Conteúdo da pasta Release:"
    ls -lh Release/
    echo ""
    echo "IMPORTANTE:"
    echo "- Este build foi criado no Linux e pode não funcionar no Windows"
    echo "- Para um build Windows funcional, execute este script em uma máquina Windows"
    echo "- Alternativamente, use Wine ou uma VM Windows"

else
    echo ""
    echo "Erro: Build falhou!"
    echo "Verifique os logs acima para mais detalhes"
    exit 1
fi
