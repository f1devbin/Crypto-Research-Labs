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


def test_scheduled_runs_write_the_digest_and_pushes_never_forecast():
    wf = yaml.load((WORKFLOWS / "research-agents.yml").read_text(), Loader=StrictLoader)
    steps = {s.get("name"): s for s in wf["jobs"]["agents"]["steps"]}
    # GitHub compares a missing input (null) as false, so "inputs.digest != false" skipped every scheduled digest
    assert "!= false" not in steps["Digest"]["if"]
    assert "github.event_name != 'workflow_dispatch'" in steps["Digest"]["if"]
    assert steps["Daily model forecast (H-029/H-030)"]["if"] == "github.event_name != 'push'"
