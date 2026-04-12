# dockerfile to run ollama on render
FROM ollama/ollama:latest
EXPOSE 11434
RUN ollama serve & sleep 10 && ollama pull gemma3:1b && ollama pull qwen3.5