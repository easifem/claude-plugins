# EASIFEM code templates

Before using a template, open a neighbouring file in the same module and
match its exact header text, imports and banner style. The repository is
the source of truth.

## GPL v3 header (library files only)

```fortran
! This program is a part of EASIFEM library
! Copyright (C) 2020-2021 Vikas Sharma, Ph.D
!
! This program is free software: you can redistribute it and/or modify
! it under the terms of the GNU General Public License as published by
! the Free Software Foundation, either version 3 of the License, or
! (at your option) any later version.
!
! This program is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
! GNU General Public License for more details.
!
! You should have received a copy of the GNU General Public License
! along with this program.  If not, see <https://www.gnu.org/licenses/>
```

## Section banner

```fortran
!----------------------------------------------------------------------------
!                                                                MethodName
!----------------------------------------------------------------------------
```

## base: module (multiple dispatch)

Specific procedures use the `obj_` prefix; use `TypeName_MethodName`
only when `obj_` would clash (see `naming.md`).

```fortran
MODULE TypeName_Method
USE BaseType, ONLY: TypeName_
USE GlobalData, ONLY: DFP
USE GlobalData, ONLY: I4B
USE GlobalData, ONLY: LGT
IMPLICIT NONE
PRIVATE

PUBLIC :: MethodName

!> author: Vikas Sharma, Ph. D.
! date: YYYY-MM-DD
! summary: ...
! (full docblock: see docblock-style.md)

INTERFACE MethodName
  MODULE SUBROUTINE obj_MethodName(obj, param)
    TYPE(TypeName_), INTENT(INOUT) :: obj
    !! object
    INTEGER(I4B), INTENT(IN) :: param
    !! meaning of param
  END SUBROUTINE obj_MethodName
END INTERFACE MethodName

END MODULE TypeName_Method
```

## base: new type

1. Define the type in `src/modules/BaseType/src/BaseType.F90`.
2. Create `src/modules/<TypeName>/` with `<TypeName>_Method.F90`
   (interfaces) and its `CMakeLists.txt`.
3. Create `src/submodules/<TypeName>/` with
   `<TypeName>_Method@<Category>Methods.F90` files and `CMakeLists.txt`.
4. Add both directories to the parent `CMakeLists.txt` the same way as
   neighbouring modules.

## base: submodule

```fortran
SUBMODULE(TypeName_Method) ConstructorMethods
USE ErrorHandling, ONLY: ErrorMsg
USE GlobalData, ONLY: stderr
IMPLICIT NONE

CONTAINS

!----------------------------------------------------------------------------
!                                                                MethodName
!----------------------------------------------------------------------------

MODULE PROCEDURE obj_MethodName
! implementation
END PROCEDURE obj_MethodName

END SUBMODULE ConstructorMethods
```

## classes: module skeleton

```fortran
! GPL v3 header

!> author: Vikas Sharma, Ph. D.
! date: YYYY-MM-DD
! summary: Brief description

MODULE ClassName_Class
USE ExceptionHandler_Class, ONLY: e
USE GlobalData, ONLY: DFP
USE GlobalData, ONLY: I4B
USE GlobalData, ONLY: LGT
IMPLICIT NONE
PRIVATE

PUBLIC :: ClassName_
PUBLIC :: ClassNamePointer_

TYPE :: ClassName_
  PRIVATE
  ! components, each with a !! comment
CONTAINS
  PRIVATE
  PROCEDURE, PUBLIC, PASS(obj) :: DEALLOCATE => obj_Deallocate
  !! deallocate the object
  FINAL :: obj_Final
END TYPE ClassName_

TYPE :: ClassNamePointer_
  CLASS(ClassName_), POINTER :: ptr => NULL()
END TYPE ClassNamePointer_

! INTERFACE blocks with full docblocks

END MODULE ClassName_Class
```

Finalizer implementation: `obj_Final` just calls `CALL obj%DEALLOCATE()`.

## classes: submodule skeleton

`modName` lives here, not in the module, and only in DEBUG mode:

```fortran
! GPL v3 header

!> author: Vikas Sharma, Ph. D.
! date: YYYY-MM-DD
! summary: Implementation of <Category> methods

SUBMODULE(ClassName_Class) GetMethods
USE SomeModule, ONLY: SomeItem
IMPLICIT NONE

#ifdef DEBUG_VER
CHARACTER(*), PARAMETER :: modName = "ClassName_Class"
#endif

CONTAINS

! MODULE PROCEDURE blocks, each preceded by a section banner

#include "../../include/errors.F90"

END SUBMODULE GetMethods
```

Include `errors.F90` (path as in neighbouring submodules) only when the
submodule uses `AssertError1/2/3`.

## classes: type-bound method

In the type definition (one-line `!!` comment per binding):

```fortran
  PROCEDURE, PUBLIC, PASS(obj) :: MethodName => obj_MethodName
  !! one-line description
```

Overloads of a generic are numbered (see `naming.md`):

```fortran
  PROCEDURE, PASS(obj) :: Set1 => obj_Set1
  !! set a single value
  PROCEDURE, PASS(obj) :: Set2 => obj_Set2
  !! set a vector of values
  GENERIC, PUBLIC :: Set => Set1, Set2
```

Interface in the module (full docblock goes here):

```fortran
INTERFACE
  MODULE SUBROUTINE obj_MethodName(obj, param)
    CLASS(ClassName_), INTENT(INOUT) :: obj
    !! object
    INTEGER(I4B), INTENT(IN) :: param
    !! meaning of param
  END SUBROUTINE obj_MethodName
END INTERFACE
```

Implementation in `ClassName_Class@<Category>.F90`:

```fortran
MODULE PROCEDURE obj_MethodName
#ifdef DEBUG_VER
CHARACTER(*), PARAMETER :: myName = "obj_MethodName()"
#endif

#ifdef DEBUG_VER
CALL e%RaiseInformation(modName//'::'//myName//' - '// &
                        '[START] ')
#endif

IF (nothing_to_do) THEN
#ifdef DEBUG_VER
  CALL e%RaiseInformation(modName//'::'//myName//' - '// &
                          '[END] ')
#endif
  RETURN
END IF

#ifdef DEBUG_VER
IF (error_condition) THEN
  CALL e%RaiseError(modName//'::'//myName//' - '// &
                    '[ERROR] :: Error description')
END IF
! or: CALL AssertError1(.NOT. error_condition, myName, 'description')
#endif

! implementation

#ifdef DEBUG_VER
CALL e%RaiseInformation(modName//'::'//myName//' - '// &
                        '[END] ')
#endif
END PROCEDURE obj_MethodName
```

Debug rules (classes):

- Every procedure, including internal helpers, raises `[START]` and
  `[END]` in DEBUG mode; add them when editing a procedure that lacks
  them. Raise `[END]` before every early `RETURN` too.
- Error checks exist **only** in DEBUG mode. The release build has no
  checks and no fallbacks for wrong input (an output may be left
  uninitialised); users run in DEBUG first. Do not add release-mode
  error handling, and do not report its absence in reviews.
- `myName` and check-only variables (e.g. `isok`) are declared inside
  `#ifdef DEBUG_VER` as well.

## Test / example program

File: `src/modules/<Module>/examples/<MethodName>_test_<N>.F90`. Pick the next
unused `<N>`. No GPL header. Group checks in `BLOCK ... END BLOCK`, each
preceded by a short comment saying what it tests. A complete real example
is in `test-example.md`.

```fortran
!> author: Vikas Sharma, Ph. D.
! date: YYYY-MM-DD
! summary: one line describing what is tested

PROGRAM main
USE BaseType, ONLY: math => TypeMathOpt
USE ExceptionHandler_Class, ONLY: e
USE GlobalData, ONLY: DFP
USE SomeModule, ONLY: SomeRoutine
USE Test_Method, ONLY: OK
IMPLICIT NONE

! global objects used by several blocks

CALL e%SetQuietMode(math%yes)

! initiate global objects

! Test 1: SomeRoutine gives a positive value
BLOCK
  REAL(DFP) :: x(3)
  x = [1.0_DFP, 2.0_DFP, 3.0_DFP]
  CALL OK(SomeRoutine(x) .GT. 0.0_DFP, "SomeRoutine is positive")
END BLOCK

! Test 2: ...
BLOCK
  ! local declarations and checks
END BLOCK

! deallocate global objects
END PROGRAM main
```

Rules:

- Use `CALL OK(condition, "label")` for every check; give exact expected
  values where possible.
- For routines overloaded over kinds, test only `REAL(DFP)` and
  `INTEGER(I4B)`.
- Cover edge cases (empty input, zero, negative values, sizes > internal
  thresholds) in separate `OK` calls.
- `e%SetQuietMode(math%yes)` keeps library messages out of the output
  (classes and kernels; base tests may omit it).
- Helper procedures go after `CONTAINS` inside the program.
