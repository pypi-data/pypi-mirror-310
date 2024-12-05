from pathlib import Path


def safe_open(file: Path, mode='r'):

    if 'w' in mode and not file.parent.exists():
        file.parent.mkdir(parents=True)

    if file.name.endswith('.gz'):
        import gzip
        return gzip.open(str(file), mode=mode)

    return file.open(mode=mode)
