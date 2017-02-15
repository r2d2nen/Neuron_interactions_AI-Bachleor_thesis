PROGRAM sps

  IMPLICIT NONE

  REAL*8 :: lb,ub
  REAL*8 :: p,h
  INTEGER :: N,ip

  N=10
  
  lb=0.0D0
  ub=+1.0D0

  h=ABS(ub-lb)/REAL(N-1,kind=8)

  WRITE(*,*) N, 1

  DO ip=1,N
     p=lb+REAL(ip-1,kind=8)*h
     WRITE(6,"(F30.18)") p
  END DO

END PROGRAM sps
