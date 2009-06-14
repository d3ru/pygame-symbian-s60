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


// This file defines the API for libsft2.dll

#ifndef __LIBSFT2_H__
#define __LIBSFT2_H__

//  Include Files

#include <e32base.h>	// CBase
#include <e32std.h>	 // TBuf

//  Constants

class CGraphicsContext;

//  Class Definitions

class CSymbianFreeType : public CBase
	{
	public:	 // new functions
		IMPORT_C static CSymbianFreeType* NewL();
		IMPORT_C static CSymbianFreeType* NewLC();
		IMPORT_C ~CSymbianFreeType();

	public:	 // new functions, example API
		IMPORT_C TVersion Version() const;

		IMPORT_C TBool InitializeFace(TDes8& aFileName, TUint32 aFontIndex, const CGraphicsDevice* aGd, TInt aSizeInPoint);
		IMPORT_C void SetFontColor(TRgb aColor, TRgb aBackColor);
		IMPORT_C void DrawString(CGraphicsContext& aGc, TPoint aPoint, const TDesC& aDes);

	private:	// new functions
		CSymbianFreeType();
		void ConstructL();

	private:	// data
		FT_Library iLibrary;
		FT_Face iFace;
		TRgb iColor;
		TRgb iBackColor;
		TSize iPPI;
	};


#endif  // __LIBSFT2_H__

