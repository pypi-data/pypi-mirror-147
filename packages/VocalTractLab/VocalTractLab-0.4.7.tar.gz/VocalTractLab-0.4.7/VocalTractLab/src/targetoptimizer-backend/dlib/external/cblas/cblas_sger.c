/*
 *
 * cblas_sger.c
 * This program is a C interface to sger.
 * Written by Keita Teranishi
 * 4/6/1998
 *
 */

#include "cblas.h"
#include "cblas_f77.h"
void cblas_sger(const enum CBLAS_ORDER order, const int M, const int N,
                const float  alpha, const float  *X, const int incX,
                const float  *Y, const int incY, float  *A, const int lda)
{
#ifdef F77_INT
   F77_INT F77_M=M, F77_N=N, F77_lda=lda, F77_incX=incX, F77_incY=incY;
#else
   #define F77_M M
   #define F77_N N
   #define F77_incX incX
   #define F77_incY incY
   #define F77_lda lda
#endif


   if (order == CblasColMajor)
   {
      F77_sger( &F77_M, &F77_N, &alpha, X, &F77_incX, Y, &F77_incY, A,
       &F77_lda);
   }
   else if (order == CblasRowMajor)
   {
      F77_sger( &F77_N, &F77_M, &alpha, Y, &F77_incY, X, &F77_incX, A, 
        &F77_lda);
   }
   else cblas_xerbla(1, "cblas_sger", "Illegal Order setting, %d\n", order);
   return;
}
