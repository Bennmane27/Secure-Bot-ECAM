# Botecam - Discord Moderation Bot

![Botecam](https://i.postimg.cc/wMQP7HJj/30dbaf0089007ae1f26f151643a72136.png)

### 🤖 Your Ultimate Discord Moderation Assistant

Botecam is a powerful Discord moderation bot designed to streamline community management and ensure a safe, organized environment on your server. Built with Python and the `discord.py` library, Botecam helps server admins handle user verification, message deletion, user muting, and much more.

## Features

### 🚀 Advanced Moderation Capabilities
- **Message Deletion:** Remove inappropriate messages or clear channels with ease.
- **User Verification:** Verify new members via a secure email code system.
- **User Muting/Unmuting:** Manage disruptive users with indefinite or time-based muting.
- **Message Logging:** Track important user activities with comprehensive message logs.
- **Emergency Mode:** Quickly delete hacked user messages in case of emergencies.

### 🔒 Secure Verification Process
- Verification via unique code sent to user email.
- Role-based access control to sensitive bot commands.
- Automated DM verification questions to ensure accurate user identity.

### 🛠️ Additional Functionalities
- **Customized Greetings:** Personalized welcome messages for new users.
- **Direct DM Link:** Quick-access buttons to assist users in verification.
- **Guild-Specific Commands:** Guild-specific command execution with slash commands.

## Commands

### General Commands

- `/info`: Get information about Botecam.
- `/inscription`: Start your verification process.
- `/find <user>`: Find a user's mentions in a specific channel.

### Moderation Commands

- `/send <salon> <message>`: Send a message in a specified channel.
- `/remove_dm <limit>`: Remove Botecam's messages from a DM.
- `/mute <member>`: Mute a user indefinitely.
- `/unmute <member>`: Unmute a user.
- `/delet_message <num_messages> <all>`: Delete a certain number of messages or all messages.
- `/urgence_delet <member>`: Delete all messages from a user across channels (for emergencies).

## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YourUsername/Botecam.git
   cd Botecam
