import pluggy

# Hook implementation for adding functionality to the cli by plugins
clihook = pluggy.HookimplMarker("cli")
