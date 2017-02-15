PROGRAM threeps

  IMPLICIT NONE

  REAL*8 :: lb,ub
  REAL*8 :: p,q,r,h
  INTEGER :: N,ip,iq,ir

  N=4
  
  lb=0.0D0
  ub=+1.0D0

  h=ABS(ub-lb)/REAL(N-1,kind=8)

  WRITE(*,*) N*N*N, 3

  DO ip=1,N
     p=lb+REAL(ip-1,kind=8)*h
     DO iq=1,N
        q=lb+REAL(iq-1,kind=8)*h
        DO ir=1,N
           r=lb+REAL(ir-1,kind=8)*h
           WRITE(6,"(3F30.18)") p,q,r
        END DO
     END DO
  END DO
  
END PROGRAM threeps
