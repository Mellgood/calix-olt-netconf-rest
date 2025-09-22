#!/bin/bash

# Nome del file di output
OUTPUT_FILE="project_contents.txt"

# Pulizia del file di output
> "$OUTPUT_FILE"

# Funzione per trovare i file e salvare contenuto e percorso
function collect_python_files {
    local dir=$1

    # Trova file Python escludendo cartelle/file nascosti e la cartella venv
    find "$dir" -type f -name "*.py" \
        ! -path "*/.*/*" \
        ! -path "*/venv/*" \
        ! -name ".*" | while read -r file; do
        echo "==== File: $file ====" >> "$OUTPUT_FILE"
        cat "$file" >> "$OUTPUT_FILE"
        echo -e "\n\n" >> "$OUTPUT_FILE"
    done
}

# Cartella di partenza, usa la directory corrente se non specificata
START_DIR="${1:-.}"

# Eseguire la funzione
collect_python_files "$START_DIR"

echo "Il contenuto dei file Python è stato salvato in $OUTPUT_FILE"
