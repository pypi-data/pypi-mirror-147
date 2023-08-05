#!/usr/bin/env python3
"""Main CLI entrypoint."""

import datetime as dt
import builtins

from konta import woob_import, woob_to_bean
from konta.config import Config
from beancount.parser import printer
from beancount.core.data import SORT_ORDER


def main():
    """Handle main CLI entrypoint."""
    conf = Config.from_toml()
    # TODO: Actually have a meaningful usecase for ingesting existing files
    # print(bean_import.import_data(conf.get_exising_input_paths()[0]))
    # TODO: parse the starting date from argparse instead of changing it here
    woob_txs = woob_import.import_data(dt.datetime(2022, 1, 9))
    # TODO: this processing loop should be in the library part, not the binary used just for the PoC
    beans = []
    for acc_id in woob_txs.keys():
        for tx in woob_txs[acc_id]["history"]:
            bean = woob_to_bean.woob_to_bean(
                conf,
                acc_id,
                tx,
            )
            if bean is not None:
                beans.append(bean)
        for tx in woob_txs[acc_id]["coming"]:
            bean = woob_to_bean.woob_to_bean(
                conf,
                acc_id,
                tx,
            )
            if bean is not None:
                beans.append(bean)
    beans = builtins.sorted(
        beans, key=lambda entry: (entry.date, SORT_ORDER.get(type(entry), 0))
    )
    for bean in beans:
        printer.print_entry(bean)


if __name__ == "__main__":
    main()
