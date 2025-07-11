import sys
import subprocess
import uvicorn
from quality_gates.settings import settings
from quality_gates.utils.logger import logger


def run_migrations():
    try:
        logger.info("Starting database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Migrations completed successfully")
            logger.info(result.stdout)
        else:
            logger.error(f"Migrations failed: {result.stderr}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "migrate":
            run_migrations()
            return
        elif command == "run":
            # Запуск сервера
            logger.info(f"Server is running on {settings.host}:{settings.port}")
            uvicorn.run("quality_gates.app:app", host=settings.host, port=settings.port, reload=settings.debug)
            return
        else:
            print("Available commands:")
            print("  migrate - Run database migrations")
            print("  run     - Start the server (default)")
            sys.exit(1)
    
    logger.info(f"Server is running on {settings.host}:{settings.port}")
    uvicorn.run("quality_gates.app:app", host=settings.host, port=settings.port, reload=settings.debug)


if __name__ == "__main__":
    main()
