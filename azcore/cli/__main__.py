#!/usr/bin/env python
"""
Az-Core CLI Entry Point

This is the main entry point for the azcore command-line interface.
It's designed to load minimal imports upfront to avoid dependency issues.
"""

import sys

def main():
    """Main CLI entry point."""
    # Import click first (lightweight)
    import click
    
    @click.group()
    @click.version_option(version="0.0.7", prog_name="azcore")
    def cli():
        """Az-Core: Advanced AI Agent Framework with RL Integration.
        
        A powerful framework for building, orchestrating, and optimizing AI agents.
        """
        pass
    
    # Import commands lazily to avoid importing the full azcore module
    from azcore.cli.commands import init, run, train, validate, stats, create
    
    # Register command groups
    cli.add_command(init.init)
    cli.add_command(run.run)
    cli.add_command(train.train)
    cli.add_command(validate.validate)
    cli.add_command(stats.stats)
    cli.add_command(create.create)
    
    # Run CLI
    cli()


if __name__ == "__main__":
    main()
