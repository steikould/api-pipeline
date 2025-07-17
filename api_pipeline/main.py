import argparse
import asyncio
from . import pipeline

def main():
    """The main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(description="API Pipeline")
    parser.add_argument(
        "--config",
        type=str,
        default="pipeline_config.yaml",
        help="The path to the pipeline configuration file.",
    )
    args = parser.parse_args()

    asyncio.run(pipeline.run_pipeline(args.config))

if __name__ == "__main__":
    main()
