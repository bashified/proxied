from colorama import Fore, Style, init
import threading
from itertools import cycle

from src.checkers import *
from src.scraper import *

MAX_THREADS = int(input("Number of threads (Defaults to 10): ") or 10)
thread_lock = threading.Lock()
mode = input("Mode (Colorful/Normal) Defaults to Normal: ")

init(autoreset=True)

INPUT_DIR = "input"
OUTPUT_DIR = "output"
TEST_URL = "http://httpbin.org/ip"
WS_TEST_URL = "ws://echo.websocket.events"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def log(status: None, message):
    if mode.lower() == "colorful":
        rainbow = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA])
        prefix = f"{Fore.MAGENTA}[~]{Fore.WHITE} "

        rainbow_text = ''.join(next(rainbow) + char for char in message)
        print(prefix + rainbow_text + Fore.RESET)
    else:
        color = {
        "valid": Fore.GREEN,
        "invalid": Fore.RED,
        "info": Fore.CYAN
        }.get(status, Fore.WHITE)
        print(f"{color}[{'+' if status == 'valid' else '-' if status == 'invalid' else '*'}]{Fore.WHITE} {message}")

def check(proxy, output_path):
    try:
        # requests
        start = time.time()
        if checkreq(proxy):
            elapsed = round((time.time() - start) * 1000)
            log("valid", f"{proxy} is valid for requests ({elapsed}ms)")
            with thread_lock:
                with open(output_path, "a") as f:
                    f.write(f"{proxy} | requests: {elapsed}ms\n")
        else:
            log("invalid", f"{proxy} invalid for requests")

        # socket
        start = time.time()
        if checksock(proxy):
            elapsed = round((time.time() - start) * 1000)
            log("valid", f"{proxy} is valid for socket ({elapsed}ms)")
            with thread_lock:
                with open(output_path, "a") as f:
                    f.write(f"{proxy} | socket: {elapsed}ms\n")
        else:
            log("invalid", f"{proxy} invalid for socket")

        # websocket
        start = time.time()
        if checkwebsock(proxy):
            elapsed = round((time.time() - start) * 1000)
            log("valid", f"{proxy} is valid for websocket ({elapsed}ms)")
            with thread_lock:
                with open(output_path, "a") as f:
                    f.write(f"{proxy} | websocket: {elapsed}ms\n")
        else:
            log("invalid", f"{proxy} invalid for websocket")

        # httpx
        start = time.time()
        if checkhttpx(proxy):
            elapsed = round((time.time() - start) * 1000)
            log("valid", f"{proxy} is valid for httpx ({elapsed}ms)")
            with thread_lock:
                with open(output_path, "a") as f:
                    f.write(f"{proxy} | httpx: {elapsed}ms\n")
        else:
            log("invalid", f"{proxy} invalid for httpx")

    except Exception as e:
        log("invalid", f"{proxy} raised error: {e}")

    # print("-" * 40) # uncomment this if not using threading else the output will be mixed

def handlefile(filename, output_name):
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, output_name)

    if not os.path.exists(input_path):
        log("info", f"{filename} not found, skipping.")
        return

    with open(input_path, "r") as f:
        proxies = [p.strip() for p in f if p.strip()]

    # Clear output file at the start
    open(output_path, "w").close()

    result_queue = Queue()
    stop_signal = object()

    def writer():
        with open(output_path, "a") as f:
            while True:
                item = result_queue.get()
                if item is stop_signal:
                    break
                f.write(item + "\n")
                result_queue.task_done()

    writer_thread = threading.Thread(target=writer)
    writer_thread.start()

    threads = []

    for proxy in proxies:
        while threading.active_count() > MAX_THREADS:
            time.sleep(0.01)

        t = threading.Thread(target=check, args=(proxy, result_queue))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    result_queue.put(stop_signal)
    writer_thread.join()

    log("info", f"Finished checking {filename}")

def checkall():
    handlefile("http.txt", "http_working.txt")
    handlefile("https.txt", "https_working.txt")
    handlefile("socks.txt", "socks_working.txt")

while True:
    print(f"\n{Fore.YELLOW}Select an option:")
    print("1. Scrape proxies")
    print("2. Check proxies")
    print("3. Exit")

    choice = input(">> ").strip()

    if choice == "1":
        getp(log)
    elif choice == "2":
        checkall()
    elif choice == "3":
        print("Exiting.")
        break
    else:
        print("Invalid input. Choose 1, 2, or 3.")