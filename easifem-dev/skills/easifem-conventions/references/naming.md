# Naming rules

## Types and modules

- Types end with `_`: `Mesh_`, `HDF5File_`, `QuadraturePoint_`.
- Pointer wrappers: `<Name>Pointer_` with component `ptr`.
- classes module: `<Name>_Class` in `<Name>_Class.F90`.
- `modName`: `CHARACTER(*), PARAMETER :: modName = "<Name>_Class"`,
  declared in **each submodule** (not in the module), inside
  `#ifdef DEBUG_VER ... #endif`.
- base module: `<Name>_Method` or `<Name>Utility`.
- Submodule: `<Module>@<Category>.F90`, `SUBMODULE(<Module>) <Category>`.

## Methods (type-bound procedures)

| Item | Rule | Example |
|---|---|---|
| Binding (public API) | PascalCase, first letter uppercase | `Initiate`, `GetRank`, `IsInitiated` |
| Specific procedure | `obj_` + binding name, uppercase first letter after `_` | `GetRank => obj_GetRank` |
| Prefix | `obj_` everywhere (base and classes); never module prefixes like `hdf5_`. Use `TypeName_MethodName` only when `obj_` would cause a name conflict (e.g. two types in one module with the same method) | `obj_Initiate`, `Mesh_Initiate` |
| Non-allocating variant | trailing `_`: fills a preallocated array and returns its extent (`tsize`, `nrow`, `ncol`); never allocates | `Get_`, `READ_` |
| Verbs | `Get…`, `Set…`, `Is…` (LOGICAL result), `Import`/`Export`, `Display`, `Deallocate`, `Initiate` | `IsCompressed` |
| Fortran keywords as bindings | written uppercase (formatter) | `OPEN`, `CLOSE`, `READ`, `WRITE`, `DEALLOCATE`, `IMPORT` |

## Variables

- camelCase: `meshVolume`, `localNodes`, `elemType`.
- Common names: `obj` (object instance), `ans` (function result).

## Overloads of a generic: numbered, never by type

Name every specific procedure of a generic with the generic name plus a
number, starting at 1. Binding names match the procedure names without
`obj_`. If the generic name ends in `_`, the number follows that `_`.

```fortran
  PROCEDURE, PASS(obj) :: Initiate1 => obj_Initiate1
  !! Initiate from ...
  PROCEDURE, PASS(obj) :: Initiate2 => obj_Initiate2
  !! Initiate from ...
  GENERIC, PUBLIC :: Initiate => Initiate1, Initiate2

  PROCEDURE, PASS(obj) :: Get_1 => obj_Get_1
  !! Get values in a preallocated real vector
  PROCEDURE, PASS(obj) :: Get_2 => obj_Get_2
  !! Get values in a preallocated real matrix
  GENERIC, PUBLIC :: Get_ => Get_1, Get_2
```

- Numbered bindings are private; only the `GENERIC` is public.
- Do **not** encode type/kind/rank in names (`obj_Write_d1`,
  `obj_Read_n2`, `_r1`, `_int` ...). That style is legacy (e.g. in
  `HDF5File_Class`) and is being migrated with `/refactor`.
- Describe the type/rank in the `!!` comment and in the docblock instead.
- When adding an overload, use the next unused number; never renumber
  existing ones unless doing a `/refactor`.
- Private helper routines that are not part of a generic get a
  descriptive PascalCase name (`obj_WriteStringHelper`), not a number.
