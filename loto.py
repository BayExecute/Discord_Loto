import discord, json, random, asyncio, typing
from discord.ext import commands
from random import randint
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"
piyango_uzunluk = 8
Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

async def sayi_cek():
	sayilar = []
	for i in range(piyango_uzunluk):
		sayilar.append(random.randint(0, 9))
		await asyncio.sleep(0.7)
	else:
		with open('loto.json', 'r+') as cmd:
			data = json.load(cmd)
			data["cekilenler"] = (sayilar)
			data["acilan"] = 1
			cmd.seek(0)
			json.dump(data, cmd, indent=4, ensure_ascii=False)
			cmd.truncate()
			return sayilar
async def skor():
	with open('loto.json', 'r+') as cmd:
		data = json.load(cmd)
		oynananlar = data["oynananlar"]
		cekilenler = data["cekilenler"]
		a = 0
		for i in list(oynananlar.values()):
			user = list(oynananlar.keys())[list(oynananlar.values()).index(i)]
			for x in range(len(i)):
				y = i[x]
				z = cekilenler[x]
				if y == str(z): a += 1
			else:
				data["tutanlar"][user] = a
				a = 0
		cmd.seek(0)
		json.dump(data, cmd, indent=4, ensure_ascii=False)
		cmd.truncate()
		await asyncio.sleep(5)

class Loto(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@Bot.command()
	@commands.has_permissions(administrator=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def piyango(self, ctx, bilet: int = 50):
		kazanan = random.randint(1, bilet)
		embed = discord.Embed(title="Piyango sonuçlandı!", description=f"**Kazanan numara: {kazanan}**", color = discord.Color.from_rgb(63, 231, 255)) 
		await ctx.send(embed=embed)

	@slash.command(name="loto", description="Lotoyu yönet!", guild_ids = [810856253403430944, 951580704544796753],
				   options = [
					   Option("islem", "Yapılacak işlem!", Type.STRING, True,
							  choices=[
								  OptionChoice("Sayıları çek", "cek"),
								  OptionChoice("Bir sayıyı aç", "ac"),
								  OptionChoice("Skoru açıkla", "acikla"),
								  OptionChoice("Sıfırla", "sifirla")
						])
				   ])
	async def loto(self, inter, islem):
		if inter.author.id in [735542825285845002, 606432618900094986]:
			if islem == "cek":
				await inter.reply("Çekiliyor...", ephemeral=True)
				tempsayilar = await sayi_cek()
				await inter.edit(f"Sayılar çekildi! {tempsayilar}")
			elif islem == "ac":
				with open('loto.json', 'r+') as cmd:
					data = json.load(cmd)
					sayilar = data["cekilenler"]
					sira = data["acilan"]
					if sira < piyango_uzunluk and not sira == piyango_uzunluk:
						sayi = sayilar[sira]
						data["acilan"] = sira + 1
						cmd.seek(0)
						json.dump(data, cmd, indent=4, ensure_ascii=False)
						cmd.truncate()
					else: sayi = None
				if sayi:
					text = ""
					for i in range(sira):
						text += str(sayilar[i])
					else:
						while len(text) <= 7: text += "▉"
					command_embed = discord.Embed(title="Sayı açılıyor!..", color = discord.Color.from_rgb(63, 231, 255)) 
					await inter.reply(embed=command_embed)
					text = text.replace("1", ":one:").replace("2", ":two:").replace("3", ":three:").replace("4", ":four:").replace("5", ":five:").replace("6", ":six:").replace("7", ":seven:").replace("8", ":eight:").replace("9", ":nine:").replace("0", ":zero:")
					command_embed = discord.Embed(title="Sayı açıldı!", description=text, color = discord.Color.from_rgb(63, 231, 255)) 
					await asyncio.sleep(3)
					await inter.edit(embed=command_embed)
				else:
					text = str(sayilar).replace('"', '').replace(", ", "").replace("[", "").replace("]", "").replace("1", ":one:").replace("2", ":two:").replace("3", ":three:").replace("4", ":four:").replace("5", ":five:").replace("6", ":six:").replace("7", ":seven:").replace("8", ":eight:").replace("9", ":nine:").replace("0", ":zero:")
					command_embed = discord.Embed(title="Tüm sayılar açıldı!", description=text, color = discord.Color.from_rgb(63, 231, 255))
					await inter.reply(embed=command_embed)
			elif islem == "acikla":
				command_embed = discord.Embed(title="Sonuçlar açıklanıyor!..", color = discord.Color.from_rgb(63, 231, 255)) 
				await inter.reply(embed=command_embed)
				await skor()
				with open('loto.json', 'r+') as cmd:
					data = json.load(cmd)
					tutanlar = data["tutanlar"]
					cmd.seek(0)
					json.dump(data, cmd, indent=4, ensure_ascii=False)
					cmd.truncate()

			elif islem == "sifirla":
				with open('loto.json', 'r+') as cmd:
					data = json.load(cmd)
					data["oynananlar"] = {}
					data["cekilenler"] = []
					data["tutanlar"] = {}
					data["acilan"] = 0
					cmd.seek(0)
					json.dump(data, cmd, indent=4, ensure_ascii=False)
					cmd.truncate()
				command_embed = discord.Embed(title="Loto sıfırlandı!", color = discord.Color.from_rgb(63, 231, 255)) 
				await inter.reply(embed=command_embed, ephemeral=True) 

		else:
			command_embed = discord.Embed(title= "Bu komutu kullanma yetkiniz yok!", color = discord.Color.from_rgb(255, 45, 45))
			command_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
			await inter.reply(embed=command_embed, ephemeral=True)

	@slash.command(name="loto_oyna", description="Loto oyna!", guild_ids = [810856253403430944, 951580704544796753], options = [Option("sayi", f"{piyango_uzunluk} tane şanslı sayı! Örnek: 89236145", Type.STRING, True)])
	async def loto_oyna(self, inter, sayi):
		role = discord.utils.find(lambda r: r.id == '959874893430812783', inter.guild.roles)
		if role in inter.author.roles or inter.author.id in [735542825285845002]:
			a = 0
			if len(sayi) == piyango_uzunluk:
				for i in range(len(sayi)):
					try: 
						if int(sayi[i]) or sayi[i] == "0": a += 1
					except: a = 0
			if a == piyango_uzunluk:		
				with open('loto.json', 'r+') as cmd:
					data = json.load(cmd)
					data["oynananlar"][f"{inter.author.id}"] = sayi
					data["tutanlar"][f"{inter.author.id}"] = 0
					cmd.seek(0)
					json.dump(data, cmd, indent=4, ensure_ascii=False)
					cmd.truncate()
				command_embed = discord.Embed(title="Sayılar eklendi!", color = discord.Color.from_rgb(63, 231, 255)) 
				command_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
				await inter.reply(embed=command_embed)
			else:
				command_embed = discord.Embed(title= "Lütfen sayıları düzgün ve yeterli bir şekilde girin!", color = discord.Color.from_rgb(255, 45, 45))
				command_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
				await inter.reply(embed=command_embed, ephemeral=True)
				
		else:
			command_embed = discord.Embed(title= "Lütfen ödeme yapın veya yaptıysanız bir yetkiliye haber verin!", color = discord.Color.from_rgb(255, 45, 45))
			command_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
			await inter.reply(embed=command_embed, ephemeral=True)

def setup(Bot):
    Bot.add_cog(Loto(Bot))
