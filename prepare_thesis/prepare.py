from pathlib import Path

DATA_DIR = Path('../data/thesis/experiments')

if __name__ == '__main__':
    DATA_DIR.mkdir(parents=True, exist_ok=True)
