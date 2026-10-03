# Automated Password Strength and Security Analyzer

This offline Python project evaluates password strength without saving, logging,
or displaying the entered password. It checks length, uppercase and lowercase
letters, numbers, special characters, common passwords, repeated characters,
and predictable number, alphabet, and keyboard patterns. It then calculates a
score, assigns a rating, and provides specific improvement suggestions.

> **Important:** This is an educational tool. A high score does not guarantee
> that a password is secure. Never place real passwords in source code, test
> files, notebooks, screenshots, commits, or issue reports.

## Project progress

Progress updated October 2, 2026.

- [x] Defined the project scope and password-security rules
- [x] Created the offline Python password analyzer
- [x] Added hidden password entry so the password is not displayed
- [x] Added checks for length, character types, common passwords, repeated
  characters, and predictable patterns
- [x] Added a 0-100 score, strength rating, and improvement suggestions
- [x] Created seven automated tests using fictional passwords
- [x] Verified that all seven automated tests pass
- [x] Created a Jupyter Notebook demonstration
- [x] Added Conda environment and VS Code setup instructions
- [ ] Complete team review and additional manual testing
- [ ] Add screenshots and final project documentation
- [ ] Upload the completed project files to the GitHub repository

GitHub repository:
[CYB333 CourseWork](https://github.com/unkownknown1/CYB333-CourseWork)

## Project files

- `password_analyzer.py` — analyzer logic and hidden-input command-line program
- `test_password_analyzer.py` — automated tests using fictional passwords
- `Password_Analyzer_Demo.ipynb` — optional Jupyter demonstration
- `environment.yml` — Conda environment definition
- `.gitignore` — prevents common local and generated files from being committed

## Set up in VS Code with Conda

1. Install the latest Microsoft **Python** and **Jupyter** extensions in VS Code.
2. Open this project folder in VS Code.
3. Open the VS Code terminal and run:

   ```powershell
   conda env create -f environment.yml
   conda activate password-analyzer
   ```

4. Press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, and select the
   `password-analyzer` Conda environment.
5. When using the notebook, select the same environment as the Jupyter kernel.

## Run the analyzer

```powershell
python password_analyzer.py
```

The terminal will not show the password while it is typed. In some VS Code or
Jupyter interfaces, hidden input may appear as a blank field; this is expected.

## Run the automated tests

```powershell
python -m unittest -v
```

All tests use fictional examples. The test suite checks common passwords,
missing character types, repetitions, predictable patterns, scoring, and the
absence of the original password from the result object.

## Upload to GitHub

After creating an empty GitHub repository, run these commands from this folder.
Replace the example URL with the URL of your repository:

```powershell
git init
git add .
git commit -m "Create automated password analyzer"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Review `git status` and the staged files before every commit. Do not commit any
file containing a real credential.

## Privacy and project scope

The initial version operates entirely offline and uses only the Python standard
library. The password exists briefly in program memory because it must be
analyzed, but the program does not save, log, print, or return it. A future
version could add a password generator or a privacy-preserving breach check that
sends only a partial password hash rather than the complete password.
