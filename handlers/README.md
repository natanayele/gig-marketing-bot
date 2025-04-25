
# GIG Bot Handler Scaffold

This package includes modular Telegram bot handlers for managing the operations of the GIG token-powered investment group. Each handler is scoped to a functional area of the startup and supports clear growth paths for governance and expansion.

## 📦 Included Handlers

- `marketing.py`: Manages marketing outreach, campaign logs, and performance feedback.
- `manufacturing.py`: Supports inventory reporting, task assignments, and order queue updates.
- `civil.py`: Interfaces with civil projects, client progress updates, and resource management.
- `governance.py`: Administers DAO-like role definitions and systemic controls.
- `vote.py`: Enables token-based governance voting processes.
- `proposal.py`: Allows creation, listing, and review of proposals.
- `investment.py`: Tracks token allocation per business investment.
- `funds.py`: Reports on GIG's token-backed treasury and liquid reserves.
- `members.py`: Details user roles, joining info, and engagement stats.
- `roles.py`: Command helpers to assign, remove, or list user roles.
- `admin.py`: Core admin actions (bot restart, member purge, emergency notices).
- `audit.py`: Logs key activities for off-chain compliance and insight.

---

## 🔌 Integration Instructions

1. Place each handler file into your `handlers/` directory.
2. Register handlers in your main bot file (`main.py` or similar):

```python
from handlers.marketing import marketing_router
from handlers.manufacturing import manufacturing_router
from handlers.civil import civil_router
# etc.

application.add_handler(CommandHandler("marketing", marketing_router))
application.add_handler(CommandHandler("manufacturing", manufacturing_router))
application.add_handler(CommandHandler("civil", civil_router))
# etc.
```

3. Define any needed environment variables in your `.env` file, for example:

```env
TELEGRAM_TOKEN=your_bot_token
HEROKU_URL=https://yourapp.herokuapp.com
```

4. Deploy to Heroku or another host and test via Telegram by issuing `/marketing`, `/vote`, `/chatid`, etc.

---

## 🧠 Future Features (To be added later)

- Smart contract API linking for token balance, on-chain vote validation
- Proposal tracking with voting logic using web3.py
- Database migration for persistent state (via PostgreSQL, SQLite, or Redis)
- Dashboard for admins (using Flask admin or React front-end)
- Multi-sig integration for financial operations (via Gnosis Safe)

Enjoy building with GIG 🚀!
