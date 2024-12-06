# Licensed under the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

<#
.SYNOPSIS

The launcher for Ultimate RVC.

.DESCRIPTION

This script is the entry point for Ultimate RVC. It is responsible for installing dependencies,
updating the application, running the application, and providing a CLI.

.PARAMETER Command
The command to run. The available commands are:

install:   Install dependencies and set up environment.
update:    Update Ultimate RVC to the latest version.
uninstall: Uninstall dependencies and user generated data.
run:       Start Ultimate RVC.
dev:       Start Ultimate RVC in development mode.
cli:       Start Ultimate RVC in CLI mode.
docs:      Generate documentation using Typer.
uv:        Run an arbitrary command using uv.
help:      Print help.

.PARAMETER Arguments
The arguments and options to run the command with. 
These are only used for the 'run', 'cli', 'docs' and 'uv' commands.

run:
    options:
        --help: Print help.
        [more information available, use --help to see all]
cli:
    options:
        --help: Print help.
        [more information available, use --help to see all]
docs:
    arguments:
        0: The module to generate documentation for.
        1: The output directory for the documentation.
uv:
    arguments:
        0: The command to run.
        [more information available, use --help to see all]
    options:
        --help: Print help.
        [more information available, use --help to see all]

#>

param (
    [Parameter(Position = 0, HelpMessage="The command to run.")]
    [string]$Command,
    [Parameter(ValueFromRemainingArguments = $true, `
        HelpMessage="The arguments to pass to the command.")]
    [string[]]$Arguments
)

$UvPath = "$(Get-location)\uv"
$env:UV_UNMANAGED_INSTALL = $UvPath
$env:UV_PYTHON_INSTALL_DIR = "$UvPath\python"
$env:UV_PYTHON_BIN_DIR = "$UV_PATH\python\bin"
$env:VIRTUAL_ENV = "$UvPath\.venv"
$env:UV_PROJECT_ENVIRONMENT = "$UvPath\.venv"
$env:UV_TOOL_DIR = "$UvPath\tools"
$env:UV_TOOL_BIN_DIR = "$UvPath\tools\bin"
$env:PATH = "$UvPath;$env:PATH"

function Main {
    param (
        [string]$Command,
        [string[]]$Arguments
    )

    switch ($Command) {
        "install" {
            Invoke-RestMethod https://astral.sh/uv/0.5.0/install.ps1 | Invoke-Expression
            uv run ./src/ultimate_rvc/core/main.py
        }
        "update" {
            git pull
        }
        "uninstall" {
            $confirmation_msg = "Are you sure you want to uninstall?`n" `
                + "This will delete all dependencies and user generated data [Y/n]"
            $confirmation = Read-Host -Prompt $confirmation_msg
            if ($confirmation -in @("", "Y", "y")) {
                git clean -dfX
                Write-Host "Uninstallation complete."
            } else {
                Write-Host "Uninstallation canceled."
            }

        }
        "run" {
            Assert-Dependencies
            uv run ./src/ultimate_rvc/web/main.py @Arguments
        }
        "dev" {
            Assert-Dependencies
            uv run gradio ./src/ultimate_rvc/web/main.py --demo-name app
        }
        "cli" {
            Assert-Dependencies
            uv run ./src/ultimate_rvc/cli/main.py @Arguments
        }
        "docs" {
            Assert-Dependencies
            if ($Arguments.Length -lt 2) {
                Write-Host "The 'docs' command requires at least two arguments."
                Exit 1
            }
            uv run python -m typer $Arguments[0] utils docs --output $Arguments[1]
        }
        "uv" {
            Assert-Dependencies
            uv @Arguments
        }
        "help" {
            Get-Help $PSCommandPath -Detailed
        }
        default {
            $error_msg = "Invalid command.`n" `
                + "To see a list of valid commands, use the 'help' command."
            Write-Host $error_msg
            Exit 1
        }
    }
}

function Assert-Dependencies {

    if (-Not (Test-Path -Path $UvPath)) {
        Write-Host "Dependencies not found. Please run './urvc install' first."
        Exit 1
    }
}

Main $Command $Arguments