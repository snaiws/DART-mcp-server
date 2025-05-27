import asyncio

from .run_server import run_stdio

def main():
    asyncio.run(run_stdio())

if __name__ == "__main__":
    main()