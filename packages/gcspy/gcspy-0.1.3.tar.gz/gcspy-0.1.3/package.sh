export CXX=/opt/homebrew/Cellar/llvm/18.1.8/bin/clang++
rm -rf build dist generator
python3 -m build
twine upload dist/*
