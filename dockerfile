# dockerfile to run ollama on render
FROM ollama/ollama:latest
EXPOSE 11434
CMD sh -c "ollama pull gemma3:1b && ollama serve"