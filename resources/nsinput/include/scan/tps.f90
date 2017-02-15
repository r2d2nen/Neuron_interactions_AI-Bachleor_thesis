PROGRAM tps

  IMPLICIT NONE

  REAL*8 :: lb,ub
  REAL*8 :: p,q,h
  INTEGER :: N,ip,iq

  N=30
  
  lb=0.0D0
  ub=+1.0D0

  h=ABS(ub-lb)/REAL(N-1,kind=8)

  WRITE(*,*) N*N, 2

  DO ip=1,N
     p=lb+REAL(ip-1,kind=8)*h
     DO iq=1,N
        q=lb+REAL(iq-1,kind=8)*h
        WRITE(6,"(2F30.18)") p,q
     END DO
  END DO
  
END PROGRAM tps
