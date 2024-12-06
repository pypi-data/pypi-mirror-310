import asyncio
from io import BytesIO
import re
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

import platform
from PIL import Image
from playwright.async_api import async_playwright
from playwright.async_api._generated import Page, Locator

from naotool.img.op import crop_to_max_height, add_top_border

__all__ = [
    "Xpost",
    "get_xposts",
]


class Xpost:
    id: str
    url: str
    sub_id: str
    text: str
    img_urls: list[str]
    timestamp: float
    date_time: datetime
    screenshot: bytes

    def __init__(
        self,
        id: str = None,
        url: str = None,
        sub_id: str = None,
        text: str = None,
        img_urls: list[str] = None,
        timestamp: float = None,
        date_time: datetime = None,
        screenshot: bytes = None,
    ):
        self.id = id
        self.url = url
        self.sub_id = sub_id
        self.text = text
        self.img_urls = img_urls
        self.timestamp = timestamp
        self.date_time = date_time
        self.screenshot = screenshot

    def __str__(self) -> str:
        dic = {}
        for k, v in self.__dict__.items():
            if v.__sizeof__() > 500:
                dic[k] = str(v)[:50] + str(v)[-50:]
            else:
                dic[k] = v
        return json.dumps(
            obj=dic,
            indent=4,
            ensure_ascii=False,
            default=lambda x: (
                x.strftime("%Y-%m-%d %H:%M:%S %Z")
                if isinstance(x, datetime)
                else str(x)
            ),
        )

    def __repr__(self) -> str:
        dic = {}
        for k, v in self.__dict__.items():
            dic[k] = v
        return json.dumps(
            obj=dic,
            indent=0,
            ensure_ascii=False,
            default=lambda x: (
                x.strftime("%Y-%m-%d %H:%M:%S %Z")
                if isinstance(x, datetime)
                else str(x)
            ),
        )


async def get_xposts(
    user_data_dir: str | Path,
    *,
    sub_ids: list[str] = ["home"],
    limit: int = 3,
    last_time: float = 0.0,
    img_dir: str = None,
    recommend: bool = False,
    local_timezone: timezone = timezone(timedelta(hours=8)),
    wait_time: int = 3,
    **playwright_args,
) -> list[Xpost]:
    """return Xposts list, sorted from old to new.

    Args:
        sub_ids (str):
            subscription id list. (note: not name.)
        limit (int, optional):
            assert `len(xpost_list) <= limit`.
        last_time (float):
            assert `xpost.timestamp > last_time`.
        img_dir (str):
            the directory to save screenshot (*.jpg).
        recommend (bool):
            when sub_id='home', whether to fetch recommended content.
        wait_time (int):
            general wait time.
            `asyncio.sleep(wait_time)`

    Returns:
        list[Xpost]: Xpost list.
    """

    x_cache: dict[str, list[Xpost]] = {}
    async with async_playwright() as ap:
        # 0.init
        browser_context = await ap.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            ignore_default_args=["--enable-automation"],
            args=[
                "--disable-infobans",
                "--disable-blink-features=Automationcontrolled",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-web-security",
                "--disable-extensions",
            ],
            **playwright_args,
        )
        page = await browser_context.new_page()
        res = []
        for sub_id in sub_ids:
            try:
                if sub_id in x_cache:
                    xs = x_cache[sub_id]
                else:
                    xs = await _get_sub_posts(
                        page=page,
                        sub_id=sub_id,
                        limit=limit,
                        last_time=last_time,
                        img_dir=img_dir,
                        recommend=recommend,
                        local_timezone=local_timezone,
                        wait_time=wait_time,
                    )
                    x_cache[sub_id] = xs
                res += xs
            except Exception as e:
                print(f"error: fetch {sub_id} error!")
                print(e)
                # traceback.print_exc()
        return res


async def _get_sub_posts(
    page: Page,
    sub_id: str = "home",
    limit: int = 3,
    last_time: float = 0.0,
    img_dir: str = None,
    recommend: bool = False,
    local_timezone: timezone = timezone(timedelta(hours=8)),
    wait_time: int = 3,
) -> list[Xpost]:
    """return Xposts list, sorted from old to new.

    Args:
        page (Page): page.
        sub_id (str):
            subscription id. (note: not name.)
        limit (int, optional):
            assert `len(xpost_list) <= limit`.
        last_time (float):
            assert `xpost.timestamp > last_time`.
        img_dir (str):
            the directory to save screenshot (*.jpg).
        recommend (bool):
            when sub_id='home', whether to fetch recommended content.
        wait_time (int):
            general wait time.
            `asyncio.sleep(wait_time)`

    Returns:
        list[Xpost]: Xpost list.
    """
    # 1.goto
    await page.goto(f"https://x.com/{sub_id}")
    await page.wait_for_load_state()
    await asyncio.sleep(wait_time)  # 给页面加载时间
    if sub_id == "home":
        if recommend:
            sub_tab = page.locator(
                "xpath=//main/div/div/div/div[1]/div/div[1]"
                "/div[1]/div/nav/div/div[2]/div/div[1]"
            )
        else:
            sub_tab = page.locator(
                "xpath=//main/div/div/div/div[1]/div/div[1]/"
                "div[1]/div/nav/div/div[2]/div/div[2]"
            )
        await sub_tab.click()
    # 2.page down
    for _ in range(2):
        await page.keyboard.press("PageDown")
        await asyncio.sleep(wait_time)  # 给页面加载时间
    # 3.get Locator by xpath
    time_loc = page.locator("xpath=//time")
    # 4.for url list
    res: list[Xpost] = []
    for t in await time_loc.all():
        xp = Xpost()
        # date_time
        utc_datetime_s = await t.get_attribute("datetime")
        if utc_datetime_s:
            utc_datetime = datetime.strptime(
                utc_datetime_s,
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
            xp.timestamp = utc_datetime.timestamp()
            if xp.timestamp <= last_time:  # out time
                continue
            xp.date_time = utc_datetime.astimezone(local_timezone)
        # start
        xp.sub_id = sub_id
        await t.click()
        await page.wait_for_load_state()  # wait
        await asyncio.sleep(wait_time)  # wait
        xp.url = page.url
        xp.id = extract_trailing_numbers(xp.url)
        # screenshot
        sections: Locator = page.locator("xpath=//section")
        section = sections.first
        if sections:
            xp.screenshot = await section.screenshot(type="jpeg")
            img = crop_to_max_height(Image.open(BytesIO(xp.screenshot)), 3000)
            img = add_top_border(img, 200)
            if img_dir:
                img_path = Path(img_dir) / f"{xp.id}.jpg"
                img.save(str(img_path), format="JPEG")
        # text
        articles: Locator = page.locator("xpath=//article")
        article = articles.first
        if text := await article.text_content():
            xp.text = text
        # img_urls
        xp.img_urls = []
        img_list = page.locator("xpath=//img | //video")
        for img in await img_list.all():
            img_url = await img.get_attribute("src")
            if not img_url:
                img_url = await img.get_attribute("poster")
            if (
                not img_url
                or not (
                    img_url.startswith("https://pbs.twimg.com/media/")
                    or img_url.startswith("https://pbs.twimg.com/card_img")
                    or img_url.startswith("https://pbs.twimg.com/ext_tw_video_thumb")
                    or xp.id in img_url
                )
                or img_url in xp.img_urls
            ):
                continue
            elif (pack := img_url.split("?")) and len(pack) > 1:
                # ps = pack[1].split("&")
                # params = "&".join([p for p in ps if "format=" in p])
                # img_url = f"{pack[0]}?{params}"
                img_url = img_url.replace("name=medium", "")
                img_url = img_url.replace("name=small", "name=medium")
            xp.img_urls.append(img_url)
        # goback
        await page.go_back()
        # res
        res.append(xp)
        if len(res) >= limit:
            break
    res.sort(key=lambda x: x.timestamp)
    return res


def extract_trailing_numbers(s) -> str:
    match = re.search(r"(\d+)$", s)
    return match.group(1) if match else 0


if __name__ == "__main__":
    xposts = asyncio.run(get_xposts(["home"], limit=6))
    print(xposts)
