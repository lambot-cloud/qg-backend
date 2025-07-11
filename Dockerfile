FROM python:3.12-alpine3.22 as python_builder


WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt


FROM python:3.12-alpine3.22

WORKDIR /app


COPY quality_gates /app/quality_gates

COPY --from=python_builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=python_builder /usr/local/bin/alembic /usr/local/bin/alembic

RUN chmod a+x /usr/local/bin/alembic

COPY alembic.ini /app/alembic.ini
COPY migrations /app/migrations

EXPOSE 8000

ENTRYPOINT ["python", "-m", "quality_gates"]
CMD ["run"]
