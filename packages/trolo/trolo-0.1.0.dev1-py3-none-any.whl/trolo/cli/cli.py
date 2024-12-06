import click
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from trolo.train import train_model
from trolo.infer import process_image, process_video, load_model
from trolo.loaders import yaml_utils
from trolo.utils.smart_defaults import infer_pretrained_model, infer_input_path, infer_device, infer_model_config_path

@click.group()
def cli():
    """D-FINE CLI tool for training, testing, and inference"""
    pass

@cli.command()
@click.argument('args', nargs=-1)
@click.option('--config', '-c', type=click.Path(exists=True), required=True, help='Path to the config file', default=infer_model_config_path())
@click.option('--resume', '-r', type=click.Path(exists=True), help='Path to the resume checkpoint')
@click.option('--tuning', '-t', type=click.Path(exists=True), help='Path to the tuning checkpoint')
@click.option('--device', '-d', type=str, help='Device to use for training')
@click.option('--seed', type=int, help='Random seed')
@click.option('--use-amp/--no-amp', default=False, help='Use automatic mixed precision')
@click.option('--output-dir', '-o', type=click.Path())
@click.option('--summary-dir', '-s', type=click.Path(), help='Path to the summary directory')
@click.option('--test-only', is_flag=True, default=False, help='Only run evaluation')
@click.option('--print-method', type=str, default='builtin', help='Method to use for printing')
@click.option('--print-rank', type=int, default=0, help='Rank for printing')
@click.option('--local-rank', type=int)
def train(args, config, resume, tuning, device, seed, use_amp, output_dir, 
          summary_dir, test_only, print_method, print_rank, local_rank):
    """Train a model with specified parameters"""
    # Parse additional arguments as updates
    update = list(args) if args else None
    
    train_model(
        config=config,
        resume=resume,
        tuning=tuning,
        device=device,
        seed=seed,
        use_amp=use_amp,
        output_dir=output_dir,
        summary_dir=summary_dir,
        test_only=test_only,
        update=update,
        print_method=print_method,
        print_rank=print_rank,
        local_rank=local_rank
    )

@cli.command()
@click.argument('args', nargs=-1)
@click.option('--model', '-m', type=click.Path(exists=True), default=infer_pretrained_model())
@click.option('--input', '-i', type=click.Path(exists=True), default=infer_input_path())
@click.option('--output', '-o', type=click.Path())
@click.option('--device', '-d', default=infer_device())
@click.option('--format', '-f', type=click.Choice(['torch', 'onnx', 'trt']), default='torch')
@click.option('--show', '-s', is_flag=True, help='Show the output image or video in a window', default=True)
@click.option('--save', '-v', is_flag=True, help='Save the output image or video', default=True)
def infer(args, model, input, output, device, format, show, save):
    """Run inference on images or videos"""
    
    # check if input is a video file, if so then use process_video otherwise process it as image
    # Parse additional arguments
    extra_args = yaml_utils.parse_cli(args)

    # Check if input is video by extension
    video_exts = {'.mp4', '.avi', '.mov', '.mkv'}
    input_path = Path(input)
    is_video = input_path.suffix.lower() in video_exts

    # Load model
    model = load_model(model, format, device)

    if is_video:
        process_video(model, input, device, format, show, save)
    else:
        process_image(model, input, device, format, show, save)
    

def main():
    cli()

if __name__ == '__main__':
    main()