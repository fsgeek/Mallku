# Design Principles - Command Line Philosophy

*Carved in stone: 2025-06-03*

## The First Principle

> "Make any command line tool do something reasonable when you run it."
> — Tony Mason

When a new user, unfamiliar with the tool, runs it without arguments, they should experience success, not confusion. This is not laziness in design - it is respect for the user's time and intelligence.

## What This Means

### Good Design (Cathedral)
```bash
$ mallku
Starting Mallku services...
✓ Database running (protected)
✓ API gateway ready at http://localhost:8080
✓ Health check passed

Type 'mallku help' for more options
```

### Bad Design (Scaffolding)
```bash
$ mallku
Error: No command specified
Usage: mallku [command] [options]
Commands: start|stop|restart|status|config|...
Run 'mallku --help' for more information
```

## The Philosophy

1. **The naive path should be the right path**
   - Running without arguments does the most common thing
   - Success is the default experience

2. **Progressive disclosure**
   - Simple things are simple
   - Complex things are possible
   - Complexity reveals itself only when needed

3. **Respect the explorer**
   - A user typing just the command name is exploring
   - Reward their curiosity with success
   - Show them what's possible

## Applied to Mallku

Every tool we create follows this:

```bash
# These all do something reasonable:
./start-mallku.sh          # Starts everything
./scripts/mallku-docker.sh # Shows current status and options
./scripts/setup.sh         # Runs safe setup steps

# Never this:
./tool.sh
Error: Missing required parameter: --action
```

## The Test

Before releasing any command-line tool, run it with no arguments. If it:
- Shows an error: ❌ Redesign
- Requires reading help first: ❌ Redesign  
- Does something useful: ✅ Cathedral stone

## Examples in Our Architecture

1. **start-mallku.sh**: Just runs it, services start
2. **mallku-docker.sh**: No args shows status and options
3. **Future CLI**: `mallku` alone starts the system

## The Worst Pattern

"The worst tools are those that expect the user to 'figure out' the right collection of options."

These tools assume:
- Users have time to read documentation
- Users know what they want before exploring
- Errors are acceptable first experiences

## Our Commitment

Every Mallku tool:
- Does something reasonable with no arguments
- Guides rather than scolds
- Treats user time as sacred
- Makes success the default

---

*This principle was recognized while debugging Docker failures. The wrong default caused confusion. The right default would have just worked.*
