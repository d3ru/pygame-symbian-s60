/* Copyright (C) 2007 Harry Li  All Rights Reserved.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307,
 * USA.
 */

#ifndef __DEBUG_H__
#define __DEBUG_H__

#include <stdio.h>
#include <time.h>

#if defined(LOGK_ENABLE)
#define HB2CS(X) do {X=X->ReAlloc(X->Des().Length()+1);X->Des().ZeroTerminate();} while(0);
#else
#define HB2CS(X)
#endif

#define LOGRESET() do {FILE* f=fopen(LOGFN, "w+");fclose(f);} while (0);

#ifdef LOG_TS
#define PTIMESTAMP do {TTime t;t.HomeTime();TDateTime d=t.DateTime();char c[24];sprintf(c, "%04d-%02d-%02d %02d:%02d:%02d : ",d.Year(),d.Month()+1,d.Day()+1,d.Hour(),d.Minute(),d.Second());fputs(c,f);} while(0);
#else
#define PTIMESTAMP
#endif

#define DLOG(X,L)  do {FILE* f=fopen(LOGFN, "a+"); PTIMESTAMP fputs(L, f);fprintf X;fputs("\r\n", f);fclose(f);} while (0);

// LOG Complete
#ifdef LOGC_ENABLE
#define LOGC(X) DLOG(X,"[LM C] ")
#else
#define LOGC(X)
#endif

// LOG Plenty
#ifdef LOGP_ENABLE
#define LOGP(X) DLOG(X,"[LM P] ")
#else
#define LOGP(X)
#endif

// LOG Naturally
#ifdef LOGN_ENABLE
#define LOGN(X) DLOG(X,"[LM N] ")
#else
#define LOGN(X)
#endif

// LOG Key only
#ifdef LOGK_ENABLE
#define LOGK(X) DLOG(X,"[LM K] ")
#else
#define LOGK(X)
#endif


#endif //__DEBUG_H__

//EOF
