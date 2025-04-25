import re
from playwright.sync_api import Playwright, sync_playwright, expect
import datetime
import os
#Ver. 1.0.0.7 beta
def run(playwright: Playwright) -> None:
    # Prepare to capture test results
    test_results = []

    def log_result(message):
        test_results.append(message + "\n")
        print(message)  # Optional: Also print to console

    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Step 1: Go to the specified URL
        page.goto("https://lk.epd47.ru/")
        log_result("Step 1: Navigated to https://lk.epd47.ru/ - PASSED")

        # Step 2: Handle the cookie notice
        page.locator("div").filter(has_text="Сайт использует cookie").locator("a").nth(2).click()
        log_result("Step 2: Handled cookie notice - PASSED")

        # Step 3: Navigate to login
        page.get_by_role("link", name="Войти через личный кабинет").click()
        log_result("Step 3: Navigated to login - PASSED")

        # Step 4: Fill in login credentials
        #Подставляются актуальные даннык лкк
        page.get_by_role("textbox", name="Логин").fill("Login") 
        page.get_by_role("textbox", name="Пароль").fill("Pasw")
        log_result("Step 4: Filled in login credentials - PASSED")

        # Step 5: Click the login button
        page.get_by_role("button", name="Войти Войти").click()
        log_result("Step 5: Clicked login button - PASSED")

        # Step 6: Handle 2FA modal
        page.locator("#modal-2fa").get_by_role("button").click()
        log_result("Step 6: Handled 2FA modal - PASSED")

        # Step 7: Navigate to лицевые счета
        page.get_by_role("link", name="Лицевые счета").click()
        log_result("Step 7: Navigated to лицевые счета - PASSED")

        # Step 8: Select account
        #LS пример 050001004672 используется для скачивания
        page.get_by_text(".a { fill: none; } .b { fill: #F86512; } Адрес").click() 
        log_result("Step 8: Selected account - PASSED")
        # Step 9: Navigate to квитанция/Справки
        page.get_by_text("Квитанция/Справки").click()
        log_result("Step 9: Navigated to квитанция/Справки - PASSED")

        # Step 10: Download квитанция
        page.get_by_role("link", name="Квитанция").click()
        with page.expect_download() as download_info:
            with page.expect_popup() as page1_info:
                page.get_by_role("button", name="Квитанция").click()
            page1 = page1_info.value
        download = download_info.value
        page1.close()
        page1.close()
        log_result("Step 10: Downloaded квитанция - PASSED")

        # Final Result
        log_result("TEST RUN PASSED")

    except Exception as e:
        log_result(f"TEST RUN FAILED: {str(e)}")

    finally:
        # Always close resources
        if 'context' in locals():
            context.close()
        if 'browser' in locals():
            browser.close()

        # Ensure the 'report' directory exists
        report_dir = "report"
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        # Write results to a text file in the 'report' directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(report_dir, f"test_report_{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as report_file:  # Specify encoding here
            report_file.writelines(test_results)
        print(f"Test report saved to {filename}")

with sync_playwright() as playwright:
    run(playwright)
