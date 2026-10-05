# Automated Password Strength and Security Analyzer

This offline Python project evaluates password strength without saving, logging, or displaying the entered password. It checks length, uppercase and lowercase letters, numbers, special characters, common passwords and simple variations, repeated characters, and predictable number, alphabet, and keyboard patterns. The program calculates a score, assigns a strength rating, and provides specific suggestions for improving the password.

> **Important:** This is an educational tool. A high score does not guarantee that a password is secure. Never place real passwords in source code, test files, notebooks, screenshots, commits, or issue reports.

## Project Progress

Progress updated October 2, 2026.

- [x] Defined the project scope and password-security rules
- [x] Created the offline Python password analyzer
- [x] Added hidden password entry so the password is not displayed
- [x] Added checks for length and character types
- [x] Added detection for common passwords and simple variations
- [x] Added detection for repeated characters and predictable patterns
- [x] Added a 0–100 score, strength rating, and improvement suggestions
- [x] Improved the scoring system to prevent short passwords from receiving high ratings
- [x] Created 11 automated tests using fictional passwords
- [x] Verified that all 11 automated tests pass
- [x] Tested the analyzer through the Python command-line program
- [x] Tested the analyzer through the Jupyter Notebook
- [x] Added Conda environment and VS Code setup instructions
- [x] Uploaded the project files to the GitHub repository
- [x] Complete the final team review
- [ ] Add final screenshots and project documentation
- [ ] Complete the written report and individual reflections

GitHub repository: [CYB333 CourseWork](https://github.com/unkownknown1/CYB333-CourseWork)

## Project Files

- `password_analyzer.py` — analyzer logic and hidden-input command-line program
- `test_password_analyzer.py` — 11 automated tests using fictional passwords
- `Password_Analyzer_Demo.ipynb` — Jupyter Notebook demonstration
- `environment.yml` — Conda environment definition
- `.gitignore` — prevents common local and generated files from being committed

## Set Up in VS Code with Conda

1. Install the latest Microsoft **Python** and **Jupyter** extensions in VS Code.
2. Open the project folder in VS Code.
3. Open the VS Code terminal and run:

```powershell
conda env create -f environment.yml
conda activate password-analyzer
```

4. Press `Ctrl+Shift+P`, select **Python: Select Interpreter**, and choose the `password-analyzer` Conda environment.
5. When using the notebook, select the same environment as the Jupyter kernel.

## Run the Analyzer

From the `Automated Password Analyzer` folder, run:

```powershell
python password_analyzer.py
```

The terminal will not display the password while it is being typed. This is expected because the program uses hidden password input.

## Run the Automated Tests

From the `Automated Password Analyzer` folder, run:

```powershell
python -m unittest -v
```

All tests use fictional passwords. The test suite verifies:

- Common-password detection
- Simple common-password variations
- Missing character types
- Repeated characters
- Number and keyboard sequences
- Scoring and rating limits
- Strong fictional passwords
- Removal of the original password from the result object

The current test result is:

```text
Ran 11 tests
OK
```

## Jupyter Notebook Demonstration

Open `Password_Analyzer_Demo.ipynb`, select the Conda Python kernel, and choose **Run All**. The notebook uses fictional passwords only and demonstrates Weak, Strong, and Very Strong results.

Do not enter a real password in the notebook because notebook inputs and outputs may be saved. Use `password_analyzer.py` when hidden input is required.

## Update the GitHub Repository

Run the following commands from the main `CourseWork` repository folder:

```powershell
git status
git add "Automated Password Analyzer"
git commit -m "Improve password scoring and automated tests"
git push origin main
```

Review `git status` and the staged files before every commit. Do not commit files containing real credentials.

## Privacy and Project Scope

The program operates entirely offline and uses only the Python standard library. A password exists briefly in memory because it must be analyzed, but the program does not save, log, display, or return it.

A future version could include a secure password generator or a privacy-preserving breach check that sends only a partial password hash instead of the complete password.