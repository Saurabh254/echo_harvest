# import logging
import coloredlogs, logging  # noqa: E401, F401

coloredlogs.install(
    fmt="[%(asctime)s] - %(filename)s - %(levelname)s - %(message)s",
    datefmt="%X %d/%m/%y",
    level=0,
)
