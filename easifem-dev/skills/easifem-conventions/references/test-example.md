# Complete test example (classes)

Tests `GetFaceDOF` and `GetTotalFaceDOF` of `FEDOF_` for orders 1 and 3.

```fortran
!> author: Vikas Sharma, Ph. D.
! date: 2026-11-02
! summary: Testing GetFaceDOF and GetTotalFaceDOF method of FEDOF class

PROGRAM main
USE BaseType, ONLY: math => TypeMathOpt
USE ExceptionHandler_Class, ONLY: e
USE FEDOF_Class, ONLY: FEDOF_
USE FEDomain_Class, ONLY: FEDomain_
USE GlobalData, ONLY: I4B
USE HDF5File_Class, ONLY: HDF5File_
USE Test_Method, ONLY: OK
IMPLICIT NONE

CHARACTER(*), PARAMETER :: filename = &
  "./meshdata/very_small_quad4_mesh.h5"
TYPE(FEDOF_) :: obj
TYPE(FEDomain_) :: dom
TYPE(HDF5File_) :: meshfile

CALL e%SetQuietMode(math%yes)
CALL meshfile%Initiate(filename, mode="READ")
CALL meshfile%OPEN()
CALL dom%Initiate(meshfile, '')

! testing for order 1, H1 and HIER
CALL obj%Initiate(baseContinuity="H1", baseInterpolation="HIER", &
                  isBrokenSpace=math%no, order=1, dom=dom)

! Testing GetFaceDOF
BLOCK
  INTEGER(I4B) :: ans(10), tsize

  CALL obj%GetFaceDOF(globalFace=1, islocal=math%yes, ans=ans, &
                      tsize=tsize)

  CALL OK(tsize .EQ. 0, &
          obj%GetCaseName()//" Size of faceDOF is zero for order=1")
END BLOCK

! Testing GetTotalFaceDOF
BLOCK
  INTEGER(I4B) :: tsize
  tsize = obj%GetTotalFaceDOF(globalFace=1, islocal=math%yes)
  CALL OK(tsize .EQ. 0, &
          obj%GetCaseName()//" Size of faceDOF is zero for order=1")
END BLOCK

! testing for order 3, H1 and HIER
CALL obj%Initiate(baseContinuity="H1", baseInterpolation="HIER", &
                  isBrokenSpace=math%no, order=3, dom=dom)

! Testing GetFaceDOF
BLOCK
  INTEGER(I4B) :: ans(10), tsize
  CALL obj%GetFaceDOF(globalElement=13, islocal=math%no, &
                      localFaceNumber=2, ans=ans, tsize=tsize)

  CALL OK(tsize .EQ. 2, &
          obj%GetCaseName()//" Size of faceDOF is 2 for order=3")

  CALL OK(ALL(ans(1:tsize) .EQ. [12, 13]), &
          obj%GetCaseName()//" faceDOF for order=3")
END BLOCK

! Testing GetTotalFaceDOF
BLOCK
  INTEGER(I4B) :: tsize

  tsize = obj%GetTotalFaceDOF(globalElement=13, islocal=math%no, &
                              localFaceNumber=2)

  CALL OK(tsize .EQ. 2, &
          obj%GetCaseName()//" GetTotalFaceDOF is 2 for order=3")
END BLOCK

CALL dom%DEALLOCATE()
CALL meshfile%DEALLOCATE()
CALL obj%DEALLOCATE()
END PROGRAM main
```
