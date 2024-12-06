export PATH="$PATH:../ft/"

seq 1 3 | map add 10

find . | filter is_file | map basename

find . -name '*.jpg' | map duplicate | map -c2 basename | map -c2 prepend "thumb_" | map run echo

seq 1 10 | foldl add 0
seq 1 10 | foldl mul 1
seq 1 10 | map append "," | foldl append ""

cat /etc/passwd | map split : | filter -c1 equal shark | map index 6
