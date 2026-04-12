# dockerfile to run ollama on render
FROM ollama/ollama:latest

# Pull the model during the IMAGE BUILD, not at runtime
RUN ollama serve & sleep 5 && ollama pull gemma3:1b && pkill ollama

EXPOSE 11434
CMD ["serve"]