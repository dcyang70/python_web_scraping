from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException, NoSuchElementException
import time, os

def get_mangaz_driver() -> webdriver:
    options = Options()

    options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    options.add_experimental_option('useAutomationExtension', False) 
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36") 

    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗
    options.add_argument("--incognito") # 無痕模式
    options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10) # 隱性等待

    url = "https://www.mangaz.com/book/detail/157901"
    driver.get(url)
    print("Page Title:", driver.title)
    return driver

def click_free_btn(driver:webdriver):
    # 使用 CSS_SELECTOR 定位「免費閱讀」按鈕
    # CSS Selector：'button.open-viewer.book-begin.ga'
    button = driver.find_element(By.CSS_SELECTOR, 'button.open-viewer.book-begin.ga' )
    button.click()

def switch_to_intermediate_wnd(driver:webdriver):
    # 取得所有視窗的代號（Handle）列表
    all_windows = driver.window_handles
    # 切換到最後一個（最新開啟的）視窗
    driver.switch_to.window(all_windows[-1])

def click_readnow(driver:webdriver):
    # 使用 PARTIAL_LINK_TEXT 定位「すぐに読む」連結元素
    Read_Now = driver.find_element(By.PARTIAL_LINK_TEXT, 'すぐに読む')
    Read_Now.click()

def create_download_folder(folder:str):
    if not os.path.exists(f"{folder}"):
        os.mkdir(folder)
    if not folder.endswith('/'):
        return folder+'/'
    return folder

def scraping(driver:webdriver, to_folder:str):
    # 建立顯式等待物件，設定最長等待時間為 10 秒
    #   提示：WebDriverWait(driver, 秒數)
    # --- 請在此填寫 ---
    wait_element = WebDriverWait(driver, 10)

    # TODO 16：設定全域圖片計數器（初始值為 0）
    #   用途：防止翻頁後檔名重複覆蓋
    # --- 請在此填寫 ---
    total_image_count = 0

    # 2. 進入無窮迴圈
    while True:

        # ── 步驟 A：擷取當前頁面圖片 ──────────────────────────────────────────

        # TODO 17：使用 find_elements 取得當前頁面所有符合條件的圖片元素
        #   CSS Selector：'div.page_image img.image'
        #   注意：find_elements（複數）回傳串列；find_element（單數）回傳單一元素
        # --- 請在此填寫 ---
        image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.page_image img.image')

        for img_element in image_elements:
            # 只處理目前畫面上「可見」的圖片，避免抓到隱藏元素
            if img_element.is_displayed():
                file_path = f"{to_folder}manga_page_{total_image_count}.png"

                # TODO 18a：對該圖片元素截圖，並儲存到 file_path
                #   提示：Selenium WebElement 本身有 .screenshot(路徑) 方法
                # --- 請在此填寫 ---
                img_element.screenshot(file_path)
                print(f"成功擷取頁面並儲存為: {file_path}")

                # TODO 18b：每成功儲存一張圖，將計數器加 1
                # --- 請在此填寫 ---
                total_image_count += 1

        # ── 步驟 B：嘗試尋找並點擊「下一頁」按鈕 ─────────────────────────────
        try:
            # TODO 18c：使用 wait_element.until(EC.element_to_be_clickable(...))
            #   等待 CSS Selector 為 'div.flip.flip-left' 的元素出現且可點擊
            #   注意：EC.element_to_be_clickable 傳入的是 (By.xxx, '選擇器') 的 tuple
            # --- 請在此填寫 ---
            next_page = wait_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.flip.flip-left')) )

            # TODO 18d：點擊下一頁按鈕
            # --- 請在此填寫 ---
            next_page.click()

            print("已點擊下一頁，等待畫面載入...")

            # TODO 18e：點擊後強制等待 2 秒，確保 DOM 與圖片載入完成
            #   提示：time.sleep(秒數)
            # --- 請在此填寫 ---
            time.sleep(2)


        # ── 步驟 C：Break Condition ────────────────────────────────────────────
        except TimeoutException:
            # 等待超過 10 秒仍找不到下一頁按鈕 → 已到達最後一頁
            print("【系統提示】找不到下一頁按鈕，已達最後一頁，結束爬取迴圈。")
            break

def drop_mangaz_driver(driver:webdriver):
    driver.quit()

if __name__ == '__main__':
    driver = get_mangaz_driver()
    click_free_btn(driver)
    switch_to_intermediate_wnd(driver)
    click_readnow(driver)
    folder = create_download_folder('downloaded_manga')
    #print("main:", folder)
    scraping(driver, folder)
    drop_mangaz_driver(driver)
