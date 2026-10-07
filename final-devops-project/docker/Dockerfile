FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000 BIND_HOST=0.0.0.0
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY final-devops-project/application/app.py ./app.py
COPY final-devops-project/application/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && chown -R app:app /app
USER app
EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=3s --start-period=5s --retries=3 CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["python", "app.py"]
