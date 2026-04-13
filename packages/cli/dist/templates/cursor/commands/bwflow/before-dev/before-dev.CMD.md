# Before Dev

Pre-development checklist and setup.

---

## Before Starting Development

### 1. Environment Check

```bash
# Verify dependencies
pnpm install

# Check environment variables
cat .env.example

# Verify tools
node --version
pnpm --version
```

### 2. Database Setup (if needed)

```bash
# Run migrations
pnpm db:migrate

# Seed data (development only)
pnpm db:seed
```

### 3. Start Services

```bash
# Backend
pnpm dev:server

# Frontend (in another terminal)
pnpm dev:client
```

### 4. Verify Setup

```bash
# Run health check
curl localhost:3000/health

# Run tests
pnpm test
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Dependencies out of sync | `pnpm install` |
| Port already in use | Check for running processes |
| Database connection failed | Verify `.env` file |
| Type errors | `pnpm type-check` |

---

## Ready to Develop

After completing above steps:
- Backend running at localhost:3000
- Frontend running at localhost:5173
- Tests passing
- Ready to start implementation
