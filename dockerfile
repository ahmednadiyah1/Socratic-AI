# dockerfile to run ollama on render
FROM ollama/ollama:latest
EXPOSE 11434
CMD ["ollama", "serve"]