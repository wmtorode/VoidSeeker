# VoidSeeker

VoidSeeker is an anti-spam bot for Discord, designed to identify, lure, and automatically ban spambots from your server.

### Features
- **Heuristic Detection**: Automatically identifies spambots based on message patterns, including spam terms, URLs, and mass mentions (@everyone/@here).
- **Honey Pot Channels**: Create a specific channel as a lure. Any unauthorized user (likely a bot) who messages this channel is immediately banned.
- **Automated Banning**: Once a spambot is detected, it is promptly banned from the server to prevent further spam.
- **Customizable Configuration**: Easily configure ban messages, heuristic settings, and honey pot text through an interactive setup wizard.
- **Role Management**: Robust role-based authorization for administrators and moderators to manage the bot's features.
- **Detailed Ban Reports**: View historical ban logs and detailed reports on each action taken by the bot.

---

### Local Development Setup

To set up VoidSeeker for local development, follow these steps:

1.  **Prerequisites**:
    - [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.
    - A Discord Bot Token (obtainable from the [Discord Developer Portal](https://discord.com/developers/applications)).

2.  **Configuration**:
    Ensure you have the following environment variables set in your `docker-compose.yml` file:
    - `DISCORD_BOT_SECRET`: Your Discord bot token.
    - `DISCORD_OWNING_USER_ID`: A semicolon-separated list of Discord user IDs that own the bot.
    - `TEST_MODE`: (Optional) Set to `yes` to enable debug logging and extra developer features.

3.  **Running with Docker Compose**:
    On Windows, you can use the provided development compose file:
    ```powershell
    docker compose -f docker/docker-compose.windev.yml up --build
    ```
    This will start the bot along with a PostgreSQL database.

4.  **Database Migrations**:
    Database migrations are typically handled automatically during startup, but you may need to manually apply them for the initial database creation. Run the following command:
    ```bash
    docker compose exec voidseeker alembic-db upgrade
    ```

---

### Deployment to Production

A primary `docker-compose.yml` file is not included in this repository. You must create your own based on the needs of your environment.

1.  **Environment Setup**:
    Ensure all necessary environment variables are set in your `docker-compose.yml` file (see [Environment Parameters](#environment-parameters)).

2.  **Volume Mapping**:
    Ensure that the volumes for logs (`/opt/voidseekerLog`) and data storage (`/opt/voidseekerStore`) are correctly mapped to persistent storage on the host.

3.  **Running the Bot**:
    Deploy using Docker Compose:
    ```bash
    docker compose up -d --build
    ```

4.  **Initial Setup**:
    Initial database creation may be needed on the first run of the bot, all other upgrades happen automatically. Run the following command:
    ```bash
    docker compose exec voidseeker alembic-db upgrade
    ```

---

### Environment Parameters

The following parameters can be set in the `docker-compose.yml` environment:

| Parameter | Description | Default |
| :--- | :--- | :--- |
| `DISCORD_BOT_SECRET` | **Required.** The secret token for your Discord bot. | - |
| `DISCORD_OWNING_USER_ID` | **Required.** Semicolon-separated list of Discord user IDs who have owner-level access. | - |
| `DATABASE_URL` | The PostgreSQL connection string. | `postgresql+psycopg://botUser:botPass@db:5432/voidseeker` |
| `TEST_MODE` | Set to `yes` to enable debug logging and the `TestModule`. | `No` |

---

### Roles Overview

VoidSeeker utilizes a role-based access control system to manage permissions. Roles are hierarchical:

- **Bot Owner**: Users listed in `DISCORD_OWNING_USER_ID`. They have global authority, including managing Server Owners and restarting/shutting down the bot.
- **Server Owner**: Per-server highest bot role (Rank 25). Can only be added/removed by a Bot Owner. They can manage Admins and Moderators.
- **Admin**: Per-server administrative role (Rank 10). They can configure bot settings using `!vsconfigure`, add/remove Moderators, and manage heuristic and honey pot settings.
- **Moderator**: Can view ban reports and detailed information about specific bans using `!vsreport` and `!vsdetails` (Rank 5).
- **ModRole**: Entire Discord roles can be assigned moderator permissions, allowing all members with that role to perform moderator actions (Rank 5).
- **Immune Roles**: Specific roles can be marked as immune, exempting their members from the bot's anti-spam heuristic checks and honey pot triggers.

---

### Getting Started

Once the bot is running and added to your server:
1. Use `!vsconfigure` to start the configuration wizard.
2. Set up your **Honey Pot Channel** and **Anti-Spam Heuristics**.
3. Add **Immune Roles** for your trusted members and bots.
4. Use `!vsreport` to monitor ban activities.
