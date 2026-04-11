# dockerfile to run ollama on render
FROM ollama/ollama:latest
EXPOSE 11434
CMD ["pull", "gemma3:1b"]
CMD ["serve"]