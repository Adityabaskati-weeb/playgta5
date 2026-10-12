"""Build a portable Windows Python runtime from the active interpreter."""
import hashlib, json, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    if sys.version_info < (3, 11):
        raise SystemExit('Python 3.11 or newer is required to build the runtime.')

    source = Path(sys.executable).resolve().parent
    target = ROOT / 'runtime'
    tag = 'python%d%d' % sys.version_info[:2]
    required = ['python.exe', 'python3.dll', tag + '.dll', 'vcruntime140.dll',
                'vcruntime140_1.dll', 'LICENSE.txt']
    missing = [name for name in required if not (source / name).is_file()]
    if missing or not (source / 'DLLs').is_dir() or not (source / 'Lib').is_dir():
        detail = ', '.join(missing) if missing else 'DLLs/ or Lib/ directory'
        raise SystemExit('The active interpreter is not a complete Windows Python distribution; missing ' + detail)

    target.mkdir(exist_ok=True)
    for name in required:
        shutil.copyfile(source / name, target / name)
    shutil.copytree(source / 'DLLs', target / 'DLLs', dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pdb'))
    with zipfile.ZipFile(target / (tag + '.zip'), 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted((source / 'Lib').rglob('*')):
            rel = path.relative_to(source / 'Lib')
            if path.is_file() and not any(part in {'site-packages', '__pycache__', 'test', 'tests'} for part in rel.parts) and path.suffix != '.pyc':
                archive.write(path, str(rel))
    # An isolated path avoids depending on the user's Python install or site packages.
    (target / (tag + '._pth')).write_text(tag + '.zip\nDLLs\n.\n..\n', encoding='ascii')
    records = []
    for path in sorted(target.rglob('*')):
        if path.is_file():
            records.append({'path': str(path.relative_to(ROOT)).replace('\\', '/'), 'bytes': path.stat().st_size,
                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {'python_version': sys.version, 'source': 'local CPython installation (path omitted)',
                'scope': 'Python executable, DLLs and standard library; third-party packages excluded',
                'files': records}
    (ROOT / 'snapshot/runtime-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Portable runtime:', len(records), 'files;', sum(r['bytes'] for r in records), 'bytes')

if __name__ == '__main__':
    main()
