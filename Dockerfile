# base image
FROM python:3.11-slim-bookworm AS base

WORKDIR /app/api

# Install Poetry
ENV POETRY_VERSION=1.8.3
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Configure Poetry
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_REQUESTS_TIMEOUT=15

FROM base AS packages

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --sync --no-cache --no-root

# production stage
FROM base AS production

EXPOSE 8000

# set timezone
ENV TZ=UTC

WORKDIR /app/api

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl nodejs libgmp-dev libmpfr-dev libmpc-dev \
    && echo "deb http://deb.debian.org/debian testing main" > /etc/apt/sources.list \
    && apt-get update \
    # For Security
    && apt-get install -y --no-install-recommends zlib1g=1:1.3.dfsg+really1.3.1-1 expat=2.6.2-1 libldap-2.5-0=2.5.18+dfsg-2 perl=5.38.2-5 libsqlite3-0=3.46.0-1 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/api/.venv
COPY --from=packages ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy source code
COPY . /app/api/