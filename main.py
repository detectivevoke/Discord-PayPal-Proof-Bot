from bs4 import BeautifulSoup
from discord.ext import commands
from playwright.async_api import async_playwright
from PIL import Image
import discord
import datetime
import re
import os

tk = "TOKEN"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")


class PayPal(object):
    def __init__(self):
        self.start_time = str(datetime.datetime.now().time())[0:5]
        self.dir = os.path.dirname(os.path.abspath(__file__))

    def find_replace(self,soup,looking_for, replacing_with):
        t = soup.find_all(string=re.compile(looking_for))
        for x in t:
            x.replace_with(x.replace(looking_for,replacing_with))
        return True


    def edit(self, amount=None,email=None):
        if amount is None:
            amount = "100"
        if email is None:
            email = "detectivevoke@gmail.com"
        html = open("html/paypal.html","r").read()
        soup = BeautifulSoup(html,features="html.parser")

        self.find_replace(soup,"AMOUNT",amount)
        self.find_replace(soup,"EMAIL",email)
        return str(soup)

    def image_crop(self,img):
        image = Image.open(img)
        rgb_im = image.convert('RGB')
        new_image = rgb_im.crop((250, 0, 1000, 500))
        new_image.save(img)
        return img

    async def screenshot(self,path):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            await page.goto('http://127.0.0.1:3000')
            await page.screenshot(path=path)
            await browser.close()
        return path



@bot.command()
async def paypal(ctx, amount=None,email=None):
    message = await ctx.send(embed=discord.Embed(color=discord.Colour.green(),description="Creating your image..."))
    try:
        os.remove("html/new.html")
    except:
        open("html/new.html", 'a')
    x = PayPal()
    soup = x.edit(amount,email)
    open("html/new.html","a").write(str(soup))
    path = await x.screenshot(path="html/voke.png")
    path = x.image_crop(path)
    await message.delete()
    await ctx.send(ctx.author.mention,file=discord.File(path))



bot.run(tk)