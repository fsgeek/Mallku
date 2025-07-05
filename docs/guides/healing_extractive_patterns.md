# Healing Extractive Patterns

*44th Artisan - Finding and smoothing the worn stones*

## What Are Extractive Patterns?

Extractive patterns in code take from users without giving back:
- Cryptic error messages that frustrate rather than teach
- Assumptions that waste time when wrong
- Missing context that forces exploration
- Technical jargon where plain language would serve

Each extraction is small, but they accumulate into barriers.

## Patterns Found and Healed

### 1. Unhelpful Error Messages

**Before:**
```python
raise ValueError(f"Unsupported provider: {provider_name}")
```

**After:**
```python
raise ConfigurationError(
    f"The '{provider_name}' voice isn't configured yet. "
    f"Available voices: {', '.join(available)}"
)
```

The error now:
- Names what's wrong in plain language
- Lists available alternatives
- Guides toward resolution

### 2. Missing Usage Context

**Before:**
```
Usage: python fire_circle_review.py review <PR_NUMBER>
```

**After:**
```
🔥 Fire Circle Code Review
This tool convenes the Fire Circle to review pull requests.
Seven AI voices provide collective wisdom on code changes.

Usage: python fire_circle_review.py review <PR_NUMBER>
Example: python fire_circle_review.py review 42

💡 Make sure you have:
   • At least 2 API keys configured
   • GITHUB_TOKEN environment variable set
   • Internet connection to reach GitHub
```

Now provides:
- What the tool does
- Concrete example
- Prerequisites clearly stated
- Common requirements listed

### 3. Generic Failure Messages

**Before:**
```python
except Exception as e:
    logger.error(f"Review failed: {e}")
    sys.exit(1)
```

**After:**
```python
except Exception as e:
    logger.error(f"Review failed: {e}")
    print("\n❌ Fire Circle review encountered an issue.")
    print(f"   {str(e)}")
    print("\n💡 Common issues:")
    print("   • Missing GITHUB_TOKEN environment variable")
    print("   • Insufficient API keys (need at least 2)")
    print("   • Network connection problems")
    print("   • PR number doesn't exist or is private")
    print("\n📝 For detailed logs, run with:")
    print("   LOGLEVEL=DEBUG python fire_circle_review.py review " + str(pr_number))
    sys.exit(1)
```

This transforms frustration into learning by:
- Acknowledging the issue
- Listing likely causes
- Providing next steps
- Teaching about debug options

## The Welcoming Error Framework

The 43rd Artisan created `welcoming_errors.py` with these principles:

1. **Errors as Teachers**: Each error is a chance to deepen understanding
2. **Context Over Correctness**: Why something failed matters more than technical details
3. **Next Steps Always**: Never leave someone stuck without options
4. **Belonging Reinforced**: "You belong here, even when things don't work"

## Finding Extractive Patterns

Look for:
- `raise Exception/Error` without helpful context
- `print("Error: ...")` without guidance
- Assumptions about environment/setup
- Technical jargon in user-facing messages
- Missing examples in usage text
- Silent failures that give no feedback

## Small Changes, Large Impact

Each healed pattern:
- Saves someone 5-10 minutes of confusion
- Prevents cascade of frustration
- Teaches rather than blocks
- Makes Mallku more welcoming

Over thousands of interactions, these small reciprocities compound into a fundamentally different experience.

## Continuing the Work

This is ongoing work. Each Artisan who:
- Adds a helpful error message
- Clarifies confusing output
- Provides examples where needed
- Explains assumptions made

...is healing extractive patterns and building reciprocal infrastructure.

---

*"In healing small extractions, we practice the largest reciprocity - making others feel welcome as we wished to feel."*
