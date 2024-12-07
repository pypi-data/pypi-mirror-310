from typing import Callable, Optional, List, Tuple, Any, Union, Dict
from tools import thread
from discord.ext.commands import Context, CommandError, ColorConverter, ColourConverter, Converter
from fast_string_match import closest_match_distance as cmd
from discord.ext import commands
from discord import Color, User, Member, File, Embed, Message
import pickle
import aiohttp
import seaborn as sns
from loguru import logger
import numpy as np
import math
from pkg_resources import resource_filename
import asyncio
import re
from io import BytesIO
from itertools import chain
import webcolors
from pydantic import BaseModel as BM

class BaseModel(BM):
    class Config:
        arbitrary_types_allowed=True
class WebSafe(BaseModel):
    hex: str
    rgb: Tuple[int]

class ColorInfoResponse(BaseModel):
    name: Optional[str] = None
    hex: str
    websafe: WebSafe
    rgb: Tuple[int]
    brightness: int
    shades: List[str]
    palette: BytesIO
    image: BytesIO

    @property
    def embed(self) -> Dict[str, Any]:
        shade = ", ".join(m.strip("#") for m in self.shades[:4])
        rgb = f"({self.rgb[0]}, {self.rgb[1]}, {self.rgb[2]})"
        embed = Embed(title=f"{hex[0]} ({hex[1]})", color=Color.from_str(hex[1]))
        embed.add_field(name="Websafe", value=f"`{self.websafe.hex} ({self.websafe.rgb})`", inline=True)
        embed.add_field(name="RGB", value=f"`{rgb}`", inline=True)
        embed.set_image(url="attachment://palette2.png")
        embed.add_field(name="Brightness", value=self.brightness, inline=True)
        embed.add_field(name="Shades", value=f"```{shade}```", inline=False)
        embed.set_thumbnail(url="attachment://palette.png")
        return {"files": [File(fp = self.image, filename = "color.png"), File(fp = self.palette, filename = "palette.png")], "embed": embed}
    
    async def to_message(self, ctx: Context) -> Message:
        return await ctx.send(**self.embed)
    




class Colors:
    def __init__(self, thread_handler: Optional[Callable] = thread):
        self.thread_handler = thread_handler
        self.colors = None

    async def generate_palette(self, hex_color: str):
        @self.thread_handler
        def generate(hex_color: str):
            from PIL import Image
            from io import BytesIO
            output = BytesIO()
            image = Image.new("RGB", (150, 150), hex_color)
            image.save(output, format="PNG")
            output.seek(0)
            return output
        return await generate(hex_color)

    def brightness(self, color_rgb):
        return (0.299 * color_rgb[0] + 0.587 * color_rgb[1] + 0.114 * color_rgb[2]) / 255

    def generate_color_swatch(self, color_hex):
        color_rgb = tuple(int(color_hex.lstrip("#")[i: i + 2], 16) for i in (0, 2, 4))
        color_swatch = np.full((100, 100, 3), color_rgb, dtype=np.uint8)
        return color_swatch

    def get_shades(self, color_hex: str, amount: Optional[int] = 5, darker: Optional[bool] = True) -> List[str]:
        rgb_color = webcolors.hex_to_rgb(color_hex)
        amount = amount - 1
        if darker:
            shades = [
                webcolors.rgb_to_hex(
                    (
                        int(rgb_color[0] * (1 - i / amount)),
                        int(rgb_color[1] * (1 - i / amount)),
                        int(rgb_color[2] * (1 - i / amount)),
                    )
                )
                for i in range(1, amount + 1)
            ]
        else:
            shades = [
                webcolors.rgb_to_hex(
                    (
                        int(min(rgb_color[0] + i / amount, 1)),
                        int(min(rgb_color[1] + i / amount, 1)),
                        int(min(rgb_color[2] + i / amount, 1)),
                    )
                )
                for i in range(1, amount + 1)
            ]
        shades.insert(0, color_hex)
        return shades

    async def generate_multi_palette(self, shades: List[str]):
        @self.thread_handler
        def generate(shades: List[str]):
            import numpy as np
            from PIL import Image, ImageFont, ImageDraw
            from io import BytesIO
            num_colors = len(shades)
            images = []

            num_per_row = (num_colors + 1) // 2  # Number of images per row

            for color_hex in shades:
                color_rgb = tuple(int(color_hex.lstrip("#")[i: i + 2], 16) for i in (0, 2, 4))
                color_swatch = np.full((100, 100, 3), color_rgb, dtype=np.uint8)
                images.append(color_swatch)

            images_row1 = images[:num_per_row]
            images_row2 = images[num_per_row:]

            collage_row1 = np.concatenate(images_row1, axis=1)
            collage_row2 = np.concatenate(images_row2, axis=1)

            collage_combined = np.concatenate([collage_row1, collage_row2], axis=0)
            collage_image = Image.fromarray(collage_combined)

            font = ImageFont.load_default()
            draw = ImageDraw.Draw(collage_image)

            for i, color_hex in enumerate(shades):
                row_index = i // num_per_row
                col_index = i % num_per_row
                x = col_index * 100 + 10
                y = row_index * 100 + 70

                color_rgb = tuple(int(color_hex.lstrip("#")[i: i + 2], 16) for i in (0, 2, 4))
                label_color = "black" if self.brightness(color_rgb) > 0.5 else "white"

                draw.text((x, y), color_hex, fill=label_color, font=font)

            buf = BytesIO()
            collage_image.save(buf, format="PNG")
            buf.seek(0)
            return buf
        return await generate(shades)

    def hex_to_brightness(self, color_hex: str) -> int:
        color_rgb = tuple(int(color_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        return int(self.brightness(color_rgb) * 100.0)

    async def load_color_map(self):
        @self.thread_handler
        def load():
            def split_tuple_of_tuples(tuple_of_tuples: Tuple[Tuple[Any, Any]], size: Optional[int] = 4):
                chunk_size = len(tuple_of_tuples) // size
                return tuple(
                    tuple_of_tuples[i: i + chunk_size]
                    for i in range(0, len(tuple_of_tuples), chunk_size)
                )
            pickle_file_path = resource_filename(__name__, 'data/colors.pkl')
            with open(pickle_file_path, "rb") as file:
                _ = split_tuple_of_tuples(pickle.load(file))
            return _
        if not self.colors:
            self.colors = await load()

    async def color_picker_(self, query: str, colors: tuple):
        if match := cmd(query, [k[0] for k in colors]):
            return [m for m in colors if m[0] == match]
        return None

    def hex_to_rgb(self, hex_color: Any):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i: i + 2], 16) for i in (0, 2, 4))

    def rgb_distance(self, color1: Any, color2: Any):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    def nearest_color(self, target_color: Any, color_list: Any):
        target_rgb = self.hex_to_rgb(target_color)
        closest_color = None
        min_distance = float("inf")

        for color in color_list:
            color_rgb = self.hex_to_rgb(color)
            distance = self.rgb_distance(target_rgb, color_rgb)
            if distance < min_distance:
                min_distance = distance
                closest_color = color

        return closest_color

    async def find_name(self, hex_: str):
        async def _find_name(hex_: str, colors: tuple):
            try:
                return [c for c in colors if c[1] == hex_][0]
            except Exception:
                return None

        data = await asyncio.gather(*[_find_name(hex_, c) for c in self.colors])
        data = [d for d in data if d is not None]
        if len(data) != 0:
            return data[0]
        else:
            return "unnamed"

    def get_websafe(self, color_hex: str) -> tuple:
        print(color_hex)
        rgb = webcolors.hex_to_rgb(color_hex)
        web_safe_rgb = [int(round(val / 51) * 51) for val in rgb]
        print(web_safe_rgb)
        web_safe_hex = webcolors.rgb_to_hex(web_safe_rgb)
        return web_safe_hex, web_safe_rgb

    async def closest_color(self, color_hex: str, name: Optional[bool] = False, with_websafe: Optional[bool] = False):
        await self.load_color_map()
        color_list = []
        for colo in self.colors:
            _color_list = [c[1] for c in colo]
            color_list.extend(_color_list)
        nearest = self.nearest_color(color_hex, color_list)
        next((c for colo in self.colors for c in colo if c[1] == nearest), None)
        rgb = webcolors.hex_to_rgb(color_hex)
        web_safe_rgb = [round(val / 51) * 51 for val in rgb]
        web_safe_hex = webcolors.rgb_to_hex(web_safe_rgb)
        if name:
            color_name = await self.find_name(web_safe_hex)
            data = (color_name, nearest)
        else:
            data = nearest
        return data
    
    async def color_info(self, query: Union[str, Member, User]) -> ColorInfoResponse:
        if isinstance(query, str):
            if query.startswith("https://"):
                query = await self.get_dominant_color(query)
        if isinstance(query, (Member, User)):
            query = await self.get_dominant_color(query.display_avatar.url)
        await self.load_color_map()
        if query.startswith("#"):
            hex = ((await self.closest_color(query, True))[0][0], query)
        else:
            try:
                Color.from_str(f"#{query}")
            except Exception:
                pass
            hex = await self.color_search(query)
        websafe, websafe_rgb = self.get_websafe(hex[1])
        palette = await self.generate_palette(hex[1])
        rg = webcolors.hex_to_rgb(hex[1])
        shades = self.get_shades(hex[1], 11)
        shades.extend(self.get_shades(hex[1], 11, False))
        palette2 = await self.generate_multi_palette(shades)
        rgb = f"({rg[0]}, {rg[1]}, {rg[2]})"
        data = {"name": hex[0], "hex": hex[1], "websafe": {"hex": websafe, "rgb": websafe_rgb}, "rgb": (rg[0], rg[1], rg[2]), "brightness": self.hex_to_brightness(hex[1]), "shades": shades, "palette": palette, "image": palette2}
        return ColorInfoResponse(**data)

    async def color_info_embed(self, ctx: Context, query: str):
        if query.startswith("https://"):
            query = await self.get_dominant_color(query)
        await self.load_color_map()
        if query.startswith("#"):
            hex = ((await self.closest_color(query, True))[0][0], query)
        else:
            try:
                Color.from_str(f"#{query}")
            except Exception:
                pass
            hex = await self.color_search(query)
        websafe = self.get_websafe(hex[1])
        palette = await self.generate_palette(hex[1])
        rg = webcolors.hex_to_rgb(hex[1])
        shades = self.get_shades(hex[1], 11)
        shades.extend(self.get_shades(hex[1], 11, False))
        palette2 = await self.generate_multi_palette(shades)
        shade = ", ".join(m.strip("#") for m in shades[:4])
        rgb = f"({rg[0]}, {rg[1]}, {rg[2]})"
        embed = Embed(title=f"{hex[0]} ({hex[1]})", color=Color.from_str(hex[1]))
        embed.add_field(name="Websafe", value=f"`{websafe}`", inline=True)
        embed.add_field(name="RGB", value=f"`{rgb}`", inline=True)
        embed.set_image(url="attachment://palette2.png")
        embed.add_field(name="Brightness", value=self.hex_to_brightness(hex[1]), inline=True)
        embed.add_field(name="Shades", value=f"```{shade}```", inline=False)
        embed.set_thumbnail(url="attachment://palette.png")
        return await ctx.send(
            files=[
                File(fp=palette2, filename="palette2.png"),
                File(fp=palette, filename="palette.png"),
            ],
            embed=embed,
        )

    async def color_search(self, query: str, with_websafe: Optional[bool] = False):
        await self.load_color_map()
        if query == "black":
            return ("Black", "#010101")
        if hex_match := re.match(r"#?[a-f0-9]{6}", query.lower()):
            color_name = await self.closest_color(query, True, True)
            return (color_name[1], query)
        matches = []
        matches = list(
            chain.from_iterable(
                await asyncio.gather(*[self.color_picker_(query, _) for _ in self.colors])
            )
        )
        match = cmd(query, tuple([k[0] for k in matches]))
        _ = [m for m in matches if m[0] == match][0]
        return _

    async def get_dominant_color(self, u: Union[Member, User, str]) -> str:
        @self.thread_handler
        def get(url: str) -> str:
            from colorgram_rs import get_dominant_color as get_dom
            return get_dom(url)

        if isinstance(u, (Member, User)):
            _ = await get(await u.display_avatar.read())
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(u) as resp:
                    _u = await resp.read()
            _ = await get(_u)
        return f"#{_}"
    
class ColorHolder:
    _colors: Optional[Colors] = None

    @classmethod
    def get_colors(cls, *args: Any) -> Colors:
        if cls._colors is None:
            cls._colors = Colors(*args)
        return cls._colors
        

class ColorConverter(Converter):
    async def convert(self, ctx: Context, argument: Union[Color, str]):
        colors = ColorHolder.get_colors()
        if isinstance(argument, Color):
            return argument
        elif argument.lower().startswith("0x"):
            return Color.from_str(argument)
        else:
            argument = str(argument).lower()
            try:
                if argument.startswith("#"):
                    return Color.from_str(argument)
                else:
                    return Color.from_str(f"#{argument}")
            except Exception:
                pass
            try:
                if argument.lower() in ("dom", "dominant"):
                    return Color.from_str(await colors.get_dominant_color(ctx.author))
                else:
                    _ = await colors.color_search(argument)
                    if isinstance(_, tuple):
                        _ = _[1]
                    return Color.from_str(_)
            except Exception as e:
                logger.info(f"Color Converter Errored with : {e}")
                raise CommandError("Invalid color hex given")
            
class ColorInfo(Converter):
    async def convert(self, ctx: Context, argument: Union[Color, str, Member, User]):
        if isinstance(argument, Color):
            argument = str(argument)
        colors = ColorHolder.get_colors()
        information = await colors.color_info(argument)
        return await information.to_message(ctx)


commands.ColorInfo = ColorInfo
ColourConverter.convert = ColorConverter.convert