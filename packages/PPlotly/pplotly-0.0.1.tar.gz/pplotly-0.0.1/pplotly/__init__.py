import importlib

main = importlib.import_module(".main", package="pplotly")

# Import all symbols dynamically
globals().update(vars(main))
