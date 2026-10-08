# Variables
BOOK_DIR := justfile_directory() + "/book"
PAGES_DIR := justfile_directory() + "/pages"

# Publish pages
publish:
    #!/usr/bin/env bash
    echo "{{GREEN}}[+] Building book{{NORMAL}}"
    mdbook build
    cd "{{ BOOK_DIR }}"
    cp -R ./* "{{PAGES_DIR}}"
    cd "{{ PAGES_DIR }}"
    git add -A
    pubdate=$(date -Iseconds)
    git commit -m "Publish: $pubdate"
    git push
    cd ..
    git commit -am "Update: $pubdate"
    git push


# Prints usage
help:
    @just --list
