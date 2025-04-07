from . import server
import asyncio
import dynamics_365_client
import tools
def main():
   """Main entry point for the package."""
   asyncio.run(server.main())

# Expose important items at package level
__all__ = ['main', 'server', 'dynamics_365_client']