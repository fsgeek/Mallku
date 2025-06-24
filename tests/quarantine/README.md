# Quarantine Zone

This directory contains tests that fail due to import errors in CI but work locally.
They are temporarily moved here to allow other tests to run and establish a working
CI baseline.

## Goal
Get these tests back into the main test suite once we resolve the import issues.

## Current Residents
- Tests with complex mallku.* imports that fail in CI despite src being in PYTHONPATH

## Guardian's Note
Perfect CI is the enemy of working CI. We build incrementally.
