from pathlib import Path

import mkdocs_gen_files


root = Path(__file__).parent.parent

for path in sorted(root.rglob('decorator_utils/**/*.py')):
    module_path = path.relative_to(root).with_suffix('')
    doc_path = path.relative_to(root).with_suffix('.md')
    full_doc_path = Path('reference', doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] in ['__init__', '__main__']:
        continue

    with mkdocs_gen_files.open(full_doc_path, 'w') as fd:
        identifier = '.'.join(parts)
        print('::: ' + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

for extra_file in ['README.md', 'LICENSE']:
    extra_file_path = root / extra_file
    with open(extra_file_path, 'r') as readme:
        content = readme.read()

        doc_path = extra_file_path.relative_to(root).with_suffix('.md')
        with mkdocs_gen_files.open(doc_path, 'w') as fd:
            print(content, file=fd)
