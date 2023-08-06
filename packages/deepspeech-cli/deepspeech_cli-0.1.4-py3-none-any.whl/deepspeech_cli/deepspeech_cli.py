#!/usr/bin/env python3

from pathlib import Path
import subprocess, typer
from enum import Enum
from . import logger

deepspeech_path = '/usr/local/Caskroom/miniconda/base/envs/speech/bin/deepspeech'
deepspeech_dir = Path.home() / 'testdir/deepspeech'

app = typer.Typer()


class Lang(str, Enum):
    en = 'en'
    zh = 'zh'


lang_opt = typer.Option(Lang.en,
                        '--lang',
                        '-l',
                        help='Language of the audio file')


def convert_audio_to_wav(path: Path) -> Path:
    """
    Convert audio file to wav format.
    """
    if path.suffix == '.wav':
        return path
    else:
        # -y: overwrites without asking
        # -ac 1: mono
        # -ar 16000: 16kHz
        rc = subprocess.run([
            'ffmpeg', '-i',
            str(path), '-ac', '1', '-ar', '16000', '-y',
            str(path.with_suffix('.wav'))
        ]).returncode
        if rc != 0:
            typer.echo(f'Failed to convert {path} to wav format.', err=True)
            raise typer.Abort()
        return path.with_suffix('.wav')


@app.command()
def transcribe(path: Path = typer.Argument(
    ..., help='Path to audio file', callback=convert_audio_to_wav),
               lang: Lang = lang_opt):
    """Transcribe audio file"""

    if lang == Lang.en:
        model = 'deepspeech-0.9.3-models.pbmm'
        scorer = 'deepspeech-0.9.3-models.scorer'

    elif lang == Lang.zh:
        model = 'deepspeech-0.9.3-models.pbmm'
        scorer = 'deepspeech-0.9.3-models.scorer'

    program = [
        deepspeech_path, '--model', model, '--scorer', scorer, '--audio',
        str(path)
    ]
    logger.info(f'Running {program}')

    proc = subprocess.run(program, cwd=deepspeech_dir, capture_output=True)
    output_path = path.with_suffix('.txt')
    output_path.write_text(proc.stdout.decode('utf-8'))
    typer.echo(f'Output saved to: {str(output_path)}')


if __name__ == '__main__':
    app()
