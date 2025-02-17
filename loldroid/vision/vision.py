import gc
from pathlib import Path

import cv2
import numpy as np
from mss import mss

from common import Template, Match
from logger import get_logger, debug_coro

logger = get_logger("loldroid.Vision")


class Vision:
    def __init__(
        self,
        bounding_box={
            "top": 0,
            "left": 0,
            "width": 1920,
            "height": 1080,
        },
    ):
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.templates = list()
        self.matches = list()
        self.bounding_box = bounding_box
        self.thresholds = {
            "minion": 0.99,
            "champion": 0.90,
            "building": 0.90,
            "Morgana": 0.60,
            "Trundle": 0.80,
        }

    @debug_coro(logger)
    async def load_templates(self, names: list, folder: str):
        for name in names:
            await self.load_template(folder=folder, name=name)

    @debug_coro(logger)
    async def load_template(self, folder: str, name: str):
        path = str(Path(__file__).parent.absolute()) + "/patterns"
        img = cv2.imread(f"{path}/{folder}/{name}.png", 0)
        name = name.split("_")[0]
        self.templates.append(Template(name=name, img=img))

    @debug_coro(logger)
    async def screenshot(self):
        self.sct_original = np.asarray(self.sct.grab(self.bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    @debug_coro(logger)
    async def get_match(self, name):
        for match in self.matches:
            if match.name == name:
                return match

    @debug_coro(logger)
    async def clear_templates(self):
        del self.templates
        gc.collect()
        self.templates = list()

    @debug_coro(logger)
    async def clear_matches(self):
        del self.matches
        gc.collect()
        self.matches = list()

    @debug_coro(logger)
    async def match_all(self, match, threshold):
        loc = np.where(match > threshold)
        return zip(*loc[::-1])

    @debug_coro(logger)
    async def match_best(self, match, threshold):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        if max_val < threshold:
            return []
        return [max_loc]

    @debug_coro(logger)
    async def match(self, match_best_only: bool = False):
        await self.clear_matches()
        for template in self.templates:
            try:
                w, h = template.img.shape[::-1]
                match = cv2.matchTemplate(
                    self.sct_img, template.img, cv2.TM_CCOEFF_NORMED
                )
                threshold = self.thresholds.get(template.name) or 0.70
                if match_best_only:
                    pts = await self.match_best(match, threshold)
                else:
                    pts = await self.match_all(match, threshold)
                for pt in pts:
                    x = pt[0] + int(w / 2)
                    y = pt[1] + int(h / 2)
                    team = "ORDER"
                    if await self.pixel_color_above_threshold(x, y, "red", 100):
                        team = "CHAOS"
                    self.matches.append(Match(name=template.name, x=x, y=y, team=team))
            except:
                logger.error(f"Template is {template}")

    @debug_coro(logger)
    async def mark_the_spot(self):
        for match in self.matches:
            color = (0, 255, 255)
            if match.team == "CHAOS":
                color = (0, 0, 255)
            if match.team == "ORDER":
                color = (255, 255, 0)
            cv2.circle(self.sct_original, (match.x, match.y), 15, color, 2)
            cv2.putText(
                self.sct_original,
                match.name,
                (match.x, match.y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
            )

    @debug_coro(logger)
    async def pixel_color_above_threshold(self, x, y, channel, threshold):
        COLORS = {"blue": 0, "green": 1, "red": 2}
        channel = COLORS[channel.lower()]
        pixel_color = tuple(int(x) for x in self.sct_original[y][x])
        return pixel_color[channel] > threshold
