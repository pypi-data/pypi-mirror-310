def main():
    # Import the main functions from your commands
    from LocalFinder.commands.bin_tracks import main as bin_tracks_main
    from LocalFinder.commands.calculate_correlation_FC import main as calc_corr_main
    from LocalFinder.commands.find_significantly_different_regions import main as find_regions_main
    from LocalFinder.commands.visualize_tracks import main as visualize_main

    import argparse
    import sys

    parser = argparse.ArgumentParser(description='LocalFinder Command-Line Interface')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for bin_tracks
    parser_bin = subparsers.add_parser('bin_tracks', help='Convert input files into bins with BedGraph format')
    # (Add arguments specific to bin_tracks here)

    # Subparser for calculate_correlation_FC
    parser_calc_corr = subparsers.add_parser('calculate_correlation_FC', help='Calculate correlation and fold change between tracks')
    # (Add arguments specific to calculate_correlation_FC here)

    # Subparser for find_significantly_different_regions
    parser_find_regions = subparsers.add_parser('find_significantly_different_regions', help='Find significantly different regions between tracks')
    # (Add arguments specific to find_significantly_different_regions here)

    # Subparser for visualize_tracks
    parser_visualize = subparsers.add_parser('visualize_tracks', help='Visualize genomic tracks')
    # (Add arguments specific to visualize_tracks here)

    # Subparser for pipeline
    parser_pipeline = subparsers.add_parser('pipeline', help='Run the full pipeline')
    # Add arguments for the pipeline
    parser_pipeline.add_argument('--input_files', nargs='+', required=True, help='Input files for binning')
    parser_pipeline.add_argument('--output_dir', type=str, required=True, help='Output directory for all results')
    parser_pipeline.add_argument('--chrom_sizes', type=str, required=True, help='Path to the chromosome sizes file')
    parser_pipeline.add_argument('--bin_size', type=int, default=200, help='Bin size for binning (default: 200bp)')
    parser_pipeline.add_argument('--method', type=str, default='localPearson_and_FC', help='Method for calculate_correlation_FC (default: localPearson_and_FC)')
    parser_pipeline.add_argument('--method_params', type=str, default='{}', help='Method-specific parameters in JSON format')
    parser_pipeline.add_argument('--bin_number_of_window', type=int, default=11, help='Bin number of window (default: 11)')
    parser_pipeline.add_argument('--step', type=int, default=1, help='Step size for sliding window (default: 1)')
    parser_pipeline.add_argument('--fc_high_percentile', type=float, default=75, help='Percentile threshold for high FC (default: 75)')
    parser_pipeline.add_argument('--fc_low_percentile', type=float, default=25, help='Percentile threshold for low FC (default: 25)')
    parser_pipeline.add_argument('--corr_high_percentile', type=float, default=75, help='Percentile threshold for high correlation (default: 75)')
    parser_pipeline.add_argument('--corr_low_percentile', type=float, default=25, help='Percentile threshold for low correlation (default: 25)')
    parser_pipeline.add_argument('--chroms', nargs='+', help='List of chromosomes to process (default: all)')
    # Add other arguments as needed

    args = parser.parse_args()

    if args.command == 'bin_tracks':
        bin_tracks_main()
    elif args.command == 'calculate_correlation_FC':
        calc_corr_main()
    elif args.command == 'find_significantly_different_regions':
        find_regions_main()
    elif args.command == 'visualize_tracks':
        visualize_main()
    elif args.command == 'pipeline':
        run_pipeline(args)
    else:
        parser.print_help()

def run_pipeline(args):
    import os
    import sys
    import json
    import argparse
    from LocalFinder.commands.bin_tracks import main as bin_tracks_main
    from LocalFinder.commands.calculate_correlation_FC import main as calc_corr_main
    from LocalFinder.commands.find_significantly_different_regions import main as find_regions_main

    # Create output directories
    os.makedirs(args.output_dir, exist_ok=True)
    bin_output_dir = os.path.join(args.output_dir, 'binned_tracks')
    calc_output_dir = os.path.join(args.output_dir, 'calculated_tracks')
    regions_output_dir = os.path.join(args.output_dir, 'significant_regions')

    os.makedirs(bin_output_dir, exist_ok=True)
    os.makedirs(calc_output_dir, exist_ok=True)
    os.makedirs(regions_output_dir, exist_ok=True)

    # Step 1: Run bin_tracks
    print("Running bin_tracks...")
    bin_output_files = [os.path.join(bin_output_dir, os.path.basename(f) + '.bedgraph') for f in args.input_files]
    bin_args = argparse.Namespace(
        input_files=args.input_files,
        output_files=bin_output_files,
        bin_size=args.bin_size,
        chrom_sizes=args.chrom_sizes,
        chroms=args.chroms
    )
    bin_tracks_main(bin_args)

    # Step 2: Run calculate_correlation_FC
    print("Running calculate_correlation_FC...")
    # Assuming two input files for simplicity
    if len(bin_output_files) < 2:
        print("Need at least two input files for calculate_correlation_FC.")
        sys.exit(1)
    calc_args = argparse.Namespace(
        track1=bin_output_files[0],
        track2=bin_output_files[1],
        method=args.method,
        method_params=args.method_params,
        bin_number_of_window=args.bin_number_of_window,
        step=args.step,
        output_dir=calc_output_dir,
        chroms=args.chroms
    )
    calc_corr_main(calc_args)

    # Step 3: Run find_significantly_different_regions
    print("Running find_significantly_different_regions...")
    # Use the output files from calculate_correlation_FC
    track_FC_file = os.path.join(calc_output_dir, 'tracks_log_Wald_pValue.bedgraph')
    track_correlation_file = os.path.join(calc_output_dir, 'tracks_pearson.bedgraph')
    regions_args = argparse.Namespace(
        track_FC=track_FC_file,
        track_correlation=track_correlation_file,
        output_dir=regions_output_dir,
        min_region_size=5,
        fc_high_percentile=args.fc_high_percentile,
        fc_low_percentile=args.fc_low_percentile,
        corr_high_percentile=args.corr_high_percentile,
        corr_low_percentile=args.corr_low_percentile,
        chroms=args.chroms
    )
    find_regions_main(regions_args)

    print("Pipeline completed successfully.")

if __name__ == '__main__':
    main()
