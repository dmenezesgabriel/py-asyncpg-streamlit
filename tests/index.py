import asyncio
import logging

from playwright.async_api import Playwright, async_playwright

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


async def run_async(playwright: Playwright, instance_name):
    logger.info(f"running instance: {instance_name}")
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    try:
        await page.goto("http://localhost:8501/")
        await page.get_by_test_id("stPopover").get_by_test_id(
            "baseButton-secondary"
        ).click()
        await page.get_by_test_id("stTextInput-RootElement").get_by_label(
            "Title"
        ).fill(f"test_{instance_name}")

        await page.get_by_test_id("baseButton-secondaryFormSubmit").click()
        await page.get_by_test_id("stButton").get_by_test_id(
            "baseButton-secondary"
        ).click()
    except Exception as error:
        logger.error(error)

    # ---------------------
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        tasks = []
        num_instances = 10  # Number of concurrent instances to run

        for i in range(num_instances):
            tasks.append(run_async(playwright, instance_name=i))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
