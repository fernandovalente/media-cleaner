import os
import subprocess
import shutil

from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class MediaCleanerConfig:
    project_dir: Path = Path(__file__).parent.resolve()
    media_in_dir: Path = project_dir / "mediain"
    media_out_dir: Path = project_dir / "mediaout"

class MediaCleaner:
    def __init__(self, config: MediaCleanerConfig = MediaCleanerConfig()):
        self.config = config

    def setup(self) -> None:
        """Ensure input and output directories exist."""
        self.config.media_in_dir.mkdir(parents=True, exist_ok=True)
        self.config.media_out_dir.mkdir(parents=True, exist_ok=True)

    def _is_valid_file(self, filepath: Path) -> bool:
        """Check if the provided path is a valid file to process (not hidden)."""
        return filepath.is_file() and not filepath.name.startswith('.')

    def _get_files_to_process(self) -> List[Path]:
        """Return a list of valid files present in the input directory."""
        return [f for f in self.config.media_in_dir.iterdir() if self._is_valid_file(f)]

    def _clean_file(self, input_path: Path, output_path: Path) -> bool:
        """
        Use exiftool to strip all metadata from the file.
        The file is copied first so the original remains untouched.
        Returns True if successful, False otherwise.
        """
        print(f"Processing: {input_path.name}")
        
        try:
            # Copy file to destination for processing
            shutil.copy2(input_path, output_path)
            
            # Execute exiftool to clean all metadata (-all=)
            # -overwrite_original prevents creating a backup file in the output directory
            subprocess.run(
                ['exiftool', '-all=', '-overwrite_original', str(output_path)],
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"Cleaned and saved to: {output_path.parent.name}/{output_path.name}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error cleaning metadata from {input_path.name}:")
            print(e.stderr)
            # Remove potentially corrupted file if it failed
            if output_path.exists():
                output_path.unlink()
            return False
        except Exception as e:
            print(f"Unexpected error processing {input_path.name}: {e}")
            return False

    def process_all(self) -> Tuple[int, int]:
        """
        Process all files in the input directory.
        Returns a tuple of (successful_count, failed_count).
        """
        self.setup()
        
        files_to_process = self._get_files_to_process()
        
        if not files_to_process:
            print(f"No files found in '{self.config.media_in_dir.name}'.")
            print("Place your images or videos there and run the script again.")
            return 0, 0

        print(f"Found {len(files_to_process)} file(s) to process.\n")
        
        results: List[bool] = []
        for file_path in files_to_process:
            out_path = self.config.media_out_dir / file_path.name
            results.append(self._clean_file(file_path, out_path))
            
        success_count = results.count(True)
        failure_count = results.count(False)
                
        return success_count, failure_count


def main():
    cleaner = MediaCleaner()
    success, failure = cleaner.process_all()
    
    if success > 0 or failure > 0:
        print("\n--- Summary ---")
        print(f"Success: {success}")
        print(f"Failures: {failure}")

if __name__ == "__main__":
    main()
