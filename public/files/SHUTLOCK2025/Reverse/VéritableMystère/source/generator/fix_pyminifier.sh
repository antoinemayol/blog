input_file="$1"
output_file="$2"

# Step 1: Reorder class variables
awk '
BEGIN {
    in_class = 0
    var_block = ""
    class_def = ""
}
/^class / {
    class_def = $0
    in_class = 1
    next
}
in_class && /^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*=/ {
    var_block = var_block $0 "\n"
    next
}
in_class && /__init__/ {
    print var_block
    print class_def
    in_class = 0
}
{
    if (!in_class || /__init__/)
        print
}
' "$input_file" > temp_reordered.py

# Step 2: Obfuscate specific strings
declare -A obfuscations
for word in bytecode flags registers stack InstructionPointer StackPointer InstructionSet isRunning; do
    rand_str=$(tr -dc 'a-zA-Z' </dev/urandom | head -c 8)
    obfuscations[$word]=$rand_str
done

cp temp_reordered.py "$output_file"
for word in "${!obfuscations[@]}"; do
    sed -i "s/\b$word\b/${obfuscations[$word]}/g" "$output_file"
done

rm temp_reordered.py
