# dockerfile to run ollama on render
FROM ollama/ollama:latest
EXPOSE 11434
CMD sh -c "pull gemma3:1b && serve"