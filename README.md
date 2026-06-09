# ATA Gideões

Sistema para gestão de membros, reuniões, atas, presenças, igrejas parceiras e agendamentos.

## Stack

- Backend: Django + Django REST Framework + Simple JWT
- Frontend: Vue 3 + Vite + TypeScript + Pinia + Tailwind + Vuetify
- Banco local: SQLite
- Banco recomendado para produção: PostgreSQL

## Como rodar o backend

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend local:

```txt
http://127.0.0.1:8000
```

## Como rodar o frontend

```bash
cd frontend
npm install
```

Crie o arquivo `frontend/.env` a partir do exemplo:

```bash
cp .env.example .env
```

Escolha para onde o frontend aponta:

```env
# local      → http://127.0.0.1:8002
# production → https://emanuelcoutinho.pythonanywhere.com
VITE_API_MODE=production
```

Para forçar uma URL específica (opcional):

```env
VITE_API_BASE_URL=https://emanuelcoutinho.pythonanywhere.com
# ou
VITE_API_BASE_URL=http://127.0.0.1:8002
```

Depois execute:

```bash
npm run dev
```

Frontend local:

```txt
http://127.0.0.1:3000
```

## Como rodar com Docker

```bash
cp .env.example .env
docker compose up --build
```

Serviços:

```txt
Backend:  http://127.0.0.1:8000
Frontend: http://127.0.0.1:3000
```

Para criar o primeiro usuário admin:

```bash
docker compose exec backend python manage.py createsuperuser
```

## Autenticação

Endpoints principais:

```txt
POST /api/auth/token/
POST /api/auth/token/refresh/
POST /api/auth/token/verify/
```

## Principais endpoints

```txt
GET/POST    /api/members/
GET/POST    /api/meetings/
GET/POST    /api/minutes/
GET/POST    /api/attendances/
GET/POST    /api/partner-churches/
GET/POST    /api/church-schedules/
GET         /api/dashboard/
```

Endpoints extras:

```txt
GET  /api/meetings/{id}/attendances/
POST /api/meetings/{id}/attendances/bulk/
GET  /api/minutes/{id}/print/
GET  /api/minutes/{id}/pdf/
```

## Observação sobre versionamento

Não versionar:

```txt
node_modules/
venv/
.venv/
db.sqlite3
__pycache__/
frontend/dist/
```

Use `.env.example` como modelo e mantenha os valores reais apenas no `.env` local ou nas variáveis do provedor de deploy.
