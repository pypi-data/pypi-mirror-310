GEN_TYPING_TARGETS += src/array_typing/array_like/__init__.pyi
GEN_TYPING_TARGETS += src/array_typing/array_like/_bool.py
GEN_TYPING_TARGETS += src/array_typing/array_like/_float.py
GEN_TYPING_TARGETS += src/array_typing/array_like/_integer.py
GEN_TYPING_TARGETS += src/array_typing/jax/__init__.pyi
GEN_TYPING_TARGETS += src/array_typing/jax/_bool.py
GEN_TYPING_TARGETS += src/array_typing/jax/_export.py
GEN_TYPING_TARGETS += src/array_typing/jax/_float.py
GEN_TYPING_TARGETS += src/array_typing/jax/_integer.py
GEN_TYPING_TARGETS += src/array_typing/numpy/__init__.pyi
GEN_TYPING_TARGETS += src/array_typing/numpy/_bool.py
GEN_TYPING_TARGETS += src/array_typing/numpy/_export.py
GEN_TYPING_TARGETS += src/array_typing/numpy/_float.py
GEN_TYPING_TARGETS += src/array_typing/numpy/_integer.py
GEN_TYPING_TARGETS += src/array_typing/torch/__init__.pyi
GEN_TYPING_TARGETS += src/array_typing/torch/_bool.py
GEN_TYPING_TARGETS += src/array_typing/torch/_export.py
GEN_TYPING_TARGETS += src/array_typing/torch/_float.py
GEN_TYPING_TARGETS += src/array_typing/torch/_integer.py

.PHONY: $(GEN_TYPING_TARGETS)
gen-array-types: $(GEN_TYPING_TARGETS)
	@ ruff check $^

# ----------------------------- Auxiliary Targets ---------------------------- #

$(GEN_TYPING_TARGETS): src/array_typing/%: templates/%.jinja scripts/gen-array-types.py
	@ python scripts/gen-array-types.py --output "$@" "$<"
