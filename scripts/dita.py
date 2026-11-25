"""Run an isolated DITA-OT with a Java argument file (avoids Windows cmd length limits)."""
import os
import pathlib
import subprocess
import sys
import tempfile

def run(toolkit, *args):
    toolkit = pathlib.Path(toolkit).resolve()
    # Oxygen's launcher puts its patches first and keeps Saxon below lib/saxon.
    jars = sorted((toolkit / 'plugins/com.oxygenxml.dost.patches/lib').glob('*.jar'))
    jars += sorted((toolkit / 'lib').glob('*.jar'))
    jars += sorted((toolkit / 'lib/saxon').glob('*.jar'))
    # Match the installed plug-in libraries declared to the toolkit classloader.
    if not args or args[0] not in ('install', 'uninstall'):
        jars += [p for p in sorted((toolkit / 'plugins').glob('*/lib/*.jar')) if p not in jars]
    classpath = os.pathsep.join([str(toolkit / 'config'), *(str(p) for p in jars)])
    with tempfile.NamedTemporaryFile(mode='w', suffix='.args', encoding='utf-8', delete=False) as f:
        f.write('-cp\n"' + classpath.replace('\\', '/') + '"\n')
        f.write('-Ddita.dir="' + toolkit.as_posix() + '"\n')
        f.write('org.dita.dost.invoker.Main\n')
        name = f.name
    try:
        return subprocess.run(['java', '@' + name, '-buildfile', str(toolkit / 'build.xml'), *map(str, args)]).returncode
    finally:
        pathlib.Path(name).unlink()

if __name__ == '__main__':
    sys.exit(run(sys.argv[1], *sys.argv[2:]))
