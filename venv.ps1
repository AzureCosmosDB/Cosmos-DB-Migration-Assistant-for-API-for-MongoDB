# Recreate the python virtual environment and reinstall libs on Windows,
# and optionally run Jupyter Notebook outside of Azure Data Studio.
# Chris Joakim, Microsoft

$dirs = ".\venv\", ".\pyvenv.cfg"
foreach ($d in $dirs) {
    if (Test-Path $d) {
        echo "deleting $d"
        del $d -Force -Recurse
    } 
}

echo 'creating new venv ...'
python -m venv .\venv\

echo 'activating new venv ...'
.\venv\Scripts\Activate.ps1

echo 'upgrading pip ...'
python -m pip install --upgrade pip 

echo 'uinstall pip-tools ...'
pip install --upgrade pip-tools

echo 'displaying python location and version'
python --version

echo 'displaying pip location and version'
pip --version

echo 'pip-compile requirements.in ...'
pip-compile --output-file .\requirements.txt .\requirements.in

echo 'pip install requirements.txt ...'
pip install -q -r .\requirements.txt

echo 'pip list ...'
pip list

echo ''
echo 'next steps:'
echo '1) be sure the python virtual environment is activated: .\venv\Scripts\activate'
echo '2) execute "jupyter notebook"'
echo '3) open the logged URL with your browser'
echo '4) select notebook "database_migration_assistant.ipynb"'
echo '5) edit the value of "source_connection_string" in the first notebook cell'
echo '6) execute all cells of the notebook'
echo '7) see output file "DMA_outputs.zip" in the repository root directory'
echo ''
