"""GitHub refuses a workflow with a duplicated key (the whole workflow stops running), while
yaml.safe_load silently keeps the last value. Catch that before it reaches GitHub."""
from pathlib import Path

import yaml

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"


class StrictLoader(yaml.SafeLoader):
    pass


def _no_duplicates(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    dup = {k for k in keys if keys.count(k) > 1}
    if dup:
        raise AssertionError(f"duplicate keys {sorted(map(str, dup))} at line {node.start_mark.line + 1}")
    return loader.construct_mapping(node, deep)


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicates)


def test_workflows_have_no_duplicate_keys():
    files = sorted(WORKFLOWS.glob("*.yml"))
    assert files
    for f in files:
        yaml.load(f.read_text(), Loader=StrictLoader)
