python3 -m venv .venv
source .venv/bin/activate
pip install pyminifier3

flag="cE5TUNVRa!My\$7eRe3NPY7h0nEnPlUs!"
challenge_file="./source/VeritableMystere.py"

echo "Setting flag: $flag"

mkdir -p ./source/tmp

bytecode_file="./source/tmp/bytecode.txt"
rm "$bytecode_file"
python3 ./source/generator/funcGenerator.py "$flag" "$bytecode_file"

myvm_out_file="./source/tmp/myVM.py"
python3 ./source/VeritableMystere/myParse.py "$bytecode_file" "./source/VeritableMystere/myVM.py" "$myvm_out_file"
pyminifier --obfuscate --obfuscate-classes --obfuscate-functions --obfuscate-import-methods --replacement-length=5 "$myvm_out_file" > ./source/tmp/obfuscated.py
./source/generator/fix_pyminifier.sh ./source/tmp/obfuscated.py ./source/tmp/obfuscated_fixed.py
pyminifier --bzip2 ./source/tmp/obfuscated_fixed.py > "$challenge_file"
