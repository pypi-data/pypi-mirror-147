import contextlib
import json
import pathlib
import shutil
import sys
import tempfile
import unittest.mock as mock
import uuid
from typing import Any
from typing import Dict
from typing import List

import pop.hub
import pytest
import yaml

TESTS_DIR = pathlib.Path()


@pytest.fixture(scope="session", autouse=True)
def tests_dir(request: pytest.Session):
    """
    When the test starts, verify that TESTS_DIR is available in non-fixture functions in this module
    """
    global TESTS_DIR
    TESTS_DIR = pathlib.Path(request.config.rootdir)


class IdemRunException(Exception):
    ...


def run_sls(
    sls: List[str],
    runtime: str = "parallel",
    test: bool = False,
    invert_state: bool = False,
    acct_file: str = None,
    acct_key: str = None,
    ret_data: str = "running",
    sls_offset: str = "sls",
    params: Dict[str, Any] = None,
    cache_dir: str = None,
    sls_sources: List[str] = None,
    hard_fail_on_collect: bool = False,
    acct_data: Dict[str, Any] = None,
    hub: pop.hub.Hub = None,
):
    """
    Run a list of sls references from idem/tests/sls/
    """
    if not hub:
        hub = pop.hub.Hub()
        hub.pop.sub.add(dyne_name="idem")
    hub.idem.RUN_NAME = name = "test"
    hub.idem.resolve.HARD_FAIL = hard_fail_on_collect
    render = "jinja|yaml|replacements"
    return _run_sls(
        hub,
        name,
        sls,
        runtime,
        test,
        acct_file,
        acct_key,
        ret_data,
        sls_offset,
        params,
        cache_dir,
        sls_sources,
        acct_data,
        render,
        invert_state=invert_state,
    )


def _run_sls(
    hub,
    name: str,
    sls: List[str],
    runtime: str,
    test: bool,
    acct_file: str,
    acct_key: str,
    ret_data: str,
    sls_offset: str,
    params: List[str],
    cache_dir: str,
    sls_sources: List[str],
    acct_data: Dict[str, Any],
    render: str,
    managed_state: Dict = None,
    invert_state: bool = False,
):
    """
    A private function to verify that the output of the various sls runners is consistent
    """
    if sls_sources:
        sls_sources_path = sls_sources
    else:
        if sls_offset:
            sls_dir = TESTS_DIR / sls_offset
        else:
            sls_dir = TESTS_DIR
        assert sls_dir.exists(), sls_dir
        sls_sources_path = [f"file://{sls_dir}"]
    param_sources = sls_sources = sls_sources_path
    hub.pop.loop.create()
    remove_cache = False
    if cache_dir is None:
        remove_cache = True
        cache_dir = tempfile.mkdtemp()
    else:
        # Cleanup is being handled by the caller
        hub.idem.managed.KEEP_CACHE_FILE = True
    context = hub.idem.managed.context(
        run_name=name, cache_dir=cache_dir, esm_plugin="local"
    )
    try:
        hub.pop.loop.CURRENT_LOOP.run_until_complete(
            _async_apply(
                hub,
                context,
                name=name,
                sls_sources=sls_sources,
                render=render,
                runtime=runtime,
                subs=["states", "nest"],
                cache_dir=cache_dir,
                sls=sls,
                test=test,
                invert_state=invert_state,
                acct_file=acct_file,
                acct_key=acct_key,
                param_sources=param_sources,
                params=params,
                acct_data=acct_data,
                managed_state=managed_state,
            )
        )
    finally:
        hub.pop.loop.CURRENT_LOOP.close()
        if remove_cache:
            shutil.rmtree(cache_dir, ignore_errors=True)
    errors = hub.idem.RUNS[name]["errors"]
    if errors:
        raise IdemRunException("\n".join(errors))
    if ret_data == "all":
        return hub.idem.RUNS[name]
    else:
        return hub.idem.RUNS[name]["running"]


async def _async_apply(hub, context, *args, **kwargs):
    """
    Call the sls runner with an async context manager
    """
    managed_state = kwargs.pop("managed_state")
    if managed_state is not None:
        return await hub.idem.state.apply(managed_state=managed_state, *args, **kwargs)
    else:
        async with context as managed_state:
            return await hub.idem.state.apply(
                *args, **kwargs, managed_state=managed_state
            )


def run_sls_validate(
    sls: List[str],
    runtime: str = "parallel",
    test: bool = False,
    sls_offset: str = "sls/validate",
):
    """
    Run SLS validation on SLS refs in idem/tests/*/validate
    """
    name = "test"
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="idem")
    hub.pop.sub.add("tests.nest")
    hub.pop.sub.load_subdirs(hub.nest)
    hub.pop.sub.load_subdirs(hub.nest.nest)
    hub.pop.sub.load_subdirs(hub.nest.nest.again)
    render = "jinja|yaml|replacements"
    cache_dir = tempfile.mkdtemp()
    sls_dir = TESTS_DIR / sls_offset
    sls_sources = [f"file://{sls_dir}"]
    hub.pop.loop.create()
    hub.pop.Loop.run_until_complete(
        hub.idem.state.validate(
            name,
            sls_sources,
            render,
            runtime,
            ["states", "nest"],
            cache_dir,
            sls,
            test,
        )
    )
    errors = hub.idem.RUNS[name]["errors"]
    if errors:
        return errors
    return hub.idem.RUNS[name]


def run_yaml_block(yaml_block: str, **kwargs):
    """
    Run states defined in a yaml string
    """
    sls_run = str(uuid.uuid4())

    data = {f"{sls_run}.sls": yaml.safe_load(yaml_block)}

    return run_sls_source(
        sls=[sls_run], sls_sources=[f"json://{json.dumps(data)}"], **kwargs
    )


def run_sls_source(
    sls: List[str],
    sls_sources: List[str],
    acct_data: Dict[str, Any] = None,
    test: bool = False,
    name: str = "run_yaml_block",
    managed_state=None,
):
    """
    Run states defined in sls sources
    """
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="idem")
    hub.pop.loop.create()
    if managed_state is None:
        managed_state = {}

    _run_sls(
        hub,
        name,
        sls,
        runtime="parallel",
        test=test,
        acct_file=None,
        acct_key=None,
        ret_data=None,
        sls_offset=None,
        params=None,
        cache_dir=tempfile.gettempdir(),
        sls_sources=sls_sources,
        acct_data=acct_data,
        render="json",
        managed_state=managed_state,
    )

    assert not hub.idem.RUNS[name]["errors"], "\n".join(hub.idem.RUNS[name]["errors"])
    return hub.idem.RUNS[name]["running"]


@contextlib.contextmanager
def tpath_hub():
    """
    Add "idem_plugin" to the test path
    """
    TPATH_DIR = str(TESTS_DIR / "tpath")

    with mock.patch("sys.path", [TPATH_DIR] + sys.path):
        hub = pop.hub.Hub()
        hub.pop.sub.add(dyne_name="idem")

        hub.pop.loop.create()

        yield hub

        hub.pop.loop.CURRENT_LOOP.close()
