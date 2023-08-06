# What is this?

If you have something you are working on that may accidentally consume
all your RAM (read: are a data scientist), you probably want your process
OOM reaped before the other ones. What you absolutely do not want is 
something like process that may fail in a bad state getting reaped instead.

If you install this package with,

```bash
pip install oom_reap_me_first
```

then do,

```python
import oom_reap_me_first.auto_enable # noqa # pylint: disable=unused-import
```

at the top of your, say, Jupyter notebook, the importing processes 
`oom_score_adj` will be set to `1000`, which means it will (probably?) 
get reaped first. 

This works particularly well if you [disable swap](https://graspingtech.com/disable-swap-ubuntu/), so you don't end up
in the dreaded situation of your REPL taking all the RAM then hitting
disk so hard that you can't even `i-i` it.

# What else should I know?


The `oom_score_adj` that controls what gets preferentially gets killed
can be configured automatically for `systemd` services. If you have something
that you *really* don't want to get killed, you should put,

```
oom score -1000
```

in the service unit definition. Alternatively, if you are not using python
you can use the `choom` (change-OOM) command

```bash
choom -p PID -n number
```

See the [man page](https://man7.org/linux/man-pages/man1/choom.1.html) here.

However, I am lazy and my solution suits me better.
