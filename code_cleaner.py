"""
Code Cleaner: Remove comments and extra whitespace from code files.
Supports multiple programming languages.
"""

import re
from enum import Enum
from typing import Dict, List, Tuple


class Language(Enum):
    """Supported programming languages and their comment patterns."""
    PYTHON = {
        'single_line': '#',
        'multi_line_start': '"""',
        'multi_line_end': '"""',
        'multi_line_alt_start': "'''",
        'multi_line_alt_end': "'''",
    }
    JAVASCRIPT = {
        'single_line': '//',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    JAVA = {
        'single_line': '//',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    C = {
        'single_line': '//',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    CPP = {
        'single_line': '//',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    RUBY = {
        'single_line': '#',
        'multi_line_start': '=begin',
        'multi_line_end': '=end',
    }
    PHP = {
        'single_line': '//',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
        'hash_comment': '#',
    }
    GO = {
        'single_line': '//',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    RUST = {
        'single_line': '//',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    SQL = {
        'single_line': '--',
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    HTML = {
        'multi_line_start': '<!--',
        'multi_line_end': '-->',
    }
    CSS = {
        'multi_line_start': '/*',
        'multi_line_end': '*/',
    }
    BASH = {
        'single_line': '#',
        'multi_line_start': ':\'',
        'multi_line_end': '\'',
    }


class CodeCleaner:
    """Remove comments and extra whitespace from source code."""

    def __init__(self, language: Language):
        self.language = language
        self.comment_config = language.value

    @staticmethod
    def detect_language(filename: str) -> Language:
        """Detect language from file extension."""
        ext_map = {
            '.py': Language.PYTHON,
            '.js': Language.JAVASCRIPT,
            '.jsx': Language.JAVASCRIPT,
            '.ts': Language.JAVASCRIPT,
            '.tsx': Language.JAVASCRIPT,
            '.java': Language.JAVA,
            '.c': Language.C,
            '.cpp': Language.CPP,
            '.cc': Language.CPP,
            '.cxx': Language.CPP,
            '.h': Language.C,
            '.hpp': Language.CPP,
            '.rb': Language.RUBY,
            '.php': Language.PHP,
            '.go': Language.GO,
            '.rs': Language.RUST,
            '.sql': Language.SQL,
            '.html': Language.HTML,
            '.htm': Language.HTML,
            '.css': Language.CSS,
            '.scss': Language.CSS,
            '.less': Language.CSS,
            '.sh': Language.BASH,
            '.bash': Language.BASH,
        }
        
        for ext, lang in ext_map.items():
            if filename.endswith(ext):
                return lang
        
        # Default to Python if unknown
        return Language.PYTHON

    def remove_comments(self, code: str) -> str:
        """Remove comments from code based on language."""
        lines = code.split('\n')
        cleaned_lines = []
        in_multiline = False
        multiline_marker = None

        for line in lines:
            # Check for multi-line comment end
            if in_multiline:
                if multiline_marker in line:
                    in_multiline = False
                continue

            # Check for multi-line comment start
            for marker_type in ['multi_line_start', 'multi_line_alt_start']:
                if marker_type in self.comment_config:
                    marker = self.comment_config[marker_type]
                    if marker in line:
                        in_multiline = True
                        multiline_marker = self.comment_config.get(
                            marker_type.replace('start', 'end'),
                            marker_type.replace('start', 'end')
                        )
                        continue

            # Remove single-line comments
            if 'single_line' in self.comment_config:
                comment_marker = self.comment_config['single_line']
                if comment_marker in line:
                    # Handle strings to avoid removing comment markers in strings
                    line = self._remove_single_line_comment(line, comment_marker)
            
            # Handle hash comments (PHP, etc.)
            if 'hash_comment' in self.comment_config and '#' not in self.comment_config.get('single_line', ''):
                line = self._remove_single_line_comment(line, '#')

            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def _remove_single_line_comment(self, line: str, comment_marker: str) -> str:
        """Remove single-line comment from a line, respecting strings."""
        in_string = False
        string_char = None
        i = 0

        while i < len(line):
            # Handle string boundaries
            if line[i] in ('"', "'") and (i == 0 or line[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = line[i]
                elif line[i] == string_char:
                    in_string = False
                    string_char = None

            # Look for comment marker outside strings
            if not in_string and line[i:i+len(comment_marker)] == comment_marker:
                return line[:i].rstrip()

            i += 1

        return line

    def remove_extra_lines(self, code: str) -> str:
        """Remove extra blank lines, keeping max one blank line between code."""
        lines = code.split('\n')
        cleaned_lines = []
        previous_blank = False

        for line in lines:
            stripped = line.strip()

            if not stripped:  # Blank line
                if not previous_blank:
                    cleaned_lines.append('')
                previous_blank = True
            else:
                cleaned_lines.append(line)
                previous_blank = False

        # Remove leading and trailing blank lines
        while cleaned_lines and not cleaned_lines[0].strip():
            cleaned_lines.pop(0)
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()

        return '\n'.join(cleaned_lines)

    def clean(self, code: str, remove_extra_lines: bool = True) -> str:
        """
        Clean code by removing comments and optionally extra blank lines.
        
        Args:
            code: Source code to clean
            remove_extra_lines: Whether to remove extra blank lines
            
        Returns:
            Cleaned code
        """
        # Remove comments
        code = self.remove_comments(code)

        # Remove extra lines if requested
        if remove_extra_lines:
            code = self.remove_extra_lines(code)

        return code


def clean_file(input_file: str, output_file: str = None, language: Language = None):
    """
    Clean a code file and save the result.
    
    Args:
        input_file: Path to input file
        output_file: Path to output file (defaults to input_file.cleaned)
        language: Programming language (auto-detected if None)
    """
    if output_file is None:
        output_file = f"{input_file}.cleaned"

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Detect language if not provided
    if language is None:
        language = CodeCleaner.detect_language(input_file)

    # Clean code
    cleaner = CodeCleaner(language)
    cleaned_code = cleaner.clean(code)

    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_code)

    print(f"✓ Cleaned code saved to: {output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python code_cleaner.py <input_file> [output_file] [language]")
        print("\nExample: python code_cleaner.py script.py cleaned_script.py python")
        print("\nSupported languages: python, javascript, java, c, cpp, ruby, php, go, rust, sql, html, css, bash")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    language_str = sys.argv[3].upper() if len(sys.argv) > 3 else None

    language = None
    if language_str:
        try:
            language = Language[language_str]
        except KeyError:
            print(f"Unknown language: {language_str}")
            sys.exit(1)

    clean_file(input_file, output_file, language)
