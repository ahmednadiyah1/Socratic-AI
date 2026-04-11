# dockerfile to run ollama on render
FROM ollama/ollama:latest
EXPOSE 11434
ENTRYPOINT ["ollama"]
CMD ["serve"]