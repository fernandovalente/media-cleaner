#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path

# Configuração de diretórios
PROJECT_DIR = Path(__file__).parent.resolve()
MEDIA_IN_DIR = PROJECT_DIR / "mediain"
MEDIA_OUT_DIR = PROJECT_DIR / "mediaout"


def ensure_directories():
    """Garante que os diretórios de entrada e saída existam."""
    MEDIA_IN_DIR.mkdir(parents=True, exist_ok=True)
    MEDIA_OUT_DIR.mkdir(parents=True, exist_ok=True)


def is_hidden(filepath):
    """Verifica se o arquivo é oculto (começa com ponto)."""
    return filepath.name.startswith('.')


def clean_file(input_path, output_path):
    """
    Usa o exiftool para remover todos os metadados do arquivo.
    Copia o arquivo temporariamente para o output e roda o exiftool inplace,
    para não alterar o arquivo original no mediain.
    """
    print(f"🔄 Processando: {input_path.name}")
    
    try:
        # Copia o arquivo para o destino para trabalharmos nele
        shutil.copy2(input_path, output_path)
        
        # Executa o exiftool para limpar todos (-all=) os metadados no arquivo copiado
        # -overwrite_original garante que não seja criado um arquivo com sufixo _original na pasta de saída
        result = subprocess.run(
            ['exiftool', '-all=', '-overwrite_original', str(output_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"✅ Limpo e salvo em: mediaout/{output_path.name}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao limpar metadados de {input_path.name}:")
        print(e.stderr)
        # Se falhou, remove o arquivo possivelmente quebrado/copiado do output
        if output_path.exists():
            output_path.unlink()
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao processar {input_path.name}: {e}")
        return False


def main():
    ensure_directories()
    
    files_to_process = [f for f in MEDIA_IN_DIR.iterdir() if f.is_file() and not is_hidden(f)]
    
    if not files_to_process:
        print(f"⚠️  Nenhum arquivo encontrado em '{MEDIA_IN_DIR}'.")
        print("Coloque suas imagens ou vídeos lá e rode o script novamente.")
        return

    print(f"📦 Encontrados {len(files_to_process)} arquivo(s) para processar.\n")
    
    sucesso, falha = 0, 0
    
    for file_path in files_to_process:
        out_path = MEDIA_OUT_DIR / file_path.name
        
        # Opcional: pular se já existir na saída
        # if out_path.exists():
        #     print(f"⏭️  Ignorando (já existe): {out_path.name}")
        #     continue

        if clean_file(file_path, out_path):
            sucesso += 1
        else:
            falha += 1
            
    print("\n--- Resumo ---")
    print(f"✅ Sucesso: {sucesso}")
    print(f"❌ Falhas: {falha}")

if __name__ == "__main__":
    main()
