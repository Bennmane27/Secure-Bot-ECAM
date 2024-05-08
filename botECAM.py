import discord
from discord.ext import commands
import random
import smtplib
from email.mime.text import MIMEText
from discord.ui import Button, View
from datetime import datetime, timezone
from discord import Embed
import asyncio
from discord import ChannelType
from discord.commands import Option
from datetime import datetime



class DMButtonView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="Go to DM", style=discord.ButtonStyle.link, url="https://discord.com/channels/@me/1230583551011852448"))

# Configuration
TOKEN = 'YOUR TOKEN BOT'
GUILD_ID = 887273797932167179
CHANNEL_IDS = [1156588936135716964, 887377116310675557]
VERIFIED_ROLE_ID = 1156874277430247435
LOG_CHANNEL_ID = 1219987623330971658  
MUTED_ROLE_ID = 1231570283664511047  # ID du rôle Muted


intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

options = {
    "1": 1226519277260111872,
    "EM": 1226519277260111872,
    "2": 1226521742051115118,
    "GE": 1226521742051115118,
    "3": 1226520587288051765,
    "IS": 1226520587288051765,
    "4": 1226520200556318791,
    "CO": 1226520200556318791,
}

option_names = {
    "1": "EM",
    "2": "GE",
    "3": "IS",
    "4": "CO",
    "EM": "EM",
    "GE": "GE",
    "IS": "IS",
    "CO": "CO",

}

def generate_random_code():
    return random.randint(1000, 9999)

def send_email(matricule, code):
    smtp_server = 'smtp.domaine.com'
    smtp_port = 587
    smtp_username = 'email@domainecom'
    smtp_password = 'password'

    subject = 'Code d\'inscription'
    body = f'Votre code d\'inscription est : {code}'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = f'{matricule}@domaine.com'

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, [f'{matricule}@ecam.be'], msg.as_string())
            print(f'Email sent to {matricule}@domaine.com')
    except Exception as e:
        print(f'Error sending email: {str(e)}')


@bot.slash_command(description="Get information about Botecam.")
async def info(ctx):
    if ctx.channel.type == discord.ChannelType.private:
        embed = discord.Embed(
            title="🤖 Information sur Botecam",
            description=f"Bonjour {ctx.author.mention}, je suis Botecam, un assistant virtuel conçu par Bennmane pour la modération des serveurs Discord.",
            color=0xFFFFFF
        )
    
        embed.add_field(name="🚀 Fonctionnalités", value="Je suis équipé de fonctionnalités avancées pour optimiser la gestion des communautés en ligne. Mes capacités incluent la suppression de messages inappropriés, la gestion des membres, et bien d'autres outils essentiels pour maintenir un environnement sain et sécurisé.", inline=False)
    
        embed.add_field(name="📞 Contact", value="Pour toute assistance ou pour obtenir plus d'informations sur mes fonctionnalités, je vous invite à contacter <@1089985258360946689> directement.", inline=False)
    
        embed.set_thumbnail(url="https://i.postimg.cc/wMQP7HJj/30dbaf0089007ae1f26f151643a72136.png")
        embed.set_footer(text="Botecam | Votre assistant de modération Discord")
    
        await ctx.send(embed=embed)
        await ctx.response.send_message("Action réussie", ephemeral=True)

@bot.slash_command(description="Remove bot's messages from a DM.")
async def remove_dm(ctx: commands.Context, limit: int):
    if ctx.author.id != 1089985258360946689:
        await ctx.defer(ephemeral=True)
        return

    def is_me(m):
        return m.author == bot.user

    deleted_count = 0
    while deleted_count < limit:
        messages = await ctx.channel.history(limit=limit).flatten()
        messages_to_delete = [message for message in messages if is_me(message) and not message.embeds]
        if not messages_to_delete:
            break  # No more messages to delete

        for message in messages_to_delete:
            if deleted_count >= limit:
                break  # We've reached the limit
            try:
                await message.delete()
                deleted_count += 1
            except discord.errors.HTTPException:
                print(f"Failed to delete message {message.id} with embeds")

    confirmation_message = await ctx.send('Deleted {} message(s)'.format(deleted_count))
    await asyncio.sleep(5)  # wait for 5 seconds
    await confirmation_message.delete()  # delete the confirmation message



@bot.slash_command(guild_ids=[GUILD_ID], 
                   description="Envoie un message dans un salon spécifique")
async def send(ctx, 
               salon: Option(description="Nom du salon"),
               message: Option(description="Message à envoyer")):
    for guild in bot.guilds:
        if guild.id == GUILD_ID:
            for channel in guild.channels:
                if channel.name == salon and channel.type == ChannelType.text:
                    await channel.send(message)
                    break
AUTHORIZED_USERS = [1089985258360946689] 

MUTED_ROLE_IDS = {
    '887273797932167179': '1231570283664511047',
    '755515640965496862': '1232817276646854656',
    # Ajoutez d'autres serveurs et rôles au besoin
}

@bot.slash_command(guild_ids=['887273797932167179', '755515640965496862'], description="Mute a user indefinitely.")
async def mute(ctx: commands.Context, member: discord.Member):
    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.respond("Vous n'êtes pas autorisé à utiliser cette commande.")
        return

    guild = ctx.guild
    muted_role_id = MUTED_ROLE_IDS[str(guild.id)]
    muted_role = guild.get_role(muted_role_id)

    if not muted_role:
        await ctx.respond("Le rôle Muted n'existe pas sur ce serveur.")
        return

    await member.add_roles(muted_role, reason="Muted by command")
    await ctx.respond(f"{member.mention} a été mute indéfiniment.")

@bot.slash_command(guild_ids=['755515640965496862', '887273797932167179'], description="Unmute a user.")
async def unmute(ctx: commands.Context, member: discord.Member):
    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.respond("Vous n'êtes pas autorisé à utiliser cette commande.")
        return

    guild = ctx.guild
    muted_role_id = MUTED_ROLE_IDS[str(guild.id)]
    muted_role = guild.get_role(muted_role_id)

    if not muted_role:
        await ctx.respond("Le rôle Muted n'existe pas sur ce serveur.")
        return

    if muted_role not in member.roles:
        await ctx.respond(f"{member.mention} n'est pas mute.")
        return

    await member.remove_roles(muted_role, reason="Unmuted by command")
    await ctx.respond(f"{member.mention} a été unmute.")

@bot.slash_command(guild_ids=[GUILD_ID], description="Find user's mentions in a specific channel")
async def find(ctx: commands.Context, user: discord.User):
    channel = bot.get_channel(1219987623330971658)
    if not channel:
        await ctx.respond("Channel not found.", ephemeral=True)
        return

    messages = await channel.history(limit=100).flatten()
    user_mentions = [message for message in messages if user in message.mentions]

    if user_mentions:
        embed = discord.Embed(
            title=f"🔍 Recherche sur {user.name}",
            description=f"Voici les messages mentionnant **{user.name}**",
            color=0xFFFFFF,  # Change the color to a nice blue
            timestamp=datetime.now(timezone.utc)  # Add a timestamp to the embed
        )
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)  # Add the author's name and avatar to the embed
        for message in user_mentions:
            embed.add_field(
                name=f"📝 Message de {message.author.name} à {message.created_at.strftime('%Y-%m-%d %H:%M')}",
                value=message.content,
                inline=False
            )
        embed.set_footer(text=f"Recherche effectuée par {ctx.author.name}", icon_url=ctx.author.avatar.url)  # Add the author's avatar to the footer
        await ctx.response.send_message(embed=embed)
    else:
        await ctx.response.send_message(f"❌ Aucun résultat sur **{user.name}** trouvé.", ephemeral=True)
@bot.slash_command(guild_ids=[GUILD_ID], description="Start your verification.")
async def inscription(ctx: commands.Context):
    if ctx.channel.id not in CHANNEL_IDS:
        await ctx.respond("Cette commande ne peut être utilisé que dans le salon <#887377116310675557>", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🔒 Démarrer votre vérification",
        description=f"Bonjour {ctx.author.mention}, je suis Botecam, un bot Discord créé par Bennmane.",
        color=0xFFFFFF
    )

    embed.add_field(name="🚀 Fonctionnalités", value="Je suis un bot de modération pour Discord qui facilite la gestion des serveurs en automatisant la gestion des utilisateurs. J'offre également des fonctionnalités personnalisables comme l'envoi de messages de bienvenue et l'organisation de sondages pour rendre la modération plus efficace.", inline=False)

    embed.add_field(name="🔒 Vérification", value="La vérification que nous effectuons a pour objectif principal d'assurer la sécurité de notre serveur. De plus, elle nous aide à optimiser l'organisation du serveur. Nous envisageons d'implémenter des modifications majeures dans un futur proche, et pour cela, il est essentiel de classifier et de trier les différentes fonctionnalités du serveur. Cette vérification est donc une méthode à la fois simple et efficace pour atteindre ces objectifs.", inline=False)

    embed.add_field(name="📞 Contact", value="Si vous avez besoin d'aide ou si vous avez des questions sur mes fonctionnalités, n'hésitez pas à contacter <@1089985258360946689>.", inline=False)

    embed.set_thumbnail(url="https://link-to-your-bot-icon.png")
    embed.set_footer(text="Botecam | Votre assistant de modération Discord")

    await ctx.author.send(embed=embed)

    await ctx.author.send("Je vous enverrai quelques questions pour vérifier votre identité. Veuillez y répondre.")


    # Here we create the view with the button that has a direct link to the DM
    view = DMButtonView()

    await ctx.respond("Vérifiez vos DM pour poursuivre le processus de vérification.Si vous avez besoin d'aide, vous pouvez envoyer un message à <@1089985258360946689> ou <@508649677189677078>.", view=view, ephemeral=True)

    user = await bot.fetch_user(ctx.author.id)
    questions = [
        "Quel est ton nom et prénom?",
        "En quel année tu t'est inscrit à l'ECAM (ta première année)?",
        "Quel est ton matricule?"
    ]

    answers = []
    year = ""  # Define year here
    for question in questions:
        await user.send(question)
        msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
        answers.append(msg.content)

        if question == "En quel année tu t'est inscrit à l'ECAM (ta première année)?":
            while True:
                if msg.content.isdigit() and 2014 <= int(msg.content) <= 2030:
                    year = msg.content
                    break
                else:
                    await user.send("Veuillez entrer une année valide. ")
                    msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
        elif question == "Quel est ton matricule?":
            while True:
                if msg.content[:2] == "19" and len(msg.content) == 6 and msg.content[2:].isdigit():
                    break
                elif msg.content[:2] == year[-2:] and len(msg.content) == 5 and msg.content[2:].isdigit():
                    break
                else:
                    await user.send("Vous devez entrer un matricule valide. Veuillez réessayer")
                    msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
            answers.append(msg.content)

    await user.send("Quel est ton options bac 2?\n1. EM\n2. GE\n3. IS\n4. CO")
    option_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
    option = option_msg.content.upper()
    while option not in options:
        await user.send("Option invalide. Veuillez réessayer.")
        option_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
        option = option_msg.content.upper()

    await user.send(f"Vous avez choisi l'option {option}. Êtes-vous sûr de votre choix? (oui/non)")
    confirm_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
    while confirm_msg.content.lower() not in ['oui', 'non']:
        await user.send("Veuillez répondre par 'oui' ou 'non'.")
        confirm_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))

    while confirm_msg.content.lower() == 'non':
        await user.send("Quel est ton options bac 2?\n1. EM\n2. GE\n3. IS\n4. CO")
        option_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
        option = option_msg.content.upper()
        while option not in options:
            await user.send("Option invalide. Veuillez réessayer.")
            option_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
            option = option_msg.content.upper()

        await user.send(f"Vous avez choisi l'option {option_names[option]}. Êtes-vous sûr de votre choix? (oui/non)")
        confirm_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
        while confirm_msg.content.lower() not in ['oui', 'non']:
            await user.send("Veuillez répondre par 'oui' ou 'non'.")
            confirm_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))


    code = generate_random_code()
    send_email(answers[2], code)
    await user.send(f"Un code de vérification a été envoyé à {answers[2]}@ecam.be. Veuillez me l'envoyer. Veille à checker tes spam si tu ne trouve pas le mail!.")

    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        code_msg = await bot.wait_for('message', check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel))
        if code_msg.content == str(code):
            await user.send("Votre code est correct. Votre inscription est maintenant terminée.")

            guild = bot.get_guild(GUILD_ID)
            member = await guild.fetch_member(user.id)
            role_ids = [options[option], VERIFIED_ROLE_ID]
            roles = [guild.get_role(role_id) for role_id in role_ids]
            await member.add_roles(*roles, reason="Verification successful")

            log_channel = guild.get_channel(LOG_CHANNEL_ID)
            from datetime import datetime
            current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            log_message = (f"Inscription de : {answers[0]}\n"
                           f"Matricule : {answers[2]}\n"  
                           f"Pseudo : <@{member.id}>\n"
                           f"Date d'inscription à l'ECAM : {answers[1]}\n"
                           f"Option : {option_names.get(option)}\n"
                           f"Date d'inscription au serveur : {current_time}")
            await log_channel.send(log_message)
            break
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                await user.send(f"Le code que vous avez entré est incorrect. Il vous reste {remaining_attempts} tentatives.")
            else:
                await user.send("Vous avez dépassé le nombre maximum de tentatives. Votre inscription a échoué.")
                break

    await ctx.respond("J'ai envoyé quelques questions dans vos DM. Veuillez y répondre.", ephemeral=True, view=DMButtonView())

AUTHORIZED_USERS = [1089985258360946689]

@bot.slash_command(guild_ids=[GUILD_ID], description="Delete a certain number of messages or all messages.")
async def delet_message(ctx: commands.Context, num_messages: int = None, all: bool = False):
    await ctx.defer()  # Indique que le bot est en train de traiter la commande

    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.followup.send("Vous n'êtes pas autorisé à utiliser cette commande.")
        return

    if num_messages is None and not all:
        await ctx.followup.send("Veuillez fournir un nombre de messages à supprimer ou utiliser l'option 'all'.")
        return

    deleted = 0
    async for message in ctx.channel.history():
        if all or deleted < num_messages:
            await message.delete()
            await asyncio.sleep(0.5)  # Ajoute un délai pour éviter de dépasser la limite de taux
            deleted += 1

    await ctx.followup.send(f"Messages supprimés : {deleted}")

AUTHORIZED_USERS = [1089985258360946689]  # Add your ID here
AUTHORIZED_ROLES = [887273798225788949, 887273798225788948]  # Replace with your authorized role IDs

@bot.slash_command(guild_ids=[GUILD_ID], description="A utiliser en cas d'urgence, si quelqu'un s'est fait hacké.")
async def urgence_delet(ctx: commands.Context, member: discord.Member=None):
    if ctx.author.id not in AUTHORIZED_USERS and not any(role.id in AUTHORIZED_ROLES for role in ctx.author.roles):
        await ctx.respond("Vous n'êtes pas autorisé à utiliser cette commande.")
        return

    if member is None:
        await ctx.respond("Veuillez spécifier un utilisateur.")
        return

    deleted = 0
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            try:
                async for message in channel.history():
                    if message.author == member:
                        await message.delete()
                        deleted += 1
                        break
            except discord.Forbidden:
                pass

    await ctx.respond(f"Messages supprimés : {deleted}")
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(f'We have logged in as {bot.user}')
    print(f'Connected to {len(bot.guilds)} guilds.')


bot.run(TOKEN)