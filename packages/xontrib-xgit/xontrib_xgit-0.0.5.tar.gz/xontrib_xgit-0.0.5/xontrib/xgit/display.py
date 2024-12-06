"""
Modify the displayhook to handle value-returning commands and update history variables.
This gives a notebook-style history of the last three values displayed, and
allows display of python values returned from commands.
"""

from threading import Lock
from typing import Any, MutableMapping
import sys
import builtins

from xonsh.procs.pipelines import HiddenCommandPipeline
from xonsh.events import events
from xonsh.built_ins import XonshSession

from xontrib.xgit.context_types import GitContext
from xontrib.xgit.decorators import session

# Our events:


events.doc(
    "on_xgit_predisplay",
    "Runs before displaying the result of a command with the value to be displayed.",
)
events.doc(
    "on_xgit_postdisplay",
    "Runs after displaying the result of a command with the value displayed.",
)

events.on_xgit_predisplay.clear()
events.on_xgit_postdisplay.clear()


_xonsh_displayhook = sys.displayhook

while hasattr(_xonsh_displayhook, "original"):
    _xonsh_displayhook = _xonsh_displayhook.original    # type: ignore

"""
Xonsh's original displayhook.
"""

@session()
def _xgit_displayhook(value: Any, /, *, XSH: XonshSession, **_):
    """
    Add handling for value-returning commands, pre- and post-display events,
    and exception protection.
    """
    ovalue = value
    env = XSH.env
    assert isinstance(env, MutableMapping), \
        f"XSH.env not a MutableMapping: {env!r}"
    if isinstance(value, HiddenCommandPipeline):
        value = XSH.ctx.get("_XGIT_RETURN", value)
        if "_XGIT_RETURN" in XSH.ctx:
            if env.get("XGIT_TRACE_DISPLAY"):
                print("clearing _XGIT_RETURN in XSH.ctx", file=sys.stderr)
            del XSH.ctx["_XGIT_RETURN"]
        else:
            if env.get("XGIT_TRACE_DISPLAY"):
                msg = (
                    "No _XGIT_RETURN, "
                    + "result has been displayed with str() and suppressed"
                )
                print(msg, file=sys.stderr)

    if env.get("XGIT_TRACE_DISPLAY") and ovalue is not value:
        sys.stdout.flush()
        print(
            f"DISPLAY: {ovalue=!r} {value=!r} type={type(ovalue).__name__}", sys.stderr
        )
        sys.stderr.flush()
    try:
        events.on_xgit_predisplay.fire(value=value)
        sys.stdout.flush()
        _xonsh_displayhook(value)
        events.on_xgit_postdisplay.fire(value=value)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.stderr.flush()

setattr(_xgit_displayhook, "original", _xonsh_displayhook)

@events.on_xgit_predisplay
@session()
def _xgit_on_predisplay(value: Any, XSH: XonshSession, **_):
    """
    Update the notebook-style convenience history variables before displaying a value.
    """
    global count
    env = XSH.env
    assert isinstance(env, MutableMapping),\
        f"XSH.env not a MutableMapping: {env!r}"
    if (
        value is not None
        and not isinstance(value, HiddenCommandPipeline)
        and env.get("XGIT_ENABLE_NOTEBOOK_HISTORY")
    ):
        count = _xgit_count()
        ivar = f"_i{count}"
        ovar = f"_{count}"
        XSH.ctx[ivar] = XSH.ctx.get("-")
        XSH.ctx[ovar] = value
        print(f"{ovar}: ", end="")


@events.on_xgit_postdisplay
@session()
def _xgit_on_postdisplay(value: Any, XSH: XonshSession, **_):
    """
    Update _, __, and ___ after displaying a value.
    """
    if value is not None and not isinstance(value, HiddenCommandPipeline):
        setattr(builtins, ",", value)
        XSH.ctx["__"] = XSH.ctx.get("+")
        XSH.ctx["___"] = XSH.ctx.get("++")


_count_lock = Lock()
# Set up the notebook-style convenience history variables.
@session()
def _xgit_count(*, XGIT: GitContext, **_):
    """
    Set up and use the counter for notebook-style history.
    """
    with _count_lock:
        counter = XGIT.__dict__.get("_xgit_counter", None)
        if not counter:
            counter = iter(range(1, sys.maxsize))
            XGIT.__dict__["_xgit_counter"] = counter
        return next(counter)


@events.on_precommand
@session()
def _on_precommand(cmd: str,  XSH: XonshSession, **_):
    """
    Before running a command, save our temporary variables.
    We associate them with the session rather than the module.
    These names are deliberately impossible to use, and are named
    after similar variables long used in REPLs.

    _, __, and ___ are the last three values displayed, and are
    directly useful. The variables here are simply to facilitate
    updating those values.
    """
    env = XSH.env
    assert isinstance(env, MutableMapping),\
        f"XSH.env not a MutableMapping: {env!r}"
    if "_XGIT_RETURN" in XSH.ctx:
        if env.get("XGIT_TRACE_DISPLAY"):
            print("Clearing _XGIT_RETURN before command", file=sys.stderr)
        del XSH.ctx["_XGIT_RETURN"]
    XSH.ctx["-"] = cmd.strip()
    XSH.ctx["+"] = builtins._  # type: ignore # noqa
    XSH.ctx["++"] = XSH.ctx.get("__")
    XSH.ctx["+++"] = XSH.ctx.get("___")

