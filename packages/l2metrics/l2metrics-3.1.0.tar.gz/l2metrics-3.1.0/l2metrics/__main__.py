"""
Copyright © 2021-2022 The Johns Hopkins University Applied Physics Laboratory LLC

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the “Software”), to 
deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import json
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from l2metrics import util
from l2metrics.parser import init_parser
from l2metrics.report import MetricsReport

logging.captureWarnings(True)
logger = logging.getLogger("l2metrics.__main__")


def run() -> None:
    # Initialize parser
    parser = init_parser()

    # Parse arguments
    args = parser.parse_args()
    kwargs = vars(args)

    if args.load_settings:
        with open(args.load_settings, "r") as settings_file:
            kwargs.update(json.load(settings_file))

    kwargs["output_dir"] = Path(args.output_dir)

    # Create output directory if it doesn't exist
    if (args.do_save or args.do_save_settings) and args.ste_store_mode is None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.do_plot and args.ste_store_mode is None:
        (args.output_dir / "plots").mkdir(parents=True, exist_ok=True)

    # Load data range data for normalization and standardize names to lowercase
    if args.data_range_file:
        with open(args.data_range_file) as data_range_file:
            data_range = json.load(data_range_file)
            data_range = {key.lower(): val for key, val in data_range.items()}
    else:
        data_range = None
    kwargs["data_range"] = data_range

    # Check for recursive flag
    if args.recursive:
        ll_metrics_df = pd.DataFrame()
        ll_metrics_dicts = []
        regime_metrics_df = pd.DataFrame()
        log_data_df = pd.DataFrame()
        task_colors = {}
        cc = util.color_cycler()

        # Subset of log data columns to store
        cols_to_store = [
            "run_id",
            "timestamp",
            "block_num",
            "block_type",
            "exp_num",
            "episode_step_count",
            "task_name",
            args.perf_measure,
        ]

        # Assign base filename
        filename = args.output_dir / (args.output if args.output else "ll_metrics")

        # Save settings used to run calculate metrics
        if args.do_save_settings and args.ste_store_mode is None:
            with open(str(filename) + "_settings.json", "w") as settings_file:
                kwargs["log_dir"] = str(kwargs.get("log_dir", ""))
                kwargs["output_dir"] = str(kwargs.get("output_dir", ""))
                logger.info(
                    f'Saving settings with name: {str(filename) + "_settings.json"}'
                )
                json.dump(kwargs, settings_file)

        # Iterate over all runs found in the directory
        dirs = [
            p
            for p in Path(args.log_dir).rglob("*")
            if p.is_dir() and (p / "logger_info.json").exists()
        ]
        dirs.sort()
        for dir in tqdm(dirs, desc=Path(args.log_dir).name):
            # Check if current path is log directory for single run
            if all(
                x in [f.name for f in dir.glob("*.json")]
                for x in ["logger_info.json", "scenario_info.json"]
            ):
                if args.ste_store_mode:
                    # Store STE data
                    try:
                        util.store_ste_data(log_dir=dir, mode=args.ste_store_mode)
                    except ValueError as e:
                        logger.error(e)
                else:
                    # Compute and store the LL metrics
                    kwargs["log_dir"] = dir
                    logger.info(f"Starting metrics report for {dir.name}")
                    report = MetricsReport(**kwargs)

                    # Add noise to log data if mean or standard deviation is specified
                    if args.noise[0] or args.noise[1]:
                        report.add_noise(mean=args.noise[0], std=args.noise[1])

                    report.calculate()
                    ll_metrics_df = pd.concat(
                        [ll_metrics_df, report.ll_metrics_df], ignore_index=True
                    )
                    ll_metrics_dicts.append(report.ll_metrics_dict)
                    regime_metrics_df = pd.concat(
                        [regime_metrics_df, report.regime_metrics_df], ignore_index=True
                    )
                    log_data_df_temp = report._log_data
                    log_data_df_temp["run_id"] = dir.name
                    log_data_df_temp = log_data_df_temp.astype(
                        {"worker_id": str}, errors="raise"
                    )
                    log_data_df_temp = log_data_df_temp.astype(
                        {
                            col: "int32"
                            for col in log_data_df_temp.select_dtypes("int64").columns
                        },
                        errors="raise",
                    )
                    log_data_df = pd.concat(
                        [
                            log_data_df,
                            log_data_df_temp[
                                log_data_df_temp.columns.intersection(cols_to_store)
                            ],
                        ],
                        ignore_index=True,
                    )

                    # Plot metrics
                    if args.do_plot:
                        # Update task color dictionary
                        new_tasks = list(
                            set(report._unique_tasks) - set(task_colors.keys())
                        )
                        new_tasks.sort()
                        for task_name, color in zip(new_tasks, cc):
                            task_colors[task_name] = color["color"]

                        # Generate plots
                        report.plot(
                            plot_types=args.plot_types,
                            save=args.do_save,
                            show_eval_lines=args.show_eval_lines,
                            output_dir=str(Path(args.output_dir) / "plots"),
                            task_colors=task_colors,
                        )
                        plt.close("all")

                    # Save data
                    if args.do_save and args.ste_store_mode is None:
                        if not ll_metrics_df.empty:
                            with open(
                                str(filename) + ".tsv", "w", newline="\n"
                            ) as metrics_file:
                                logger.info(
                                    f'Saving metrics TSV with name: {str(filename) + ".tsv"}'
                                )
                                ll_metrics_df.set_index(["run_id"]).to_csv(
                                    metrics_file, sep="\t"
                                )
                        if ll_metrics_dicts:
                            with open(
                                str(filename) + ".json", "w", newline="\n"
                            ) as metrics_file:
                                logger.info(
                                    f'Saving metrics JSON with name: {str(filename) + ".json"}'
                                )
                                json.dump(ll_metrics_dicts, metrics_file)
                        if not regime_metrics_df.empty:
                            with open(
                                str(filename) + "_regime.tsv", "w", newline="\n"
                            ) as metrics_file:
                                logger.info(
                                    f'Saving regime metrics TSV with name: {str(filename) + "_regime.tsv"}'
                                )
                                regime_metrics_df.set_index(["run_id"]).to_csv(
                                    metrics_file, sep="\t"
                                )
                        if not log_data_df.empty:
                            logger.info(
                                f'Saving log data with name: {str(filename) + "_data.feather"}'
                            )
                            log_data_df.reset_index(drop=True).to_feather(
                                str(filename) + "_data.feather"
                            )
    else:
        if args.ste_store_mode:
            # Store STE data
            util.store_ste_data(log_dir=Path(args.log_dir), mode=args.ste_store_mode)
        else:
            # Initialize metrics report
            logger.info(f"Starting metrics report for {Path(args.log_dir).name}")
            report = MetricsReport(**kwargs)

            # Save settings used to calculate metrics
            if args.do_save_settings:
                report.save_settings(output_dir=args.output_dir, filename=args.output)

            # Add noise to log data if mean or standard deviation is specified
            if args.noise[0] or args.noise[1]:
                report.add_noise(mean=args.noise[0], std=args.noise[1])

            # Calculate metrics in order of their addition to the metrics list.
            report.calculate()

            # Print table of metrics
            report.report()

            # Save metrics to file
            if args.do_save:
                report.save_metrics(output_dir=args.output_dir, filename=args.output)
                report.save_data(output_dir=args.output_dir, filename=args.output)

            # Plot metrics
            if args.do_plot:
                report.plot(
                    plot_types=args.plot_types,
                    save=args.do_save,
                    show_eval_lines=args.show_eval_lines,
                    output_dir=str(Path(args.output_dir) / "plots"),
                )
                if not args.do_save:
                    plt.show()

                plt.close("all")


if __name__ == "__main__":
    # Configure logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    handler.setStream(tqdm)
    handler.terminator = ""

    logging.basicConfig(level=logging.INFO, handlers=[handler])

    try:
        run()
    except (KeyError, ValueError) as e:
        logger.exception(e)
